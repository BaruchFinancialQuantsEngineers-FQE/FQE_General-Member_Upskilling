# SQL Exercises

Eight exercises against `data/fqe.db`, in increasing difficulty. Exercises 7 and 8 use window functions.

Write each answer in its own file, for example `my_answers/07.sql`, then check it:

```bash
python sql/check.py 7 my_answers/07.sql
```

## Schema

```sql
CREATE TABLE tickers (
    ticker TEXT PRIMARY KEY,
    sector TEXT NOT NULL
);

CREATE TABLE prices (
    ticker     TEXT NOT NULL,     -- joins to tickers.ticker
    trade_date TEXT NOT NULL,     -- ISO text, 'YYYY-MM-DD'
    close      REAL NOT NULL,
    volume     INTEGER NOT NULL,
    PRIMARY KEY (ticker, trade_date)
);
```

Dates are ISO text, so string comparison sorts them correctly. `'2024-03-15' < '2024-04-01'` is true.

## How answers are checked

The checker compares your rows with the reference rows. Column names do not matter. Column count, column position, and values do. Floats match within 1e-9.

Row order matters only where the exercise says "Sort" (exercises 2, 6, 7, and 8). Everywhere else, any order passes.

---

## Exercise 1: SELECT and WHERE

**Difficulty: 1**

Return every row for ticker `TCH1` in March 2024.

Columns, in order: `ticker`, `trade_date`, `close`, `volume`.

Hint: `BETWEEN` is inclusive on both ends.

## Exercise 2: ORDER BY and LIMIT

**Difficulty: 1**

Find the 10 highest-volume days across all tickers.

Columns, in order: `ticker`, `trade_date`, `volume`.

Sort by `volume` descending. Break ties by `ticker`, then `trade_date`, both ascending.

## Exercise 3: Aggregates with GROUP BY

**Difficulty: 1**

For each ticker, report the number of trading days, the lowest close, the highest close, and the average volume.

Columns, in order: `ticker`, `n_days`, `min_close`, `max_close`, `avg_volume`.

Return one row per ticker.

## Exercise 4: GROUP BY with HAVING

**Difficulty: 2**

For each ticker and calendar year, compute the average close. Keep only the ticker-years whose average close is above 100.

Columns, in order: `ticker`, `year`, `avg_close`. The `year` column is text, for example `'2024'`.

Hint: `substr(trade_date, 1, 4)` extracts the year. `WHERE` filters rows before grouping; `HAVING` filters groups after.

## Exercise 5: JOIN to tickers

**Difficulty: 2**

For each sector, report the number of distinct tickers and the total shares traded over the full sample.

Columns, in order: `sector`, `n_tickers`, `total_volume`.

## Exercise 6: Common table expression and self-join

**Difficulty: 3**

For each ticker, compute the total return from its first close to its last close: `last_close / first_close - 1`. Include the sector.

Columns, in order: `ticker`, `sector`, `first_close`, `last_close`, `total_return`.

Sort by `total_return` descending.

Hint: use a `WITH` clause to find each ticker's first and last `trade_date`, then join `prices` to that result twice.

## Exercise 7: LAG for daily returns

**Difficulty: 3**

Write this query from memory. The skills plan asks every member to be able to do so.

Compute the simple daily return for each ticker: today's close divided by the previous close, minus one. The first row of each ticker has no previous close, so its return is `NULL`.

Columns, in order: `ticker`, `trade_date`, `close`, `daily_return`.

Sort by `ticker`, then `trade_date`.

<details>
<summary>Reference query (try it first)</summary>

```sql
SELECT ticker,
       trade_date,
       close,
       close / LAG(close) OVER (PARTITION BY ticker ORDER BY trade_date) - 1 AS daily_return
FROM prices
ORDER BY ticker, trade_date;
```

`PARTITION BY ticker` restarts the window for each ticker. Without it, the first row of each ticker after the first would divide by the last close of the previous ticker.

</details>

## Exercise 8: 21-day moving average

**Difficulty: 3**

Compute a 21-day moving average of `close` for each ticker. The window covers the current row and the 20 rows before it.

Columns, in order: `ticker`, `trade_date`, `close`, `ma_21`.

Sort by `ticker`, then `trade_date`.

Use `AVG(close) OVER (PARTITION BY ... ORDER BY ... ROWS BETWEEN 20 PRECEDING AND CURRENT ROW)`.

Note: for the first 20 rows of each ticker, the frame holds fewer than 21 rows, and `AVG` averages whatever is there. The checked answer keeps those rows as they are.

Extension (not checked): return `NULL` for `ma_21` until a full 21-row window exists. Hint: `COUNT(*) OVER (same window)`.
