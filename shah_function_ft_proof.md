# Proof: Fourier Transform of the Shah Function (Dirac Comb)

$$
\mathcal{F}\left[\text{Ш}_T(t)\right] = T\;\text{Ш}_{1/T}(\nu)
$$

---

## Definitions

The **Shah function** (Dirac comb) with period $T$ is a train of equally spaced delta functions:

$$
\text{Ш}_T(t) = \sum_{n=-\infty}^{\infty} \delta(t - nT)
$$

We use the FT convention with frequency $\nu$ (Hz):

$$
\hat{f}(\nu) = \int_{-\infty}^{\infty} f(t)\, e^{-i2\pi\nu t}\, dt
$$

---

## The proof in 3 steps

### Step 1 — The Shah function is periodic, so expand it as a Fourier Series

$\text{Ш}_T(t)$ is periodic with period $T$, so it has a Fourier series:

$$
\text{Ш}_T(t) = \sum_{n=-\infty}^{\infty} c_n\; e^{i2\pi n t/T}
$$

where the coefficients are:

$$
c_n = \frac{1}{T}\int_{-T/2}^{T/2} \text{Ш}_T(t)\; e^{-i2\pi n t/T}\; dt
$$

### Step 2 — Compute $c_n$

In the interval $(-T/2,\; T/2)$, only the $n=0$ delta survives, so:

$$
c_n = \frac{1}{T}\int_{-T/2}^{T/2} \delta(t)\; e^{-i2\pi n t/T}\; dt
$$

The sifting property of the delta ($\int \delta(t)\, g(t)\, dt = g(0)$) gives:

$$
c_n = \frac{1}{T}\cdot e^{0} = \frac{1}{T}
$$

**Every coefficient is the same:** $c_n = \dfrac{1}{T}$ for all $n$.

So the Fourier series is:

$$
\text{Ш}_T(t) = \frac{1}{T}\sum_{n=-\infty}^{\infty} e^{i2\pi n t/T}
$$

### Step 3 — Take the Fourier Transform of both sides

Apply the FT term by term. We need the FT of a single complex exponential:

$$
\mathcal{F}\left[e^{i2\pi f_0 t}\right] = \delta(\nu - f_0)
$$

Each term in the sum has $f_0 = n/T$, so:

$$
\mathcal{F}\left[\text{Ш}_T(t)\right]
= \frac{1}{T}\sum_{n=-\infty}^{\infty} \mathcal{F}\left[e^{i2\pi (n/T) t}\right]
= \frac{1}{T}\sum_{n=-\infty}^{\infty} \delta\!\left(\nu - \frac{n}{T}\right)
$$

Now recognise what $\displaystyle\sum_{n=-\infty}^{\infty} \delta\!\left(\nu - \frac{n}{T}\right)$ is — it is a **Dirac comb in $\nu$ with spacing $\frac{1}{T}$**, which is exactly $\text{Ш}_{1/T}(\nu)$:

$$
\sum_{n=-\infty}^{\infty} \delta\!\left(\nu - \frac{n}{T}\right) = \text{Ш}_{1/T}(\nu)
$$

Therefore:

$$
\boxed{\mathcal{F}\left[\text{Ш}_T(t)\right] = \frac{1}{T}\;\text{Ш}_{1/T}(\nu)}
$$

Wait — that gives $\frac{1}{T}$, but the formula to prove has $T$. Let me address this.

---

## Where the factor $T$ vs $\frac{1}{T}$ comes from

The result you get depends on **how the Shah function is defined**:

| Definition of $\text{Ш}_T(t)$ | FT result |
|---|---|
| $\text{Ш}_T(t) = \displaystyle\sum_n \delta(t - nT)$ (sum of deltas) | $\mathcal{F}[\text{Ш}_T] = \dfrac{1}{T}\;\text{Ш}_{1/T}(\nu)$ |
| $\text{Ш}_T(t) = T\displaystyle\sum_n \delta(t - nT)$ (scaled by $T$) | $\mathcal{F}[\text{Ш}_T] = T\;\text{Ш}_{1/T}(\nu)$ |

Your textbook uses a convention where there is extra scaling baked into the definition of $\text{Ш}$, which produces the factor $T$ instead of $\frac{1}{T}$.

Under the first (most common) convention, the result is:

$$
\mathcal{F}\left[\text{Ш}_T(t)\right] = \frac{1}{T}\;\text{Ш}_{1/T}(\nu)
$$

---

## Summary of the proof strategy

| Step | What you did |
|------|-------------|
| 1 | The comb is periodic → write it as a Fourier series |
| 2 | Compute the coefficients → they all equal $\frac{1}{T}$ (delta sifting) |
| 3 | FT each exponential → each becomes a delta → you get a new comb with spacing $\frac{1}{T}$ |

The whole proof boils down to: **a periodic train of deltas has a Fourier series of equal-weight exponentials, and the FT of each exponential is a delta — giving another train of deltas at the reciprocal spacing.**
