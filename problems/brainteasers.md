# Brainteaser Problem Set

Thirty original problems for the Brainteaser Battle on Thursday, October 15. The set covers five topics with six problems each: probability (B01 to B06), expected value (B07 to B12), combinatorics (B13 to B18), mental math (B19 to B24), and estimation (B25 to B30).

Each problem lists its topic and a difficulty from 1 (warm-up) to 3 (hard). Solutions are hidden. Attempt each problem before you open its solution. Every numeric answer is checked by `problems/verify.py`.

Unless a problem says otherwise, dice are fair and six-sided, coins are fair, and draws are uniformly random.

---

## Probability

### B01. The highest of three dice

Topic: probability | Difficulty: 1

You roll three dice. What is the probability that the largest value shown is exactly 5?

<details><summary>Solution</summary>

The event "maximum is exactly 5" equals "all dice are at most 5" minus "all dice are at most 4."

$$P(\max \le 5) = \left(\tfrac{5}{6}\right)^3 = \tfrac{125}{216}, \qquad P(\max \le 4) = \left(\tfrac{4}{6}\right)^3 = \tfrac{64}{216}.$$

The difference is $\tfrac{125 - 64}{216} = \tfrac{61}{216} \approx 0.282$.

**Answer:** 61/216

</details>

### B02. Second card beats the first

Topic: probability | Difficulty: 1

You deal two cards from a shuffled standard 52-card deck. Aces are high, and suits do not matter. What is the probability that the second card has a strictly higher rank than the first?

<details><summary>Solution</summary>

The second card matches the first card's rank with probability $\tfrac{3}{51} = \tfrac{1}{17}$, because 3 of the remaining 51 cards share that rank.

Otherwise the two ranks differ. By symmetry, the second rank is higher or lower with equal probability. So the answer is

$$\tfrac{1}{2}\left(1 - \tfrac{1}{17}\right) = \tfrac{8}{17} \approx 0.471.$$

**Answer:** 8/17

</details>

### B03. Two heads or three tails

Topic: probability | Difficulty: 3

You flip a coin repeatedly. You stop as soon as you see two heads in a row (HH) or three tails in a row (TTT). What is the probability that you stop on HH?

<details><summary>Solution</summary>

Track the current streak. Let $h$ be the probability of finishing on HH when the last flip was a single H. Let $t_1$ and $t_2$ be the same probability when the current streak is one T or two T's.

$$h = \tfrac{1}{2}(1) + \tfrac{1}{2} t_1, \qquad t_1 = \tfrac{1}{2} h + \tfrac{1}{2} t_2, \qquad t_2 = \tfrac{1}{2} h + \tfrac{1}{2}(0).$$

Substitute: $t_2 = h/2$, so $t_1 = h/2 + h/4 = 3h/4$. Then $h = \tfrac{1}{2} + \tfrac{3h}{8}$, which gives $h = \tfrac{4}{5}$ and $t_1 = \tfrac{3}{5}$.

The first flip is H or T with equal probability, so the answer is $\tfrac{1}{2}\cdot\tfrac{4}{5} + \tfrac{1}{2}\cdot\tfrac{3}{5} = \tfrac{7}{10}$.

**Answer:** 7/10

</details>

### B04. First red on an even draw

Topic: probability | Difficulty: 2

A bag holds 4 red and 6 blue marbles. You draw marbles one at a time without replacement until you draw the first red. What is the probability that the first red appears on an even-numbered draw?

<details><summary>Solution</summary>

The positions of the 4 red marbles in the full draw order form a uniformly random 4-element subset of $\{1, \dots, 10\}$. There are $\binom{10}{4} = 210$ such subsets.

The first red is at position $k$ when position $k$ is red and the other 3 reds lie in positions $k+1, \dots, 10$. That happens in $\binom{10-k}{3}$ subsets.

Sum over even $k$: $\binom{8}{3} + \binom{6}{3} + \binom{4}{3} + \binom{2}{3} = 56 + 20 + 4 + 0 = 80$.

The probability is $\tfrac{80}{210} = \tfrac{8}{21} \approx 0.381$.

**Answer:** 8/21

</details>

### B05. Uneven dice duel

Topic: probability | Difficulty: 2

Ana and Ben take turns rolling one die, with Ana rolling first. Ana wins the moment she rolls a 5 or a 6. Ben wins the moment he rolls a 6. What is the probability that Ana wins?

<details><summary>Solution</summary>

In each full round (Ana then Ben), nobody wins with probability $\tfrac{2}{3}\cdot\tfrac{5}{6} = \tfrac{5}{9}$. If a round ends with no winner, the game restarts in the same position.

Let $p$ be Ana's winning probability. Ana wins immediately with probability $\tfrac{1}{3}$, or the round passes with no winner and she is back where she started:

$$p = \tfrac{1}{3} + \tfrac{5}{9} p \quad\Longrightarrow\quad p = \tfrac{1/3}{4/9} = \tfrac{3}{4}.$$

**Answer:** 3/4

</details>

### B06. Overlapping coffee breaks

Topic: probability | Difficulty: 2

Priya arrives at a coffee cart at a uniformly random time between 8:00 and 9:00. Omar arrives at a uniformly random time between 8:30 and 9:30, independently. Each waits 10 minutes for the other and then leaves. What is the probability that they meet?

<details><summary>Solution</summary>

Measure minutes after 8:00. Priya's time $X$ is uniform on $[0, 60]$. Write Omar's time as $30 + Y$ with $Y$ uniform on $[0, 60]$. They meet when $|X - (30 + Y)| \le 10$, that is, when $20 \le X - Y \le 40$.

For $X, Y$ uniform on the square $[0, 60]^2$, the region where $X - Y \ge a$ (for $0 \le a \le 60$) is a triangle of area $\tfrac{(60 - a)^2}{2}$. So the favorable area is

$$\frac{40^2}{2} - \frac{20^2}{2} = 800 - 200 = 600.$$

Divide by the square's area of 3600 to get $\tfrac{1}{6}$.

**Answer:** 1/6

</details>

---

## Expected value

### B07. One reroll on a ten-sided die

Topic: expected value | Difficulty: 1

You roll a ten-sided die with faces 1 through 10. You may either keep the result or reroll once and keep the second result. You are paid the final face value in dollars. What is the expected payout under the best strategy?

<details><summary>Solution</summary>

A reroll is worth its expected value, $5.5$. Keep the first roll exactly when it beats 5.5, that is, when it is 6 or more.

With probability $\tfrac{1}{2}$ the first roll is 6 to 10, averaging 8. With probability $\tfrac{1}{2}$ you reroll and average 5.5. The expected payout is

$$\tfrac{1}{2}(8) + \tfrac{1}{2}(5.5) = 6.75 = \tfrac{27}{4}.$$

**Answer:** 27/4

</details>

### B08. Neighbors in a row

Topic: expected value | Difficulty: 3

You roll a die repeatedly and stop when two consecutive rolls differ by exactly 1 (for example, a 3 followed by a 4, or a 5 followed by a 4). What is the expected total number of rolls?

<details><summary>Solution</summary>

Let $E_v$ be the expected number of additional rolls when the last roll was $v$. Faces 1 and 6 have one neighbor; faces 2 through 5 have two. By symmetry, write $a = E_1 = E_6$, $b = E_2 = E_5$, and $c = E_3 = E_4$.

The next roll always counts, and the process continues only when the new face is not a neighbor:

$$a = 1 + \tfrac{1}{6}(2a + b + 2c), \qquad b = 1 + \tfrac{1}{6}(a + 2b + c), \qquad c = 1 + \tfrac{1}{6}(2a + b + c).$$

Subtracting the third equation from the first gives $6a = 7c$. The second gives $b = (6 + a + c)/4$. Substituting into the first yields $c = \tfrac{60}{17}$, $a = \tfrac{70}{17}$, and $b = \tfrac{58}{17}$.

The first roll is uniform, so the total is

$$1 + \tfrac{1}{6}(2a + 2b + 2c) = 1 + \tfrac{a + b + c}{3} = 1 + \tfrac{188}{51} = \tfrac{239}{51} \approx 4.686.$$

**Answer:** 239/51

</details>

### B09. Finding every winning ticket

Topic: expected value | Difficulty: 3

A box holds 20 tickets, and 3 of them are winners. You draw tickets one at a time without replacement until you have drawn all 3 winners. What is the expected number of draws?

<details><summary>Solution</summary>

The number of draws equals the largest position among the 3 winners, where the positions form a uniform random 3-subset of $\{1, \dots, 20\}$.

The 3 winners split the 17 losing tickets into 4 gaps, and by symmetry each gap holds $\tfrac{17}{4}$ losers on average. Only the last gap comes after the final winner, so the expected number of draws is

$$20 - \tfrac{17}{4} = \tfrac{63}{4} = 15.75.$$

Equivalently, the expected maximum of $k$ random positions out of $n$ is $\tfrac{k(n+1)}{k+1} = \tfrac{3 \cdot 21}{4}$.

**Answer:** 63/4

</details>

### B10. Pricing a squared payout

Topic: expected value | Difficulty: 2

You flip a coin until the first tail. Let $N$ be the total number of flips, including the tail. The game pays $N^2$ dollars. What is the fair price of the game?

<details><summary>Solution</summary>

$N$ is geometric with success probability $p = \tfrac{1}{2}$, so $E[N] = \tfrac{1}{p} = 2$ and $\operatorname{Var}(N) = \tfrac{1-p}{p^2} = 2$.

Then $E[N^2] = \operatorname{Var}(N) + E[N]^2 = 2 + 4 = 6$.

**Answer:** 6

</details>

### B11. Distinct faces in six rolls

Topic: expected value | Difficulty: 2

You roll a die six times. What is the expected number of distinct faces that appear?

<details><summary>Solution</summary>

Use an indicator for each face. Face $j$ never appears with probability $\left(\tfrac{5}{6}\right)^6$, so it appears with probability $1 - \left(\tfrac{5}{6}\right)^6$.

By linearity of expectation, the expected count is

$$6\left(1 - \tfrac{15625}{46656}\right) = 6 - \tfrac{15625}{7776} = \tfrac{31031}{7776} \approx 3.991.$$

**Answer:** 31031/7776

</details>

### B12. Larger times smaller

Topic: expected value | Difficulty: 2

You roll two dice. Let $M$ be the larger value and $m$ the smaller value (equal if the dice match). What is $E[M \cdot m]$?

<details><summary>Solution</summary>

The product of the larger and smaller values equals the product of the two dice, $X \cdot Y$. The dice are independent, so

$$E[M m] = E[XY] = E[X]\,E[Y] = 3.5^2 = \tfrac{49}{4}.$$

**Answer:** 49/4

</details>

---

## Combinatorics

### B13. Rearranging ARBITRAGE

Topic: combinatorics | Difficulty: 1

How many distinct strings can you form by rearranging all the letters of the word ARBITRAGE?

<details><summary>Solution</summary>

ARBITRAGE has 9 letters. A and R each appear twice, and the other letters appear once. The count is

$$\frac{9!}{2!\,2!} = \frac{362880}{4} = 90720.$$

**Answer:** 90720

</details>

### B14. Detour on a grid

Topic: combinatorics | Difficulty: 2

You walk from $(0, 0)$ to $(6, 4)$ using unit steps right or up. How many paths avoid the point $(3, 2)$?

<details><summary>Solution</summary>

All paths: choose which 4 of the 10 steps go up, $\binom{10}{4} = 210$.

Paths through $(3, 2)$: $\binom{5}{2}$ ways to reach it, then $\binom{5}{2}$ ways to finish (3 right and 2 up). That is $10 \times 10 = 100$.

Paths that avoid it: $210 - 100 = 110$.

**Answer:** 110

</details>

### B15. Capped allocations

Topic: combinatorics | Difficulty: 2

You allocate 12 identical lots across 4 desks. Each desk receives a whole number of lots from 0 to 5. How many allocations are possible?

<details><summary>Solution</summary>

Count nonnegative solutions of $a + b + c + d = 12$ with every variable at most 5.

Without the cap, stars and bars gives $\binom{15}{3} = 455$.

If a given variable is at least 6, subtract 6 from it: $\binom{9}{3} = 84$ solutions, and there are 4 choices of variable.

If two given variables are each at least 6, the rest sum to 0: $\binom{3}{3} = 1$ solution, with $\binom{4}{2} = 6$ choices of pair. Three variables cannot all exceed 5.

By inclusion and exclusion: $455 - 4(84) + 6(1) = 125$.

**Answer:** 125

</details>

### B16. Coloring a ring of desks

Topic: combinatorics | Difficulty: 3

Six desks stand in a ring, labeled 1 through 6, so desk 6 neighbors desk 1. Each desk is painted red, green, or blue, and neighboring desks must have different colors. How many colorings are possible?

<details><summary>Solution</summary>

Let $L_n$ count valid colorings of a line of $n$ desks with 3 colors, and let $R_n$ count valid ring colorings. A line has $L_n = 3 \cdot 2^{n-1}$ colorings. A line coloring either has desk $n$ different from desk 1 (a valid ring) or equal to desk 1 (which merges into a valid ring of $n - 1$ desks). So $L_n = R_n + R_{n-1}$.

Solving this recursion with $R_3 = 6$ gives the closed form $R_n = 2^n + 2(-1)^n$. Check: $R_3 = 8 - 2 = 6$.

For $n = 6$: $R_6 = 64 + 2 = 66$.

**Answer:** 66

</details>

### B17. Mixed interview panel

Topic: combinatorics | Difficulty: 1

A team has 7 traders and 5 quants. How many 4-person panels contain at least one trader and at least one quant?

<details><summary>Solution</summary>

Count all panels and remove the single-role ones:

$$\binom{12}{4} - \binom{7}{4} - \binom{5}{4} = 495 - 35 - 5 = 455.$$

**Answer:** 455

</details>

### B18. Partners at a round table

Topic: combinatorics | Difficulty: 2

Four trading pairs (8 people) sit at a round table with 8 seats. Seatings that differ only by a rotation count as the same. How many seatings put every pair in adjacent seats?

<details><summary>Solution</summary>

Glue each pair into one block. Four blocks around a circle can be arranged in $(4 - 1)! = 6$ ways up to rotation.

Within each block, the two partners can sit in 2 orders, giving $2^4 = 16$.

The total is $6 \times 16 = 96$.

**Answer:** 96

</details>

---

## Mental math

Work these without paper. Aim for under 20 seconds each.

### B19. Product near a square

Topic: mental math | Difficulty: 1

Compute $47 \times 53$.

<details><summary>Solution</summary>

Write the factors around 50: $(50 - 3)(50 + 3) = 2500 - 9 = 2491$.

**Answer:** 2491

</details>

### B20. Square ending in five

Topic: mental math | Difficulty: 1

Compute $115^2$.

<details><summary>Solution</summary>

For a number ending in 5, write it as $10n + 5$. Its square is $100\,n(n+1) + 25$. Here $n = 11$, so $11 \times 12 = 132$, and the square is $13225$.

**Answer:** 13225

</details>

### B21. Sixteenths to decimals

Topic: mental math | Difficulty: 1

Write $\tfrac{13}{16}$ as a decimal.

<details><summary>Solution</summary>

Since $\tfrac{1}{16} = 0.0625$, we get $\tfrac{13}{16} = 1 - \tfrac{3}{16} = 1 - 0.1875 = 0.8125$.

**Answer:** 0.8125

</details>

### B22. Swapping percentages

Topic: mental math | Difficulty: 1

Compute 18% of 350 plus 35% of 180.

<details><summary>Solution</summary>

$x\%$ of $y$ equals $y\%$ of $x$, because both equal $\tfrac{xy}{100}$. So both terms equal 35% of 180, which is $63$. The sum is $126$.

**Answer:** 126

</details>

### B23. A block of odd numbers

Topic: mental math | Difficulty: 2

Compute the sum of all odd numbers from 21 to 79, inclusive.

<details><summary>Solution</summary>

There are $\tfrac{79 - 21}{2} + 1 = 30$ terms. An arithmetic sequence averages its first and last terms, $\tfrac{21 + 79}{2} = 50$. The sum is $30 \times 50 = 1500$.

**Answer:** 1500

</details>

### B24. Cancelling products

Topic: mental math | Difficulty: 2

Compute $999 \times 1001 - 998 \times 1002$.

<details><summary>Solution</summary>

Use the difference of squares on each product: $999 \times 1001 = 1000^2 - 1$ and $998 \times 1002 = 1000^2 - 4$. The difference is $-1 - (-4) = 3$.

**Answer:** 3

</details>

---

## Estimation

Give each answer to the precision stated. Show the shortcut you used.

### B25. A root just past a square

Topic: estimation | Difficulty: 1

Estimate $\sqrt{2026}$ to three decimal places.

<details><summary>Solution</summary>

Note $45^2 = 2025$. For small $h$, $\sqrt{x^2 + h} \approx x + \tfrac{h}{2x}$. So $\sqrt{2026} \approx 45 + \tfrac{1}{90} = 45.0111\ldots$, which rounds to $45.011$.

**Answer:** 45.011

</details>

### B26. Compounding at two percent

Topic: estimation | Difficulty: 2

Estimate $1.02^{36}$ to two decimal places.

<details><summary>Solution</summary>

Use logarithms. $\ln 1.02 \approx 0.02 - \tfrac{0.02^2}{2} = 0.0198$. Then $36 \times 0.0198 = 0.7128$.

Since $\ln 2 \approx 0.6931$, we have $e^{0.7128} = 2\,e^{0.0197} \approx 2 \times 1.0199 \approx 2.040$. The rule of 72 gives the same first guess: at 2% per period, money doubles in about 36 periods.

**Answer:** 2.04

</details>

### B27. Daily volatility from annual

Topic: estimation | Difficulty: 1

A stock has annualized volatility of 32%. Assuming 252 trading days per year, estimate its daily volatility in percent, to three decimal places.

<details><summary>Solution</summary>

Volatility scales with the square root of time, so daily volatility is $\tfrac{32\%}{\sqrt{252}}$.

Since $16^2 = 256$, $\sqrt{252} \approx 16 - \tfrac{4}{32} = 15.875$. Then $\tfrac{32}{15.875} \approx 2.016$, so daily volatility is about $2.016\%$.

**Answer:** 2.016

</details>

### B28. Ninety-nine percent, one hundred times

Topic: estimation | Difficulty: 2

Estimate $0.99^{100}$ to three decimal places.

<details><summary>Solution</summary>

Take logarithms: $100 \ln 0.99 = 100\left(-0.01 - \tfrac{0.0001}{2} - \tfrac{0.000001}{3} - \cdots\right) \approx -1.00503$.

So $0.99^{100} \approx e^{-1} \times e^{-0.00503} \approx 0.36788 \times 0.99498 \approx 0.36603$, which rounds to $0.366$.

**Answer:** 0.366

</details>

### B29. Coffee near campus

Topic: estimation | Difficulty: 2

Estimate the number of cups of coffee sold on a typical weekday within a 10-minute walk of Baruch's Newman Vertical Campus. Interviewers grade the structure of your estimate, not the final number.

<details><summary>Solution</summary>

One reasonable structure:

1. A 10-minute walk covers roughly a 0.5-mile radius, about 0.8 square miles of Midtown South and Gramercy.
2. Daytime population in that area: about 80,000 residents and 150,000 workers and students, so about 230,000 people.
3. Share who buy at least one coffee on a weekday: about 40%, or about 92,000 buyers.
4. Cups per buyer: about 1.3.

This gives roughly 120,000 cups per day. A cross-check from the supply side: about 150 coffee outlets (cafes, delis, carts, chains) selling 600 to 1,000 cups each gives 90,000 to 150,000.

Any answer in the range of 50,000 to 250,000 with a clear structure and a cross-check is strong.

**Answer:** open-ended (roughly 120,000; no single correct value)

</details>

### B30. Losing years for a good strategy

Topic: estimation | Difficulty: 3

A strategy has an annualized Sharpe ratio of 1.5 with a zero risk-free rate. Assume annual returns are normally distributed. Estimate the probability that a given year has a negative return, to four decimal places.

<details><summary>Solution</summary>

With mean $\mu$ and standard deviation $\sigma$, the Sharpe ratio is $\mu / \sigma = 1.5$. A negative year means the return falls more than 1.5 standard deviations below its mean:

$$P(R < 0) = P\left(Z < -\tfrac{\mu}{\sigma}\right) = \Phi(-1.5).$$

Recall $\Phi(-1) \approx 0.1587$ and $\Phi(-2) \approx 0.0228$. The standard value is $\Phi(-1.5) \approx 0.0668$, so about one year in fifteen loses money.

**Answer:** 0.0668

</details>
