# Handoff: FQE Fall 2026 Skills Plan Starter Repository

## Objective

Build a starter repository that general members of FQE (Financial Quants and Engineers, Baruch College) use to complete the Fall 2026 skills plan. The repository supplies the drills, exercises, problem sets, and code skeletons that the plan references. Members prepare for each club event using the matching folder.

Source plan: "FQE Fall 2026 General Member Skills Plan" (Claude Doc, owned by Alexi Tilly). This handoff restates everything needed from it; you do not need the doc.

## Before you start

Confirm these with the user before writing code:

1. Repository name and owner. Default assumption: `fqe-fall26-skills` under the `baruchfqe` GitHub organization.
2. Whether the FQE project template repository is available locally. If it is, mirror its README structure and folder conventions. If not, use the README skeleton at the end of this file.
3. Python version available to members. Default assumption: Python 3.11.

## Calendar constraints (build order follows these deadlines)

Today is Thursday, October 1, 2026. Members need each component before the event it supports.

| Ship by | Component | Supports event |
| --- | --- | --- |
| Oct 5 | `drills/market_making` and `templates/debrief.md` | Trading Competition, Fri Oct 9 |
| Oct 8 | `problems/brainteasers` | Brainteaser Battle, Thu Oct 15 |
| Oct 13 | `data/` generator and `sql/` exercises | SQL & Databases, Tue Oct 20 |
| Oct 18 | `pandas/` case study starter | Data Case Study, Thu Oct 22 |
| Oct 22 | `problems/math` | Math Competition, Fri Oct 30 |
| Nov 4 | `backtest/` Hackathon skeleton | Hackathon, Thu Nov 12 |
| Nov 4 | `.github/ISSUE_TEMPLATE/` checkpoints | Checkpoints Oct 14, Nov 4, Dec 10 |

Build and commit in this order. Each component must be usable on its own.

## Target structure

```
fqe-fall26-skills/
  README.md
  pyproject.toml
  data/
    make_data.py
  drills/market_making/
    drill.py
    test_drill.py
    README.md
  problems/
    brainteasers.md
    math.md
    verify.py
  sql/
    exercises.md
    solutions/            # one .sql file per exercise
    check.py
  pandas/
    case_study_starter.ipynb
    case_study_starter.py
    presentation_outline.md
  backtest/
    fqe_backtest/
      __init__.py
      core.py
      strategies.py
    tests/
      test_core.py
    example.py
    README.md
  templates/
    debrief.md
  .github/ISSUE_TEMPLATE/
    checkpoint-1.md
    checkpoint-2.md
    checkpoint-3.md
```

Dependencies: `numpy`, `pandas`, `matplotlib`, `pytest`, `jupyter`. Standard library `sqlite3` for SQL. No other runtime dependencies without asking.

## Component specs

### 1. Market-making drill (`drills/market_making/`)

A terminal program for practicing two-sided quotes on the sum of dice.

Modes:

- **Pair mode.** Player A quotes a bid and ask on the sum of three six-sided dice. Player B chooses buy (at the ask), sell (at the bid), or pass. Dice are rolled and the trade settles. Roles swap each round.
- **Solo mode.** The user quotes; a bot taker trades whenever the quote is mispriced against fair value. The bot buys when `ask < fair_value` and sells when `bid > fair_value`, and otherwise trades with probability 0.5 on a random side. This rewards tight quotes centered on fair value.
- **Reveal variant (flag `--reveal`).** One die is shown before quoting, so fair value becomes `revealed + 7`.

Settlement: if the taker buys at the ask, taker P&L is `outcome - ask` and quoter P&L is `ask - outcome`. If the taker sells at the bid, taker P&L is `bid - outcome` and quoter P&L is `outcome - bid`.

Rules and output:

- Configurable maximum spread (`--max-spread`, default 4). Reject quotes wider than the maximum or with `bid >= ask`.
- After each round, print the roll, the trade, round P&L, and cumulative P&L per player.
- At the end, print a summary: rounds played, average spread quoted, total P&L per player, and P&L per round.
- Seedable RNG (`--seed`) for reproducible sessions.

Tests (`test_drill.py`): settlement math for both sides, fair value with and without a revealed die, quote validation, and deterministic output under a fixed seed.

### 2. Debrief template (`templates/debrief.md`)

Half-page template members fill in within 48 hours of the Trading Competition. Three prompts: where P&L came from by instrument, the largest loss and its cause, and one change for next time. Include a short filled example using invented numbers.

### 3. Problem sets (`problems/`)

- `brainteasers.md`: 30 original problems across probability, expected value, combinatorics, mental math, and estimation.
- `math.md`: 25 original problems across conditional probability and Bayes' rule, linearity of expectation with indicator variables, common distributions, random walks and gambler's ruin, basic linear algebra, and series.

Requirements:

- Write original problems. Do not reproduce problems from Zhou, Crack, Joshi, or any other published book; the skills plan already points members to those books.
- Tag each problem with topic and difficulty (1 to 3).
- Hide each solution in a `<details>` block with a worked solution, not only the answer.
- `verify.py` checks every problem with a numeric answer by Monte Carlo simulation (at least 1,000,000 trials where feasible) or exact enumeration, and fails if any stated answer is off by more than the simulation tolerance. Run it and fix any failures before committing.

### 4. Synthetic data (`data/make_data.py`)

Generate data locally so the repository commits no licensed or vendor data. Members can swap in WRDS or Bloomberg pulls later.

- 8 tickers across at least 3 sectors, 504 trading days (business days starting 2024-01-02).
- Prices follow geometric Brownian motion with per-ticker drift and volatility, seed 2026.
- Outputs: `data/prices.csv` (columns `ticker, trade_date, close, volume`), `data/tickers.csv` (columns `ticker, sector`), and `data/fqe.db` (SQLite with tables `prices` and `tickers`).
- Add the generated files to `.gitignore`; members run the script once.

### 5. SQL exercises (`sql/`)

`exercises.md` holds 8 exercises in increasing difficulty, ending with window functions. Required coverage: SELECT and WHERE, ORDER BY and LIMIT, GROUP BY with HAVING, a JOIN to `tickers`, and LAG for daily returns. Exercise 7 must be this query, which the skills plan asks members to write from memory:

```sql
SELECT ticker,
       trade_date,
       close,
       close / LAG(close) OVER (PARTITION BY ticker ORDER BY trade_date) - 1 AS daily_return
FROM prices
ORDER BY ticker, trade_date;
```

Exercise 8: 21-day moving average of close per ticker using `AVG(...) OVER (... ROWS BETWEEN 20 PRECEDING AND CURRENT ROW)`.

`check.py` takes an exercise number and a path to the member's `.sql` file, runs it and the reference solution against `data/fqe.db`, and reports match or mismatch (compare row sets with a float tolerance of 1e-9). Confirm the local SQLite version supports window functions (3.25 or later).

### 6. pandas case study starter (`pandas/`)

A notebook and an equivalent `.py` script that:

1. Load `data/prices.csv` with parsed dates.
2. Compute daily log returns per ticker.
3. Compute 21-day rolling volatility, annualized by the square root of 252.
4. Compare average volatility by sector with a groupby and merge to `tickers.csv`.
5. Produce one labeled chart.

Leave clearly marked `# TODO (member)` cells for steps 3 to 5, with the reference solution in a separate `solutions` section at the end of the notebook. `presentation_outline.md` gives the three-minute format: question, data, one chart, the finding with a number, one caveat.

### 7. Hackathon backtest skeleton (`backtest/`)

A small package members fork for the Hackathon.

`core.py` functions, each with type hints and docstrings:

- `simple_returns(prices: pd.Series) -> pd.Series`
- `positions_from_signal(signal: pd.Series) -> pd.Series`: shifts the signal by one bar so a position at time t uses information through t-1 only.
- `strategy_returns(positions: pd.Series, returns: pd.Series) -> pd.Series`
- `sharpe(returns: pd.Series, periods: int = 252) -> float`: annualized, risk-free rate zero.
- `max_drawdown(returns: pd.Series) -> float`: computed on compounded equity, `equity = (1 + r).cumprod()`, drawdown `equity / equity.cummax() - 1`, returned as a negative number.

`strategies.py`: one moving-average crossover and one short-horizon mean-reversion signal, each returning values in [-1, 1].

`example.py` runs both strategies on one synthetic ticker and prints Sharpe and maximum drawdown.

Tests (`tests/test_core.py`) must include:

- A look-ahead test: a signal equal to the next bar's return sign must not produce perfect returns after `positions_from_signal`.
- Sharpe on a constant-return series raises or returns infinity in a documented way rather than dividing by zero silently.
- Maximum drawdown on a hand-built series matches a value computed by hand.

Note: the skills plan doc shows a shortened snippet that sums log returns for drawdown. The package uses compounded simple returns as specified above; flag this to the user so the doc can be aligned.

### 8. Checkpoint issue templates (`.github/ISSUE_TEMPLATE/`)

One template per checkpoint, each a task list members copy into an issue or Discord post:

- Checkpoint 1 (Oct 14): competed in the Trading Competition or ran three market-making drills; debrief posted; application tracker started.
- Checkpoint 2 (Nov 4): SQL returns query runs; case study slide presented; 20 probability problems completed; Python, Git, and the FQE template set up.
- Checkpoint 3 (Dec 10): Hackathon repository pushed with a README; résumé updated with fall results; spring desk chosen.

## Writing rules for member-facing text

- Formal American English, short paragraphs, specific instructions.
- No em dashes. No filler phrases.
- Every README opens with what the folder is for and the event it supports, then a quick start that reaches a first result in under five minutes.

## Root README skeleton (use if no FQE template is available)

```
# FQE Fall 2026 Skills Starter

What this is: drills and exercises for the FQE Fall 2026 general member skills plan.

## Quick start
1. Install Python 3.11 and run `pip install -e .`
2. Run `python data/make_data.py`
3. Open the folder for your next event (table below)

## Folders by event
| Event | Date | Folder |

## Checkpoints

## Contributing
Branch from main, open a pull request, request review from a board member.
```

## Definition of done

- `pytest` passes from the repository root.
- `python problems/verify.py` passes.
- `python data/make_data.py` followed by `python sql/check.py 7 sql/solutions/07.sql` reports a match.
- `python backtest/example.py` prints Sharpe and maximum drawdown for both strategies.
- Every folder has a README with a working quick start.
- No vendor data, credentials, or copyrighted problem text committed.

Report back to the user with: what shipped, anything deferred, and any decision you made that this handoff did not cover.
