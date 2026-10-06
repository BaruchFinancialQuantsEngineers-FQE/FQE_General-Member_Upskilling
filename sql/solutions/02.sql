-- Exercise 2: ORDER BY and LIMIT
SELECT ticker,
       trade_date,
       volume
FROM prices
ORDER BY volume DESC, ticker, trade_date
LIMIT 10;
