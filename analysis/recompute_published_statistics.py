#!/usr/bin/env python3
"""Recompute the deposited item statistics from the response file beside them.

Reads survey_responses_deidentified.tab (54 responses, 41 variables, CC0 1.0)
and compares every recomputed mean and SD against table_item_means_sd.tab.
Both files come from doi:10.7910/DVN/BXO2QA, so this is an internal-consistency
check of that deposit.

Columns are addressed by name. A position-based mapping written against the
58-column collection file is not valid for the 41-column public deposit.

SD follows the convention of the deposited table, the sample SD (ddof=1).
"""
from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path

RESPONSES = "data/survey_responses_deidentified.tab"
BENCHMARK = "data/table_item_means_sd.tab"


def as_float(value):
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return None


def mean(values):
    return sum(values) / len(values) if values else None


def sample_sd(values):
    """Sample SD (ddof=1), the convention of the deposited table: all 33 of its
    items reproduce with ddof=1."""
    if len(values) < 2:
        return None
    m = sum(values) / len(values)
    return math.sqrt(sum((v - m) ** 2 for v in values) / (len(values) - 1))


def read_tab(path: Path) -> tuple[list[str], list[list[str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        header = next(reader)
        rows = [row for row in reader if row and any(cell.strip() for cell in row)]
    return header, rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=RESPONSES)
    parser.add_argument("--benchmark", default=BENCHMARK)
    args = parser.parse_args()

    header, rows = read_tab(Path(args.data))
    print(f"Responses: {len(rows)} rows, {len(header)} columns")

    bench_header, bench_rows = read_tab(Path(args.benchmark))
    print(f"Table: {len(bench_rows)} tabulated items\n")

    # The benchmark truncates long item labels to 120 characters, so match on a
    # prefix rather than on equality.
    checked = agreed = 0
    failures = []
    cursor = 0
    for item, n_str, mean_str, sd_str in bench_rows:
        label = item.strip().strip('"')
        idx = next((i for i in range(cursor, len(header))
                    if header[i].startswith(label[:min(len(label), 110)])), None)
        if idx is None:
            failures.append((label[:70], "no column match", "", ""))
            continue
        cursor = idx + 1
        values = [as_float(r[idx]) for r in rows]
        values = [v for v in values if v is not None]
        got_n, got_mean, got_sd = len(values), mean(values), sample_sd(values)
        checked += 1
        ok = (
            got_n == int(n_str)
            and abs(round(got_mean, 2) - float(mean_str)) < 0.005
            and abs(round(got_sd, 2) - float(sd_str)) < 0.005
        )
        if ok:
            agreed += 1
        else:
            failures.append((label[:70],
                             f"n={got_n} vs {n_str}",
                             f"mean={got_mean:.2f} vs {mean_str}",
                             f"sd={got_sd:.2f} vs {sd_str}"))

    for label, a, b, c in failures:
        print(f"  MISMATCH  {label}\n            {a}  {b}  {c}")

    print(f"\n{agreed}/{checked} tabulated items reproduce exactly.")
    if failures:
        print(f"{len(failures)} item(s) did not match or could not be located.")
        return 1
    print("Every tabulated mean and SD recomputes from the response file.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
