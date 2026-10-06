-- Exercise 3: aggregate functions with GROUP BY
SELECT ticker,
       COUNT(*)    AS n_days,
       MIN(close)  AS min_close,
       MAX(close)  AS max_close,
       AVG(volume) AS avg_volume
FROM prices
GROUP BY ticker;
