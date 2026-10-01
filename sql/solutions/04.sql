-- Exercise 4: GROUP BY with HAVING
SELECT ticker,
       substr(trade_date, 1, 4) AS year,
       AVG(close)               AS avg_close
FROM prices
GROUP BY ticker, year
HAVING AVG(close) > 100;
