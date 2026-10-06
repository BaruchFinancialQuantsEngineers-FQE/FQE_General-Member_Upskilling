# Synthetic Data

This folder generates the price data used by the SQL exercises for **SQL & Databases on Tuesday, October 20** and the pandas starter for **Data Case Study on Thursday, October 22**. Everything is simulated locally, so the repository contains no licensed or vendor data.

## Quick start

From the repository root (the script also works from any other directory):

```bash
python data/make_data.py
```

Expected output:

```
Wrote 4,032 price rows for 8 tickers (2024-01-02 to 2025-12-05).
```

The script writes three files in this folder. They are listed in `.gitignore`, so do not commit them. Rerunning the script overwrites them with identical contents.

## Outputs

| File | Contents |
| --- | --- |
| `prices.csv` | Columns `ticker, trade_date, close, volume`; 504 rows per ticker |
| `tickers.csv` | Columns `ticker, sector` |
| `fqe.db` | SQLite database with tables `prices` and `tickers`, same columns as the CSV files |

In `fqe.db`, `trade_date` is ISO text (`'YYYY-MM-DD'`), `close` is `REAL`, and `volume` is `INTEGER`. The primary key of `prices` is `(ticker, trade_date)`.

## Universe

All tickers are fictional. The digit suffix marks each symbol as synthetic.

| Ticker | Sector | Start price | Annual drift | Annual volatility |
| --- | --- | --- | --- | --- |
| TCH1 | Technology | 120.00 | 18% | 40% |
| TCH2 | Technology | 45.00 | 12% | 45% |
| TCH3 | Technology | 260.00 | 10% | 32% |
| FIN1 | Financials | 80.00 | 8% | 24% |
| FIN2 | Financials | 35.00 | 6% | 28% |
| ENR1 | Energy | 60.00 | 5% | 33% |
| ENR2 | Energy | 95.00 | 3% | 30% |
| HLT1 | Health Care | 150.00 | 7% | 20% |

## How the data is generated

- **Dates.** 504 business days from 2024-01-02, built with `pd.bdate_range`. This calendar skips weekends but not exchange holidays, so dates such as 2025-01-01 appear.
- **Prices.** Geometric Brownian motion with daily step `exp((mu - sigma^2 / 2) dt + sigma sqrt(dt) Z)`, where `dt = 1/252` and `Z` is standard normal. Closes are rounded to cents.
- **Volume.** Integer share counts: a per-ticker base level, scaled up on days with large price moves, times lognormal noise.
- **Seed.** `numpy.random.default_rng(2026)`. Every member gets the same numbers.

Realized volatility in a given sample differs from the parameter above because of sampling noise. That gap is a useful discussion point for the case study.

## Swapping in real data

To use a WRDS or Bloomberg pull instead, produce files with the same columns and types. The SQL exercises and the pandas starter read only these columns. Do not commit licensed data to this repository.
