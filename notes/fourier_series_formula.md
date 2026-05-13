# The Fourier Series Formula

---

## What is it?

Any periodic function $f(t)$ with period $T$ can be decomposed into a sum of complex exponentials (sinusoids).

---

## The two formulas

### Formula 1 — The expansion

$$
f(t) = \sum_{n=-\infty}^{\infty} c_n \; e^{i\, 2\pi\, n\, t \,/\, T}
$$

This says: $f(t)$ equals an infinite sum of complex exponentials, each weighted by a coefficient $c_n$.

| Symbol | Meaning |
|--------|---------|
| $T$ | Period of the function |
| $n$ | Integer index: $\ldots, -2, -1, 0, 1, 2, \ldots$ |
| $c_n$ | Weight of the $n$-th harmonic (computed by Formula 2) |
| $e^{i2\pi n t/T}$ | Complex exponential oscillating at frequency $\frac{n}{T}$ Hz |

---

### Formula 2 — The coefficients

$$
c_n = \frac{1}{T} \int_{-T/2}^{T/2} f(t) \; e^{-i\, 2\pi\, n\, t \,/\, T} \; dt
$$

This says: to find how much of the $n$-th frequency is in $f$, multiply $f(t)$ by $e^{-i2\pi n t/T}$, integrate over one period, and divide by $T$.

Notice the sign flip:
- Expansion uses $e^{+i(\ldots)}$
- Coefficient formula uses $e^{-i(\ldots)}$

This is the same forward/inverse sign relationship as the Fourier Transform.

---

## How it was used in the Shah function proof

We needed the Fourier series of $\text{Ш}_T(t) = \displaystyle\sum_k \delta(t - kT)$.

### Step A — Plug into the coefficient formula

$$
c_n = \frac{1}{T} \int_{-T/2}^{T/2} \text{Ш}_T(t) \; e^{-i2\pi n t/T} \; dt
$$

### Step B — Only one delta survives

In the interval $\left(-\frac{T}{2},\; \frac{T}{2}\right)$, the only delta function that falls inside is $\delta(t)$ (the one at $t = 0$).

All the others ($\delta(t - T)$, $\delta(t + T)$, $\delta(t - 2T)$, etc.) are **outside** this interval.

So the integral simplifies to:

$$
c_n = \frac{1}{T} \int_{-T/2}^{T/2} \delta(t) \; e^{-i2\pi n t/T} \; dt
$$

### Step C — Apply the sifting property

The sifting property of the delta function says:

$$
\int \delta(t) \; g(t) \; dt = g(0)
$$

Here $g(t) = e^{-i2\pi n t/T}$, so $g(0) = e^{0} = 1$.

Therefore:

$$
c_n = \frac{1}{T} \cdot 1 = \frac{1}{T}
$$

### Step D — Every coefficient is the same

No matter what $n$ is, the coefficient is always $\frac{1}{T}$.

So the Fourier series of the Shah function is:

$$
\text{Ш}_T(t) = \frac{1}{T} \sum_{n=-\infty}^{\infty} e^{i2\pi n t/T}
$$

This is what we then Fourier-transformed term by term in the main proof.
