#!/usr/bin/env python3
"""Package-level fail-closed hostile mutations for the retained h=1 certificate."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

PACKAGE = Path(__file__).resolve().parent.parent
VERIFIER = Path("verifier/verify_h1_package.py")


def run(root: Path, identity_only: bool = True) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, "-O", "-B", str(root / VERIFIER)]
    if identity_only:
        command.append("--identity-only")
    return subprocess.run(
        command,
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="strict",
        timeout=600,
    )


def mutate_bytes(root: Path, rel: str, offset: int = 0) -> None:
    path = root / rel
    raw = bytearray(path.read_bytes())
    if not raw:
        raise RuntimeError(f"cannot byte-mutate empty file {rel}")
    raw[offset % len(raw)] ^= 1
    path.write_bytes(raw)


def refresh_sum(root: Path, rel: str) -> None:
    import hashlib
    sums = root / "metadata/SHA256SUMS"
    lines = sums.read_text(encoding="ascii").splitlines()
    file_digest = hashlib.sha256((root / rel).read_bytes()).hexdigest()
    replaced = [f"{file_digest}  {rel}" if line[66:] == rel else line for line in lines]
    sums.write_text("\n".join(replaced) + "\n", encoding="ascii", newline="\n")


def reanchor_ledger_mutation(root: Path) -> None:
    """Rewrite the unsigned copied envelope so only strict ledger semantics can reject."""
    import hashlib
    ledger = root / "ledger/ordered-rows.json"
    verifier = root / "verifier/verify_h1_package.py"
    manifest = root / "metadata/manifest.json"
    value = json.loads(manifest.read_text(encoding="ascii"))
    old = dict(value["ordered_ledger"])
    new = {"bytes": ledger.stat().st_size, "sha256": hashlib.sha256(ledger.read_bytes()).hexdigest()}
    value["ordered_ledger"]["bytes"] = new["bytes"]
    value["ordered_ledger"]["sha256"] = new["sha256"]
    value["identities"]["ordered_ledger"] = dict(new)
    text = verifier.read_text(encoding="ascii")
    old_size_token = f"{old['bytes']:,}".replace(",", "_")
    new_size_token = f"{new['bytes']:,}".replace(",", "_")
    for before, after in ((old_size_token, new_size_token), (old["sha256"], new["sha256"])):
        if before not in text:
            raise RuntimeError("ledger frozen identity mutation needle absent")
        text = text.replace(before, after)
    verifier.write_text(text, encoding="ascii", newline="\n")
    value["identities"]["package_verifier_source"] = {
        "bytes": verifier.stat().st_size,
        "sha256": hashlib.sha256(verifier.read_bytes()).hexdigest(),
    }
    manifest.write_text(
        json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n",
        encoding="ascii",
        newline="\n",
    )
    refresh_sum(root, "ledger/ordered-rows.json")
    refresh_sum(root, "verifier/verify_h1_package.py")
    refresh_sum(root, "metadata/manifest.json")


def mutate_manifest(root: Path, operation) -> None:
    path = root / "metadata/manifest.json"
    value = json.loads(path.read_text(encoding="ascii"))
    operation(value)
    path.write_text(
        json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n",
        encoding="ascii",
        newline="\n",
    )


def case(name: str, mutation, identity_only: bool = True, expected: str | None = None) -> None:
    with tempfile.TemporaryDirectory(prefix=f"h1-package-mutation-{name}-") as directory:
        root = Path(directory) / "package"
        shutil.copytree(PACKAGE, root, symlinks=True)
        mutation(root)
        result = run(root, identity_only)
        if result.returncode == 0:
            raise RuntimeError(f"mutation escaped: {name}\n{result.stdout[-4000:]}")
        if expected is not None and expected not in result.stdout:
            raise RuntimeError(
                f"mutation {name} failed at the wrong gate; expected {expected!r}\n"
                f"{result.stdout[-4000:]}"
            )
        print(f"PASS reject {name}")


def main() -> None:
    clean_identity = run(PACKAGE, True)
    if clean_identity.returncode != 0:
        raise RuntimeError(f"clean identity gate failed\n{clean_identity.stdout[-4000:]}")

    cases = [
        ("extra-file", lambda root: (root / "EXTRA").write_text("orphan\n"), "package tree differs"),
        ("missing-proof", lambda root: (root / "artifacts/h1-parent.drat.xz").unlink(), "package tree differs"),
        (
            "symlink-cnf",
            lambda root: (
                (root / "artifacts/h1-parent.cnf").unlink(),
                os.symlink("../ledger/ordered-rows.json", root / "artifacts/h1-parent.cnf"),
            ),
            "nonregular file",
        ),
        ("mode-drift", lambda root: os.chmod(root / "artifacts/h1-parent.cnf", 0o600), "mode mismatch"),
        ("setuid-mode", lambda root: os.chmod(root / "tools/drat-trim", 0o4755), "mode mismatch"),
        ("setgid-directory", lambda root: os.chmod(root / "artifacts", 0o2755), "directory mode mismatch"),
        ("cnf-byte", lambda root: mutate_bytes(root, "artifacts/h1-parent.cnf", 250_000), "manifest identity mismatch"),
        ("proof-byte", lambda root: mutate_bytes(root, "artifacts/h1-parent.drat.xz", 1_000), "manifest identity mismatch"),
        ("ledger-byte", lambda root: mutate_bytes(root, "ledger/ordered-rows.json", 100), "manifest identity mismatch"),
        ("checker-binary", lambda root: mutate_bytes(root, "tools/drat-trim", 500), "manifest identity mismatch"),
        ("checker-source", lambda root: mutate_bytes(root, "tools/drat-trim.c", 500), "manifest identity mismatch"),
        ("independent-checker-source", lambda root: mutate_bytes(root, "verifier/check_h1_selector_parent.py", 500), "manifest identity mismatch"),
        ("composite-source", lambda root: mutate_bytes(root, "verifier/check_h1_composite_bridge.py", 500), "manifest identity mismatch"),
        ("verifier-source", lambda root: mutate_bytes(root, "verifier/verify_h1_package.py", 500), "manifest identity mismatch"),
        ("manifest-byte", lambda root: mutate_bytes(root, "metadata/manifest.json", 100), None),
        ("sums-byte", lambda root: mutate_bytes(root, "metadata/SHA256SUMS", 1), "SHA256SUMS"),
        (
            "unsafe-sums-path",
            lambda root: (root / "metadata/SHA256SUMS").write_text(
                (root / "metadata/SHA256SUMS").read_text(encoding="ascii").replace(
                    "  artifacts/h1-parent.cnf", "  ../h1-parent.cnf", 1
                ),
                encoding="ascii",
            ),
            "unsafe package path",
        ),
        (
            "ledger-bare-array",
            lambda root: (
                (lambda path, value: path.write_text(
                    json.dumps(value["rows"], separators=(",", ":"), ensure_ascii=True) + "\n",
                    encoding="ascii",
                    newline="\n",
                ))(
                    root / "ledger/ordered-rows.json",
                    json.loads((root / "ledger/ordered-rows.json").read_text(encoding="ascii")),
                ),
                reanchor_ledger_mutation(root),
            ),
            "ledger root must be the typed envelope object",
            False,
        ),
        (
            "ledger-noncanonical-whitespace",
            lambda root: (
                (lambda path, value: path.write_text(
                    json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n",
                    encoding="ascii",
                    newline="\n",
                ))(
                    root / "ledger/ordered-rows.json",
                    json.loads((root / "ledger/ordered-rows.json").read_text(encoding="ascii")),
                ),
                reanchor_ledger_mutation(root),
            ),
            "ledger is not exact canonical compact sorted ASCII JSON",
            False,
        ),
        (
            "duplicate-manifest-key",
            lambda root: (root / "metadata/manifest.json").write_text(
                (root / "metadata/manifest.json").read_text(encoding="ascii").replace(
                    '  "schema":', '  "schema": "shadow",\n  "schema":', 1
                ),
                encoding="ascii",
            ),
            "duplicate JSON key",
        ),
        (
            "scope-widening",
            lambda root: mutate_manifest(root, lambda value: value.__setitem__("scope", "all order 18")),
            "manifest scope changed",
        ),
        (
            "remove-h0-exclusion",
            lambda root: mutate_manifest(root, lambda value: value["exclusions"].remove("family-S h=0")),
            "manifest exclusions changed",
        ),
        (
            "proof-raw-hash",
            lambda root: mutate_manifest(
                root, lambda value: value["proof"]["raw"].__setitem__("sha256", "0" * 64)
            ),
            "proof metadata changed",
        ),
        (
            "checker-role",
            lambda root: mutate_manifest(
                root, lambda value: value["proof_checker"].__setitem__("role", "provenance only")
            ),
            "proof-checker metadata changed",
        ),
        (
            "solver-role",
            lambda root: mutate_manifest(
                root, lambda value: value["proof_producer"].__setitem__("role", "proof validity")
            ),
            "proof-producer metadata changed",
        ),
        (
            "mathematical-count",
            lambda root: mutate_manifest(
                root, lambda value: value["mathematical_counts"].__setitem__("composite_cases", 742_319)
            ),
            "mathematical counts changed",
        ),
        (
            "manifest-identity",
            lambda root: mutate_manifest(
                root,
                lambda value: value["identities"]["cnf"].__setitem__("sha256", "0" * 64),
            ),
            "manifest identity mismatch",
        ),
    ]

    for entry in cases:
        if len(entry) == 3:
            name, mutation, expected = entry
            identity_only = True
        else:
            name, mutation, expected, identity_only = entry
        case(name, mutation, identity_only, expected)

    # Full semantic gates: rewrite SHA256SUMS so package identity checks pass,
    # then require independent reconstruction or proof authentication to reject.
    def reanchor_mutated_verifier(root: Path, old_digest: str, new_digest: str) -> None:
        """Update the copied verifier's frozen digest and its internal envelope.

        This is deliberately hostile: it simulates an attacker who can rewrite
        the whole unsigned internal hash envelope.  The independent semantic or
        proof check must still reject the changed mathematical artifact.
        """
        import hashlib
        verifier = root / "verifier/verify_h1_package.py"
        text = verifier.read_text(encoding="ascii")
        if old_digest not in text:
            raise RuntimeError("frozen digest mutation needle absent from verifier")
        verifier.write_text(text.replace(old_digest, new_digest), encoding="ascii", newline="\n")
        value = json.loads((root / "metadata/manifest.json").read_text(encoding="ascii"))
        value["identities"]["package_verifier_source"] = {
            "bytes": verifier.stat().st_size,
            "sha256": hashlib.sha256(verifier.read_bytes()).hexdigest(),
        }
        (root / "metadata/manifest.json").write_text(
            json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n",
            encoding="ascii",
            newline="\n",
        )
        refresh_sum(root, "verifier/verify_h1_package.py")
        refresh_sum(root, "metadata/manifest.json")

    def semantic_cnf(root: Path) -> None:
        import hashlib
        path = root / "artifacts/h1-parent.cnf"
        raw = bytearray(path.read_bytes())
        needle = b"-23293 -11506 0"
        index = raw.find(needle)
        if index < 0:
            raise RuntimeError("CNF mutation needle absent")
        raw[index] = ord("2")
        path.write_bytes(raw)
        digest = hashlib.sha256(raw).hexdigest()
        manifest = root / "metadata/manifest.json"
        value = json.loads(manifest.read_text(encoding="ascii"))
        old_digest = value["cnf"]["sha256"]
        value["cnf"]["sha256"] = digest
        value["identities"]["cnf"]["sha256"] = digest
        manifest.write_text(
            json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n",
            encoding="ascii",
            newline="\n",
        )
        refresh_sum(root, "artifacts/h1-parent.cnf")
        refresh_sum(root, "metadata/manifest.json")
        reanchor_mutated_verifier(root, old_digest, digest)

    def semantic_proof(root: Path) -> None:
        import hashlib
        path = root / "artifacts/h1-parent.drat.xz"
        mutate_bytes(root, "artifacts/h1-parent.drat.xz", path.stat().st_size // 2)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        value = json.loads((root / "metadata/manifest.json").read_text(encoding="ascii"))
        old_digest = value["proof"]["xz"]["sha256"]
        value["proof"]["xz"]["sha256"] = digest
        value["identities"]["proof_xz"]["sha256"] = digest
        (root / "metadata/manifest.json").write_text(
            json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n",
            encoding="ascii",
            newline="\n",
        )
        refresh_sum(root, "artifacts/h1-parent.drat.xz")
        refresh_sum(root, "metadata/manifest.json")
        reanchor_mutated_verifier(root, old_digest, digest)

    case("semantic-cnf-with-rehashed-envelope", semantic_cnf, False, "independent")
    case("proof-with-rehashed-envelope", semantic_proof, False, "proof")

    print(f"PASS package-level hostile mutations cases={len(cases) + 2}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
