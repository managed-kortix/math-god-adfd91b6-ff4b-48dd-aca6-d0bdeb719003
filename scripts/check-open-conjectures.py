#!/usr/bin/env python3
"""Read every public Open Conjecture Board record and reconcile the manifest.

This is read-only. It uses the API's opaque next_cursor exactly as returned and
never treats public absence as proof of rejection.
"""

from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "research" / "publication-manifest.json"
API = "https://openconjectures.org/api/v1/conjectures"


def normalize(value: str | None) -> str:
    value = value or ""
    value = value.replace("\\geq", ">=").replace("\\ge", ">=")
    value = value.replace("−", "-").replace("–", "-")
    return re.sub(r"[^a-z0-9+>=-]+", " ", value.lower()).strip()


def fetch_all() -> tuple[list[dict], list[dict]]:
    records: list[dict] = []
    pages: list[dict] = []
    cursor: str | None = None
    seen: set[str] = set()
    while True:
        query = {"per_page": "100"}
        if cursor:
            if cursor in seen:
                raise SystemExit("cursor loop detected")
            seen.add(cursor)
            query["cursor"] = cursor
        url = API + "?" + urllib.parse.urlencode(query)
        with urllib.request.urlopen(url, timeout=30) as response:
            payload = json.load(response)
        data = payload.get("data")
        pagination = payload.get("pagination")
        if not isinstance(data, list) or not isinstance(pagination, dict):
            raise SystemExit("unexpected Board API response shape")
        records.extend(data)
        pages.append({
            "page": pagination.get("page"),
            "count": len(data),
            "reported_total": pagination.get("total"),
        })
        cursor = pagination.get("next_cursor")
        if not cursor:
            expected = pagination.get("total")
            if isinstance(expected, int) and expected != len(records):
                raise SystemExit(
                    f"pagination mismatch: fetched {len(records)}, expected {expected}"
                )
            break
    ids = [record.get("id") for record in records]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate public conjecture IDs across pages")
    return records, pages


def source_url(record: dict) -> str:
    source = record.get("source")
    return (source.get("url") or "") if isinstance(source, dict) else ""


def main() -> None:
    records, pages = fetch_all()
    manifest = json.loads(MANIFEST.read_text())
    matches = []
    for item in manifest.get("results", []):
        wanted_statement = normalize(item.get("statement"))
        wanted_source = item.get("source_url", "").removesuffix("v1").rstrip("/")
        found = []
        for record in records:
            statement = normalize(record.get("statement_oneline"))
            full = normalize(record.get("statement_full_latex"))
            record_source = source_url(record).removesuffix("v1").rstrip("/")
            statement_match = wanted_statement in statement or wanted_statement in full
            source_match = bool(wanted_source and record_source == wanted_source)
            # A shared source paper is insufficient: require the exact statement
            # match as well when source URLs coincide.
            if statement_match or (source_match and statement_match):
                found.append({
                    "id": record.get("id"),
                    "effective_status": record.get("effective_status"),
                    "public_actions": record.get("public_actions"),
                    "statement_oneline": record.get("statement_oneline"),
                })
        matches.append({
            "manifest_id": item.get("id"),
            "manifest_ocb_status": item.get("ocb", {}).get("status"),
            "public_matches": found,
            "publicly_listed": bool(found),
        })
    print(json.dumps({
        "api": API,
        "pages": pages,
        "public_record_count": len(records),
        "manifest_reconciliation": matches,
        "caveat": "Public absence does not distinguish pending review from rejection.",
    }, indent=2))


if __name__ == "__main__":
    main()
