# Parseval's Theorem (Plancherel's Theorem)

**Question:** What is the frequency-domain equivalent of $\displaystyle\int_{-\infty}^{\infty} |f(t)|^2\, dt$?

---

## The Theorem

$$
\boxed{\int_{-\infty}^{\infty} |f(t)|^2\, dt = \frac{1}{2\pi}\int_{-\infty}^{\infty} |\hat{f}(\omega)|^2\, d\omega}
$$

In words: the **total energy of a signal is the same in both the time and frequency domains** (up to a $\frac{1}{2\pi}$ scaling factor from the FT convention).

---

## Why the Conjugate Appears

The starting point is how to expand the modulus squared of a complex number:

$$
|f(t)|^2 = f(t) \cdot \overline{f(t)}
$$

and identically in the frequency domain:

$$
|\hat{f}(\omega)|^2 = \hat{f}(\omega) \cdot \overline{\hat{f}(\omega)}
$$

So the integral $\int |f|^2\, dt$ is really an **inner product of $f$ with its own complex conjugate**.  
Parseval says this inner product is preserved by the Fourier transform.

---

## General Form (Two Different Signals)

For two signals $f$ and $g$:

$$
\int_{-\infty}^{\infty} f(t)\,\overline{g(t)}\, dt
= \frac{1}{2\pi}\int_{-\infty}^{\infty} \hat{f}(\omega)\,\overline{\hat{g}(\omega)}\, d\omega
$$

Setting $g = f$ recovers the energy version, since $f\,\overline{f} = |f|^2$.

---

## Where Does the $\frac{1}{2\pi}$ Come From?

It is a consequence of the FT convention, just like the sign in the frequency shift property.

| Frequency variable | FT definition | Parseval factor |
|---|---|---|
| $\omega$ (rad/s) | $\hat{f}(\omega)=\int f(t)\,e^{\pm i\omega t}\,dt$ | $\dfrac{1}{2\pi}$ |
| $\nu$ (Hz), $\nu = \omega/2\pi$ | $\hat{f}(\nu) = \int f(t)\,e^{\pm i 2\pi\nu t}\,dt$ | $1$ (no factor!) |

The $\frac{1}{2\pi}$ disappears entirely when you work in **Hz** instead of **rad/s** — this is the unitary convention used in many physics texts.

---

## Physical Interpretation

| Domain | Quantity |
|---|---|
| Time | $\|f(t)\|^2$ is **instantaneous power** |
| Time | $\int_{-\infty}^{\infty}\|f(t)\|^2\,dt$ is **total energy** |
| Frequency | $\|\hat{f}(\omega)\|^2$ is the **energy spectral density** (energy per unit frequency) |
| Frequency | $\frac{1}{2\pi}\int_{-\infty}^{\infty}\|\hat{f}(\omega)\|^2\,d\omega$ is **total energy** |

Parseval's theorem is the statement that both rows give the **same total energy** — the Fourier transform is an energy-preserving (unitary) operation.
