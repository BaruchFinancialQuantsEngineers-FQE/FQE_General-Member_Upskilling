# Markets Primer by Asset Class

Prepared October 6, 2026, for FQE (Financial Quants and Engineers, Baruch College) general members. This primer explains how financial markets work, one asset class at a time, so you can answer market questions in quant interviews and follow the speakers at club events. It complements the event folders in this repository and the [resource map](../research/resources.md), which covers interview math, SQL, pandas, and backtesting but not markets.

Items marked "(verify)" could not be confirmed from a primary or standard source. The [verification status](#verification-status) note at the end explains the method.

## Contents

1. [Purpose and how to use this primer](#1-purpose-and-how-to-use-this-primer)
2. [Market structure basics](#2-market-structure-basics)
3. [Asset classes](#3-asset-classes)
   - [3.1 Equities](#31-equities)
   - [3.2 Fixed income and rates](#32-fixed-income-and-rates)
   - [3.3 Credit](#33-credit)
   - [3.4 Foreign exchange](#34-foreign-exchange)
   - [3.5 Commodities](#35-commodities)
   - [3.6 Derivatives across assets](#36-derivatives-across-assets)
   - [3.7 Digital assets](#37-digital-assets)
4. [Cross-asset view and interview practice](#4-cross-asset-view-and-interview-practice)
5. [Glossary](#5-glossary)
6. [Resources by asset class](#6-resources-by-asset-class)

## 1. Purpose and how to use this primer

Quant interviews rarely test market trivia, but they do test whether you understand what you would be trading, modeling, or building for. A candidate who can explain why a bond price falls when yields rise, or why an at-the-money call is worth about $0.4\sigma S\sqrt{T}$, sounds like someone who can learn the desk quickly.

**30-minute first pass.** Read Section 2, then the first two paragraphs and the worked example of each asset class in Section 3, then the Fed transmission table in Section 4. Skip the formulas on the first pass. Come back to the sections your target role needs.

**Which sections matter for which role.**

| Role | Read closely | Skim |
| --- | --- | --- |
| Quantitative trader (market making, prop) | Section 2 (order books, spreads, market makers); 3.1 Equities; 3.6 Derivatives (put-call parity, Greeks); Section 4 | 3.3 Credit |
| Quantitative researcher (systematic, buy side) | 3.1 Equities; 3.2 Rates; 3.5 Commodities (roll yield); Section 4 cross-asset links | 3.7 Digital assets |
| Quantitative developer | Section 2 (order books, clearing, settlement, venues); quoting conventions in every asset class | Black-Scholes derivation |
| Bank quant, strats, or risk | 3.2 Rates (duration, convexity, SOFR); 3.3 Credit (CDS); 3.4 FX (covered interest parity); 3.6 Derivatives | 3.1 Equities microstructure |

Pair this primer with the market-making drill in `drills/market_making/` before the Trading Competition on Friday, October 9.

## 2. Market structure basics

**Primary and secondary markets.** In the primary market, an issuer sells new securities to investors and receives the cash: an IPO, a Treasury auction, or a new corporate bond deal. In the secondary market, investors trade existing securities with each other, and the issuer receives nothing.

**Exchanges and OTC markets.** An exchange is a regulated venue where many participants post orders into a central limit order book under common rules: the NYSE, Nasdaq, Cboe, and CME. Over-the-counter (OTC) markets are dealer networks where participants trade bilaterally, by phone, chat, or electronic request for quote (RFQ). US stocks, listed options, and futures trade mostly on exchanges. Most bonds, FX, and swaps trade OTC. Alternative trading systems (ATSs) are SEC-regulated electronic venues that match orders but are not exchanges; dark pools are ATSs that do not display orders publicly.

**Order books, bid, and ask.** A limit order book lists resting buy orders (bids) and sell orders (asks or offers) by price, with time priority at each price in most equity venues. The best bid and best ask form the inside quote. The bid-ask spread is the cost of immediacy: a market order buys at the ask or sells at the bid. A stock quoted 99.98 bid, 100.02 ask has a 4-cent spread, or 4 basis points of the midpoint.

**Market makers and liquidity.** Market makers quote both sides and earn the spread in exchange for inventory risk and adverse selection (trading against better-informed traders). A liquid market has tight spreads, deep size, and prices that recover quickly after a large trade.

**Clearing and settlement.** Clearing confirms a trade and calculates obligations; a central counterparty (CCP) becomes buyer to every seller and seller to every buyer. Settlement is the actual exchange of cash and securities. US equities moved from T+2 to T+1 settlement (one business day after the trade date) with a compliance date of May 28, 2024. US Treasury cash trades face a new SEC central clearing requirement; after an extension in February 2025, compliance dates are December 31, 2026 for cash trades and June 30, 2027 for repo (check the SEC for later changes).

**Key participants.**

| Participant | What it does |
| --- | --- |
| Dealers (bank trading desks) | Make markets OTC in bonds, FX, swaps, and structured products using the bank's balance sheet |
| Proprietary trading firms | Trade their own capital, often as electronic market makers in listed products (for example, Jane Street, Optiver, SIG, HRT) |
| Hedge funds | Run pooled money for investors with flexible strategies: systematic, discretionary macro, relative value, multi-manager |
| Asset managers | Run mutual funds, ETFs, and pensions for clients, mostly long only and benchmarked to an index |
| Central banks | Set short-term interest rates, manage reserves, and act as lender of last resort |

**Key US regulators.**

| Regulator | Main role |
| --- | --- |
| SEC (Securities and Exchange Commission) | Federal regulator of securities markets: stocks, bonds, listed options, exchanges, ATSs, broker-dealers, investment advisers, and security-based swaps such as single-name CDS |
| CFTC (Commodity Futures Trading Commission) | Federal regulator of US derivatives markets: futures, options on futures, and most swaps; polices fraud and manipulation in spot commodities, including bitcoin |
| FINRA (Financial Industry Regulatory Authority) | Self-regulatory organization overseeing broker-dealers under SEC supervision; runs TRACE, the bond trade reporting system |
| Federal Reserve | Conducts monetary policy through the FOMC, supervises bank holding companies, and operates payment systems |

Note that "OCC" means two different organizations: the Options Clearing Corporation (the CCP for US listed options) and the Office of the Comptroller of the Currency (a bank regulator). Context tells you which.

## 3. Asset classes

### 3.1 Equities

**What it is.** A share of common stock is a residual claim on a company's assets and earnings after creditors are paid, usually with voting rights. Returns come from price changes and dividends.

**How it trades and who trades it.** US stocks trade on many competing exchanges, on ATSs, and with wholesalers that fill retail orders. Electronic market makers supply most displayed liquidity. ETFs trade like stocks; authorized participants keep ETF prices near the basket's value by creating and redeeming shares.

**Quoting.** Prices are in dollars per share, in one-cent increments for most stocks. In September 2024 the SEC adopted a half-cent increment for some heavily traded stocks; its effective date was challenged by exchanges (verify current status). Market capitalization is price times shares outstanding, and indexes such as the S&P 500 are cap weighted.

**Main risks.** Market (beta) risk, company-specific risk, liquidity risk in small names, and gap risk around earnings announcements.

**Core formulas.** Simple and log returns, with dividend $D$:

$$R = \frac{P_1 + D - P_0}{P_0}, \qquad r = \ln\frac{P_1 + D}{P_0}$$

The CAPM relates expected excess return to market exposure: $E[R_i] - r_f = \beta_i \left(E[R_m] - r_f\right)$, with $\beta_i = \mathrm{Cov}(R_i, R_m)/\mathrm{Var}(R_m)$.

**Worked example.** You buy at \$100.00, receive a \$2.00 dividend, and sell at \$108.00. Simple return is $(108 + 2 - 100)/100 = 10.0\%$. Log return is $\ln(1.10) = 9.53\%$. Log returns add across periods; simple returns add across assets in a portfolio.

**What quant roles do.** Traders make markets in stocks, ETFs, and baskets. Researchers build cross-sectional signals (value, momentum, quality) and risk models. Developers build low-latency order handling and market data feeds.

**Resources.** Harris, *Trading and Exchanges* (Oxford University Press, 2003); [Investor.gov, Introduction to Investing](https://www.investor.gov/introduction-investing); [Investor.gov glossary: ATSs](https://www.investor.gov/introduction-investing/investing-basics/glossary/alternative-trading-systems-atss); [Kenneth French Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html).

### 3.2 Fixed income and rates

**What it is.** A bond is a loan to the issuer: the holder receives fixed or floating coupons and the face value at maturity. US Treasuries are the benchmark: bills (one year or less, issued at a discount), notes (2 to 10 years), and bonds (20 and 30 years), plus TIPS, which adjust principal for inflation. SIFMA reports about \$30 trillion of Treasuries outstanding in 2025, the largest US fixed income sector.

**How it trades and who trades it.** The Treasury sells new issues at auction; they then trade OTC through primary dealers and electronic interdealer platforms, and Treasury futures trade on CME. Holders include foreign central banks, the Fed, banks, money funds, pensions, and hedge funds running basis and relative value trades.

**Quoting.** Prices are quoted per 100 of face value. Treasury notes and bonds are quoted in 32nds: 99-16 means $99 + 16/32 = 99.50$. Traders think in yields and quote changes in basis points (1 bp = 0.01%). The quoted (clean) price excludes accrued interest; the buyer pays the dirty price.

**The yield curve.** The curve plots yield against maturity. It normally slopes upward because investors demand a term premium. An inverted curve (2-year yield above 10-year) has historically preceded several US recessions. The front end tracks expected Fed policy; the long end adds expected growth, inflation, and term premium.

**SOFR.** The Secured Overnight Financing Rate measures the cost of borrowing cash overnight against Treasury collateral (repo). The New York Fed publishes it each business day at about 8:00 a.m. ET as a volume-weighted median of repo transactions. SOFR replaced USD LIBOR, whose remaining panel settings ended after June 30, 2023; the Fed's rule under the LIBOR Act names SOFR-based replacements for legacy contracts. Most new USD floating-rate loans and swaps reference SOFR.

**Main risks.** Interest rate risk (prices fall when yields rise), reinvestment risk, inflation risk, liquidity risk in off-the-run issues, and for anything other than Treasuries, credit risk (Section 3.3).

**Core formulas.** Price of a bond with annual coupon $C$, face $F$, yield $y$, and $T$ years:

$$P = \sum_{t=1}^{T} \frac{C}{(1+y)^t} + \frac{F}{(1+y)^T}$$

Macaulay duration is the present-value-weighted average time to cash flows, and modified duration measures price sensitivity:

$$D_{\text{mac}} = \frac{1}{P}\sum_{t} \frac{t \cdot CF_t}{(1+y)^t}, \qquad D_{\text{mod}} = \frac{D_{\text{mac}}}{1+y}, \qquad \frac{\Delta P}{P} \approx -D_{\text{mod}}\,\Delta y + \tfrac{1}{2}\,\text{Conv}\,(\Delta y)^2$$

DV01 (dollar value of a basis point) is $D_{\text{mod}} \times P \times 0.0001$.

**Worked example.** A 5-year bond pays a 4% annual coupon on 100 face, and its yield is 5%. Price is 95.67 (below par because the coupon is below the yield). Macaulay duration is 4.62 years, modified duration is 4.40, and convexity is 24.47. DV01 is 0.042 per 100 face. If yields rise 50 bp, duration alone predicts a price change of $-4.40 \times 0.005 \times 95.67 = -2.10$. Adding convexity gives $-2.076$, which matches the exact repricing of $-2.076$ to three decimals.

**What quant roles do.** Bank strats build yield curves from SOFR swaps and Treasury futures, price swaps and swaptions, and compute DV01 ladders. Relative value researchers trade curve shapes and futures basis.

**Resources.** Tuckman and Serrat, *Fixed Income Securities*, 4th ed. (Wiley, 2022); Fabozzi and Fabozzi, *Bond Markets, Analysis, and Strategies*, 10th ed. (MIT Press, 2021); [NY Fed SOFR page](https://www.newyorkfed.org/markets/reference-rates/sofr); [CME Group, Introduction to Treasuries](https://www.cmegroup.com/education/courses/introduction-to-treasuries).

### 3.3 Credit

**What it is.** Credit markets price the risk that a borrower other than the US government fails to pay. Corporate bonds rated BBB- or higher (by S&P and Fitch; Baa3 by Moody's) are investment grade (IG). Bonds rated below that are high yield (HY), also called junk. SIFMA reports about \$11.5 trillion of US corporate bonds outstanding in the third quarter of 2025.

**How it trades and who trades it.** Corporate bonds trade OTC through dealers, increasingly on electronic RFQ and portfolio-trading platforms. FINRA's TRACE system publishes trade prices, generally within 15 minutes. Credit default swaps (CDS) trade OTC; index CDS (CDX in North America) are centrally cleared and far more liquid than most single bonds. Insurers, pensions, asset managers, and credit hedge funds hold most of it.

**Quoting.** Credit is quoted as a spread over a benchmark, in basis points: a bond yielding 6.20% when the matching Treasury yields 4.40% trades at a spread of 180 bp. Since the 2009 "Big Bang" standardization, North American CDS pay a fixed coupon of 100 bp (IG) or 500 bp (HY), and the difference from the market spread is settled as an upfront payment.

**Main risks.** Default risk, downgrade risk, spread widening in risk-off markets, recovery uncertainty, and poor liquidity in stress, when spreads and bid-ask both widen.

**Core formulas.** A rough credit triangle links the spread $s$, the annual default probability (hazard rate) $\lambda$, and recovery rate $R$:

$$s \approx \lambda\,(1 - R)$$

A CDS buyer pays the spread on the notional each year (usually quarterly) and receives $(1 - R) \times \text{notional}$ if the reference entity defaults.

**Worked example.** The 180 bp spread above, with an assumed 40% recovery, implies $\lambda \approx 0.018/0.60 = 3.0\%$ per year. Buying \$10 million of CDS protection at 180 bp costs \$180,000 per year, or \$45,000 per quarter. This spread-implied probability is risk-neutral and usually exceeds historical default rates because investors also demand compensation for spread volatility and illiquidity.

**What quant roles do.** Bank credit strats build hazard-rate curves and price CDS and tranches. Systematic credit researchers build signals from spreads, equity data, and fundamentals. Risk teams model counterparty exposure (CVA).

**Resources.** [FINRA, What Is TRACE](https://www.finra.org/investors/insights/what-is-TRACE); [BIS Quarterly Review, "The 'Big Bang' in the CDS market"](https://www.bis.org/publ/qtrpdf/r_qt1012z.htm); [FRED, ICE BofA US High Yield OAS](https://fred.stlouisfed.org/series/BAMLH0A0HYM2); Tuckman and Serrat (chapters on corporate bonds and CDS).

### 3.4 Foreign exchange

**What it is.** The FX market exchanges one currency for another. It is the largest financial market: the BIS 2025 Triennial Survey measured average turnover of \$9.6 trillion per day in April 2025, up 28% from 2022, with the US dollar on one side of 89% of trades.

**How it trades and who trades it.** FX trades OTC around the clock on weekdays, through bank dealers, electronic platforms, and nonbank market makers. Products are spot (settles in two business days for most pairs, one for USD/CAD), outright forwards, FX swaps (a spot plus an offsetting forward, the largest product by volume), currency options, and CME FX futures. Users include corporate hedgers, asset managers, central banks, and macro funds.

**Quoting.** A pair is quoted as BASE/QUOTE: EUR/USD at 1.1000 means one euro costs 1.10 dollars. A pip is usually the fourth decimal (0.0001); for yen pairs it is the second. Forwards are quoted as forward points added to spot.

**Main risks.** Exchange rate moves, central bank intervention, gap risk around policy announcements, and for emerging market currencies, capital controls and convertibility risk.

**Core formulas.** Covered interest parity (CIP) says a hedged foreign deposit earns the same as a domestic one. With domestic rate $r_d$ (the quote currency) and foreign rate $r_f$ (the base currency):

$$F = S\,\frac{1 + r_d T}{1 + r_f T} \quad \text{(simple)}, \qquad F = S\,e^{(r_d - r_f)T} \quad \text{(continuous)}$$

The higher-yielding currency trades at a forward discount. Uncovered interest parity (no hedge) is a hypothesis, not an arbitrage, and often fails; the carry trade bets on that failure.

**Worked example.** EUR/USD spot is 1.1000, the one-year USD rate is 4%, and the EUR rate is 2%. The one-year forward is $1.1000 \times 1.04/1.02 = 1.1216$, or about +216 forward points. With continuous compounding, $1.1000\,e^{0.02} = 1.1222$. Since 2008, CIP has shown persistent deviations (the cross-currency basis) because of bank balance sheet costs and hedging demand.

**What quant roles do.** Electronic FX market makers price spot and forwards across many venues. Bank quants price FX options and model volatility smiles. Systematic researchers trade carry, momentum, and value across currencies.

**Resources.** [BIS Triennial Survey, OTC FX turnover in April 2025](https://www.bis.org/statistics/rpfx25_fx.htm); [Borio et al., "Covered interest parity lost," BIS Quarterly Review, September 2016](https://www.bis.org/publ/qtrpdf/r_qt1609e.htm); [CME Group, Introduction to FX](https://www.cmegroup.com/education/courses/introduction-to-fx.html).

### 3.5 Commodities

**What it is.** Commodities are physical goods: energy (crude oil, natural gas), metals (gold, copper), and agriculture (corn, soybeans, cattle). Financial exposure is almost always through futures, because storing and shipping the physical good is costly.

**How it trades and who trades it.** Futures trade on exchanges such as CME Group (including NYMEX and COMEX) and ICE. Producers and consumers hedge (a farmer sells next year's harvest forward), trading houses arbitrage locations and grades, and speculators, trend followers (CTAs), and index investors take the other side.

**Quoting.** Each contract has a fixed size, delivery month, and price unit (for example, dollars per barrel of crude). The futures curve is the set of prices across delivery months.

**Contango and backwardation.** In contango, futures prices are above spot and rise with maturity, typical when storage is plentiful. In backwardation, futures are below spot, typical when inventories are tight and holding the physical good has a convenience yield.

**Main risks.** Price risk, weather and supply shocks, storage and delivery risk (most speculators close or roll positions before delivery), and roll risk.

**Core formulas.** The cost-of-carry model, with financing rate $r$, storage cost $u$, and convenience yield $y$ (all continuous):

$$F = S\,e^{(r + u - y)T}$$

Roll yield is the return from rolling an expiring contract into the next: negative in contango, positive in backwardation.

**Worked example.** Spot crude is \$80.00, $r = 4\%$, storage costs 2% per year, and the convenience yield is zero. The 3-month futures price is $80\,e^{0.06 \times 0.25} = \$81.21$. Now suppose you buy a futures contract at \$81.00 while spot is \$80.00, and spot stays at \$80.00. The future converges to spot at expiry, so you lose \$1.00, or $80/81 - 1 = -1.23\%$, even though "oil was flat."

**What quant roles do.** Traders run calendar spreads and relative value across grades and locations. Researchers build trend-following and carry signals across futures.

**Resources.** [CME Group, Introduction to Futures](https://www.cmegroup.com/education/courses/introduction-to-futures.html); [CME Group, What is contango and backwardation](https://www.cmegroup.com/education/courses/introduction-to-base-metals/what-is-contango-and-backwardation.html).

### 3.6 Derivatives across assets

**What it is.** A derivative's value depends on an underlying asset or rate. The four building blocks are forwards (a custom OTC agreement to trade at a set price on a future date), futures (standardized, exchange-traded, marked to market daily, with margin), options (the right but not the obligation to buy, a call, or sell, a put, at the strike $K$), and swaps (exchanges of cash flow streams, such as fixed against SOFR).

**How it trades and who trades it.** Listed options trade on Cboe, Nasdaq, NYSE, and other exchanges and clear through the Options Clearing Corporation. Futures trade on CME, ICE, and Cboe Futures Exchange. Swaps trade OTC, increasingly on swap execution facilities, and standard swaps must be centrally cleared. The BIS 2025 survey measured OTC interest rate derivatives turnover of \$7.9 trillion per day in April 2025.

**Quoting.** Futures are quoted in the underlying's units. Options are quoted in premium per share (US equity options usually cover 100 shares), and traders compare them by implied volatility. Swaps are quoted by their fixed rate.

**Main risks.** Market risk through the Greeks, volatility risk, counterparty risk for uncleared OTC trades, and margin calls, which can force liquidation of a position that would have recovered.

**Core formulas.** Forward on an asset with continuous dividend yield $q$: $F = S e^{(r - q)T}$. Put-call parity for European options on a non-dividend stock: $C - P = S - K e^{-rT}$.

Black-Scholes for a European call (no dividends):

$$C = S\,N(d_1) - K e^{-rT} N(d_2), \qquad d_1 = \frac{\ln(S/K) + (r + \sigma^2/2)T}{\sigma\sqrt{T}}, \qquad d_2 = d_1 - \sigma\sqrt{T}$$

**Black-Scholes intuition.** A long call can be replicated by holding $N(d_1)$ shares and borrowing, rebalanced continuously. Because the hedge removes the stock's direction, the price does not depend on the stock's expected return, only on volatility $\sigma$. $N(d_2)$ is the risk-neutral probability the call finishes in the money. The model assumes constant volatility and lognormal prices; real markets show a volatility smile or skew, which is why traders quote implied volatility rather than price.

**The Greeks.**

| Greek | Definition | Long call sign | Intuition |
| --- | --- | --- | --- |
| Delta $\Delta$ | $\partial V/\partial S$ | + (between 0 and 1) | Shares-equivalent exposure; hedge ratio |
| Gamma $\Gamma$ | $\partial^2 V/\partial S^2$ | + | How fast delta changes; largest at the money near expiry |
| Vega | $\partial V/\partial \sigma$ | + | Profit from a rise in implied volatility |
| Theta $\Theta$ | $\partial V/\partial t$ | usually negative | Time decay; the cost of owning gamma |
| Rho $\rho$ | $\partial V/\partial r$ | + | Sensitivity to interest rates |

**Worked example.** Take $S = 100$, $K = 100$, $r = 5\%$, $\sigma = 20\%$, $T = 1$. Then $d_1 = 0.35$ and $d_2 = 0.15$, so $C = 10.45$ and the put is $P = 5.57$. Check parity: $C - P = 4.88$ and $S - Ke^{-rT} = 100 - 95.12 = 4.88$. Delta is $N(0.35) = 0.637$, gamma is 0.0188, and vega is 0.375 per volatility point. The shortcut $C \approx 0.4\,\sigma S\sqrt{T} = 8.0$ applies to an at-the-money option with zero rates; the gap to 10.45 is mostly the 5% rate. With a 2% dividend yield, the one-year forward on this stock is $100\,e^{0.03} = 103.05$.

**What quant roles do.** Options traders quote and hedge books of thousands of options by their Greeks. Bank quants build pricing models and volatility surfaces and compute risk for exotic products. Developers build pricing libraries and real-time risk systems.

**Resources.** Hull, *Options, Futures, and Other Derivatives*, 11th ed. (Pearson, 2021, copyright 2022); [Options Industry Council](https://www.optionseducation.org/); [Cboe Options Institute Learning Portal](https://www.cboe.com/optionsinstitute/learningportal); [MIT OCW 18.S096](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/).

### 3.7 Digital assets

**What it is.** Cryptocurrencies such as bitcoin and ether are native tokens of public blockchains. Stablecoins are tokens designed to hold a fixed value, usually one US dollar, backed by reserves.

**How it trades and who trades it.** Spot crypto trades around the clock on centralized exchanges and decentralized exchanges. CME lists bitcoin and ether futures. The SEC approved the first US spot bitcoin exchange-traded products on January 10, 2024.

**Regulation.** The CFTC treats bitcoin as a commodity and regulates crypto derivatives. The GENIUS Act, signed July 18, 2025, created a federal framework for payment stablecoins, including 1:1 reserve backing. A broader market-structure bill dividing spot crypto oversight between the SEC and CFTC had not become law as of early October 2026 (verify).

**Main risks.** Very high volatility, exchange and custody failure, smart contract bugs, stablecoin de-pegging, and regulatory change. A token with 3% daily volatility has annualized volatility of about $0.03\sqrt{365} = 57\%$ (using 365 days because crypto trades every day).

**What quant roles do.** Market making across venues, funding-rate and basis arbitrage between spot and perpetual futures, and on-chain data research.

**Resources.** [CFTC bitcoin resource page](https://www.cftc.gov/bitcoin); [CFTC, Bitcoin Basics](https://www.cftc.gov/sites/default/files/2019-12/oceo_bitcoinbasics0218.pdf).

## 4. Cross-asset view and interview practice

### How the markets typically interact

These are tendencies, not laws. Signs depend on whether growth, inflation, or policy drives the move. In 2022, stocks and bonds fell together because inflation drove both.

- **Rates and equities.** Higher real yields lower the present value of future earnings, so long-duration growth stocks are most rate-sensitive. When yields rise because growth is strong, stocks can rise too.
- **Rates and the dollar.** Higher US rates relative to other countries tend to strengthen the dollar, because they raise the return on dollar assets.
- **The dollar and commodities.** Commodities are priced in dollars, so a stronger dollar tends to coincide with weaker dollar commodity prices. Gold often moves inversely to real yields because it pays no income.
- **Equities and credit.** Credit spreads and equity prices usually move in opposite directions: both reflect the value of the firm and the risk of default. HY spreads behave more like equities than like Treasuries.
- **Risk-on and risk-off.** In stress, investors buy Treasuries, the dollar, the yen, and gold, and sell equities, HY credit, emerging market currencies, and industrial commodities.

### How a Fed rate decision transmits

Markets price expected policy in advance through fed funds futures and SOFR futures, so prices move on the **surprise** relative to expectations, not on the decision itself. The table shows typical first-day reactions to a hawkish surprise (a larger hike or smaller cut than priced). A dovish surprise reverses the signs.

| Market | Typical reaction to a hawkish surprise | Mechanism |
| --- | --- | --- |
| Front-end Treasuries (2-year) | Yields rise most | Directly reprice the expected policy path |
| Long-end Treasuries (10-year, 30-year) | Yields rise less; curve flattens | Tighter policy lowers expected future inflation and growth |
| US dollar | Strengthens | Higher relative rates attract capital |
| Equities | Fall, led by long-duration growth stocks | Higher discount rate and slower expected growth |
| Credit | Spreads widen, HY more than IG | Higher funding costs and default risk |
| Commodities and gold | Usually weaken | Stronger dollar, higher real yields, weaker demand |
| Emerging markets | Currencies and bonds weaken | Dollar funding becomes more expensive |

The FOMC sets a target range for the federal funds rate, 25 bp wide, and steers it with administered rates such as interest on reserve balances. SOFR and other money market rates follow. Check the current range on the [Federal Reserve's monetary policy page](https://www.federalreserve.gov/monetarypolicy.htm) (verify URL) before an interview.

### Interview practice prompts

Answer each prompt aloud in under a minute before opening the answer.

<details>
<summary>1. A bond's yield rises from 5% to 5.5%. Its modified duration is 4.4 and its price is 95.67. Estimate the new price.</summary>

The price falls by about $4.4 \times 0.005 \times 95.67 \approx 2.10$, to about 93.57. Convexity makes the true drop slightly smaller (2.08), so the true price is about 93.59.
</details>

<details>
<summary>2. A stock is at 50, a 1-year European call with strike 50 is 6, rates are zero, and there are no dividends. What is the put worth? What do you do if it trades at 7?</summary>

Put-call parity with $r = 0$ gives $P = C - S + K = 6 - 50 + 50 = 6$. If the put trades at 7, it is rich: sell the put, buy the call, and short the stock. That locks in 1 at expiry regardless of the stock price.
</details>

<details>
<summary>3. Why is a futures price on crude oil sometimes below the spot price?</summary>

Backwardation. When inventories are tight, holders of physical oil earn a convenience yield (they can keep refineries running or meet sudden demand), which outweighs financing and storage costs. In $F = S e^{(r + u - y)T}$, a large $y$ makes $F < S$.
</details>

<details>
<summary>4. The one-year USD rate is 4% and the JPY rate is 0.5%. Will the USD/JPY forward be above or below spot?</summary>

Below. The yen is the quote currency, so $F = S(1 + r_{JPY})/(1 + r_{USD})$, which is less than $S$. The higher-yielding currency (USD) trades at a forward discount, which offsets its interest advantage. Otherwise you could borrow yen, convert, invest in dollars, and sell dollars forward for a riskless profit.
</details>

<details>
<summary>5. What is the delta of an at-the-money call, and why is it not exactly 0.5?</summary>

Roughly 0.5. Under Black-Scholes it is $N(d_1)$, and $d_1 = (r + \sigma^2/2)T/(\sigma\sqrt{T}) > 0$ at the money, so delta is slightly above 0.5 (0.637 in the Section 3.6 example, mostly due to the 5% rate). A trader would also note that delta is not the probability of finishing in the money; that is closer to $N(d_2)$ under the risk-neutral measure.
</details>

<details>
<summary>6. Why did US markets replace LIBOR with SOFR?</summary>

LIBOR was based on bank submissions about unsecured borrowing that rarely occurred, which made it fragile and open to manipulation. SOFR is calculated from a large volume of actual overnight Treasury repo transactions, published by the New York Fed. The remaining USD LIBOR panel settings ended after June 30, 2023.
</details>

<details>
<summary>7. What does a market maker lose to, and how does it protect itself?</summary>

It loses to informed traders (adverse selection) and to inventory moving against it. It protects itself by widening the spread when uncertainty or order imbalance is high, skewing quotes to reduce unwanted inventory, limiting size, and hedging in correlated instruments. You practice the same skills in the market-making drill.
</details>

<details>
<summary>8. The Fed cuts rates by 25 bp, exactly as expected. What happens to the 2-year yield?</summary>

Very little on the decision itself, because the cut was already priced. The market reacts to the statement, the projections, and the press conference, which change expectations for future meetings.
</details>

<details>
<summary>9. Why can a long-only commodity index lose money when spot prices are flat?</summary>

Negative roll yield in contango. The fund buys deferred futures above spot and sells them back as they converge down toward spot near expiry. Section 3.5 shows a 1.23% loss in one roll with spot unchanged.
</details>

## 5. Glossary

| Term | Definition |
| --- | --- |
| Adverse selection | Losses a market maker takes from trading with better-informed counterparties |
| Alternative trading system (ATS) | SEC-regulated electronic venue that matches orders but is not an exchange; includes dark pools |
| Backwardation | Futures prices below spot, typical when supply is tight |
| Basis point (bp) | One hundredth of a percentage point, 0.01% |
| Beta | Sensitivity of an asset's return to the market's return |
| Bid, ask, and spread | Bid is the highest price a buyer will pay; ask (offer) is the lowest price a seller will accept; the spread is ask minus bid, the cost of immediate execution |
| Carry | Return from holding a position if prices do not change (coupon or rate differential minus funding) |
| Central counterparty (CCP) | Clearinghouse that becomes buyer to every seller and seller to every buyer |
| Contango | Futures prices above spot, typical when storage is ample |
| Convenience yield | Benefit from holding the physical commodity rather than a futures contract |
| Convexity | Curvature of the price-yield relationship; second-order rate sensitivity |
| Covered interest parity (CIP) | No-arbitrage link between spot, forward, and the two currencies' interest rates |
| Credit default swap (CDS) | Contract paying the buyer the loss on a reference debt if the issuer defaults, in exchange for a periodic premium |
| Delta | Change in an option's value per unit change in the underlying price |
| Clean and dirty price | Clean price is the quoted bond price excluding accrued interest; dirty price adds accrued interest and is what the buyer pays |
| Duration (modified) | Percentage price change of a bond per unit change in yield |
| DV01 | Dollar price change for a 1 bp change in yield |
| Forward | Custom OTC contract to trade an asset at a set price on a future date |
| Futures | Standardized exchange-traded forward, marked to market daily with margin |
| Gamma | Rate of change of delta with respect to the underlying price |
| High yield (HY) | Bonds rated below investment grade (below BBB- or Baa3) |
| Implied volatility | The volatility that makes a pricing model match an option's market price |
| Investment grade (IG) | Bonds rated BBB- or Baa3 and above |
| Limit order book | Ranked list of resting buy and sell limit orders on a venue |
| Liquidity | Ability to trade size quickly at a price near the current quote |
| Margin | Collateral posted to cover potential losses on a position |
| Market maker | Firm that continuously quotes bids and offers and earns the spread for holding inventory risk |
| OTC (over the counter) | Bilateral trading through dealers rather than on an exchange |
| Put-call parity | No-arbitrage relation $C - P = S - Ke^{-rT}$ for European options |
| Repo | Sale of a security with an agreement to buy it back; in effect a collateralized loan |
| Roll yield | Return from rolling an expiring futures contract into a later one |
| Settlement | Final exchange of cash and securities after a trade; T+1 for US equities |
| SOFR | Secured Overnight Financing Rate; the main USD benchmark rate, based on Treasury repo |
| Swap | Agreement to exchange cash flow streams, such as fixed against floating rates |
| Vega | Change in an option's value per change in implied volatility |
| Yield curve | Yields of comparable bonds plotted against maturity |

## 6. Resources by asset class

Costs reflect the publisher's access model as of October 2026. Books are not free; the Newman Library may hold copies.

| Resource | Type | Cost | Asset class | Link |
| --- | --- | --- | --- | --- |
| Harris, *Trading and Exchanges: Market Microstructure for Practitioners* (Oxford University Press, 2003) | Book | Paid | Market structure, equities | [OUP Academic](https://academic.oup.com/book/52292) |
| Investor.gov, Introduction to Investing and glossary | SEC investor education | Free | Market structure, equities | [investor.gov](https://www.investor.gov/introduction-investing) |
| Investor.gov bulletin, "New T+1 settlement cycle" | SEC investor bulletin | Free | Market structure | [Bulletin](https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins/new-t1-settlement-cycle-what-investors-need-know-investor-bulletin) |
| Yale ECON 252, Financial Markets (Shiller, Spring 2011) | Video course | Free | All | [Open Yale Courses, Lecture 1](https://oyc.yale.edu/economics/econ-252-11/lecture-1) |
| MIT OCW 15.401 Finance Theory I (Lo, Fall 2008) | Course: video, notes, problem sets | Free | Equities, fixed income, derivatives | [MIT OCW](https://ocw.mit.edu/courses/15-401-finance-theory-i-fall-2008/) |
| MIT OCW 18.S096 Topics in Mathematics with Applications in Finance (Fall 2013) | Course: video, notes | Free | Rates, derivatives, risk | [MIT OCW](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/) |
| Kenneth French Data Library | Data | Free | Equities | [Tuck](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html) |
| Tuckman and Serrat, *Fixed Income Securities*, 4th ed. (Wiley, 2022) | Book | Paid | Rates, credit | [Wiley-VCH listing](https://www.wiley-vch.de/en/areas-interest/finance-economics-law/fixed-income-securities-978-1-119-83555-4) |
| Fabozzi and Fabozzi, *Bond Markets, Analysis, and Strategies*, 10th ed. (MIT Press, 2021) | Book | Paid | Rates, credit | [Penguin Random House listing](https://penguinrandomhouse.com/books/isbn/9780262046275) |
| NY Fed, Secured Overnight Financing Rate data | Primary data and methodology | Free | Rates | [newyorkfed.org](https://www.newyorkfed.org/markets/reference-rates/sofr) |
| Federal Reserve Board, LIBOR Act final rule (December 16, 2022) | Press release | Free | Rates | [federalreserve.gov](https://www.federalreserve.gov/newsevents/pressreleases/bcreg20221216a.htm) |
| SEC Investor Bulletin, Interest Rate Risk | SEC investor bulletin | Free | Rates | [investor.gov](https://www.investor.gov/news-alerts/investor-bulletins/interest-rate-risk-when-interest-rates-go-prices-fixed-rate-bonds-fal) |
| SIFMA US Treasury Securities Statistics | Industry statistics | Free | Rates | [sifma.org](https://www.sifma.org/research/statistics/us-treasury-securities-statistics) |
| CME Group, Introduction to Treasuries | Online course | Free | Rates | [cmegroup.com](https://www.cmegroup.com/education/courses/introduction-to-treasuries) |
| FINRA, What Is TRACE | Regulator education | Free | Credit | [finra.org](https://www.finra.org/investors/insights/what-is-TRACE) |
| BIS Quarterly Review, "The 'Big Bang' in the CDS market" (December 2010) | Article | Free | Credit | [bis.org](https://www.bis.org/publ/qtrpdf/r_qt1012z.htm) |
| FRED, ICE BofA US High Yield Index OAS | Data | Free | Credit | [FRED](https://fred.stlouisfed.org/series/BAMLH0A0HYM2) |
| BIS Triennial Survey, OTC FX turnover in April 2025 | Primary statistics | Free | FX, derivatives | [bis.org](https://www.bis.org/statistics/rpfx25_fx.htm) |
| Borio et al., "Covered interest parity lost," BIS Quarterly Review, September 2016 | Article | Free | FX | [bis.org](https://www.bis.org/publ/qtrpdf/r_qt1609e.htm) |
| CME Group, Introduction to FX | Online course | Free | FX | [cmegroup.com](https://www.cmegroup.com/education/courses/introduction-to-fx.html) |
| CME Group, Introduction to Futures | Online course | Free | Commodities, derivatives | [cmegroup.com](https://www.cmegroup.com/education/courses/introduction-to-futures.html) |
| CME Group, What is contango and backwardation | Lesson | Free | Commodities | [cmegroup.com](https://www.cmegroup.com/education/courses/introduction-to-base-metals/what-is-contango-and-backwardation.html) |
| Hull, *Options, Futures, and Other Derivatives*, 11th ed. (Pearson, 2021, copyright 2022) | Book | Paid | Derivatives, FX, commodities | [Pearson (Global Edition)](https://www.pearson.com/store/en-gb/p/options-futures-and-other-derivatives-global-edition/P200000004519) |
| Options Industry Council (OCC) | Courses, webinars, calculators | Free | Derivatives | [optionseducation.org](https://www.optionseducation.org/) |
| Cboe Options Institute Learning Portal | Courses, webinars | Free (verify for live classes) | Derivatives | [cboe.com](https://www.cboe.com/optionsinstitute/learningportal) |
| CFTC bitcoin resource page | Regulator education | Free | Digital assets | [cftc.gov](https://www.cftc.gov/bitcoin) |
| Federal Reserve, Monetary Policy | Primary policy page | Free | Cross-asset | [federalreserve.gov](https://www.federalreserve.gov/monetarypolicy.htm) (verify) |

## Verification status

Facts were checked by web search on October 6, 2026. Direct page fetches were blocked by the network egress proxy (for example, sec.gov), as for the [resource map](../research/resources.md#method-and-limits), so "verified" means the fact or URL appeared in a search result attributed to the cited page. Open each primary link once before putting a figure on a slide.

- **Verified, primary source:** T+1 compliance date of May 28, 2024 (Investor.gov); SOFR definition and publication time (NY Fed); end of USD LIBOR panels after June 30, 2023 and the LIBOR Act rule (Federal Reserve Board); FX turnover of \$9.6 trillion per day, 89% USD share, and \$7.9 trillion OTC interest rate derivatives turnover (BIS, April 2025); Treasuries and corporate bonds outstanding (SIFMA); TRACE 15-minute reporting (FINRA); contango and backwardation (CME Group); every course, education page, and data link in Section 6 except the one marked below.
- **Verified, secondary sources only:** SEC Treasury clearing compliance dates (law firm and trade press summaries of the February 2025 extension); spot bitcoin ETP approval on January 10, 2024; GENIUS Act signing on July 18, 2025; CDS standard coupons of 100 and 500 bp; the 2024 half-cent tick rule; the Kenneth French Data Library URL (secondary only, as noted in the resource map) and the cftc.gov/bitcoin URL (from a news report of the page's launch); book editions and publishers for Hull (11th, Pearson; no 12th edition found), Tuckman and Serrat (4th, Wiley, 2022), Fabozzi and Fabozzi (10th, MIT Press, 2021), and Harris (Oxford, 2003).
- **Marked (verify):** status of the CLARITY Act market-structure bill; current status of the half-cent tick rule; whether Cboe live classes are free; the Federal Reserve monetary policy page URL.
- **Not source-based:** worked examples are arithmetic, checked with a Python calculation. Cross-asset links in Section 4 are textbook tendencies. The primer does not quote the current federal funds range or current yields because they change after each FOMC meeting.
