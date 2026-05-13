# Proof of Parseval's Theorem

$$\int_{-\infty}^{\infty} |f(t)|^2\, dt = \int_{-\infty}^{\infty} |\hat{f}(\omega)|^2\, d\omega$$

---

## Convention Used (Symmetric / Unitary)

This no-factor version of Parseval holds under the **symmetric convention**, where both the FT and its inverse carry a $\frac{1}{\sqrt{2\pi}}$:

$$
\hat{f}(\omega) = \frac{1}{\sqrt{2\pi}}\int_{-\infty}^{\infty} f(t)\, e^{-i\omega t}\, dt
\qquad
f(t) = \frac{1}{\sqrt{2\pi}}\int_{-\infty}^{\infty} \hat{f}(\omega)\, e^{+i\omega t}\, d\omega
$$

---

## Proof

### Step 1 — Expand $|f(t)|^2$ using the conjugate

$$
\int_{-\infty}^{\infty} |f(t)|^2\, dt = \int_{-\infty}^{\infty} f(t)\, \overline{f(t)}\, dt
$$

### Step 2 — Substitute the inverse FT for $\overline{f(t)}$

Take the complex conjugate of the inverse FT formula:

$$
f(t) = \frac{1}{\sqrt{2\pi}}\int_{-\infty}^{\infty} \hat{f}(\omega)\, e^{+i\omega t}\, d\omega
\implies
\overline{f(t)} = \frac{1}{\sqrt{2\pi}}\int_{-\infty}^{\infty} \overline{\hat{f}(\omega)}\, e^{-i\omega t}\, d\omega
$$

Substitute this into Step 1:

$$
= \int_{-\infty}^{\infty} f(t) \cdot \frac{1}{\sqrt{2\pi}}\int_{-\infty}^{\infty} \overline{\hat{f}(\omega)}\, e^{-i\omega t}\, d\omega\; dt
$$

### Step 3 — Swap the order of integration

By absolute convergence (Fubini), move the $t$-integral inside:

$$
= \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{\infty} \overline{\hat{f}(\omega)} \left( \int_{-\infty}^{\infty} f(t)\, e^{-i\omega t}\, dt \right) d\omega
$$

### Step 4 — Recognise the inner integral as the FT

By definition: $\hat{f}(\omega) = \dfrac{1}{\sqrt{2\pi}}\displaystyle\int_{-\infty}^{\infty} f(t)\, e^{-i\omega t}\, dt$

So: $\displaystyle\int_{-\infty}^{\infty} f(t)\, e^{-i\omega t}\, dt = \sqrt{2\pi}\;\hat{f}(\omega)$

Substitute:

$$
= \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{\infty} \overline{\hat{f}(\omega)}\cdot \sqrt{2\pi}\;\hat{f}(\omega)\; d\omega
$$

### Step 5 — Simplify

The $\sqrt{2\pi}$ factors cancel:

$$
= \int_{-\infty}^{\infty} \hat{f}(\omega)\,\overline{\hat{f}(\omega)}\; d\omega
= \int_{-\infty}^{\infty} |\hat{f}(\omega)|^2\; d\omega
$$

---

## Result

$$
\boxed{\int_{-\infty}^{\infty} |f(t)|^2\, dt = \int_{-\infty}^{\infty} |\hat{f}(\omega)|^2\, d\omega}
\qquad \blacksquare
$$

---

## Where did the $\frac{1}{\sqrt{2\pi}}$ go?

It appeared **twice** in Step 4 — once from the $\frac{1}{\sqrt{2\pi}}$ sitting outside the integral, and once as $\sqrt{2\pi}$ from the FT definition — and they cancelled exactly:

$$
\frac{1}{\sqrt{2\pi}} \cdot \sqrt{2\pi} = 1
$$

This cancellation is **precisely why** the symmetric convention is chosen — it makes Parseval's theorem clean with no leftover factor.  
If you use the asymmetric convention ($e^{-i\omega t}$ with no $\frac{1}{\sqrt{2\pi}}$), the $\sqrt{2\pi}$ factors do not cancel and you are left with a $\frac{1}{2\pi}$ on the right-hand side.

---

## Summary of the proof strategy

| Step | What you did |
|------|-------------|
| 1 | Write $\|f\|^2 = f \cdot \bar{f}$ |
| 2 | Replace $\bar{f}(t)$ with the **conjugated inverse FT** |
| 3 | **Swap** the order of integration (Fubini / absolute convergence) |
| 4 | Recognise $\int f(t)e^{-i\omega t}dt$ as $\sqrt{2\pi}\,\hat{f}(\omega)$ |
| 5 | Cancel the $\sqrt{2\pi}$ factors and get $|\hat{f}|^2$ |
