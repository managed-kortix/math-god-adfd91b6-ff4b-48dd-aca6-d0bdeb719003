#!/usr/bin/env python3
"""Emit the frozen 57-shard q,H_CC partition of uncertified clean-sink parents."""

import argparse
import hashlib
from collections import defaultdict
from pathlib import Path

import m6_clean_sink_group_cnf as source

HERE = Path(__file__).resolve().parent
FORMAT = "m6-clean-sink-balanced-shard-cnf-v1"
MANIFEST_FORMAT = "m6-clean-sink-balanced-shards-v1"
HASH_LEDGER_FORMAT = "m6-clean-sink-balanced-shard-hashes-v1"
CAP = 500
EXCLUDED_GROUP = "B6-l4"
GROUP_KEYS = source.GROUP_KEYS[1:]
IDENTITY_PATHS = {
    "clean-parent-manifest": HERE / "m6-clean-sink-selector-groups.tsv",
    "clean-remaining-stream": HERE / "m6-clean-sink-remaining.tsv",
    "clean-partition-manifest": HERE / "m6-clean-sink-manifest.tsv",
    "clean-sink-theorem": HERE.parent / "attempts" / "tick52-rooted-clean-sink-theorem.md",
    "balanced-partition-theorem": HERE.parent / "attempts" / "tick53-clean-sink-balanced-shards.md",
    "excluded-certificate-ledger": HERE / "m6-clean-sink-B6-l4-certificate.tsv",
    "excluded-certificate-verifier": HERE / "verify_m6_clean_sink_B6_l4_certificate.py",
}
IDENTITIES = {
    "clean-parent-manifest": (1838, "6e7eee0ddd5b4c7ef02cdf459c9a0647f720513e7ee4987a3a8b0c17af37eeda"),
    "clean-remaining-stream": (2262190, "416b7e51a73637784342a374be8e15a1a58032b61fc1140f39f0768d1ff4b642"),
    "clean-partition-manifest": (2104, "733e06c8aa9881e0006409efff23729f1bf88d8af7b1a70e8a78fd3775b53217"),
    "clean-sink-theorem": (4156, "bd0631529bb4658061663460b718ef2ee3186d02fdc599fb2673d3cff3b94ee2"),
    "balanced-partition-theorem": (2490, "a6aa643ae2cad46349a8a1aee88f837e112532aef2858913c9e19289e8200a87"),
    "excluded-certificate-ledger": (1807, "e46e7189e50d423f721e481868b6c5b2cbe4f3ab9d208407f652a27c4c6359e2"),
    "excluded-certificate-verifier": (7741, "91f5b7c89d3ab23b63df2eea5b632aa64f1465f1baf6c15d9676ea5d4002aea9"),
}
# (group, q, H_CC, parent count, balanced shard sizes). This is the frozen table.
BALANCING_TABLE = (
    ("B6-l5", 0, 0, 398, (398,)), ("B6-l5", 0, 1, 326, (326,)),
    ("B6-l5", 0, 2, 78, (78,)), ("B6-l5", 1, 0, 97, (97,)),
    ("B6-l5", 1, 1, 99, (99,)), ("B6-l5", 1, 2, 26, (26,)),
    ("B6-l6", 0, 0, 80, (80,)), ("B6-l6", 0, 1, 97, (97,)),
    ("B6-l6", 0, 2, 36, (36,)), ("B6-l6", 0, 3, 7, (7,)),
    ("B7-l2", 0, 0, 3973, (497, 497, 497, 497, 497, 496, 496, 496)),
    ("B7-l2", 1, 0, 2694, (449, 449, 449, 449, 449, 449)),
    ("B7-l2", 2, 0, 1212, (404, 404, 404)), ("B7-l2", 3, 0, 213, (213,)),
    ("B7-l2", 4, 0, 27, (27,)),
    ("B7-l3", 0, 0, 2064, (413, 413, 413, 413, 412)),
    ("B7-l3", 0, 1, 724, (362, 362)), ("B7-l3", 1, 0, 1306, (436, 435, 435)),
    ("B7-l3", 1, 1, 389, (389,)), ("B7-l3", 2, 0, 341, (341,)),
    ("B7-l3", 2, 1, 141, (141,)), ("B7-l3", 3, 0, 36, (36,)),
    ("B7-l3", 3, 1, 15, (15,)),
    ("B7-l4", 0, 0, 818, (409, 409)), ("B7-l4", 0, 1, 322, (322,)),
    ("B7-l4", 1, 0, 290, (290,)), ("B7-l4", 1, 1, 148, (148,)),
    ("B7-l4", 2, 0, 47, (47,)), ("B7-l4", 2, 1, 24, (24,)),
    ("B7-l5", 0, 0, 159, (159,)), ("B7-l5", 0, 1, 110, (110,)),
    ("B7-l5", 1, 0, 32, (32,)), ("B7-l5", 1, 1, 21, (21,)),
    ("B7-l6", 0, 0, 26, (26,)), ("B7-l6", 0, 1, 16, (16,)),
)
PARENTS = 16392
SHARDS = 57
MANIFEST_BYTES = 8414
MANIFEST_SHA256 = "20f6d04a9e8ca0662efd011ead7804402d3c0dd21e025311cb4485fae8403fdb"
SHARD_CNF_SHA256 = {
    "B6-l5-q0-c0-s00": "efe08b1b0cf386b554bff65c60c991a71bb208bc878486ef0b11ad14e408b140",
    "B6-l5-q0-c1-s00": "b7ee1d02d94aa3d79a7c245469fbb68f6370aa890804c8228efbc7b3b545cec0",
    "B6-l5-q0-c2-s00": "60cdb0f2bc29c77a2d63e77ed903e2ce9fb8395fac6896b98e25aa103f21874a",
    "B6-l5-q1-c0-s00": "37a97cb3b6c6b61dc4265a7aba0b308ddbd2ab55a20e395a1edc591f7544738a",
    "B6-l5-q1-c1-s00": "b9fc424845c0eafaa27202b5b635ace893a55bc341a04dd6b1447818b1155d96",
    "B6-l5-q1-c2-s00": "677fcbf44934cbf873edb042a544d3a39cae5b1213a24d970a375836d268f0dd",
    "B6-l6-q0-c0-s00": "8ac6a92283a4b93a5a78eecc36405156239c05f35e18e06292c3c5e5f451ff04",
    "B6-l6-q0-c1-s00": "c46667ee6d14b5fbcbc7053d219d06f26ded111a8721abb1779977f9966dffca",
    "B6-l6-q0-c2-s00": "5dc89ab0fbf751a952fbec4100fbc07a6f18350019e8acb358b576d5183e195a",
    "B6-l6-q0-c3-s00": "2d987c4264c31702599e3e4150a1d49ad589fbac5f7689d702a86c7174de8f60",
    "B7-l2-q0-c0-s00": "b95175a0c2a8bd5752e761c5dd667af440cc600ccc1ff1558923948af836b189",
    "B7-l2-q0-c0-s01": "18e081476d9850a8207df12405ccaaa71349d498e33fbcae1548ab6497bea380",
    "B7-l2-q0-c0-s02": "2f518f45118547167773ce0fd6de0908ecb2e782008b9a81a541f61f63fd251d",
    "B7-l2-q0-c0-s03": "b3ba754722c98202bbc6e03122245ee6edcca044b2f554e16e670b9842fa39db",
    "B7-l2-q0-c0-s04": "a52824335407976f189b8898d2bfbd1eb9f3d2bd9d8642d01e76b3f2548a9484",
    "B7-l2-q0-c0-s05": "696519341cf077af99197e41b4ee68f2b148929f9eecb551eea05beb63b701de",
    "B7-l2-q0-c0-s06": "b2daad7b3d1b4428c29dc971167f3ab53f624ed52d4d7c67797a467262f32b38",
    "B7-l2-q0-c0-s07": "59110bb3b21fa1cfcb675fb6d423c5228a0c11ca0d5b785af5c3a393c04cd20d",
    "B7-l2-q1-c0-s00": "d0013eb6ec2e8596cab64bf6ba0cdd464e7a7ecbaa9a8498ddaacc6491cef5ed",
    "B7-l2-q1-c0-s01": "7243dcdb5ebb62631006e8b38957dfe0c08a7fa5bdc8e971cf72e19430d91e37",
    "B7-l2-q1-c0-s02": "eb34c98ed1e82828c19195a3e4796a872738d04a1348580ac7e312a75980281b",
    "B7-l2-q1-c0-s03": "05ace442252dd90580a6e2882d8f887ea1c5704dd93fd8c3dad408291f213dbd",
    "B7-l2-q1-c0-s04": "ec57d1fa1cc61b190dc189fe95ff1f1d6ecbe701c0bc27032753117f43c2ce6c",
    "B7-l2-q1-c0-s05": "210a13016930f52829e286a9de5a9c5e241fc06df5a41e9fdc9fae8172473e62",
    "B7-l2-q2-c0-s00": "aa56207d928f60636531783d29cdcb11c63f2f1eb8d04491431ed614e0eeadb6",
    "B7-l2-q2-c0-s01": "c84b581e39c5c3d270030b95ff66a8f2f21355ae64f645e92384a0ba25c9987a",
    "B7-l2-q2-c0-s02": "724a405fc57675635d63c7bb502cda781739d6a928c98bf145ad2a0bd6893ac0",
    "B7-l2-q3-c0-s00": "eae22653e08bbb103dcd29c5a34da4468c76c7f877074b0d06cddb956cf6bbec",
    "B7-l2-q4-c0-s00": "b05fe37d34e9f6bae35988c0e3bd044d45a55c9907fe142d686ec4b0d40d623c",
    "B7-l3-q0-c0-s00": "59e908b0121d68ef5c0dfcae547c1d587e081eb73963e41f9e62e6323d84495b",
    "B7-l3-q0-c0-s01": "601f5534be265b16ba70333191ff1c7da12bc06921592eeb5547710f7cb80014",
    "B7-l3-q0-c0-s02": "3a9c3e4e394d9b70316792b07deb553af2c8b9d99f2879058923f22361bdf708",
    "B7-l3-q0-c0-s03": "4151a8f7029c5cb5f147debdee08b5a02a67b83a5708fa7f5653483e084a1c0e",
    "B7-l3-q0-c0-s04": "24b9d9162a75c370debf4f850d8b81c7e0658fe0e01b2cdf637d5ff480d23cef",
    "B7-l3-q0-c1-s00": "039d8abcfc1a1c0abbfa853d9036e55df960cfb84567a7b82075c4bd031f298d",
    "B7-l3-q0-c1-s01": "fb5fa6244a4694047e1c36e210afbacaaa2533c2a4488b16f9b619dbac7b6000",
    "B7-l3-q1-c0-s00": "81155eb126cbebe65d9ce5f3398624a7dbf369d30a389031b2eec4084a8f19ab",
    "B7-l3-q1-c0-s01": "c82606dcfe687bc11e0bbad2450e50013da7597d0d97c59c5fc6b86153641104",
    "B7-l3-q1-c0-s02": "67941797bfd40ad5ef9b7a6d156dc031eb533f62adc1a77cf3878e93d0c62765",
    "B7-l3-q1-c1-s00": "814578a99167845213f5b110ea26af31be733826ba68335bf5a45b87582eff40",
    "B7-l3-q2-c0-s00": "0bebd4ebea898d0fad1092aec1361210c057089ce95aedb28f2c8b8c04fdb5a3",
    "B7-l3-q2-c1-s00": "2261a6086c81ac651936951f2a2ab7cdbfa0251a6298ea1cfaa3e9595d99359c",
    "B7-l3-q3-c0-s00": "7b01475396b109b0eee00dfd02eb85acbe2db907d1b9015c07bfe1b9dfaf0a96",
    "B7-l3-q3-c1-s00": "f447fdff7fb99f503f27a6a6c6cd3a93213d4c261155c8b754197f345b182778",
    "B7-l4-q0-c0-s00": "5639ab5959ac2461bffe285b47b7740d1c454c917e71bd211a2530f4bca13a90",
    "B7-l4-q0-c0-s01": "f6a42ef3358c8337dff5b5fa6d65835845e9f71f7efd7554838572d62d72c38f",
    "B7-l4-q0-c1-s00": "6bfa81a2ac1e4b83ed864a33ab000fe822d9172095ed3d528b405ba8fa71d10d",
    "B7-l4-q1-c0-s00": "f5c7f02ffb626f22884d66e575e05885dc597689f0def3784542c5f2cad5558b",
    "B7-l4-q1-c1-s00": "9c12471adf3759c20b2e0f932d8d770f85666e7de5cdc535cf2615a5661ed5a2",
    "B7-l4-q2-c0-s00": "1e9ec47b1c8b7f2970c78130a687b013ff861b9d55c127452991ceb848322bde",
    "B7-l4-q2-c1-s00": "8cc6fc8a38e41701c54f4845d42defa708d22a28d9b0775887b1c898cb121b34",
    "B7-l5-q0-c0-s00": "1977ea031eb86e9745d97746cc888124f80d64690d7e1a8ae521b4ccbd321798",
    "B7-l5-q0-c1-s00": "8c505550c8dccb0520dd8ce8661127397c7d596550cf38325989290e3d7bc4e1",
    "B7-l5-q1-c0-s00": "a30d197c095f8689152118338ceaf264f546da35efb8f7e2f196cbd63489ba3d",
    "B7-l5-q1-c1-s00": "96ab3e2de41022bef76d82e85b65bd19b2feb1208316c79691f1086e7f904ff5",
    "B7-l6-q0-c0-s00": "3dc7688622e5ee0b433b015ab8e64ee69eb8885a540b630b11cbe28b8dcc1059",
    "B7-l6-q0-c1-s00": "720c388ed40319d95246905454c5dd405d17ae29f0f8a9a8df0145d9ba94b533",
}
HASH_LEDGER_BYTES = 5972
HASH_LEDGER_SHA256 = "46045d216f32a22b1d618910c4e3fc5528c700b34277be2e17eab89e6ccae125"


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def verify_identities():
    for name, path in IDENTITY_PATHS.items():
        if identity(path) != IDENTITIES[name]:
            raise RuntimeError(f"frozen bound identity changed: {name}")


def parameters(row):
    holes = source.parent.embedded_holes(row["branch"], row["word"], row["edges"])[1]
    labels = source.parent.CELL_LABELS[row["branch"]]
    b, c = set(labels[2]), set(labels[3])
    q = sum((low in b and high in c) or (high in b and low in c) for low, high in holes)
    h_cc = sum(low in c and high in c for low, high in holes)
    return q, h_cc


def shard_key(group, q, h_cc, part):
    return f"{group}-q{q}-c{h_cc}-s{part:02d}"


def load_shards():
    verify_identities()
    groups = source.load_groups()
    if set(groups) != set(source.GROUP_KEYS) or len(groups[EXCLUDED_GROUP]) != 2470:
        raise RuntimeError("clean parent groups or certified exclusion changed")
    cells = defaultdict(list)
    for group in GROUP_KEYS:
        for member in groups[group]:
            cells[group, *parameters(member[2])].append(member)
    shards = []
    for group, q, h_cc, total, sizes in BALANCING_TABLE:
        members = cells.pop((group, q, h_cc), None)
        if members is None or len(members) != total or sum(sizes) != total:
            raise RuntimeError("q,H_CC balancing table does not match clean parents")
        if max(sizes) > CAP or max(sizes) - min(sizes) > 1:
            raise RuntimeError("canonical cell balancing violates cap or balance")
        offset = 0
        for part, size in enumerate(sizes):
            shard_members = members[offset:offset + size]
            shards.append((shard_key(group, q, h_cc, part), group, q, h_cc, part,
                           len(sizes), shard_members))
            offset += size
    if cells or len(shards) != SHARDS or sum(len(row[-1]) for row in shards) != PARENTS:
        raise RuntimeError("57-shard cover is not exhaustive and exact")
    return shards


def member_payload(members):
    lines = ["columns\tselector-ordinal,accepted-ordinal,cover-index"]
    lines.extend(f"{i:03d}\t{accepted:05d}\t{cover:06d}"
                 for i, (accepted, cover, _) in enumerate(members))
    return ("\n".join(lines) + "\n").encode("ascii")


def dimensions(group, count):
    return source.parent.BASE_VARIABLES + count, source.parent.BASE_CLAUSES[group[:2]] + 1 + 153 * count


def manifest_payload(shards):
    lines = [MANIFEST_FORMAT]
    for name, (size, digest) in IDENTITIES.items():
        lines.extend((f"{name}-bytes\t{size}", f"{name}-sha256\t{digest}"))
    lines.extend((f"excluded-certified-group\t{EXCLUDED_GROUP}:2470", f"cap\t{CAP}",
                  f"groups\t{len(GROUP_KEYS)}", f"q-hcc-cells\t{len(BALANCING_TABLE)}",
                  f"shards\t{SHARDS}", f"parents\t{PARENTS}",
                  "columns\tshard-ordinal,key,parent-group,q,H_CC,cell-part,cell-parts,parents,first-selector,last-selector,variables,clauses,member-sha256"))
    for ordinal, (key, group, q, h_cc, part, parts, members) in enumerate(shards):
        variables, clauses = dimensions(group, len(members))
        lines.append(f"{ordinal:02d}\t{key}\t{group}\t{q}\t{h_cc}\t{part}\t{parts}\t{len(members)}\t"
                     f"{source.parent.BASE_VARIABLES + 1}\t{variables}\t{variables}\t{clauses}\t"
                     f"{hashlib.sha256(member_payload(members)).hexdigest()}")
    return ("\n".join(lines) + "\n").encode("ascii")


def hash_ledger_payload(shards, manifest):
    lines = [HASH_LEDGER_FORMAT, f"partition-manifest-bytes\t{len(manifest)}",
             f"partition-manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}",
             f"shards\t{SHARDS}",
             "columns\tshard-ordinal,key,parents,variables,clauses,cnf-sha256"]
    for ordinal, shard in enumerate(shards):
        key, group, _, _, _, _, members = shard
        variables, clauses = dimensions(group, len(members))
        lines.append(f"{ordinal:02d}\t{key}\t{len(members)}\t{variables}\t{clauses}\t{SHARD_CNF_SHA256[key]}")
    return ("\n".join(lines) + "\n").encode("ascii")


def build_shard(group, members):
    return source.build_group(group, members)


def write_shard(path, ordinal, shard, cnf, selectors, manifest):
    key, group, q, h_cc, part, parts, members = shard
    metadata = [("format", FORMAT), ("shard-manifest-format", MANIFEST_FORMAT),
                ("shard-manifest-bytes", str(len(manifest))),
                ("shard-manifest-sha256", hashlib.sha256(manifest).hexdigest())]
    for name, (size, digest) in IDENTITIES.items():
        metadata.extend(((f"{name}-bytes", str(size)), (f"{name}-sha256", digest)))
    metadata.extend((("excluded-certified-group", f"{EXCLUDED_GROUP}:2470"),
                     ("cap", str(CAP)), ("shard-ordinal", str(ordinal)), ("shard-key", key),
                     ("parent-group", group), ("branch", group[:2]), ("lambda", group[4:]),
                     ("q", str(q)), ("H_CC", str(h_cc)), ("cell-part", str(part)),
                     ("cell-parts", str(parts)), ("parents", str(len(members))),
                     ("member-sha256", hashlib.sha256(member_payload(members)).hexdigest()),
                     ("base-variables", str(source.parent.BASE_VARIABLES)),
                     ("base-variable-map-sha256", source.parent.BASE_VARIABLE_MAP_SHA256),
                     ("base-clauses", str(source.parent.BASE_CLAUSES[group[:2]])),
                     ("base-clause-sha256", source.parent.BASE_CLAUSE_SHA256[group[:2]]),
                     ("alo-clauses", "1"), ("guarded-hole-clauses-per-parent", "153"),
                     ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1]))))
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata:
            handle.write(f"c {name} {value}\n")
        for name, number in cnf.names.items():
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--shard", type=int)
    selection.add_argument("--key")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--hash-ledger-output", type=Path)
    args = parser.parse_args()
    if args.output is None and args.manifest_output is None and args.hash_ledger_output is None:
        parser.error("at least one output is required")
    shards = load_shards()
    manifest = manifest_payload(shards)
    digest = hashlib.sha256(manifest).hexdigest()
    if MANIFEST_BYTES and (len(manifest), digest) != (MANIFEST_BYTES, MANIFEST_SHA256):
        raise RuntimeError("balanced shard manifest fingerprint changed")
    if args.manifest_output:
        args.manifest_output.write_bytes(manifest)
    ledger = hash_ledger_payload(shards, manifest)
    ledger_digest = hashlib.sha256(ledger).hexdigest()
    if HASH_LEDGER_BYTES and (len(ledger), ledger_digest) != (HASH_LEDGER_BYTES, HASH_LEDGER_SHA256):
        raise RuntimeError("balanced shard hash ledger fingerprint changed")
    if args.hash_ledger_output:
        args.hash_ledger_output.write_bytes(ledger)
    if args.output:
        matches = [(i, shard) for i, shard in enumerate(shards)
                   if i == args.shard or shard[0] == args.key]
        if len(matches) != 1:
            parser.error("--output requires exactly one valid --shard or --key")
        ordinal, shard = matches[0]
        cnf, selectors = build_shard(shard[1], shard[-1])
        write_shard(args.output, ordinal, shard, cnf, selectors, manifest)
        file_hash = hashlib.sha256(args.output.read_bytes()).hexdigest()
        if SHARD_CNF_SHA256 and file_hash != SHARD_CNF_SHA256[shard[0]]:
            raise RuntimeError("balanced shard CNF fingerprint changed")
        print(f"shard={ordinal:02d} key={shard[0]} parents={len(shard[-1])} vars={len(cnf.names)} "
              f"clauses={len(cnf.clauses)} bytes={args.output.stat().st_size} sha256={file_hash}")
    print(f"shards={SHARDS} parents={PARENTS} cap={CAP} manifest_bytes={len(manifest)} sha256={digest}")


if __name__ == "__main__":
    main()
