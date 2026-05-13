# Swapping the Order of Summation — Step by Step

---

## The starting point

We have this double sum:

$$
\sum_{m=-\infty}^{\infty} \left( \sum_{k=-\infty}^{\infty} x[k]\, h_1[m-k] \right) h_2[n-m]
$$

The outer sum is over $m$, the inner sum is over $k$.

---

## Step 1 — Move $h_2[n-m]$ inside the inner sum

$h_2[n-m]$ does **not** depend on $k$ at all — $k$ is the inner summation variable and $h_2[n-m]$ contains no $k$.  
So it is just a **constant** with respect to the inner sum, and we can pull it inside:

$$
= \sum_{m=-\infty}^{\infty} \sum_{k=-\infty}^{\infty} x[k]\, h_1[m-k]\, h_2[n-m]
$$

Now we have a **double sum** with both $m$ and $k$ ranging over all integers.

---

## Step 2 — Visualise the double sum as a 2D grid

Think of the summand $x[k]\, h_1[m-k]\, h_2[n-m]$ as a value at each point $(k, m)$ of an infinite 2D grid:

```
m ↑
  |  ...  ...  ...  ...
3 |  ·    ·    ·    ·
2 |  ·    ·    ·    ·
1 |  ·    ·    ·    ·
0 |  ·    ·    ·    ·
  +--------------------→ k
     0    1    2    3
```

Each dot holds the value $f(k,m) = x[k]\, h_1[m-k]\, h_2[n-m]$.

**Currently** we are summing by iterating over **rows first** (fix $m$, sum over all $k$), then adding up all rows (sum over all $m$):

$$
\underbrace{\sum_{m}}_{\text{rows}} \underbrace{\sum_{k}}_{\text{columns}} f(k,m)
$$

---

## Step 3 — Swap: iterate columns first, then rows

We can equally well add up all the values by iterating over **columns first** (fix $k$, sum over all $m$), then add up all columns:

$$
\underbrace{\sum_{k}}_{\text{columns}} \underbrace{\sum_{m}}_{\text{rows}} f(k,m)
$$

The **total sum is the same** — we are just adding the same infinite grid of numbers in a different order. This is valid as long as the total sum converges absolutely (Fubini's theorem for series).

$$
\sum_{m=-\infty}^{\infty} \sum_{k=-\infty}^{\infty} x[k]\, h_1[m-k]\, h_2[n-m]
= \sum_{k=-\infty}^{\infty} \sum_{m=-\infty}^{\infty} x[k]\, h_1[m-k]\, h_2[n-m]
$$

---

## Step 4 — Factor out what doesn't depend on $m$

Now the **outer** sum is over $k$, and the inner sum is over $m$.  
The term $x[k]$ has **no $m$ in it**, so it is a constant with respect to the inner sum and factors out:

$$
= \sum_{k=-\infty}^{\infty} x[k] \underbrace{\sum_{m=-\infty}^{\infty} h_1[m-k]\, h_2[n-m]}_{\text{this will become }(h_1 \ast h_2)[n-k]}
$$

---

## Final result of the swap

$$
\sum_{m=-\infty}^{\infty} \left( \sum_{k=-\infty}^{\infty} x[k]\, h_1[m-k] \right) h_2[n-m]
\;=\;
\sum_{k=-\infty}^{\infty} x[k] \sum_{m=-\infty}^{\infty} h_1[m-k]\, h_2[n-m]
$$

---

## Why is this allowed? (Absolute convergence)

For ordinary finite sums, you can always swap order — it is just addition and addition is commutative and associative.

For **infinite** sums, re-ordering terms can change the result if the series is only conditionally convergent (Riemann rearrangement theorem).  
**Absolute convergence** (i.e., $\sum |f(k,m)| < \infty$) guarantees that any re-ordering gives the same result. This is the discrete version of **Fubini's theorem**.

In signal processing we almost always assume our signals are absolutely summable ($\ell^1$), which is exactly the condition that makes this swap legitimate.

---

## Quick summary of what happened

| Step | Action |
|------|--------|
| 1 | Pull $h_2[n-m]$ inside the inner $k$-sum (it has no $k$) |
| 2 | Recognise we have a 2D sum over the grid $(k, m)$ |
| 3 | **Swap** outer/inner: sum over $k$ first, then $m$ (valid by absolute convergence) |
| 4 | Pull $x[k]$ outside the inner $m$-sum (it has no $m$) |
