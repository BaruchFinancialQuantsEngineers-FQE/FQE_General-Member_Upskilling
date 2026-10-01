-- Exercise 6: common table expression and a second JOIN
WITH bounds AS (
    SELECT ticker,
           MIN(trade_date) AS first_date,
           MAX(trade_date) AS last_date
    FROM prices
    GROUP BY ticker
)
SELECT b.ticker,
       t.sector,
       p_first.close                     AS first_close,
       p_last.close                      AS last_close,
       p_last.close / p_first.close - 1  AS total_return
FROM bounds AS b
JOIN prices AS p_first
  ON p_first.ticker = b.ticker AND p_first.trade_date = b.first_date
JOIN prices AS p_last
  ON p_last.ticker = b.ticker AND p_last.trade_date = b.last_date
JOIN tickers AS t
  ON t.ticker = b.ticker
ORDER BY total_return DESC;
