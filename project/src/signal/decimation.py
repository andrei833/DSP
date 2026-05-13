"""Decimation and resampling utilities."""

from __future__ import annotations

from typing import Optional, Tuple

import numpy as np
from scipy.signal import firwin, lfilter


def design_lowpass_fir(
    cutoff_hz: float,
    sample_rate: float,
    num_taps: int = 129,
    window: str = "hann",
) -> np.ndarray:
    """Design a real-valued lowpass FIR filter."""

    nyq = 0.5 * sample_rate
    cutoff = min(cutoff_hz / nyq, 0.999)
    return firwin(num_taps, cutoff, window=window)


def apply_fir(x: np.ndarray, taps: np.ndarray) -> np.ndarray:
    """Apply an FIR filter using direct form."""

    return lfilter(taps, 1.0, x)


def decimate(
    x: np.ndarray,
    sample_rate: float,
    factor: int,
    cutoff_hz: Optional[float] = None,
    num_taps: int = 129,
) -> Tuple[np.ndarray, float]:
    """Decimate by an integer factor with anti-alias filtering."""

    if factor <= 1:
        return x, sample_rate

    if cutoff_hz is None:
        cutoff_hz = 0.45 * (sample_rate / factor)

    taps = design_lowpass_fir(cutoff_hz, sample_rate, num_taps=num_taps)
    filtered = apply_fir(x, taps)
    return filtered[::factor], sample_rate / factor


def upsample(x: np.ndarray, factor: int) -> np.ndarray:
    """Upsample by inserting zeros between samples."""

    if factor <= 1:
        return x

    y = np.zeros((x.size * factor,), dtype=x.dtype)
    y[::factor] = x
    return y


def resample_rational(
    x: np.ndarray,
    sample_rate: float,
    up: int,
    down: int,
    cutoff_hz: Optional[float] = None,
    num_taps: int = 161,
) -> Tuple[np.ndarray, float]:
    """Resample by a rational factor using explicit upsample/filter/downsample."""

    if up <= 0 or down <= 0:
        raise ValueError("up and down must be positive integers")

    if up == 1 and down == 1:
        return x, sample_rate

    upsampled = upsample(x, up)
    sample_rate_up = sample_rate * up
    new_rate = sample_rate * up / down

    if cutoff_hz is None:
        cutoff_hz = 0.45 * min(sample_rate, new_rate)

    taps = design_lowpass_fir(cutoff_hz, sample_rate_up, num_taps=num_taps)
    filtered = apply_fir(upsampled, taps)

    return filtered[::down], new_rate
