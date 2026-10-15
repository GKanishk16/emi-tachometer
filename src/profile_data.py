#!/usr/bin/env python3
"""Profile manually supplied CSV files and write a schema-grounded dictionary.

Author: Kanishk Gupta

This intentionally makes no fixed column-name assumptions. Put the Kaggle CSV
files in data/raw/ and run: python src/profile_data.py
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
OUTPUT = ROOT / "docs" / "DATA_DICTIONARY.md"


def infer_interpretation(column: str, dtype: str, samples: list[Any]) -> str:
    """Return a cautious, explicitly inferred interpretation from evidence."""
    name = re.sub(r"[^a-z0-9]+", " ", column.lower()).strip()
    values = " ".join(str(value).lower() for value in samples if value is not None)
    hints: list[str] = []
    patterns = [
        (r"default|target|label|outcome", "may represent a target or outcome"),
        (r"date|month|year|time|vintage", "may represent a date or time attribute"),
        (r"age|dob|birth", "may represent borrower or asset age"),
        (r"loan|disburs|amount|principal|emi", "may represent a loan or repayment measure"),
        (r"bureau|score|credit|history", "may represent credit bureau information"),
        (r"branch|state|city|district|pin", "may represent geography or servicing location"),
        (r"manufacturer|make|model|vehicle|asset", "may describe the financed vehicle"),
        (r"employment|occupation|income", "may describe borrower employment or income"),
        (r"id|key|code|number", "may be an identifier or code"),
    ]
    for pattern, hint in patterns:
        if re.search(pattern, name):
            hints.append(hint)
    if any(token in values for token in ("yrs", "year", "mon", "month")):
        hints.append("sample values suggest a duration field")
    if "date" in dtype:
        hints.append("the inferred pandas dtype is date-like")
    if not hints:
        hints.append(f"observed as {dtype}; meaning is not established from the profile alone")
    return "Inferred: " + "; ".join(dict.fromkeys(hints)) + ". Validate with the dataset documentation before use."


def markdown_cell(value: Any) -> str:
    if value is None or (not isinstance(value, (list, dict)) and pd.isna(value)):
        return "(null)"
    return str(value).replace("|", "\\|").replace("\n", " ")


def profile_file(path: Path, sample_size: int) -> tuple[int, list[dict[str, Any]]]:
    # Read the input as provided. pandas inference is reported, never treated as
    # a cleaning decision. The file path and raw data remain untouched.
    frame = pd.read_csv(path, low_memory=False, encoding="utf-8-sig")
    records: list[dict[str, Any]] = []
    for column in frame.columns:
        series = frame[column]
        non_null = series.dropna()
        samples = [markdown_cell(v) for v in non_null.drop_duplicates().head(sample_size).tolist()]
        records.append({
            "column": str(column),
            "dtype": str(series.dtype),
            "null_pct": (float(series.isna().mean()) * 100.0) if len(series) else 0.0,
            "unique_count": int(series.nunique(dropna=True)),
            "samples": samples,
            "interpretation": infer_interpretation(str(column), str(series.dtype), non_null.head(sample_size).tolist()),
        })
    return len(frame), records


def write_dictionary(files: list[Path], sample_size: int) -> None:
    sections = [
        "# Data Dictionary\n\n",
        "Author: Kanishk Gupta\n\n",
        "> Generated from the CSV files currently present in `data/raw/`. Interpretations are heuristic and explicitly **inferred**; validate them against the source documentation. Re-run `python src/profile_data.py` after changing the raw files.\n",
    ]
    for path in files:
        row_count, records = profile_file(path, sample_size)
        sections.extend([f"\n## `{path.relative_to(ROOT)}`\n\n", f"Rows: {row_count:,} · Columns: {len(records)}\n\n"])
        sections.append("| Column | pandas dtype | Null % | Unique count | Sample values | Interpretation |\n|---|---|---:|---:|---|---|\n")
        for item in records:
            samples = ", ".join(item["samples"]) if item["samples"] else "(no non-null samples)"
            sections.append(
                f"| {markdown_cell(item['column'])} | {markdown_cell(item['dtype'])} | "
                f"{item['null_pct']:.2f}% | {item['unique_count']:,} | {samples} | {markdown_cell(item['interpretation'])} |\n"
            )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("".join(sections), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample-size", type=int, default=5, help="distinct non-null sample values per column")
    args = parser.parse_args()
    files = sorted(RAW_DIR.glob("*.csv"))
    if not files:
        print(f"No CSV files found in {RAW_DIR}. Add the manually downloaded dataset, then rerun.", file=sys.stderr)
        return 2
    try:
        write_dictionary(files, max(1, args.sample_size))
    except (UnicodeDecodeError, pd.errors.ParserError, OSError, ValueError) as exc:
        print(f"Could not profile input CSV: {exc}", file=sys.stderr)
        return 1
    print(f"Profiled {len(files)} CSV file(s); wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
