Content of https://mathoverflow.net/questions/420333/sum-of-guesses-minimization-problem-also-does-this-problem-already-exist-in-the

Inspired by some recent real-world situations, I thought of this problem:

An adversary has selected a positive real number $p \ge 1$ not known to you. You have to pick numbers $x_1, x_2, \dots$ in sequence. Your "cost" is the ratio of $\left(\sum_{i=1}^n x_i \right) / p$ where $n$ is the smallest positive integer such that $x_n \ge p$. In other words, you get to keep guessing until you exceed the number selected by the adversary, and you want to minimize your "proportional" excess over just directly guessing $p$ (the best move). Question: what is the strategy that minimizes the supremum of cost over all possible $p$, and what is that value of supremum of cost?

I'm curious if this problem already exists in the literature (it seems like a very "natural" dynamic optimization problem and closely tracked some real-world use cases). I'm also interested in rigorous solutions.

I think these are true, but it would be good to see rigorous proof or disproof, or better solutions.

**Infinite case**

The supremum of cost with the best strategy is 4, and a strategy of $x_i = 2^i$ is an example of such a best strategy. And essentially any best strategy must have $\lim_{i \to \infty} x_{i+1} / x_i = 2$.

**Loose proof sketch for infinite case**

If we are restricted to geometrically growing sequences, with the ratio of successive terms being $r$, the problem boils down to minimizing $r^2/(r - 1)$; this is minimized at $r = 2$ and the value of $r^2/(r - 1)$ is 4.

**Claim for finite case**

Given a finite upper bound $B$ on $p$ known prior to choosing the strategy, we can concretely work out strategies with slightly lower (better) supremum of cost than 4. Concrete examples:

1. When $B \le 2$, the best strategy is to just pick $B$ as the first step (later choices don't matter). The supremum of cost is $B$.
2. When $2 < B \le 2 + \sqrt{5}$, the best strategy is to play a two-step game: pick $x_1 = 1 + \sqrt{1 + 4B} / 2$ and $x_2 = B$. The supremum of cost is $1 + \sqrt{1 + 4B} / 2$.
3. When $2 + \sqrt{5} < B \le 9$, the best strategy is to play a three-step game: pick $x_1$ as the largest root of $x^2(x - 2) = B$, pick $x_2 = x_1(x_1 - 1)$, and pick $x_3 = B$. We have similar transition thresholds for $B$ for each increase in the number of steps.

**Loose proof sketch for finite case**

The general idea is that for a $n$-step solution, we should have (based on a calculus-of-variations-like reasoning):

$$x_1 = \frac{x_1 + x_2}{x_1} = \frac{x_1 + x_2 + x_3}{x_2} = \frac{x_1 + x_2 + x_3 + x_4}{x_3} = \dots \frac{\sum_{i=1}^n x_i}{x_{n-1}}$$

This works out to explicit expressions for $x_i$ in terms of $x_1$, all of them polynomials with the polynomial for $x_i$ of degree $i$ and having at least $x_1^{\lfloor i/2 \rfloor}$ dividing it. We must also have $x_n = B$, so we solve to get a degree $n$ polynomial equation for $x_1$ in terms of $B$.

To find the transitions between where a $(n - 1)$-step game is optimal and a $n$-step game is optimal, we need to basically solve for $x_{n - 1} = x_n$, which also gives a polynomial equation. We need to take an appropriate root (the largest one??).

**Claim on limiting behavior of finite case**

Regardless of the value of $B$, the value of $x_1$ that minimizes the supremum of cost can never be more than 4 (this is intuitively clear from the infinite case where we already have a sequence that doesn't do worse than 4). If we define $x_1(B)$ and $n(B)$ as the values of $x_1$ and $n$ for the optimal strategy for $B$, then $\lim_{B \to \infty} x_1(B) = 4$, and $\lim_{B \to \infty} B^{1/n(B)} = 2$.

**Probably similar problem**

A probably similar problem is the one of finding an unknown number on the real line (positive or negative) starting from the origin, with the goal being to traverse the minimum distance as a multiple of the value of the number. If there's a lower bound of 1 on the number, the problem is very similar to sum-of-guesses-minimization (the key being that we alternate between positive and negative guesses). I think the asymptotic strategy remains the same: double the magnitude of the guess each time. However, the actual ratios are different, though, and in particular the supremum of the cost with the doubling strategy turns out to be 9 instead of 4.
