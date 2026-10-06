# FQE Fall 2026 Upskilling Resource Map

Prepared October 1, 2026, for the FQE Fall 2026 General Member Skills Plan. Context: `docs/HANDOFF.md`.

## Method and limits

Every claim below carries a source URL. Research used web search with result extracts from the cited pages. Direct page fetches were blocked by the network egress proxy for most domains (sqlite.org, python.org, devguide.python.org, pandas.pydata.org, guides.newman.baruch.cuny.edu, stat110.hsites.harvard.edu). As a result, "Verified" in this document means the fact appeared in a search extract attributed to the cited URL, preferably a primary source. A board member should open each primary URL once before the fact goes on a slide.

Status labels used throughout:

- **Verified (primary):** confirmed from an extract of the publisher, official documentation, or institution page.
- **Verified (secondary):** confirmed only from retailer, catalog, or third-party pages.
- **Unverified:** could not be confirmed, or sources conflict.

## 1. Market making and trading games (Trading Competition, Fri Oct 9)

Figgie is the strongest free practice resource. Jane Street invented it in 2013 to simulate open-outcry commodities trading, and it is available as a free app and online at figgie.com.

| Resource | Type | Cost | Why it matters | Source URL |
| --- | --- | --- | --- | --- |
| Figgie by Jane Street | Card game, app, web | Free | Practice quoting, inference from order flow, and trading against other players | https://www.janestreet.com/culture/street-view/level-up-your-trading-skills-with-the-new-figgie-app/ |
| Figgie (Google Play) | Mobile app | Free | Android access for members | https://play.google.com/store/apps/details?id=com.janestreet.figgie&hl=en_US |
| Figgie (App Store) | Mobile app | Free | iOS access for members | https://apps.apple.com/us/app/figgie-by-jane-street/id6466661064 |
| Optiver Ready Trader Go | Algorithmic market-making competition | Free to enter | Builds a market-making bot against a simulated exchange; Optiver states no prior market-making knowledge is required | https://readytradergo.optiver.com/ |
| Jane Street Puzzles | Monthly puzzle page | Free | Ongoing probability and logic practice from a trading firm | https://www.janestreet.com/puzzles/ |

Note: whether Ready Trader Go runs in 2026, and whether US students are eligible, is unverified. Past rounds (2021, 2023) are documented at https://optiver.com/working-at-optiver/career-hub/ready-trader-go-2023/.

Drill math check: the expected sum of three fair six-sided dice is 3 x 3.5 = 10.5. With one die revealed, fair value is the revealed value plus 2 x 3.5 = 7. This matches the handoff's `revealed + 7`. (Arithmetic, no source needed.)

## 2. Brainteasers and probability interview prep (Brainteaser Battle, Thu Oct 15)

The three interview books are commercial; the handoff correctly forbids reproducing their problems. Blitzstein and Hwang is the only one of the four with a free official online edition.

### Bibliographic details

| Title | Author(s) | Edition | Year | Publisher | ISBN-13 | Status | Source URL |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A Practical Guide to Quantitative Finance Interviews | Xinfeng Zhou | Listed by retailers as "14th Edition" (CreateSpace printing); original Lulu printing also exists | 2008 | CreateSpace Independent Publishing Platform (April 9, 2008); earlier printing by Lulu.com, ISBN 9781435715752 | 9781438236667 | Title, author, year, ISBN: Verified (secondary). Edition label: Unverified (retailer-assigned, no publisher page found) | https://www.amazon.com/Practical-Guide-Quantitative-Finance-Interviews/dp/1438236662 ; https://www.abebooks.com/9781435715752/Practical-Guide-Quantitative-Finance-Interviews-1435715756/plp |
| Heard on The Street: Quantitative Questions from Wall Street Job Interviews | Timothy Falcon Crack | Revised 26th | 2025 (August 25, 2025) | Timothy Crack (self-published) | 9781067058326 | Verified (secondary) | https://blackwells.co.uk/bookshop/product/Heard-on-The-Street-by-Timothy-Falcon-Crack/9781067058326 |
| Quant Job Interview Questions and Answers | Mark Joshi, Nicholas Denson, Andrew Downes | Second | 2013 (May 25, 2013) | Pilot Whale Press | 9780987122827 | Verified (secondary) | https://www.amazon.com/Quant-Interview-Questions-Answers-Second/dp/0987122827 |
| Introduction to Probability | Joseph K. Blitzstein, Jessica Hwang | Second | 2019 | Chapman & Hall/CRC (CRC Press), Texts in Statistical Science series | 9781138369917 | Verified (secondary) | https://books.google.com/books/about/Introduction_to_Probability_Second_Editi.html?id=1_-GDwAAQBAJ |

Crack edition history: the 25th edition (ISBN 9781991155481) appeared August 5, 2024, with 242 quantitative questions. The 26th edition contains 246 quantitative and 278 non-quantitative questions, more than 500 in total, per retailer listings. Source: https://www.betterworldbooks.com/product/detail/heard-on-the-street-quantitative-questions-from-wall-street-job-interviews-revised-25th-9781991155481/new

Joshi et al. contains over 300 questions with full solutions, covering option pricing, probability, numerical algorithms, and C++. Source: https://www.amazon.com/Quant-Interview-Questions-Answers-Second/dp/0987122827

### Free probability resources

| Resource | Type | Cost | Why it matters | Source URL |
| --- | --- | --- | --- | --- |
| Introduction to Probability, 2nd ed., free online edition | Textbook (official free version) | Free | The Stat 110 text; strong on conditioning, indicators, and story proofs used in interviews | http://probabilitybook.net (linked from https://stat110.hsites.harvard.edu/) |
| Harvard Stat 110 course site | Handouts, practice problems with solutions | Free | Strategic practice sets map directly to brainteaser topics | https://stat110.hsites.harvard.edu/ |
| Stat 110 lectures on YouTube | 34 video lectures | Free | Full lecture series by Blitzstein | https://www.youtube.com/playlist?list=PL2SOU6wwxB0uwwH80KTQ6ht66KWxbzTIo |
| Stat110x on edX | Online course | Free to audit; paid certificate optional | Interactive version complementary to the lectures | https://www.edx.org/course/introduction-to-probability-0 |
| Jane Street Puzzles | Puzzle archive | Free | Harder stretch problems | https://www.janestreet.com/puzzles/ |

Do not link to unofficial PDF copies of the Blitzstein and Hwang text that appear in search results; use probabilitybook.net only.

## 3. SQL and window functions (SQL & Databases, Tue Oct 20)

SQLite added window functions in release 3.25.0, dated 2018-09-15. This confirms the handoff's minimum of 3.25. The SQLite developers used the PostgreSQL window function documentation as their reference for expected behavior.

Python's `sqlite3` module links to whatever SQLite library the interpreter was built against, and the module's own minimum is far below 3.25 (the Python 3.13 documentation states a minimum of SQLite 3.15.2). A Python 3.11 build can therefore lack window functions if it links an old system SQLite. The python.org Windows installer for 3.11 bundles SQLite 3.39.4 or later (3.40.1 as of 3.11.3), so official Windows builds are safe. `check.py` should print `sqlite3.sqlite_version` and fail with a clear message below 3.25.0.

| Resource | Type | Cost | Why it matters | Source URL |
| --- | --- | --- | --- | --- |
| SQLite: Window Functions | Official docs | Free | Authoritative syntax for `LAG`, `OVER`, `PARTITION BY`, and `ROWS BETWEEN` frames used in Exercises 7 and 8 | https://sqlite.org/windowfunctions.html |
| SQLite Release 3.25.0 (2018-09-15) | Official release log | Free | Confirms window functions first shipped in 3.25.0 | https://www.sqlite.org/releaselog/3_25_0.html |
| Python `sqlite3` docs | Official docs | Free | Module behavior and minimum SQLite version | https://docs.python.org/3.13/library/sqlite3.html |
| CPython issue 94328 / PR 98676 | Official repository | Free | Records the 3.11 Windows installer move to SQLite 3.39.4 | https://github.com/python/cpython/pull/98676 |
| Kaggle Learn: Intro to SQL and Advanced SQL | Interactive course | Free, with certificate | Advanced SQL covers analytic (window) functions; uses BigQuery, so dialect differs slightly from SQLite | https://www.kaggle.com/learn |
| LeetCode SQL 50 | Problem set | Free plan | Interview-style drills including window functions | https://www.boot.dev/blog/backend/best-sql-practice-sites (secondary description) |
| SQLZoo | Interactive tutorials | Free | Basic SELECT through joins and some window functions | https://www.boot.dev/blog/backend/best-sql-practice-sites (secondary description) |
| SQLBolt | Interactive lessons | Free, no login | Good first hour on SELECT, WHERE, JOIN; does not cover window functions | https://sqlquest.app/vs-sqlbolt/ (secondary description) |

## 4. pandas data analysis (Data Case Study, Thu Oct 22)

The current stable pandas documentation is version 3.0.6, per page titles in search results. Link members to the stable `/docs/` paths so links do not go stale.

| Resource | Type | Cost | Why it matters | Source URL |
| --- | --- | --- | --- | --- |
| Group by: split-apply-combine | Official user guide | Free | Step 4 of the case study (sector averages); also documents `rolling()` on groupby objects | https://pandas.pydata.org/docs/user_guide/groupby.html |
| `DataFrame.rolling` | Official API reference | Free | Step 3 (21-day rolling volatility). With an integer window, `min_periods` defaults to the window size, so the first 20 values are NaN | https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rolling.html |
| Windowing operations | Official user guide | Free | Conceptual guide to rolling, expanding, and exponentially weighted windows | https://pandas.pydata.org/docs/user_guide/window.html |
| Merge, join, concatenate and compare | Official user guide | Free | Step 4 merge to `tickers.csv`; documents left, right, outer, inner, and cross joins | https://pandas.pydata.org/docs/user_guide/merging.html |
| `DataFrameGroupBy.rolling` | Official API reference | Free | Per-ticker rolling windows in one call | https://pandas.pydata.org/pandas-docs/version/2.2/reference/api/pandas.core.groupby.DataFrameGroupBy.rolling.html |
| Kaggle Learn: Pandas | Interactive course | Free, with certificate | Short hands-on exercises for members new to pandas | https://www.kaggle.com/learn |

## 5. Math competition topics (Math Competition, Fri Oct 30)

| Resource | Type | Cost | Why it matters | Source URL |
| --- | --- | --- | --- | --- |
| MIT OCW 18.600 Probability and Random Variables (Fall 2019, Sheffield) | Course: notes, problem sets, exams | Free | Covers distributions, conditional probability, joint distributions, CLT, and Markov chains; practice exams included | https://ocw.mit.edu/courses/18-600-probability-and-random-variables-fall-2019/ |
| MIT OCW 18.06 Linear Algebra (Spring 2010, Strang) | Course: video lectures, OCW Scholar format | Free | Systems, vector spaces, eigenvalues, positive definite matrices; covers the plan's linear algebra block | https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/pages/final-1806-lecture-2023/ |
| Harvard Stat 110 and free textbook | Course and textbook | Free | Indicator variables, Bayes' rule, gambler's ruin, and common distributions | https://stat110.hsites.harvard.edu/ |

MIT reports that Strang gave his final 18.06 lecture on May 15, 2023. Source: https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/pages/final-1806-lecture-2023/

## 6. Backtesting and the Hackathon (Thu Nov 12)

### Definitions checked against the handoff

**Sharpe ratio.** Sharpe introduced the measure in 1966 as the "reward-to-variability ratio" and restated it in "The Sharpe Ratio," Journal of Portfolio Management, Fall 1994, pp. 49 to 58. The standard definition uses return in excess of a benchmark or risk-free rate. The handoff's choice of a zero risk-free rate is a simplification; the docstring should state it.

**Annualization.** Multiplying a per-period Sharpe ratio by the square root of the number of periods (sqrt(252) for daily data) is correct only when returns are independent and identically distributed. Lo (2002) shows that serial correlation can overstate annualized Sharpe ratios by more than 65 percent for hedge fund returns and derives the general correction. The handoff's `sqrt(252)` is the standard convention for daily data; the docstring should state the i.i.d. assumption.

**Maximum drawdown.** Standard references define maximum drawdown as the largest peak-to-trough decline in cumulative value. The handoff's method (equity = cumulative product of 1 + r, drawdown = equity / running maximum - 1, reported as a negative number) matches this definition.

**Log-return drawdown in the plan doc.** Summing log returns gives log equity. Drawdown computed in log space equals ln(1 + DD), not DD. The peak and trough dates are the same, but the magnitude differs: a 50 percent simple drawdown appears as about -0.693 in log space. The handoff is right to flag this and align the doc to compounded simple returns. (Arithmetic, no source needed.)

**Look-ahead bias.** Using information not available at decision time inflates backtest results. Shifting the signal one bar, as `positions_from_signal` does, is the standard guard. Bailey, Borwein, López de Prado, and Zhu (2014) cover the related and larger problem of backtest overfitting.

| Resource | Type | Cost | Why it matters | Source URL |
| --- | --- | --- | --- | --- |
| Sharpe, "The Sharpe Ratio" (1994) | Primary paper, author's site | Free | Original definition and the warning on annualization | https://web.stanford.edu/~wfsharpe/art/art.htm |
| Lo, "The Statistics of Sharpe Ratios," Financial Analysts Journal 58(4), 2002, pp. 36 to 52 | Primary paper | Free PDF (hosted by a student club) | When sqrt(T) annualization fails; standard errors for Sharpe | https://traders.studentorg.berkeley.edu/papers/The-Statistics-of-Sharpe-Ratios.pdf |
| Bailey, Borwein, López de Prado, Zhu, "Pseudo-Mathematics and Financial Charlatanism," Notices of the AMS 61(5), May 2014, pp. 458 to 471 | Primary paper, publisher PDF | Free | Accessible explanation of backtest overfitting for a Hackathon talk | https://www.ams.org/notices/201405/rnoti-p458.pdf |
| Bailey and López de Prado, "The Deflated Sharpe Ratio" | Primary paper | Free | Adjusts Sharpe for multiple testing and non-normality | https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf |
| Magdon-Ismail and Atiya, maximum drawdown of Brownian motion | Research papers | Abstract free | Formal treatment of maximum drawdown as a risk measure | https://www.semanticscholar.org/paper/On-the-maximum-drawdown-of-a-Brownian-motion-Magdon-Ismail-Atiya/02bd29696844c0d428412d7300fa5056f0aa9172 |

## 7. Data access for students

**WRDS.** Newman Library subscribes to many (26) but not all WRDS datasets. Currently enrolled Baruch students and faculty can request a day pass by email or register for a personal account with a Baruch or CUNY SPS email address. Registration can take up to a week. Access is limited to the immediate Baruch community; alumni and students from other CUNY schools are excluded. Members should register by mid-October if they want WRDS data for the Hackathon.

**Bloomberg.** The Newman Library guide states that the Wasserman Trading Floor in the Subotnick Financial Services Center (Room 125, 151 East 25th Street) provides eleven Bloomberg terminals. A separate source mentions 55 workstations on the trading floor; the total workstation count versus Bloomberg terminal count is unverified. Hours and booking rules are unverified.

**Licensing.** Vendor data must not be committed to a public repository. The handoff's synthetic-data approach is consistent with this.

| Resource | Type | Cost | Why it matters | Source URL |
| --- | --- | --- | --- | --- |
| Newman Library: Access to Financial Data Platforms | Library guide | Free to Baruch students | Entry point for WRDS and Bloomberg access | https://guides.newman.baruch.cuny.edu/AccessFinData |
| Newman Library: Two Ways to Access WRDS | Library blog | Free | Day pass versus personal account | https://blogs.baruch.cuny.edu/newmanreference/2013/11/12/two-ways-to-access-wrds-databases/ |
| Newman Library: Bloomberg Professional at Baruch | Library guide | Free to Baruch students | Terminal location and count | https://guides.newman.baruch.cuny.edu/Bloomberg |
| Kenneth French Data Library | Factor and portfolio returns (CSV) | Free, no registration | Fama-French factors, momentum, industry portfolios back to 1926 | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html |
| FRED (Federal Reserve Bank of St. Louis) | Economic data and API | Free; API key required | Rates and macro series for the risk-free rate or case studies | https://fred.stlouisfed.org/docs/api/api_key.html |
| pandas-datareader | Python library | Free | Reads FRED and Ken French data into pandas | https://pandas-datareader.readthedocs.io/en/latest/readers/fred.html |

The Ken French library URL was confirmed only through a secondary source (https://instituteforautomatedresearch.org/wiki/datasets/ken-french/).

## 8. Tooling

**Python 3.11.** Python 3.11 is in security-fix-only status until October 2027 (end of life October 31, 2027), per PEP 664. Bug-fix releases ended April 1, 2024. In this phase python.org ships source-only releases; 3.11.9 was the last release with Windows and macOS binary installers. Members who install from python.org on Windows or macOS will get 3.11.9, not the latest 3.11 security release.

For comparison, per third-party summaries of the Python devguide: 3.12 is security-only until October 2028, 3.13 bug-fix support ends October 1, 2026 (today), and 3.14 (released October 7, 2025) receives bug fixes until October 1, 2027 with end of life in October 2030. These dates are unverified against the devguide itself because the page could not be fetched.

| Resource | Type | Cost | Why it matters | Source URL |
| --- | --- | --- | --- | --- |
| Status of Python versions | Official devguide | Free | Authoritative support dates | https://devguide.python.org/versions/ |
| PEP 664: Python 3.11 Release Schedule | Official PEP | Free | 3.11 lifecycle | https://peps.python.org/pep-0664/ |
| Pro Git (Chacon and Straub) | Book, official free online edition | Free | Complete Git reference; Checkpoint 2 requires Git setup | https://git-scm.com/book |
| GitHub Student Developer Pack | Student program | Free with student verification | Free developer tools; requires age 13 or older and enrollment, verified by school email or ID | https://education.github.com/pack |
| GitHub Community FAQ on the Student Pack and Copilot | Official community discussion | Free | Current details on Copilot access for students | https://github.com/orgs/community/discussions/111352 |

GitHub Copilot terms for students changed in 2026 according to third-party sources (a Copilot Student plan in March 2026 and a pause on new sign-ups in April 2026). This is unverified against GitHub's own pages; do not put it on a slide without checking https://education.github.com/pack.

## Corrections to the handoff

No factual statement in HANDOFF.md is contradicted. Three items need refinement:

1. **Python 3.11 installers.** The handoff's default of Python 3.11 is still supported (security fixes until October 2027), but python.org no longer ships 3.11 binary installers past 3.11.9. The root README step "Install Python 3.11" should say "Python 3.11 or later" and the `pyproject.toml` should use `requires-python = ">=3.11"` so members can install 3.12, 3.13, or 3.14. Source: https://peps.python.org/pep-0664/ and https://www.python.org/downloads/release/python-31111/
2. **SQLite version check location.** The handoff asks to confirm the "local SQLite version." The version that matters is the one linked into each member's Python (`sqlite3.sqlite_version`), not a system `sqlite3` binary. Python's own minimum is below 3.25. `check.py` should test this at runtime. Source: https://docs.python.org/3.13/library/sqlite3.html
3. **Sharpe docstring.** The handoff's annualized Sharpe with `sqrt(252)` and a zero risk-free rate is a standard convention, but standard references define Sharpe on excess returns and note that `sqrt(T)` scaling assumes i.i.d. returns. The `sharpe()` docstring should state both assumptions. Sources: https://web.stanford.edu/~wfsharpe/art/art.htm and https://traders.studentorg.berkeley.edu/papers/The-Statistics-of-Sharpe-Ratios.pdf

Confirmed as correct: SQLite 3.25.0 minimum for window functions; drawdown on compounded equity; the one-bar signal shift against look-ahead bias; the reveal-variant fair value of `revealed + 7`; the handoff's flag that the plan doc's log-return drawdown should be aligned.

## Verification status

| Claim | Status | Source URL |
| --- | --- | --- |
| SQLite window functions first released in 3.25.0, 2018-09-15 | Verified (primary) | https://www.sqlite.org/releaselog/3_25_0.html |
| Python `sqlite3` minimum SQLite is 3.15.2 (Python 3.13 docs) | Verified (primary) | https://docs.python.org/3.13/library/sqlite3.html |
| Python 3.11 Windows installer bundles SQLite 3.39.4, later 3.40.1 | Verified (primary) | https://github.com/python/cpython/pull/98676 ; https://docs.python.org/release/3.11.3/whatsnew/changelog.html |
| Python 3.11 security-only until October 2027 | Verified (primary) | https://peps.python.org/pep-0664/ |
| 3.11.9 was the last 3.11 release with binary installers | Verified (secondary, consistent with python.org release pages) | https://www.python.org/downloads/release/python-31111/ |
| Python 3.12 to 3.14 support dates | Unverified (third-party summaries only) | https://endoflife.ai/python |
| Zhou: title, author, 2008, CreateSpace, ISBN 9781438236667 | Verified (secondary) | https://www.amazon.com/Practical-Guide-Quantitative-Finance-Interviews/dp/1438236662 |
| Zhou: "14th Edition" label | Unverified | https://booksrun.com/9781438236667-a-practical-guide-to-quantitative-finance-interviews-14th-editionth |
| Crack: Revised 26th edition, August 25, 2025, ISBN 9781067058326 | Verified (secondary) | https://blackwells.co.uk/bookshop/product/Heard-on-The-Street-by-Timothy-Falcon-Crack/9781067058326 |
| Joshi, Denson, Downes: 2nd ed., Pilot Whale Press, 2013 | Verified (secondary) | https://www.amazon.com/Quant-Interview-Questions-Answers-Second/dp/0987122827 |
| Blitzstein and Hwang: 2nd ed., CRC Press, 2019, ISBN 9781138369917 | Verified (secondary) | https://books.google.com/books/about/Introduction_to_Probability_Second_Editi.html?id=1_-GDwAAQBAJ |
| Free official online edition at probabilitybook.net; free Stat 110 materials and edX course | Verified (primary) | https://stat110.hsites.harvard.edu/ |
| Figgie free app, invented at Jane Street in 2013 | Verified (primary) | https://www.janestreet.com/culture/street-view/level-up-your-trading-skills-with-the-new-figgie-app/ |
| Ready Trader Go running in 2026 and open to US students | Unverified | https://readytradergo.optiver.com/ |
| pandas stable docs at version 3.0.6 | Verified (primary) | https://pandas.pydata.org/docs/user_guide/groupby.html |
| `rolling` with integer window: `min_periods` defaults to window size | Verified (primary) | https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rolling.html |
| MIT OCW 18.600 and 18.06 free | Verified (primary) | https://ocw.mit.edu/courses/18-600-probability-and-random-variables-fall-2019/ |
| Sharpe 1994, JPM Fall 1994, pp. 49 to 58 | Verified (secondary) | https://web.stanford.edu/~wfsharpe/art/art.htm |
| Lo 2002: sqrt(T) annualization requires i.i.d.; overstatement above 65 percent | Verified (primary, paper PDF) | https://traders.studentorg.berkeley.edu/papers/The-Statistics-of-Sharpe-Ratios.pdf |
| Bailey et al. 2014, Notices AMS 61(5), 458 to 471 | Verified (primary) | https://www.ams.org/notices/201405/rnoti-p458.pdf |
| Maximum drawdown is the largest peak-to-trough decline | Verified (secondary) | https://en.wikipedia.org/wiki/Drawdown_(economics) |
| Baruch WRDS: 26 datasets, day pass or account, Baruch community only | Verified (primary) | https://guides.newman.baruch.cuny.edu/AccessFinData ; https://blogs.baruch.cuny.edu/newmanreference/2013/11/12/two-ways-to-access-wrds-databases/ |
| Baruch Bloomberg: eleven terminals, Wasserman Trading Floor, SFSC Room 125 | Verified (primary) | https://guides.newman.baruch.cuny.edu/Bloomberg |
| Bloomberg hours and booking rules | Unverified | https://guides.newman.baruch.cuny.edu/Bloomberg |
| Ken French Data Library free, no registration | Verified (secondary) | https://instituteforautomatedresearch.org/wiki/datasets/ken-french/ |
| FRED API free with key | Verified (primary) | https://fred.stlouisfed.org/docs/api/api_key.html |
| Pro Git free online | Verified (primary) | https://git-scm.com/learn |
| GitHub Student Pack eligibility (13+, enrolled, verified) | Verified (secondary) | https://github.com/orgs/community/discussions/111352 |
| GitHub Copilot student plan changes in 2026 | Unverified | https://perkstack.co/blog/github-student-pack-guide |
| SQLBolt lacks window functions; SQLZoo and LeetCode SQL 50 include them | Verified (secondary) | https://www.boot.dev/blog/backend/best-sql-practice-sites |

## Sources

1. https://www.sqlite.org/releaselog/3_25_0.html
2. https://sqlite.org/windowfunctions.html
3. https://docs.python.org/3.13/library/sqlite3.html
4. https://github.com/python/cpython/pull/98676
5. https://docs.python.org/release/3.11.3/whatsnew/changelog.html
6. https://peps.python.org/pep-0664/
7. https://devguide.python.org/versions/
8. https://www.python.org/downloads/release/python-31111/
9. https://endoflife.ai/python
10. https://www.amazon.com/Practical-Guide-Quantitative-Finance-Interviews/dp/1438236662
11. https://www.abebooks.com/9781435715752/Practical-Guide-Quantitative-Finance-Interviews-1435715756/plp
12. https://booksrun.com/9781438236667-a-practical-guide-to-quantitative-finance-interviews-14th-editionth
13. https://blackwells.co.uk/bookshop/product/Heard-on-The-Street-by-Timothy-Falcon-Crack/9781067058326
14. https://www.betterworldbooks.com/product/detail/heard-on-the-street-quantitative-questions-from-wall-street-job-interviews-revised-25th-9781991155481/new
15. https://www.amazon.com/Quant-Interview-Questions-Answers-Second/dp/0987122827
16. https://books.google.com/books/about/Introduction_to_Probability_Second_Editi.html?id=1_-GDwAAQBAJ
17. https://stat110.hsites.harvard.edu/
18. http://probabilitybook.net
19. https://www.youtube.com/playlist?list=PL2SOU6wwxB0uwwH80KTQ6ht66KWxbzTIo
20. https://www.edx.org/course/introduction-to-probability-0
21. https://www.janestreet.com/culture/street-view/level-up-your-trading-skills-with-the-new-figgie-app/
22. https://play.google.com/store/apps/details?id=com.janestreet.figgie&hl=en_US
23. https://apps.apple.com/us/app/figgie-by-jane-street/id6466661064
24. https://www.janestreet.com/puzzles/
25. https://readytradergo.optiver.com/
26. https://optiver.com/working-at-optiver/career-hub/ready-trader-go-2023/
27. https://www.kaggle.com/learn
28. https://www.boot.dev/blog/backend/best-sql-practice-sites
29. https://sqlquest.app/vs-sqlbolt/
30. https://pandas.pydata.org/docs/user_guide/groupby.html
31. https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rolling.html
32. https://pandas.pydata.org/docs/user_guide/window.html
33. https://pandas.pydata.org/docs/user_guide/merging.html
34. https://pandas.pydata.org/pandas-docs/version/2.2/reference/api/pandas.core.groupby.DataFrameGroupBy.rolling.html
35. https://ocw.mit.edu/courses/18-600-probability-and-random-variables-fall-2019/
36. https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/pages/final-1806-lecture-2023/
37. https://web.stanford.edu/~wfsharpe/art/art.htm
38. https://traders.studentorg.berkeley.edu/papers/The-Statistics-of-Sharpe-Ratios.pdf
39. https://www.ams.org/notices/201405/rnoti-p458.pdf
40. https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf
41. https://www.semanticscholar.org/paper/On-the-maximum-drawdown-of-a-Brownian-motion-Magdon-Ismail-Atiya/02bd29696844c0d428412d7300fa5056f0aa9172
42. https://en.wikipedia.org/wiki/Drawdown_(economics)
43. https://guides.newman.baruch.cuny.edu/AccessFinData
44. https://blogs.baruch.cuny.edu/newmanreference/2013/11/12/two-ways-to-access-wrds-databases/
45. https://guides.newman.baruch.cuny.edu/Bloomberg
46. https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
47. https://instituteforautomatedresearch.org/wiki/datasets/ken-french/
48. https://fred.stlouisfed.org/docs/api/api_key.html
49. https://pandas-datareader.readthedocs.io/en/latest/readers/fred.html
50. https://git-scm.com/book
51. https://git-scm.com/learn
52. https://education.github.com/pack
53. https://github.com/orgs/community/discussions/111352
54. https://perkstack.co/blog/github-student-pack-guide
