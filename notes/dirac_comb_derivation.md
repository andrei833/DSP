# Where Does the Dirac Comb Formula Come From?

---

## The formula

$$
\sum_{n=-\infty}^{\infty} e^{i2\pi n t/T} = T \sum_{k=-\infty}^{\infty} \delta(t - kT)
$$

Left side: a sum of harmonics. Right side: a train of deltas.  
**They are equal.** But why?

---

## Building intuition: what happens when you add harmonics?

### Start with one harmonic

$$
e^{i2\pi \cdot 0 \cdot t/T} = 1
$$

This is just a flat constant. Boring.

### Add two more ($n = -1$ and $n = +1$)

$$
1 + e^{i2\pi t/T} + e^{-i2\pi t/T} = 1 + 2\cos\!\left(\frac{2\pi t}{T}\right)
$$

Now you get a bump at $t = 0$ (where all three terms equal 1 and add up to 3) and partial cancellation elsewhere.

### Add more and more harmonics ($n = -N \ldots N$)

$$
S_N(t) = \sum_{n=-N}^{N} e^{i2\pi n t/T}
$$

As $N$ grows:
- At $t = 0, \pm T, \pm 2T, \ldots$ → **all terms equal 1** → they add up to $2N+1$ → growing spike
- At all other $t$ → the terms point in **random directions** on the unit circle → they cancel out

```
N = 1:     /\      /\      /\
          /  \    /  \    /  \      gentle bumps
         /    \  /    \  /    \

N = 5:     |       |       |
          /|\     /|\     /|\       sharper spikes
         / | \   / | \   / | \

N = ∞:     ↑       ↑       ↑       perfect delta functions
           |       |       |
   ────────┘       └───────┘────
         -T        0        T
```

### Why do they add up at $t = kT$?

At $t = kT$ (any integer multiple of the period):

$$
e^{i2\pi n (kT)/T} = e^{i2\pi nk} = 1 \quad \text{for every } n
$$

because $e^{i2\pi \cdot \text{(integer)}} = 1$ always. So **every single harmonic equals 1** at these points, and they all add constructively.

### Why do they cancel everywhere else?

At any other $t$, the phases $e^{i2\pi n t/T}$ spread evenly around the unit circle as $n$ varies. Equal spacing around a circle sums to zero — this is the same reason that the $N$-th roots of unity sum to zero.

---

## The precise formula (with the closed-form partial sum)

The finite sum actually has a closed form (geometric series):

$$
S_N(t) = \sum_{n=-N}^{N} e^{i2\pi n t/T} = \frac{\sin\!\left(\pi(2N+1)t/T\right)}{\sin\!\left(\pi t/T\right)}
$$

This is the **Dirichlet kernel**. As $N \to \infty$:

- The central peak gets **taller** (height $= 2N+1$) and **narrower** (width $\sim T/(2N+1)$)
- The area under the peak stays $= T$ (peak height × peak width)
- The side lobes oscillate faster and faster, averaging to zero

This is exactly the behaviour of a delta function scaled by $T$:

$$
\lim_{N \to \infty} S_N(t) = T \sum_{k=-\infty}^{\infty} \delta(t - kT)
$$

---

## Summary

| What happens | Why |
|---|---|
| Spikes at $t = 0, \pm T, \pm 2T, \ldots$ | All harmonics equal 1 at integer multiples of $T$ → constructive interference |
| Zero everywhere else | Harmonics have evenly spread phases → destructive interference (cancel out) |
| Height of spikes → $\infty$ | More and more terms adding up to 1 each |
| Width of spikes → 0 | Cancellation becomes more precise |
| Area of each spike → $T$ | Height grows as $2N+1$, width shrinks as $T/(2N+1)$, product stays $T$ |

A function that is zero everywhere, infinite at one point, with finite area = **delta function**.

Repeating every $T$ = **Dirac comb**.

$$
\boxed{\sum_{n=-\infty}^{\infty} e^{i2\pi n t/T} = T \sum_{k=-\infty}^{\infty} \delta(t - kT)}
$$
