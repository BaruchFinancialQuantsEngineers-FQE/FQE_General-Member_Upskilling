-- Exercise 7: LAG for daily returns
SELECT ticker,
       trade_date,
       close,
       close / LAG(close) OVER (PARTITION BY ticker ORDER BY trade_date) - 1 AS daily_return
FROM prices
ORDER BY ticker, trade_date;
