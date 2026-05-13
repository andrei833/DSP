# The Core Insight of Parseval's Proof

---

## What we are trying to show

$$
\int_{-\infty}^{\infty} f(t)\,\overline{f(t)}\, dt
\;=\;
\int_{-\infty}^{\infty} \hat{f}(\omega)\,\overline{\hat{f}(\omega)}\, d\omega
$$

Both sides are the same thing written with a conjugate:
$\;f \cdot \bar{f} = |f|^2\;$ in time, and $\;\hat{f}\cdot\overline{\hat{f}} = |\hat{f}|^2\;$ in frequency.

---

## The one trick: conjugate the IFT formula

Recall the Inverse Fourier Transform:

$$
f(t) = \frac{1}{\sqrt{2\pi}}\int_{-\infty}^{\infty} \hat{f}(\omega)\; e^{+i\omega t}\; d\omega
$$

Now take the **complex conjugate of both sides**:

$$
\overline{f(t)} = \frac{1}{\sqrt{2\pi}}\int_{-\infty}^{\infty} \overline{\hat{f}(\omega)}\; e^{-i\omega t}\; d\omega
$$

The only thing that changed in the exponent is:

$$
e^{+i\omega t} \quad\longrightarrow\quad e^{-i\omega t}
$$

because conjugating a complex exponential just **flips the sign of $i$**:

$$
\overline{e^{+i\omega t}} = e^{-i\omega t}
$$

---

## Why that sign flip is the whole game

After you substitute $\overline{f(t)}$ and swap the order of integration, you end up with this inner integral sitting inside:

$$
\int_{-\infty}^{\infty} f(t)\; e^{-i\omega t}\; dt
$$

But look — **this is exactly the definition of $\hat{f}(\omega)$** (the Fourier Transform):

$$
\hat{f}(\omega) = \frac{1}{\sqrt{2\pi}}\int_{-\infty}^{\infty} f(t)\; e^{-i\omega t}\; dt
$$

The $e^{-i\omega t}$ in the FT kernel appeared naturally from conjugating the IFT.  
So the inner integral is just $\hat{f}(\omega)$, and you are left with:

$$
\int_{-\infty}^{\infty} \overline{\hat{f}(\omega)}\;\hat{f}(\omega)\; d\omega
= \int_{-\infty}^{\infty} |\hat{f}(\omega)|^2\; d\omega
$$

---

## The full chain in one picture

$$
\int f \cdot \bar{f}\; dt
\;\xrightarrow{\text{replace }\bar{f}\text{ with conjugated IFT}}\;
\int \bar{f}\!\!\!(\omega) \underbrace{\left[\int f(t)\,e^{-i\omega t}dt\right]}_{\displaystyle\sqrt{2\pi}\;\hat{f}(\omega)} d\omega
\;\xrightarrow{\text{simplify}}\;
\int |\hat{f}(\omega)|^2\; d\omega
$$

---

## One-line summary

> Conjugating $f(t)$ through the IFT formula **flips** $e^{+i\omega t} \to e^{-i\omega t}$.  
> That flipped sign turns the IFT kernel into the **FT kernel**, so the inner integral becomes $\hat{f}(\omega)$.  
> The result is $|\hat{f}(\omega)|^2$ — and that is Parseval's theorem.
