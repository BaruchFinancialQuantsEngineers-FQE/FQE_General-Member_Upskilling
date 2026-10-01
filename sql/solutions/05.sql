-- Exercise 5: JOIN to tickers
SELECT t.sector,
       COUNT(DISTINCT p.ticker) AS n_tickers,
       SUM(p.volume)            AS total_volume
FROM prices AS p
JOIN tickers AS t
  ON t.ticker = p.ticker
GROUP BY t.sector;
