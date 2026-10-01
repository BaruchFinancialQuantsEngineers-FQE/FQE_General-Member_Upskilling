-- Exercise 8: 21-day moving average with a window frame
SELECT ticker,
       trade_date,
       close,
       AVG(close) OVER (
           PARTITION BY ticker
           ORDER BY trade_date
           ROWS BETWEEN 20 PRECEDING AND CURRENT ROW
       ) AS ma_21
FROM prices
ORDER BY ticker, trade_date;
