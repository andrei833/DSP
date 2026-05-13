"""FM demodulation utilities."""

from __future__ import annotations

from typing import Optional

import numpy as np

from ..signal.decimation import apply_fir, design_lowpass_fir


def phase_discriminator(iq: np.ndarray) -> np.ndarray:
    """FM discriminator: angle(x[n] * conj(x[n-1]))."""

    return np.angle(iq[1:] * np.conj(iq[:-1]))


def de_emphasis(x: np.ndarray, sample_rate: float, tau: float) -> np.ndarray:
    """Apply a 1st-order de-emphasis filter with time constant tau."""

    alpha = np.exp(-1.0 / (sample_rate * tau))
    y = np.empty_like(x)
    y[0] = x[0]
    for i in range(1, x.size):
        y[i] = alpha * y[i - 1] + (1.0 - alpha) * x[i]
    return y


def fm_demod(
    iq: np.ndarray,
    sample_rate: float,
    lpf_cutoff_hz: float,
    num_taps: int = 129,
    de_emphasis_tau: Optional[float] = None,
) -> np.ndarray:
    """FM demodulation: discriminator + LPF (+ optional de-emphasis)."""

    discr = phase_discriminator(iq)
    taps = design_lowpass_fir(lpf_cutoff_hz, sample_rate, num_taps=num_taps)
    audio = apply_fir(discr, taps)

    if de_emphasis_tau is not None:
        audio = de_emphasis(audio, sample_rate, de_emphasis_tau)

    return audio
