# SQL Exercises

This folder prepares you for **SQL & Databases on Tuesday, October 20**. It holds eight exercises against a local SQLite database of synthetic prices, a reference solution for each, and a checker that tells you whether your answer matches.

## Quick start

1. From the repository root, build the database (about two seconds):

   ```bash
   python data/make_data.py
   ```

2. Confirm the checker works by running it on a reference solution:

   ```bash
   python sql/check.py 7 sql/solutions/07.sql
   ```

   Expected output: `MATCH on exercise 7: 4032 rows (row order checked).`

3. Open `exercises.md`, write your answer to Exercise 1 in a new file such as `my_answers/01.sql`, and check it:

   ```bash
   python sql/check.py 1 my_answers/01.sql
   ```

## Files

| File | Purpose |
| --- | --- |
| `exercises.md` | Eight exercises, schema, and hints |
| `solutions/01.sql` to `solutions/08.sql` | Reference solutions |
| `check.py` | Compares your query's output with the reference output |

## How the checker works

`check.py` runs your query and the reference query against `data/fqe.db` and compares the results.

- Floats match when they differ by at most 1e-9.
- `NULL` matches `NULL`.
- Row order is ignored unless the exercise specifies a sort (exercises 2, 6, 7, and 8).
- Column names are ignored. Column count and position are compared.

It prints `MATCH` and exits with code 0, or prints `MISMATCH` with the row count difference and the first differing rows and exits with code 1.

Each `.sql` file must contain a single `SELECT` statement. Comments are allowed.

## Requirements

Window functions (exercises 7 and 8) need SQLite 3.25.0 or later. The checker verifies this on every run. Check your version directly with:

```bash
python -c "import sqlite3; print(sqlite3.sqlite_version)"
```

Python 3.11 from python.org or most package managers ships a recent enough SQLite.

## Exploring the data interactively

You do not need a separate SQLite client. This one-liner runs any query:

```bash
python -c "import sqlite3; c = sqlite3.connect('data/fqe.db'); print(*c.execute('SELECT * FROM tickers'), sep='\n')"
```

If you prefer a graphical tool, DB Browser for SQLite opens `data/fqe.db` directly.

## Study approach

Attempt each exercise without opening `solutions/`. If you are stuck for more than ten minutes, read the hint, then the solution, then close it and write the query again from a blank file.

Exercise 7 is the query the skills plan asks you to write from memory. Repeat it until you can type it without looking. Checkpoint 2 (November 4) asks you to confirm that it runs.
