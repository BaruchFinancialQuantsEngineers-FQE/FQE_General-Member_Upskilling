# Hackathon Backtest Skeleton

This folder is a small Python package for testing daily trading signals. Fork it for the FQE Hackathon on Thursday, November 12, add your own strategy, and present its Sharpe ratio and maximum drawdown.

The package computes returns, converts signals into positions without look-ahead bias, and reports annualized Sharpe and maximum drawdown. It ships with two example strategies and a test suite.

## Quick start (under five minutes)

Run these commands from the repository root.

1. Install the repository: `pip install -e .`
2. Optional: generate the synthetic dataset with `python data/make_data.py`. Without it, the example generates its own synthetic prices.
3. Run the example: `python backtest/example.py`
4. Run the tests: `python -m pytest backtest -q`

The example prints a table like this one. Your numbers depend on the data.

```
Data: ENR1 from data/prices.csv, 504 bars
Strategy                        Sharpe    Max DD
------------------------------------------------
MA crossover (20/50)              0.77    -29.2%
Mean reversion (5, z=1.0)        -0.51    -40.1%
```

Steps 3 and 4 also work without `pip install -e .`, since the example and the tests add this folder to the import path.

## Package layout

| File | Contents |
| --- | --- |
| `fqe_backtest/core.py` | `simple_returns`, `positions_from_signal`, `strategy_returns`, `sharpe`, `max_drawdown` |
| `fqe_backtest/strategies.py` | `ma_crossover` (trend following) and `mean_reversion` (rolling z-score) |
| `tests/test_core.py` | Look-ahead, Sharpe, drawdown, and signal-range tests |
| `example.py` | Runs both strategies on one ticker and prints the results |

## Conventions

- `returns[t]` is the simple return from the close of bar t-1 to the close of bar t.
- `signal[t]` may use prices through the close of bar t.
- `positions[t]` is the exposure held during bar t. It equals `signal[t-1]`, and the first position is 0 (flat).
- Sharpe is annualized with 252 periods per year, a risk-free rate of zero, and the sample standard deviation (`ddof=1`). It raises `ValueError` when returns have zero volatility, because the ratio is undefined.
- Maximum drawdown uses compounded equity, `equity = (1 + r).cumprod()`, against a running peak that starts at 1.0. It is reported as a negative number, or 0.0 if equity never falls below its peak.

## Fork and add a strategy

1. Fork the repository on GitHub and clone your fork.
2. Create a branch: `git checkout -b hackathon/<team-name>`
3. Add a function to `fqe_backtest/strategies.py`. It takes a price series and returns a signal series with the same index and values in [-1, 1]. Use only data through bar t when computing `signal[t]`.

   ```python
   def momentum(prices: pd.Series, lookback: int = 60) -> pd.Series:
       """Long when the trailing return is positive, short when negative."""
       trailing = prices / prices.shift(lookback) - 1
       return np.sign(trailing).fillna(0.0)
   ```

4. Export it in `fqe_backtest/__init__.py` and add it to the `strategies` dictionary in `example.py`.
5. Add your strategy to the `test_signals_within_bounds` parameter list in `tests/test_core.py`, then run `python -m pytest backtest -q`.
6. Commit, push, and write your results and assumptions in your fork's README.

Always pass a signal through `positions_from_signal` before `strategy_returns`. Never multiply a raw signal by same-bar returns.

## Look-ahead bias

Look-ahead bias occurs when a backtest uses information that was not available at the time of the trade. The result looks profitable on paper and fails in live trading.

The most common case is a signal computed from today's close that also earns today's return. In practice, you see the close, decide, and trade at the next opportunity, so the first return you can earn is tomorrow's. `positions_from_signal` enforces this by lagging the signal one bar.

The test `test_look_ahead_signal_is_neutralized_by_shift` demonstrates the effect. A signal equal to the sign of the return it will earn wins on every bar when used unshifted. After `positions_from_signal`, its hit rate falls to roughly 50 percent.

The shift does not protect you from every form of look-ahead. Other sources include indicators computed with `shift(-1)` or centered rolling windows, parameters tuned on the full sample, and universes chosen with knowledge of which tickers survived. Check for these yourself.

## Note on the skills plan snippet

The skills plan doc shows a shortened snippet that sums log returns for drawdown. This package uses compounded simple returns, `(1 + r).cumprod()`, which is the correct equity-curve definition. A drawdown read off cumulative log returns is in log units, not percent, and the gap grows with the size of the loss. For example, a 50 percent loss is a log drawdown of -0.69. Use this package's `max_drawdown` for Hackathon results.
