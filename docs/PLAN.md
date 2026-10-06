# FQE Fall 2026 General Member Skills and Pathways Plan

Prepared October 1, 2026, for general members of FQE (Financial Quants and Engineers, Baruch College). This plan ties each club event to a folder in this repository, a weekly time budget, and one recruiting action. It is grounded in two research files, which hold the full source tables:

- [Career pathways research](research/career_pathways.md): roles, firms, Summer 2027 timing, discovery programs, Baruch entry points.
- [Resource map](research/resources.md): books, courses, documentation, and data access for each event.

Dates marked "(verify)" are listed in the research as unverified, secondary only, prior cycle, or in conflict with another source. Open the linked page before acting on them. Section 6 lists every open item for the board.

## 1. Purpose and outcome

The plan builds the skills that quant trading, research, development, and bank quant interviews test, and it turns each club event into evidence a member can show. A member who completes the plan by Thursday, December 10 can show the following artifacts.

| Artifact | Built from | Use on a résumé or in an interview |
| --- | --- | --- |
| Trading Competition result or three logged drill sessions, plus a written debrief | `drills/market_making/`, `templates/debrief.md` | Talk through quoting, fair value, and a loss you learned from |
| Brainteaser and math problem log (at least 20 probability problems) | `problems/` | Practice for probability and expected-value screens |
| Daily-returns window query written from memory, checked by `sql/check.py` | `data/`, `sql/` | Answer a SQL window-function question on a whiteboard |
| Three-minute case study slide with one chart and one number | `pandas/` | A data-analysis story with a quantified finding |
| Hackathon repository with a README stating strategy, data, Sharpe ratio, and maximum drawdown | `backtest/` | A résumé project line and a backtest you can defend, including look-ahead control |
| Application tracker with live Summer 2027 roles and discovery programs | Checkpoint 1 | Evidence of an organized recruiting cycle |
| Updated résumé and a chosen spring desk | Checkpoint 3 | Fall results stated as specific lines |

Summer 2027 quant postings are already live on firm sites for Jane Street, HRT, SIG, Two Sigma, D. E. Shaw, Optiver, AQR, and BlackRock ([career pathways, Section 3](research/career_pathways.md#3-recruiting-timeline-for-summer-2027)). For a Baruch sophomore or junior, October 2026 is mid-cycle. The plan therefore starts recruiting actions in week one rather than after the Hackathon.

## 2. Week-by-week schedule

Run every command from the repository root. Set up once before the first drill:

```bash
pip install -e .
python data/make_data.py
```

Time budgets are for a member who attends the event and completes the folder work. Members who also apply to live roles should add one to two hours per week for applications.

### Week of September 28

- **Club event:** None on the plan calendar. The FQE site lists the Trading Competition trading day as Friday, October 2 (verify; see Section 6).
- **Folder:** Root setup, then `drills/market_making/`.
- **Commands:**

  ```bash
  python drills/market_making/drill.py --rounds 5 --seed 1
  python drills/market_making/drill.py --mode solo --rounds 10
  ```

- **Time:** 2 hours (30 minutes setup, 90 minutes drills).
- **Recruiting:** Start the application tracker with columns for firm, role, deadline, and status. Add the live Summer 2027 postings: [Jane Street QT](https://www.janestreet.com/join-jane-street/position/8617344002/), [SIG QT](https://careers.sig.com/quantitative-trading-internships-co-ops/jobs/10718?lang=en-us), [HRT Algorithm Development](https://www.hudsonrivertrading.com/hrt-job/algorithm-development-quant-research-trading-internship-summer-2027/), [Two Sigma QR](https://careers.twosigma.com/careers/JobDetail/New-York-New-York-United-States-Quantitative-Researcher-Intern-2027-Summer/13945), [D. E. Shaw QA](https://www.deshaw.com/careers/quantitative-analyst-intern-new-york-summer-2027-5890), and others from [career pathways, Section 2](research/career_pathways.md#2-firm-types-with-nyc-presence). Third-party guides report that interview slots fill by late October (verify).

### Week of October 5

- **Club event:** Trading Competition, Friday, October 9 (verify; the FQE site says October 2).
- **Folder:** `drills/market_making/`, then `templates/debrief.md`.
- **Commands:**

  ```bash
  python drills/market_making/drill.py --mode solo --rounds 10 --max-spread 2
  python drills/market_making/drill.py --mode solo --rounds 10 --reveal
  python drills/market_making/drill.py --mode pair --rounds 10
  python -m pytest drills -q
  ```

  Log P&L per round for each session. Fill in `templates/debrief.md` within 48 hours of the competition.
- **Time:** 4 hours (2 hours drills, 1 hour Figgie, 1 hour debrief).
- **Recruiting:** Read the [Optiver numerical test](https://numericaltest.optiver.com/) page, which describes the eight-minute, calculator-free mental-math screen in Optiver's trading application. Optiver assessments can be taken only once every eight months, so practice timed arithmetic first and take the test only as part of a real application. Check the [Citadel Securities Quant Invitational](https://www.citadelsecurities.com/careers/programs-and-events/the-citadel-securities-quant-invitational/) page: the prior-cycle deadline was October 10, 2025, and a fall 2026 deadline is likely (verify). Members who want WRDS data for the Hackathon should register now, since registration can take up to a week ([Newman Library guide](https://guides.newman.baruch.cuny.edu/AccessFinData)).

### Week of October 12

- **Club events:** Checkpoint 1, Wednesday, October 14. Brainteaser Battle, Thursday, October 15.
- **Folder:** `problems/brainteasers.md`.
- **Commands:** Open `problems/brainteasers.md` and work B01 to B30 in order, attempting each before opening its solution. File Checkpoint 1 by opening a new issue from the "Checkpoint 1 (Oct 14)" template. To confirm the published answers, run:

  ```bash
  python problems/verify.py
  ```

- **Time:** 5 hours (4 hours on 30 problems, 1 hour on Checkpoint 1).
- **Recruiting:** Add an "apply this month" list to the tracker. Juniors, seniors, and MFE applicants should decide on the Baruch [Pre-MFE seminars](https://mfe.baruch.cuny.edu/pre-mfe-program/) before the first one starts on October 19 ($1,650 tuition per seminar where listed).

### Week of October 19

- **Club events:** SQL & Databases, Tuesday, October 20. Data Case Study, Thursday, October 22.
- **Folders:** `data/`, `sql/`, `pandas/`.
- **Commands:**

  ```bash
  python -c "import sqlite3; print(sqlite3.sqlite_version)"
  python sql/check.py 7 sql/solutions/07.sql
  python sql/check.py 1 my_answers/01.sql
  python pandas/case_study_starter.py --solution
  python pandas/case_study_starter.py
  jupyter notebook pandas/case_study_starter.ipynb
  ```

  The SQLite version must be 3.25.0 or later for exercises 7 and 8. Complete all eight SQL exercises, then rewrite exercise 7 from a blank file until `check.py` reports a match without notes. For the case study, fill in the three `# TODO (member)` steps and build one slide with `pandas/presentation_outline.md`.
- **Time:** 6 hours (3 hours SQL, 3 hours case study and slide).
- **Recruiting:** Pre-MFE seminars begin: Probability Theory on October 19, Advanced Calculus on October 20, Numerical Linear Algebra on October 21, and Statistics on October 22 ([Pre-MFE Program](https://mfe.baruch.cuny.edu/pre-mfe-program/)). Members already registered for the [Cornell Trading Competition](https://cornellquantfund.org/competition) compete Saturday, October 24, at Cornell Tech; applications closed September 20, so others should note it for fall 2027.

### Week of October 26

- **Club event:** Math Competition, Friday, October 30.
- **Folder:** `problems/math.md`.
- **Commands:** Work the 25 problems in `problems/math.md`. Count problems completed in both sets toward the 20 required for Checkpoint 2. Run `python problems/verify.py` if you edit or add any answer.
- **Time:** 5 hours.
- **Recruiting:** Follow up on any application submitted in early October. Read the [Jane Street trading interview primer](https://www.janestreet.com/static/pdfs/trading-interview.pdf) before any first-round interview.

### Week of November 2

- **Club event:** Checkpoint 2, Wednesday, November 4.
- **Folders:** `sql/`, `pandas/`, then `backtest/` to prepare for the Hackathon.
- **Commands:**

  ```bash
  python sql/check.py 7 my_answers/07.sql
  python backtest/example.py
  python -m pytest backtest -q
  git checkout -b hackathon/<team-name>
  ```

  File Checkpoint 2 from the "Checkpoint 2 (Nov 4)" template. Read the backtest README sections on conventions and look-ahead bias before the Hackathon.
- **Time:** 4 hours (1 hour checkpoint, 3 hours backtest package).
- **Recruiting:** First- and second-year members graduating winter 2028 or spring 2029 should draft the [SIG Discovery Program](https://careers.sig.com/jobs/11148?lang=en-us) application this week. It closes Monday, November 16, 2026, and leads to Summer 2028 internships.

### Week of November 9

- **Club event:** Hackathon, Thursday, November 12.
- **Folder:** `backtest/`.
- **Commands:** Add one strategy to `fqe_backtest/strategies.py`, register it in `fqe_backtest/__init__.py` and `example.py`, add it to `test_signals_within_bounds`, then run:

  ```bash
  python -m pytest backtest -q
  python backtest/example.py
  ```

  Always pass a signal through `positions_from_signal` before `strategy_returns`.
- **Time:** 6 hours plus the event.
- **Recruiting:** Submit the SIG Discovery application before Monday, November 16.

### Week of November 16

- **Club event:** None.
- **Folder:** Your Hackathon fork of `backtest/`.
- **Commands:** Write the fork's README in the order the research firms describe: data acquired, model built, backtest analyzed. State the strategy, the data, the Sharpe ratio, and the maximum drawdown printed by `python backtest/example.py`. Push the branch.
- **Time:** 3 hours.
- **Recruiting:** SIG Discovery closes Monday, November 16. Check discovery program pages for spring 2027 dates: [Discover Citadel](https://www.citadel.com/careers/programs-and-events/discover-citadel/) (prior cycle April 9 to 11, 2026, deadline March 6, 2026; verify), [Optiver FutureFocus](https://www.optiver.com/join-us/students/programs/futurefocus/) (prior cycle March 2026; verify), and [Two Sigma New Seekers Summit](https://www.twosigma.com/new-seekers-summit/) (last confirmed February 6, 2025; verify).

### Week of November 23

- **Club event:** None (Thanksgiving week).
- **Folder:** None required.
- **Commands:** None. Optional reading: Sharpe (1994) and Lo (2002) from Section 4, to prepare for questions on your Hackathon numbers.
- **Time:** 1 to 2 hours.
- **Recruiting:** Eligible members should check [Jane Street INSIGHT NYC](https://www.janestreet.com/apply-insight-nyc/), which runs January 4 to 9, 2027. The application deadline is not listed in the research (verify).

### Week of November 30

- **Club event:** None.
- **Folder:** `templates/`, your Hackathon fork.
- **Commands:** Draft résumé lines for each fall result: competition placement or drill results, the Hackathon repository with its Sharpe and drawdown, and the case study finding with its number.
- **Time:** 3 hours.
- **Recruiting:** Note spring targets for desk choice: [Rotman International Trading Competition](https://www.rotman.utoronto.ca/faculty-and-research/education-labs/bmo-financial-group-finance-research-and-trading-lab/rotman-international-trading-competition/), February 18 to 20, 2027 (verify); [IMC Prosperity](https://prosperity.imc.com/), which ran April 14 to 30, 2026, with a 2027 edition unverified (verify); and the [Citadel Datathons](https://www.citadel.com/careers/programs-and-events/datathons/).

### Week of December 7

- **Club event:** Checkpoint 3, Thursday, December 10.
- **Folder:** `.github/ISSUE_TEMPLATE/`.
- **Commands:** File Checkpoint 3 from the "Checkpoint 3 (Dec 10)" template with links to your Hackathon repository and résumé lines.
- **Time:** 2 hours.
- **Recruiting:** Update every tracker row with its current status. Set a monthly reminder to recheck discovery program pages through February.

### Summary

| Week of | Event | Folder | Hours |
| --- | --- | --- | --- |
| Sep 28 | (Trading Competition per FQE site, Oct 2, verify) | setup, `drills/market_making/` | 2 |
| Oct 5 | Trading Competition, Fri Oct 9 (verify) | `drills/market_making/`, `templates/` | 4 |
| Oct 12 | Checkpoint 1, Wed Oct 14; Brainteaser Battle, Thu Oct 15 | `problems/brainteasers.md` | 5 |
| Oct 19 | SQL & Databases, Tue Oct 20; Data Case Study, Thu Oct 22 | `data/`, `sql/`, `pandas/` | 6 |
| Oct 26 | Math Competition, Fri Oct 30 | `problems/math.md` | 5 |
| Nov 2 | Checkpoint 2, Wed Nov 4 | `sql/`, `pandas/`, `backtest/` | 4 |
| Nov 9 | Hackathon, Thu Nov 12 | `backtest/` | 6 |
| Nov 16 | None | Hackathon fork | 3 |
| Nov 23 | None | None | 1 to 2 |
| Nov 30 | None | résumé, Hackathon fork | 3 |
| Dec 7 | Checkpoint 3, Thu Dec 10 | `.github/ISSUE_TEMPLATE/` | 2 |

Total: about 42 hours over eleven weeks, plus event attendance.

## 3. Pathways by role

Every member completes the full plan. This table shows where to spend extra time and which verified external resources to add. Role descriptions and sources are in [career pathways, Section 1](research/career_pathways.md#1-role-families).

| Role | Plan components that matter most | Add these resources |
| --- | --- | --- |
| Quantitative trader | Market-making drill, Trading Competition, Brainteaser Battle, Math Competition; add timed mental math | [Jane Street primer](https://www.janestreet.com/static/pdfs/trading-interview.pdf); [Optiver numerical test](https://numericaltest.optiver.com/); [Figgie](https://www.janestreet.com/culture/street-view/level-up-your-trading-skills-with-the-new-figgie-app/); [SIG Discovery](https://careers.sig.com/jobs/11148?lang=en-us) for first and second years |
| Quantitative researcher | Math Competition, pandas case study, Hackathon | [Harvard Stat 110](https://stat110.hsites.harvard.edu/) and [free textbook](http://probabilitybook.net); [Lo (2002)](https://traders.studentorg.berkeley.edu/papers/The-Statistics-of-Sharpe-Ratios.pdf); [Bailey et al. (2014)](https://www.ams.org/notices/201405/rnoti-p458.pdf); [D. E. Shaw interviewing guide](https://www.deshaw.com/assets/articles/D_E_Shaw_Group_Interviewing_Guide.pdf) |
| Quantitative developer | Hackathon package and tests, Git setup, SQL | [Jane Street SWE prep](https://www.janestreet.com/preparing-for-a-software-engineering-interview/); [Pro Git](https://git-scm.com/book); [GitHub Student Developer Pack](https://education.github.com/pack). FQE has no algorithms practice; members must add it on their own. |
| Bank quant, strats, or risk | Math Competition (distributions, linear algebra, series), SQL, pandas case study | [MIT OCW 18.600](https://ocw.mit.edu/courses/18-600-probability-and-random-variables-fall-2019/); [MIT OCW 18.06](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/pages/final-1806-lecture-2023/); [Pre-MFE seminars](https://mfe.baruch.cuny.edu/pre-mfe-program/); [J.P. Morgan Quantitative Finance](https://careers.jpmorgan.com/careers/programs/qr-summer-associate) (graduate program) |

The Goldman Sachs and J.P. Morgan quant programs found in the research are summer associate programs for graduate students. Undergraduates aiming at bank quant roles should treat the Baruch MFE and Pre-MFE path as the main entry point.

## 4. Resources by event

Each list is a short selection. The full tables, bibliographic details, and verification status are in the [resource map](research/resources.md).

**Trading Competition.** [Figgie by Jane Street](https://www.janestreet.com/culture/street-view/level-up-your-trading-skills-with-the-new-figgie-app/) (free app and web); [Jane Street Puzzles](https://www.janestreet.com/puzzles/); [Optiver Ready Trader Go](https://readytradergo.optiver.com/) (2026 run and US eligibility unverified).

**Brainteaser Battle.** [Harvard Stat 110](https://stat110.hsites.harvard.edu/) and the [free official textbook](http://probabilitybook.net); [Stat 110 lectures](https://www.youtube.com/playlist?list=PL2SOU6wwxB0uwwH80KTQ6ht66KWxbzTIo); [Jane Street probability primer](https://www.janestreet.com/static/pdfs/trading-interview.pdf). The interview books by Zhou, Crack, and Joshi et al. are listed with ISBNs in the [resource map, Section 2](research/resources.md#2-brainteasers-and-probability-interview-prep-brainteaser-battle-thu-oct-15). Use only probabilitybook.net for the Blitzstein and Hwang text, not unofficial PDF copies.

**SQL & Databases.** [SQLite window functions](https://sqlite.org/windowfunctions.html); [SQLite 3.25.0 release log](https://www.sqlite.org/releaselog/3_25_0.html); [Kaggle Learn](https://www.kaggle.com/learn) Intro and Advanced SQL (BigQuery dialect).

**Data Case Study.** [pandas group by](https://pandas.pydata.org/docs/user_guide/groupby.html); [`DataFrame.rolling`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rolling.html) (with an integer window, the first 20 values of a 21-day window are NaN); [merge and join](https://pandas.pydata.org/docs/user_guide/merging.html).

**Math Competition.** [MIT OCW 18.600](https://ocw.mit.edu/courses/18-600-probability-and-random-variables-fall-2019/); [MIT OCW 18.06](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/pages/final-1806-lecture-2023/); [Harvard Stat 110](https://stat110.hsites.harvard.edu/).

**Hackathon.** [Sharpe, "The Sharpe Ratio" (1994)](https://web.stanford.edu/~wfsharpe/art/art.htm); [Lo, "The Statistics of Sharpe Ratios" (2002)](https://traders.studentorg.berkeley.edu/papers/The-Statistics-of-Sharpe-Ratios.pdf), on when square-root-of-252 annualization overstates Sharpe; [Bailey et al. (2014)](https://www.ams.org/notices/201405/rnoti-p458.pdf), on backtest overfitting; [Kenneth French Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html) and [FRED API](https://fred.stlouisfed.org/docs/api/api_key.html) for free real data; [Newman Library financial data guide](https://guides.newman.baruch.cuny.edu/AccessFinData) for WRDS and Bloomberg. Do not commit vendor data.

**Markets primer.** For how equities, rates, credit, FX, commodities, and derivatives trade and are quoted, with interview practice prompts, read the [markets primer](markets/README.md).

## 5. Checkpoints with pass criteria

Criteria are copied from `.github/ISSUE_TEMPLATE/`. A checkpoint passes when every box is checked and each item has the requested evidence.

### Checkpoint 1: due Wednesday, October 14, 2026

- [ ] Competed in the Trading Competition (Friday, October 9) **or** ran three market-making drill sessions with `python drills/market_making/drill.py`
  - Evidence (team name, or P&L per round for each drill session):
- [ ] Posted a debrief using `templates/debrief.md` within 48 hours of the competition or the last drill
  - Link to post:
- [ ] Started an application tracker (spreadsheet or document with firm, role, deadline, and status columns)
  - Number of roles listed:

### Checkpoint 2: due Wednesday, November 4, 2026

- [ ] SQL daily returns query runs and matches the reference: `python sql/check.py 7 <your-file>.sql` reports a match
  - Output line:
- [ ] Presented a case study slide (Data Case Study, Thursday, October 22, or a later session) using `pandas/presentation_outline.md`
  - Link to slide:
- [ ] Completed 20 probability problems from `problems/brainteasers.md` or `problems/math.md`
  - Problem numbers completed:
- [ ] Set up Python 3.11 or later and installed this repository with `pip install -e .`
- [ ] Set up Git: cloned this repository, made a branch, and pushed one commit
  - Link to branch or commit:
- [ ] Set up a project from the FQE project template repository
  - Link to repository:

### Checkpoint 3: due Thursday, December 10, 2026

- [ ] Pushed your Hackathon repository (built from `backtest/`) with a README that states the strategy, the data, and the Sharpe ratio and maximum drawdown
  - Link to repository:
- [ ] Updated your résumé with fall results (competition placements, Hackathon project, case study)
  - Lines added:
- [ ] Chose a spring desk
  - Desk name:

## 6. Open items for the board

**(a) Trading Competition date.** The [FQE site](https://baruchfqe.github.io/) lists applications closing September 28 and the trading day on October 2. The handoff, the root README, the drill README, the debrief template, and Checkpoint 1 all say Friday, October 9. If October 2 is correct, the event falls before the drill's ship date of October 5, and members should satisfy Checkpoint 1 through three drill sessions. Confirm the date and update either the site or the repository.

**(b) Drawdown snippet in the plan doc.** The original skills plan doc shows a shortened snippet that sums log returns to compute drawdown. The repository computes drawdown on compounded simple returns, `equity = (1 + r).cumprod()`, with drawdown `equity / equity.cummax() - 1`. Drawdown measured on summed log returns equals ln(1 + DD), not DD. Peak and trough dates match, but the magnitude is wrong: a 50 percent drawdown reads as about -0.69. Replace the doc snippet with the repository definition:

```python
equity = (1 + r).cumprod()
max_dd = (equity / equity.cummax() - 1).min()
```

**(c) Links that need a manual check.** The research environment's proxy blocked direct page fetches for citadel.com, imc.com, janestreet.com, mfe.baruch.cuny.edu, sig.com, optiver.com, sqlite.org, python.org, devguide.python.org, pandas.pydata.org, guides.newman.baruch.cuny.edu, and stat110.hsites.harvard.edu. Facts from those domains were confirmed from search-result extracts only. Before any date goes on a slide or in a Discord announcement, a board member should open these pages first, because members act on them this fall:

1. [SIG Discovery Program](https://careers.sig.com/jobs/11148?lang=en-us) (November 16 deadline)
2. [Pre-MFE Program](https://mfe.baruch.cuny.edu/pre-mfe-program/) (seminar dates and tuition)
3. [Jane Street INSIGHT NYC](https://www.janestreet.com/apply-insight-nyc/) (January 4 to 9 dates)
4. [Citadel Securities Quant Invitational](https://www.citadelsecurities.com/careers/programs-and-events/the-citadel-securities-quant-invitational/) (fall 2026 deadline)
5. [Newman Library financial data guide](https://guides.newman.baruch.cuny.edu/AccessFinData) and [Bloomberg guide](https://guides.newman.baruch.cuny.edu/Bloomberg)
6. [Optiver numerical test](https://numericaltest.optiver.com/) and [Optiver recruitment FAQ](https://www.optiver.com/join-us/stories/optiver-europe-recruitment-faq/) (eight-month retake rule)

**(d) Other unverified items from the research.**

| Item | Status in research | Source |
| --- | --- | --- |
| Quant applications opened July to August 2026; interview slots fill by late October | Secondary only | [Extern](https://www.extern.com/post/quant-internships-summer-2027-guide) |
| Jane Street INSIGHT NYC application deadline | Unverified | [INSIGHT NYC](https://www.janestreet.com/apply-insight-nyc/) |
| Discover Citadel 2027 dates | Unverified, inferred from prior cycle | [Discover Citadel](https://www.citadel.com/careers/programs-and-events/discover-citadel/apply-for-discover-citadel-us-cap/) |
| Citadel Securities Quant Invitational fall 2026 deadline | Unverified | [Quant Invitational](https://www.citadelsecurities.com/careers/programs-and-events/the-citadel-securities-quant-invitational/) |
| Optiver FutureFocus, Jane Street FTTP, FOCUS, Bridge, and AMP 2026 to 2027 dates | Prior cycle or not located | [career pathways, Section 3](research/career_pathways.md#early-insight-and-discovery-programs-first--and-second-year-students) |
| Two Sigma New Seekers Summit 2026 to 2027 dates | Unverified | [New Seekers Summit](https://www.twosigma.com/new-seekers-summit/) |
| Rotman ITC February 18 to 20, 2027 | Search summary only | [Rotman RITC](https://www.rotman.utoronto.ca/faculty-and-research/education-labs/bmo-financial-group-finance-research-and-trading-lab/rotman-international-trading-competition/) |
| IMC Prosperity 2027 edition; IMC NYC office | Unverified | [Prosperity](https://prosperity.imc.com/) |
| Optiver Ready Trader Go in 2026 and US eligibility | Unverified | [Ready Trader Go](https://readytradergo.optiver.com/) |
| Open public SIG competition | Unverified | [SIG Trading](https://sig.com/careers/trading/) |
| Bloomberg hours, booking rules, and terminal versus workstation count | Unverified | [Bloomberg guide](https://guides.newman.baruch.cuny.edu/Bloomberg) |
| Python 3.12 to 3.14 support dates | Third-party summaries only | [Python devguide](https://devguide.python.org/versions/) |
| GitHub Copilot student plan changes in 2026 | Unverified | [GitHub Student Pack](https://education.github.com/pack) |
| Zhou "14th Edition" label | Unverified | [resource map, Section 2](research/resources.md#bibliographic-details) |
| Baruch MFE team won the 2023 Rotman competition | Secondary only | [Baruch MFE](https://mfe.baruch.cuny.edu/) |
| Ken French Data Library URL | Confirmed through a secondary source | [Ken French](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html) |

**(e) Repository gaps noticed while writing this plan.**

1. Resolved: `problems/math.md` and `problems/verify.py` shipped on October 1; `python problems/verify.py` reports 53 passed, 0 failed, 2 skipped.
2. Resolved: Checkpoint 2 now reads "Python 3.11 or later," matching the root README and `pyproject.toml`. The resource map notes that python.org no longer ships 3.11 binary installers after 3.11.9.
3. Checkpoint 2 requires a project from the FQE project template repository. That template was not available when this repository was built. Publish its link or drop the item.
4. The career research recommends a timed mental-math drill, because Optiver's first trading screen is an eight-minute, calculator-free numerical test. The repository has none.
