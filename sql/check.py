"""Check a member's SQL answer against the reference solution.

Usage (from the repository root):

    python sql/check.py 7 path/to/my_answer.sql

The script runs both queries against data/fqe.db and compares the results.
Floats match when they differ by at most 1e-9. NULL matches NULL. Row order
is ignored unless the exercise asks for a specific order (exercises 2, 6, 7,
and 8). Column names are not compared; column count and position are.

Exit code 0 means MATCH. Exit code 1 means MISMATCH or an error.
"""

from __future__ import annotations

import argparse
import math
import sqlite3
import sys
from collections import Counter
from pathlib import Path

MIN_SQLITE = (3, 25, 0)
FLOAT_TOL = 1e-9
ORDERED_EXERCISES = {2, 6, 7, 8}
N_EXERCISES = 8
MAX_DIFF_ROWS = 5

SQL_DIR = Path(__file__).resolve().parent
REPO_ROOT = SQL_DIR.parent
DB_PATH = REPO_ROOT / "data" / "fqe.db"
SOLUTIONS_DIR = SQL_DIR / "solutions"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def check_sqlite_version() -> None:
    version = tuple(int(part) for part in sqlite3.sqlite_version.split("."))
    if version < MIN_SQLITE:
        fail(
            f"SQLite {sqlite3.sqlite_version} does not support window functions. "
            "Exercises 7 and 8 need SQLite 3.25.0 or later. "
            "Install a newer Python (3.11 from python.org ships a recent SQLite)."
        )


def run_query(con: sqlite3.Connection, path: Path, label: str) -> list[tuple]:
    try:
        sql = path.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"cannot read {label} file {path}: {exc}")
    try:
        return [tuple(row) for row in con.execute(sql).fetchall()]
    except sqlite3.Warning as exc:
        fail(f"{label} file must contain exactly one SQL statement ({exc}).")
    except sqlite3.Error as exc:
        fail(f"{label} query failed: {exc}")
    return []  # unreachable; keeps type checkers quiet


def values_equal(a: object, b: object) -> bool:
    if a is None or b is None:
        return a is None and b is None
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if isinstance(a, float) or isinstance(b, float):
            if math.isnan(a) and math.isnan(b):
                return True
            return abs(a - b) <= FLOAT_TOL
        return a == b
    return a == b


def rows_equal(a: tuple, b: tuple) -> bool:
    return len(a) == len(b) and all(values_equal(x, y) for x, y in zip(a, b))


def sort_key(row: tuple) -> tuple:
    """Total order over mixed SQLite values: NULL < numbers < text < blobs."""
    key = []
    for value in row:
        if value is None:
            key.append((0, 0))
        elif isinstance(value, (int, float)):
            key.append((1, round(float(value), 6)))
        elif isinstance(value, str):
            key.append((2, value))
        else:
            key.append((3, bytes(value)))
    return tuple(key)


def compare(expected: list[tuple], actual: list[tuple], ordered: bool) -> list[str]:
    """Return a list of difference lines; empty means the results match."""
    diffs: list[str] = []
    exp_cols = len(expected[0]) if expected else None
    act_cols = len(actual[0]) if actual else None
    if exp_cols is not None and act_cols is not None and exp_cols != act_cols:
        diffs.append(f"Column count differs: expected {exp_cols}, got {act_cols}.")
        diffs.append(f"  expected first row: {expected[0]}")
        diffs.append(f"  your first row:     {actual[0]}")
        return diffs
    if len(expected) != len(actual):
        diffs.append(
            f"Row count differs: expected {len(expected)}, got {len(actual)} "
            f"({len(actual) - len(expected):+d})."
        )

    if ordered:
        return diffs + ordered_diff(expected, actual)
    return diffs + unordered_diff(expected, actual)


def ordered_diff(expected: list[tuple], actual: list[tuple]) -> list[str]:
    """Compare row by row in the order returned."""
    diffs: list[str] = []
    for i, (e, a) in enumerate(zip(expected, actual), start=1):
        if not rows_equal(e, a):
            if not diffs:
                diffs.append("First differing rows (by row number):")
            diffs.append(f"  row {i}: expected {e}")
            diffs.append(f"  row {i}: got      {a}")
            if len(diffs) > 2 * MAX_DIFF_ROWS:
                break
    n = len(actual)
    for row in expected[n:n + MAX_DIFF_ROWS]:
        diffs.append(f"  missing from your result: {row}")
    n = len(expected)
    for row in actual[n:n + MAX_DIFF_ROWS]:
        diffs.append(f"  extra in your result:     {row}")
    return diffs


def unordered_diff(expected: list[tuple], actual: list[tuple]) -> list[str]:
    """Compare as multisets of rows, ignoring order."""
    exp_sorted = sorted(expected, key=sort_key)
    act_sorted = sorted(actual, key=sort_key)
    if len(exp_sorted) == len(act_sorted) and all(
        rows_equal(e, a) for e, a in zip(exp_sorted, act_sorted)
    ):
        return []
    exp_counts = Counter(sort_key(r) for r in expected)
    act_counts = Counter(sort_key(r) for r in actual)
    missing_keys = exp_counts - act_counts
    extra_keys = act_counts - exp_counts
    missing = [r for r in exp_sorted if missing_keys[sort_key(r)] > 0]
    extra = [r for r in act_sorted if extra_keys[sort_key(r)] > 0]
    diffs: list[str] = []
    if not missing and not extra:
        diffs.append("Rows differ in values beyond the 1e-9 float tolerance.")
    for row in missing[:MAX_DIFF_ROWS]:
        diffs.append(f"  missing from your result: {row}")
    for row in extra[:MAX_DIFF_ROWS]:
        diffs.append(f"  extra in your result:     {row}")
    return diffs


def main() -> None:
    parser = argparse.ArgumentParser(description="Check an FQE SQL exercise answer.")
    parser.add_argument("exercise", type=int, help=f"exercise number, 1 to {N_EXERCISES}")
    parser.add_argument("sql_file", type=Path, help="path to your .sql file")
    args = parser.parse_args()

    check_sqlite_version()
    if not 1 <= args.exercise <= N_EXERCISES:
        fail(f"exercise must be between 1 and {N_EXERCISES}, got {args.exercise}.")
    if not DB_PATH.exists():
        fail(f"{DB_PATH} not found. Run python data/make_data.py first.")
    if not args.sql_file.exists():
        fail(f"{args.sql_file} not found.")

    solution = SOLUTIONS_DIR / f"{args.exercise:02d}.sql"
    con = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    try:
        expected = run_query(con, solution, "reference")
        actual = run_query(con, args.sql_file, "your")
    finally:
        con.close()

    ordered = args.exercise in ORDERED_EXERCISES
    diffs = compare(expected, actual, ordered)
    order_note = "row order checked" if ordered else "row order ignored"
    if diffs:
        print(f"MISMATCH on exercise {args.exercise} ({order_note}).")
        for line in diffs:
            print(line)
        sys.exit(1)
    print(f"MATCH on exercise {args.exercise}: {len(actual)} rows ({order_note}).")
    sys.exit(0)


if __name__ == "__main__":
    main()
