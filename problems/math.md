# Math Problem Set

Twenty-five original problems for the Math Competition on Friday, October 30. The set covers six topics:

- Conditional probability and Bayes' rule (M01 to M04)
- Linearity of expectation with indicator variables (M05 to M08)
- Common distributions (M09 to M12)
- Random walks and gambler's ruin (M13 to M16)
- Basic linear algebra (M17 to M21)
- Series (M22 to M25)

Each problem lists its topic and a difficulty from 1 (warm-up) to 3 (hard). Solutions are hidden. Attempt each problem before you open its solution. Every numeric answer is checked by `problems/verify.py`.

Unless a problem says otherwise, dice are fair and six-sided, coins are fair, and draws are uniformly random.

---

## Conditional probability and Bayes' rule

### M01. Flagged trades

Topic: conditional probability | Difficulty: 1

A compliance system reviews trades. 2% of trades are improper. The system flags 95% of improper trades and also flags 4% of proper trades. A trade is flagged. What is the probability that it is improper?

<details><summary>Solution</summary>

Let $I$ be "improper" and $F$ be "flagged." By Bayes' rule,

$$P(I \mid F) = \frac{P(F \mid I)P(I)}{P(F \mid I)P(I) + P(F \mid I^c)P(I^c)} = \frac{0.95 \times 0.02}{0.95 \times 0.02 + 0.04 \times 0.98} = \frac{0.019}{0.0582}.$$

This equals $\tfrac{190}{582} = \tfrac{95}{291} \approx 0.326$. Even with a sensitive test, most flags are false alarms because improper trades are rare.

**Answer:** 95/291

</details>

### M02. Which coin, then what next

Topic: conditional probability | Difficulty: 3

A jar holds two coins. One is fair. The other lands heads with probability $\tfrac{3}{4}$. You pick a coin at random and flip it three times, getting three heads. You flip the same coin once more. What is the probability that this fourth flip is heads?

<details><summary>Solution</summary>

Let $B$ be "the biased coin was chosen." The likelihoods of HHH are $\left(\tfrac{3}{4}\right)^3 = \tfrac{27}{64}$ for the biased coin and $\left(\tfrac{1}{2}\right)^3 = \tfrac{8}{64}$ for the fair coin. With equal priors,

$$P(B \mid HHH) = \frac{27}{27 + 8} = \frac{27}{35}, \qquad P(B^c \mid HHH) = \frac{8}{35}.$$

Average the next-flip probability over the posterior:

$$P(H_4 \mid HHH) = \tfrac{27}{35}\cdot\tfrac{3}{4} + \tfrac{8}{35}\cdot\tfrac{1}{2} = \tfrac{81}{140} + \tfrac{16}{140} = \tfrac{97}{140} \approx 0.693.$$

**Answer:** 97/140

</details>

### M03. A die picks the box

Topic: conditional probability | Difficulty: 2

Box A holds 3 red and 2 blue balls. Box B holds 2 red and 3 blue balls. You roll a die and use box A on a 1 or 2, and box B otherwise. You draw two balls from the chosen box without replacement, and both are red. What is the probability that you used box A?

<details><summary>Solution</summary>

The priors are $P(A) = \tfrac{1}{3}$ and $P(B) = \tfrac{2}{3}$. The likelihoods of two reds are

$$P(RR \mid A) = \tfrac{3}{5}\cdot\tfrac{2}{4} = \tfrac{3}{10}, \qquad P(RR \mid B) = \tfrac{2}{5}\cdot\tfrac{1}{4} = \tfrac{1}{10}.$$

By Bayes' rule,

$$P(A \mid RR) = \frac{\tfrac{1}{3}\cdot\tfrac{3}{10}}{\tfrac{1}{3}\cdot\tfrac{3}{10} + \tfrac{2}{3}\cdot\tfrac{1}{10}} = \frac{3/30}{3/30 + 2/30} = \frac{3}{5}.$$

**Answer:** 3/5

</details>

### M04. Three signals disagree

Topic: conditional probability | Difficulty: 2

Tomorrow the market goes up or down with prior probability $\tfrac{1}{2}$ each. Three independent signals each predict the direction. Their accuracies are 0.8, 0.6, and 0.7. The first two signals say "up" and the third says "down." What is the posterior probability that the market goes up?

<details><summary>Solution</summary>

Given "up," the observed signals have probability $0.8 \times 0.6 \times 0.3 = 0.144$, since the third signal is wrong. Given "down," they have probability $0.2 \times 0.4 \times 0.7 = 0.056$.

With equal priors the posterior is the normalized likelihood:

$$P(\text{up} \mid \text{signals}) = \frac{0.144}{0.144 + 0.056} = \frac{0.144}{0.2} = 0.72 = \frac{18}{25}.$$

**Answer:** 18/25

</details>

---

## Linearity of expectation and indicators

### M05. Neighbors after a shuffle

Topic: linearity of expectation | Difficulty: 2

Cards labeled 1 through 10 are shuffled into a row. For how many values of $i$ in $\{1, \dots, 9\}$ do we expect cards $i$ and $i + 1$ to sit next to each other, in either order?

<details><summary>Solution</summary>

Let $X_i$ indicate that cards $i$ and $i+1$ are adjacent. Treat the two cards as one block: there are $9!$ orders of 9 objects and 2 orders within the block, so

$$P(X_i = 1) = \frac{2 \cdot 9!}{10!} = \frac{2}{10} = \frac{1}{5}.$$

By linearity, $E\left[\sum_{i=1}^{9} X_i\right] = 9 \cdot \tfrac{1}{5} = \tfrac{9}{5}$. The indicators are dependent, but linearity does not need independence.

**Answer:** 9/5

</details>

### M06. Runs from a biased coin

Topic: linearity of expectation | Difficulty: 2

A coin lands heads with probability $\tfrac{1}{3}$. You flip it 12 times. A run is a maximal block of identical consecutive outcomes; for example, HHTHTT has 4 runs. What is the expected number of runs?

<details><summary>Solution</summary>

The number of runs is 1 plus the number of positions $j \in \{2, \dots, 12\}$ where flip $j$ differs from flip $j - 1$. Each such change has probability $2pq = 2 \cdot \tfrac{1}{3} \cdot \tfrac{2}{3} = \tfrac{4}{9}$.

There are 11 such positions, so

$$E[\text{runs}] = 1 + 11 \cdot \tfrac{4}{9} = \tfrac{53}{9} \approx 5.889.$$

**Answer:** 53/9

</details>

### M07. Lonely bins

Topic: linearity of expectation | Difficulty: 2

You throw 10 balls independently and uniformly into 5 bins. What is the expected number of bins that contain exactly one ball?

<details><summary>Solution</summary>

Fix a bin. The number of balls in it is Binomial$(10, \tfrac{1}{5})$, so it holds exactly one ball with probability

$$10 \cdot \tfrac{1}{5} \cdot \left(\tfrac{4}{5}\right)^9 = 2\left(\tfrac{4}{5}\right)^9.$$

Summing 5 identical indicators gives $10\left(\tfrac{4}{5}\right)^9 = \tfrac{10 \cdot 262144}{1953125} = \tfrac{524288}{390625} \approx 1.342$.

**Answer:** 524288/390625

</details>

### M08. Consecutive lottery numbers

Topic: linearity of expectation | Difficulty: 2

A lottery draws 5 distinct numbers from $\{1, 2, \dots, 25\}$. What is the expected number of pairs of consecutive integers among the drawn numbers? (For example, the draw $\{3, 4, 5, 11, 20\}$ has 2 such pairs.)

<details><summary>Solution</summary>

For each $j \in \{1, \dots, 24\}$, let $X_j$ indicate that both $j$ and $j + 1$ are drawn. The probability that two specific numbers are both among the 5 drawn is

$$\frac{\binom{23}{3}}{\binom{25}{5}} = \frac{5 \cdot 4}{25 \cdot 24} = \frac{1}{30}.$$

By linearity, the expected count is $24 \cdot \tfrac{1}{30} = \tfrac{4}{5}$.

**Answer:** 4/5

</details>

---

## Common distributions

### M09. Orders in a half minute

Topic: distributions | Difficulty: 1

Orders arrive as a Poisson process at an average rate of 3 per minute. What is the probability that at least 2 orders arrive in a given 30-second window? Give four decimal places.

<details><summary>Solution</summary>

The count in 30 seconds is Poisson with mean $\lambda = 1.5$. Use the complement:

$$P(N \ge 2) = 1 - e^{-\lambda}(1 + \lambda) = 1 - 2.5\,e^{-1.5}.$$

With $e^{-1.5} \approx 0.223130$, this is $1 - 0.557825 = 0.442175$, or $0.4422$ to four places.

**Answer:** 0.4422

</details>

### M10. Waiting for both servers

Topic: distributions | Difficulty: 2

Two independent jobs start at the same time. Their run times are exponential with means 2 minutes and 3 minutes. What is the expected time until both jobs finish?

<details><summary>Solution</summary>

Let $X$ and $Y$ be the run times, with rates $\tfrac{1}{2}$ and $\tfrac{1}{3}$. Use $\max(X, Y) = X + Y - \min(X, Y)$.

The minimum of independent exponentials is exponential with the summed rate, $\tfrac{1}{2} + \tfrac{1}{3} = \tfrac{5}{6}$, so $E[\min] = \tfrac{6}{5}$. Therefore

$$E[\max(X, Y)] = 2 + 3 - \tfrac{6}{5} = \tfrac{19}{5} = 3.8 \text{ minutes}.$$

**Answer:** 19/5

</details>

### M11. The third six

Topic: distributions | Difficulty: 2

You roll a die repeatedly. What is the probability that the third six appears on exactly the tenth roll?

<details><summary>Solution</summary>

This is a negative binomial event. The tenth roll must be a six, and exactly 2 of the first 9 rolls must be sixes:

$$\binom{9}{2}\left(\tfrac{1}{6}\right)^3\left(\tfrac{5}{6}\right)^7 = \frac{36 \cdot 5^7}{6^{10}} = \frac{2812500}{60466176} = \frac{78125}{1679616} \approx 0.0465.$$

**Answer:** 78125/1679616

</details>

### M12. A wedge of the normal plane

Topic: distributions | Difficulty: 2

$X$ and $Y$ are independent standard normal random variables. What is $P(X > 0 \text{ and } X + Y > 0)$?

<details><summary>Solution</summary>

The pair $(X, Y)$ is rotationally symmetric, so the probability of a wedge through the origin equals its angle divided by $360°$.

The half-plane $X > 0$ covers angles from $-90°$ to $90°$. The half-plane $X + Y > 0$ covers angles from $-45°$ to $135°$. Their intersection runs from $-45°$ to $90°$, an angle of $135°$.

The probability is $\tfrac{135}{360} = \tfrac{3}{8}$.

**Answer:** 3/8

</details>

---

## Random walks and gambler's ruin

### M13. How long a fair game lasts

Topic: random walks | Difficulty: 1

You start with \$4 and bet \$1 at a time on fair coin flips. You stop when you reach \$0 or \$10. What is the expected number of bets?

<details><summary>Solution</summary>

Let $E_i$ be the expected number of bets starting with $i$ dollars. Then $E_0 = E_{10} = 0$ and

$$E_i = 1 + \tfrac{1}{2}E_{i-1} + \tfrac{1}{2}E_{i+1}.$$

The second difference of $E_i$ is the constant $-2$, so $E_i$ is quadratic. The solution matching both boundaries is $E_i = i(10 - i)$. Check: $\tfrac{1}{2}(i-1)(11-i) + \tfrac{1}{2}(i+1)(9-i) + 1 = i(10-i)$.

So $E_4 = 4 \times 6 = 24$.

**Answer:** 24

</details>

### M14. An edge in your favor

Topic: random walks | Difficulty: 2

You start with \$3 and bet \$1 at a time. Each bet wins with probability 0.6 and loses with probability 0.4. You stop at \$0 or \$6. What is the probability that you reach \$6?

<details><summary>Solution</summary>

For a biased walk with $r = q/p$, the probability of reaching $N$ before 0 from $i$ is

$$P_i = \frac{1 - r^i}{1 - r^N}.$$

Here $r = \tfrac{0.4}{0.6} = \tfrac{2}{3}$, $i = 3$, and $N = 6$:

$$P_3 = \frac{1 - 8/27}{1 - 64/729} = \frac{19/27}{665/729} = \frac{19 \cdot 27}{665} = \frac{27}{35} \approx 0.771.$$

A shortcut: $1 - r^6 = (1 - r^3)(1 + r^3)$, so $P_3 = \tfrac{1}{1 + r^3} = \tfrac{1}{1 + 8/27} = \tfrac{27}{35}$.

**Answer:** 27/35

</details>

### M15. First return to zero

Topic: random walks | Difficulty: 2

A simple symmetric random walk starts at 0 and moves $+1$ or $-1$ with equal probability each step. What is the probability that its first return to 0 happens at step 6?

<details><summary>Solution</summary>

Count paths of length 6 that end at 0 and avoid 0 at steps 2 and 4. By symmetry, count those that stay strictly positive and double.

A strictly positive path must start with $+1$ and end with $-1$. In between, the 4 middle steps form a path from 1 to 1 that never drops below 1. That is a Dyck path of length 4, and there are $C_2 = 2$ of them (the Catalan number).

So there are $2 \times 2 = 4$ favorable paths out of $2^6 = 64$, and the probability is $\tfrac{4}{64} = \tfrac{1}{16}$.

**Answer:** 1/16

</details>

### M16. How long a favorable game lasts

Topic: random walks | Difficulty: 3

Use the setup of M14: start at \$3, win each \$1 bet with probability 0.6, and stop at \$0 or \$6. What is the expected number of bets?

<details><summary>Solution</summary>

Let $E_i$ satisfy $E_i = 1 + pE_{i+1} + qE_{i-1}$ with $E_0 = E_6 = 0$. Each bet changes wealth by $p - q = 0.2$ on average, so $W_n - 0.2n$ is a martingale. By optional stopping, with $T$ the stopping time,

$$E[W_T] - 0.2\,E[T] = 3.$$

From M14, $E[W_T] = 6 \cdot \tfrac{27}{35} = \tfrac{162}{35}$. So

$$E[T] = \frac{162/35 - 3}{0.2} = 5\left(\frac{162 - 105}{35}\right) = \frac{57}{7} \approx 8.143.$$

**Answer:** 57/7

</details>

---

## Basic linear algebra

### M17. Largest eigenvalue

Topic: linear algebra | Difficulty: 1

Find the largest eigenvalue of

$$A = \begin{pmatrix} 4 & 1 \\ 2 & 3 \end{pmatrix}.$$

<details><summary>Solution</summary>

For a $2 \times 2$ matrix, the eigenvalues solve $\lambda^2 - (\operatorname{tr} A)\lambda + \det A = 0$. Here $\operatorname{tr} A = 7$ and $\det A = 12 - 2 = 10$, so

$$\lambda^2 - 7\lambda + 10 = (\lambda - 5)(\lambda - 2) = 0.$$

The largest eigenvalue is 5.

**Answer:** 5

</details>

### M18. Determinant of a constant-off-diagonal matrix

Topic: linear algebra | Difficulty: 2

Let $A$ be the $5 \times 5$ matrix with 3 on the diagonal and 1 in every other entry. Compute $\det A$.

<details><summary>Solution</summary>

Write $A = 2I + J$, where $J$ is the all-ones matrix. $J$ has rank 1 with eigenvalue 5 (eigenvector all ones) and eigenvalue 0 with multiplicity 4.

So $A$ has eigenvalues $2 + 5 = 7$ once and $2$ four times. The determinant is the product of the eigenvalues:

$$\det A = 7 \cdot 2^4 = 112.$$

**Answer:** 112

</details>

### M19. Valid equal correlations

Topic: linear algebra | Difficulty: 3

Three assets have pairwise correlations all equal to $\rho$. The correlation matrix has 1 on the diagonal and $\rho$ off the diagonal. What is the smallest value of $\rho$ for which this is a valid (positive semidefinite) correlation matrix?

<details><summary>Solution</summary>

Write the matrix as $(1 - \rho)I + \rho J$ with $J$ the $3 \times 3$ all-ones matrix. $J$ has eigenvalues 3, 0, 0, so the matrix has eigenvalues

$$1 + 2\rho \quad \text{(once)}, \qquad 1 - \rho \quad \text{(twice)}.$$

Positive semidefinite means all eigenvalues are nonnegative: $\rho \ge -\tfrac{1}{2}$ and $\rho \le 1$. The smallest value is $-\tfrac{1}{2}$.

Intuition: if every pair is strongly negatively correlated, the sum of the three assets would have negative variance, which is impossible. Indeed $\operatorname{Var}(X_1 + X_2 + X_3) = 3 + 6\rho \ge 0$.

**Answer:** -1/2

</details>

### M20. Long-run share of bull days

Topic: linear algebra | Difficulty: 1

A market switches between a bull regime and a bear regime each day. From bull, it stays bull with probability 0.9. From bear, it stays bear with probability 0.7. In the long run, what fraction of days are bull days?

<details><summary>Solution</summary>

The stationary distribution $\pi = (\pi_{\text{bull}}, \pi_{\text{bear}})$ satisfies $\pi P = \pi$. In a two-state chain, the flow out of each state balances the flow in:

$$\pi_{\text{bull}} \cdot 0.1 = \pi_{\text{bear}} \cdot 0.3.$$

So $\pi_{\text{bull}} = 3\pi_{\text{bear}}$, and with $\pi_{\text{bull}} + \pi_{\text{bear}} = 1$, we get $\pi_{\text{bull}} = \tfrac{3}{4}$.

**Answer:** 3/4

</details>

### M21. Projection matrices

Topic: linear algebra | Difficulty: 3

Let $P$ be a real $n \times n$ matrix with $P^2 = P$.

1. Show that every eigenvalue of $P$ is 0 or 1.
2. Show that $\operatorname{tr}(P) = \operatorname{rank}(P)$.

<details><summary>Solution</summary>

Part 1. Suppose $Pv = \lambda v$ with $v \ne 0$. Then $\lambda v = Pv = P^2 v = \lambda^2 v$, so $\lambda^2 = \lambda$ and $\lambda \in \{0, 1\}$.

Part 2. Every vector splits as $v = Pv + (v - Pv)$. The first part lies in the column space $\operatorname{col}(P)$. The second lies in the null space, since $P(v - Pv) = Pv - P^2 v = 0$. The two spaces intersect only in 0: if $w = Pu$ and $Pw = 0$, then $w = Pu = P^2 u = Pw = 0$. So $\mathbb{R}^n = \operatorname{col}(P) \oplus \operatorname{null}(P)$.

On $\operatorname{col}(P)$, $P$ acts as the identity, because $P(Pu) = Pu$. On $\operatorname{null}(P)$, it acts as 0. In a basis built from the two subspaces, $P$ is diagonal with $\operatorname{rank}(P)$ ones and the rest zeros. The trace does not depend on the basis, so $\operatorname{tr}(P) = \operatorname{rank}(P)$.

**Answer:** proof (no numeric answer)

</details>

---

## Series

### M22. Weighted by squares

Topic: series | Difficulty: 3

Evaluate $\displaystyle\sum_{n=1}^{\infty} \frac{n^2}{3^n}$.

<details><summary>Solution</summary>

Start from $\sum_{n \ge 0} x^n = \tfrac{1}{1 - x}$ for $|x| < 1$. Differentiate and multiply by $x$ twice:

$$\sum_{n \ge 1} n x^n = \frac{x}{(1 - x)^2}, \qquad \sum_{n \ge 1} n^2 x^n = \frac{x(1 + x)}{(1 - x)^3}.$$

At $x = \tfrac{1}{3}$:

$$\frac{\tfrac{1}{3}\cdot\tfrac{4}{3}}{\left(\tfrac{2}{3}\right)^3} = \frac{4/9}{8/27} = \frac{3}{2}.$$

**Answer:** 3/2

</details>

### M23. A finite telescope

Topic: series | Difficulty: 2

Evaluate $\displaystyle\sum_{n=1}^{48} \frac{1}{n(n+2)}$ as a fraction in lowest terms.

<details><summary>Solution</summary>

Use partial fractions: $\tfrac{1}{n(n+2)} = \tfrac{1}{2}\left(\tfrac{1}{n} - \tfrac{1}{n+2}\right)$. In the sum, every term cancels except the first two positive terms and the last two negative terms:

$$\frac{1}{2}\left(1 + \frac{1}{2} - \frac{1}{49} - \frac{1}{50}\right).$$

Since $\tfrac{1}{49} + \tfrac{1}{50} = \tfrac{99}{2450}$ and $\tfrac{3}{2} = \tfrac{3675}{2450}$, the sum is

$$\frac{1}{2}\cdot\frac{3576}{2450} = \frac{3576}{4900} = \frac{894}{1225}.$$

**Answer:** 894/1225

</details>

### M24. A growing perpetuity

Topic: series | Difficulty: 1

An asset pays \$5 one year from now. Each later annual payment grows by 2%, forever. The discount rate is 7% per year. What is the present value?

<details><summary>Solution</summary>

The present value is a geometric series:

$$PV = \sum_{k=1}^{\infty} \frac{5(1.02)^{k-1}}{(1.07)^k} = \frac{5}{1.07}\sum_{j=0}^{\infty}\left(\frac{1.02}{1.07}\right)^j = \frac{5}{1.07}\cdot\frac{1.07}{1.07 - 1.02} = \frac{5}{0.05} = 100.$$

This is the Gordon growth formula, $PV = \tfrac{C}{r - g}$.

**Answer:** 100

</details>

### M25. An exponential in disguise

Topic: series | Difficulty: 2

Evaluate $\displaystyle\sum_{n=1}^{\infty} \frac{n\,2^n}{n!}$ to four decimal places.

<details><summary>Solution</summary>

Cancel $n$ against $n!$: $\tfrac{n}{n!} = \tfrac{1}{(n-1)!}$ for $n \ge 1$. Substitute $m = n - 1$:

$$\sum_{n \ge 1} \frac{2^n}{(n-1)!} = 2\sum_{m \ge 0} \frac{2^m}{m!} = 2e^2 \approx 14.7781.$$

A probability check: if $N \sim \text{Poisson}(2)$, then $E[N] = e^{-2}\sum_{n \ge 1} n\,\tfrac{2^n}{n!} = 2$, so the sum is $2e^2$.

**Answer:** 14.7781

</details>
