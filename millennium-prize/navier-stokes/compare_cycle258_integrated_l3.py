#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from scout_cycle258_integrated_l3 import compare_reports


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n64", type=Path, required=True)
    parser.add_argument("--n128", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    coarse = json.loads(args.n64.read_text(encoding="ascii"))
    fine = json.loads(args.n128.read_text(encoding="ascii"))
    report = compare_reports(coarse, fine)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
