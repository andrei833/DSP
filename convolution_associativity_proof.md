# Associativity of Discrete Convolution

**Goal:** Prove that $(x \ast h_1) \ast h_2 = x \ast (h_1 \ast h_2)$

---

## Definition

The discrete convolution is defined as:

$$
(x \ast h)[n] = \sum_{k=-\infty}^{\infty} x[k]\, h[n - k]
$$

---

## Proof

### Step 1 — Expand the left side

Let $y[n] = x[n] \ast h_1[n]$, i.e.:

$$
y[m] = \sum_{k=-\infty}^{\infty} x[k]\, h_1[m - k]
$$

Now convolve $y$ with $h_2$:

$$
(y \ast h_2)[n] = \sum_{m=-\infty}^{\infty} y[m]\, h_2[n - m]
$$

### Step 2 — Substitute the expression for $y[m]$

$$
= \sum_{m=-\infty}^{\infty} \left( \sum_{k=-\infty}^{\infty} x[k]\, h_1[m - k] \right) h_2[n - m]
$$

Assuming absolute convergence, swap the order of summation:

$$
= \sum_{k=-\infty}^{\infty} x[k] \sum_{m=-\infty}^{\infty} h_1[m - k]\, h_2[n - m]
$$

---

### Step 3 — 🔑 The Key Substitution

You now have the inner sum:

$$
\sum_{m=-\infty}^{\infty} h_1[m - k]\, h_2[n - m]
$$

The two indices $m-k$ and $n-m$ share the variable $m$, which is what makes this tricky.
The trick is to **eliminate $m$ in favor of the argument of $h_1$**.

**Let $\ell = m - k$**, which means $m = \ell + k$.

When $m$ ranges over all integers, so does $\ell$.  
Substitute into both terms:

| Old expression | After substitution $\ell = m - k$ |
|---|---|
| $h_1[m - k]$ | $h_1[\ell]$ |
| $h_2[n - m]$ | $h_2[n - (\ell + k)] = h_2[(n-k) - \ell]$ |

The inner sum becomes:

$$
\sum_{\ell=-\infty}^{\infty} h_1[\ell]\, h_2[(n - k) - \ell]
$$

**This is exactly the definition of $(h_1 \ast h_2)[n-k]$!**

---

### Step 4 — Conclude

Substituting back into the outer sum:

$$
\sum_{k=-\infty}^{\infty} x[k] \underbrace{\sum_{\ell=-\infty}^{\infty} h_1[\ell]\, h_2[(n-k) - \ell]}_{(h_1 \ast h_2)[n-k]}
$$

$$
= \sum_{k=-\infty}^{\infty} x[k]\, (h_1 \ast h_2)[n - k]
$$

$$
= \boxed{x[n] \ast (h_1[n] \ast h_2[n])}
$$

$\blacksquare$

---

## Summary of the substitution

| Why it works |
|---|
| The inner sum has $m$ appearing in **two different shifted positions**: $h_1[m-k]$ and $h_2[n-m]$. |
| Setting $\ell = m - k$ **clears the shift in $h_1$**, leaving $h_1[\ell]$. |
| The shift in $h_2$ then becomes $h_2[(n-k) - \ell]$, which is exactly the convolution variable for $(h_1 \ast h_2)$ evaluated at $n-k$. |
| The result is a clean single convolution of $x$ with the combined filter $h_1 \ast h_2$. |
