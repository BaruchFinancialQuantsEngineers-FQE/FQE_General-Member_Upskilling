-- Exercise 1: SELECT and WHERE
SELECT ticker,
       trade_date,
       close,
       volume
FROM prices
WHERE ticker = 'TCH1'
  AND trade_date BETWEEN '2024-03-01' AND '2024-03-31';
