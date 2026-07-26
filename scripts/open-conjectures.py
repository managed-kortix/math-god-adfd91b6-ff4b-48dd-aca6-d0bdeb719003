#!/usr/bin/env python3
"""Prepare or explicitly submit Open Conjecture Board form payloads.

Network writes are impossible without --submit. Verification links are handled
through Gmail and are never accepted by or printed from this script.
"""

from __future__ import annotations

import argparse
import json
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "research" / "publication-manifest.json"
ENDPOINT = "https://openconjectures.org/submit"


def load(item_id: str) -> dict:
    data = json.loads(MANIFEST.read_text())
    matches = [x for x in data["results"] if x["id"] == item_id]
    if len(matches) != 1:
        raise SystemExit(f"expected exactly one manifest item {item_id!r}")
    return matches[0]


def payload(item: dict, name: str, email: str) -> dict[str, str]:
    if item["kind"] != "open_conjecture":
        raise SystemExit("only open_conjecture manifest items use /submit")
    return {
        "submitter_name": name,
        "email": email,
        "statement_oneline": item["statement"],
        "statement_full_latex": (
            item["statement"] + " Source: " + item["source_label"] + ". "
            "The general problem remains open; listed special-class results "
            "must not be interpreted as a resolution."
        ),
        "source_url": item["source_url"],
        "year": str(item["year"]),
        "area": item["area"],
        "website": "",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest_id")
    parser.add_argument("--name", default="Agent Mirko")
    parser.add_argument("--email", default="agent@kortix.ai")
    parser.add_argument("--submit", action="store_true")
    args = parser.parse_args()
    body = payload(load(args.manifest_id), args.name, args.email)
    if not args.submit:
        redacted = dict(body)
        redacted["email"] = "<private email>"
        print(json.dumps({"endpoint": ENDPOINT, "payload": redacted}, indent=2))
        return
    request = urllib.request.Request(
        ENDPOINT,
        data=urllib.parse.urlencode(body).encode(),
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        text = response.read().decode("utf-8", "replace")
    if "Thanks — check your email" not in text:
        raise SystemExit("submission response was not the expected verification prompt")
    print("submission accepted; retrieve and inspect the Gmail verification message")


if __name__ == "__main__":
    main()
