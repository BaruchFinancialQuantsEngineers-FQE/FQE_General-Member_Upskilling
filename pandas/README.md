# pandas Case Study Starter

This folder prepares you for **Data Case Study on Thursday, October 22**. It contains a notebook and an equivalent Python script that walk through a small analysis: daily returns, rolling volatility, a sector comparison, and one chart. You then present the result in three minutes using `presentation_outline.md`.

## Quick start

1. From the repository root, generate the data once:

   ```bash
   python data/make_data.py
   ```

2. Run the reference solution to see the target result:

   ```bash
   python pandas/case_study_starter.py --solution
   ```

   The last line reads: `Finding: Technology has the highest average volatility at 38.8%, 1.9 times Health Care at 20.4%.` The chart is saved to `pandas/output/sector_volatility.png`.

3. Open the notebook and work through steps 3 to 5:

   ```bash
   jupyter notebook pandas/case_study_starter.ipynb
   ```

## Files

| File | Purpose |
| --- | --- |
| `case_study_starter.ipynb` | Notebook version. Steps 3 to 5 are `# TODO (member)` cells; solutions are at the end. |
| `case_study_starter.py` | Script version of the same analysis. Fill in the three `# TODO (member)` functions. |
| `presentation_outline.md` | Three-minute format: question, data, one chart, finding with a number, one caveat. |
| `output/` | Generated charts. Ignored by Git. |

## The five steps

1. Load `data/prices.csv` with parsed dates. Provided.
2. Compute daily log returns per ticker. Provided.
3. Compute 21-day rolling volatility, annualized by the square root of 252. Your work.
4. Merge with `data/tickers.csv` and compare average volatility by sector with a groupby. Your work.
5. Produce one labeled chart. Your work.

## Working in the script

Running `python pandas/case_study_starter.py` with no flag runs your code. It stops at the first step you have not finished and tells you which function to fill in. Once all three functions return results, it prints the same finding as `--solution` if your code is correct.

The script uses the non-interactive Agg backend, so it saves the chart to a file and never opens a window.

## Working in the notebook

Run the cells in order. The TODO cells set `vol` and `by_sector` to `None`; replace those lines with your code. The **Solutions** section at the end overwrites both variables with the reference results, so run it only after your attempt.

## Going further

Once the reference analysis works, pick your own question for the presentation. Options that use the same data:

- Does volatility cluster? Plot `rolling_vol` over time for one ticker.
- Is volume higher on high-volatility days? Compare average volume across volatility quintiles.
- How correlated are tickers within a sector compared with across sectors?
