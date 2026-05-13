# Frequency Shift Property — Why $+a$ and Not $-a$?

**Claim:** $\mathcal{F}\left[f(t)e^{iat}\right] = \hat{f}(\omega + a)$

The sign is **not arbitrary**. It is a strict mathematical consequence of which Fourier transform definition you use.  Here is the full derivation of both cases so you can see exactly where the sign comes from.

---

## The two conventions

| Convention | Definition |
|------------|------------|
| **A** (common in engineering/DSP) | $\hat{f}(\omega) = \displaystyle\int_{-\infty}^{\infty} f(t)\, e^{+i\omega t}\, dt$ |
| **B** (common in mathematics) | $\hat{f}(\omega) = \displaystyle\int_{-\infty}^{\infty} f(t)\, e^{-i\omega t}\, dt$ |

---

## Proof under Convention A — gives $+a$

Start from the definition with $e^{+i\omega t}$:

$$
\mathcal{F}\left[f(t)e^{iat}\right](\omega)
= \int_{-\infty}^{\infty} f(t)\,e^{iat} \cdot e^{+i\omega t}\, dt
$$

Combine the two exponentials (the exponents simply add):

$$
= \int_{-\infty}^{\infty} f(t)\, e^{i(\omega + a)t}\, dt
$$

By the **definition of the Fourier transform**, $\displaystyle\int f(t)\,e^{i\Omega t}\,dt = \hat{f}(\Omega)$.  
Here $\Omega = \omega + a$, so:

$$
\boxed{= \hat{f}(\omega + a)}
$$

**The $+a$ comes directly from the fact that both the kernel and $e^{iat}$ have the same sign in the exponent, so $+ia$ and $+i\omega$ add together.**

---

## Proof under Convention B — gives $-a$

Start from the definition with $e^{-i\omega t}$:

$$
\mathcal{F}\left[f(t)e^{iat}\right](\omega)
= \int_{-\infty}^{\infty} f(t)\,e^{iat} \cdot e^{-i\omega t}\, dt
$$

Combine the exponentials:

$$
= \int_{-\infty}^{\infty} f(t)\, e^{-i(\omega - a)t}\, dt
$$

By definition $\displaystyle\int f(t)\,e^{-i\Omega t}\,dt = \hat{f}(\Omega)$.  
Here $\Omega = \omega - a$, so:

$$
\boxed{= \hat{f}(\omega - a)}
$$

**The $-a$ comes from the fact that $e^{iat}$ has the opposite sign to the kernel $e^{-i\omega t}$, so $+ia$ subtracts from $-i\omega$.**

---

## Side by side: where the sign comes from

$$
e^{iat} \cdot e^{\pm i\omega t} = e^{i(\pm\omega + a)t}
\begin{cases}
e^{i(\omega + a)t} & \text{if kernel is } e^{+i\omega t} \Rightarrow \hat{f}(\omega+a) \\
e^{-i(\omega - a)t} & \text{if kernel is } e^{-i\omega t} \Rightarrow \hat{f}(\omega-a)
\end{cases}
$$

The **only arithmetic** happening is adding exponents. The sign of the result is locked in the moment you choose your FT convention — there is no freedom after that.

---

## Is this just convention, or is it real?

It is **both**. Yes, the choice of sign in the FT definition is a convention. But once that convention is fixed, the sign of the frequency shift is a **hard mathematical theorem** — you cannot get $+a$ from convention B without making an error, and you cannot get $-a$ from convention A without making an error.

Your textbook/course uses **Convention A** ($e^{+i\omega t}$), which is why the answer is $\hat{f}(\omega + a)$.
If you computed $\hat{f}(\omega - a)$, you were silently using **Convention B** in your head — that is the only reason for the discrepancy.

---

## Memory aid

> Multiplying $f(t)$ by $e^{iat}$ **shifts the frequency axis by $+a$** in the direction that matches the sign in the FT kernel.
>
> - kernel $e^{+i\omega t}$: shift is $+a$ ✓  
> - kernel $e^{-i\omega t}$: shift is $-a$ ✓
