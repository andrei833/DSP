"""Channel selection and decimation utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
from scipy.signal import firwin, lfilter


@dataclass
class ChannelizedIQ:
    """Container for channelized IQ and updated sample rate."""

    iq: np.ndarray
    sample_rate: float
    center_hz: float
    bandwidth_hz: float


def frequency_shift(iq: np.ndarray, sample_rate: float, freq_hz: float) -> np.ndarray:
    """Shift spectrum by freq_hz using complex mixing."""

    n = np.arange(iq.size)
    mixer = np.exp(-1j * 2.0 * np.pi * freq_hz * n / sample_rate)
    return iq * mixer


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


def apply_fir(iq: np.ndarray, taps: np.ndarray) -> np.ndarray:
    """Apply an FIR filter to complex IQ using lfilter."""

    return lfilter(taps, 1.0, iq)


def decimate(iq: np.ndarray, factor: int, taps: Optional[np.ndarray] = None) -> np.ndarray:
    """Decimate IQ by an integer factor with optional anti-alias filtering."""

    if factor <= 1:
        return iq

    if taps is not None:
        iq = apply_fir(iq, taps)

    return iq[::factor]


def channel_select(
    iq: np.ndarray,
    sample_rate: float,
    center_hz: float,
    bandwidth_hz: float,
    decim_factor: int = 1,
    num_taps: int = 129,
) -> ChannelizedIQ:
    """Shift to center_hz, lowpass filter, and decimate to isolate a channel."""

    shifted = frequency_shift(iq, sample_rate, center_hz)
    taps = design_lowpass_fir(bandwidth_hz * 0.5, sample_rate, num_taps=num_taps)
    filtered = apply_fir(shifted, taps)
    decimated = decimate(filtered, decim_factor)
    new_rate = sample_rate / decim_factor

    return ChannelizedIQ(
        iq=decimated,
        sample_rate=new_rate,
        center_hz=center_hz,
        bandwidth_hz=bandwidth_hz,
    )
