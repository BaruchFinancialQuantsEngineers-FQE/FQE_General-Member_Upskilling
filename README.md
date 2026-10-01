# FQE Fall 2026 Skills Starter

This repository holds the drills, exercises, problem sets, and code skeletons for the FQE (Financial Quants and Engineers, Baruch College) Fall 2026 general member skills plan. Each folder prepares you for one club event. Open the folder for your next event and follow its README.

## Quick start

1. Install Python 3.11 or later, then install this repository and its dependencies from the repository root:

   ```bash
   pip install -e .
   ```

2. Generate the synthetic market data used by the SQL and pandas exercises:

   ```bash
   python data/make_data.py
   ```

3. Confirm everything works by running a five-round market-making drill:

   ```bash
   python drills/market_making/drill.py --rounds 5 --seed 1
   ```

4. Open the folder for your next event (table below).

## Folders by event

| Event | Date | Folder | What you do there |
| --- | --- | --- | --- |
| Trading Competition | Fri, Oct 9 | `drills/market_making/`, `templates/` | Practice two-sided quotes on dice, then file a debrief with `templates/debrief.md` |
| Brainteaser Battle | Thu, Oct 15 | `problems/brainteasers.md` | Work 30 problems in probability, expected value, combinatorics, mental math, and estimation |
| SQL & Databases | Tue, Oct 20 | `data/`, `sql/` | Generate the database, then complete 8 SQL exercises ending with window functions |
| Data Case Study | Thu, Oct 22 | `pandas/` | Compute returns and rolling volatility, compare sectors, and present one chart |
| Math Competition | Fri, Oct 30 | `problems/math.md` | Work 25 problems in probability, distributions, random walks, linear algebra, and series |
| Hackathon | Thu, Nov 12 | `backtest/` | Fork the backtest package and build and evaluate a trading strategy |

Other folders:

- `docs/` holds the research and build plan behind this repository. Members do not need it to complete the exercises.
- `slides/` holds presentation slides for workshops and the FQE slide template.
- `.github/ISSUE_TEMPLATE/` holds the checkpoint task lists described below.

## Checkpoints

Each checkpoint is a task list. Open a new issue in this repository and choose the matching template, or copy the list into a Discord post. Check off each item and add the requested evidence.

| Checkpoint | Due | Requirements |
| --- | --- | --- |
| Checkpoint 1 | Wed, Oct 14 | Competed in the Trading Competition or ran three market-making drills; debrief posted; application tracker started |
| Checkpoint 2 | Wed, Nov 4 | SQL returns query runs; case study slide presented; 20 probability problems completed; Python, Git, and the FQE template set up |
| Checkpoint 3 | Thu, Dec 10 | Hackathon repository pushed with a README; résumé updated with fall results; spring desk chosen |

## Running the tests

From the repository root:

```bash
python -m pytest
python problems/verify.py
```

## Data policy

This repository commits no vendor or licensed data. All market data is synthetic and generated locally by `data/make_data.py`. You may replace it with your own WRDS or Bloomberg pulls, but do not commit those files.

## Contributing

1. Branch from `main` with a descriptive name, for example `fix-sql-exercise-5`.
2. Run `python -m pytest` and confirm it passes.
3. Open a pull request that explains the change in two or three sentences.
4. Request review from a board member. Do not merge your own pull request.
