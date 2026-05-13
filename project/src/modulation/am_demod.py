"""AM demodulation utilities."""

from __future__ import annotations

import numpy as np

from ..signal.decimation import apply_fir, design_lowpass_fir


def envelope_demod(
    iq: np.ndarray,
    sample_rate: float,
    lpf_cutoff_hz: float,
    num_taps: int = 129,
) -> np.ndarray:
    """Envelope detector for AM: |x[n]|, DC removal, and LPF."""

    mag = np.abs(iq)
    mag = mag - np.mean(mag)
    taps = design_lowpass_fir(lpf_cutoff_hz, sample_rate, num_taps=num_taps)
    return apply_fir(mag, taps)


def coherent_demod(
    iq: np.ndarray,
    sample_rate: float,
    carrier_hz: float,
    lpf_cutoff_hz: float,
    num_taps: int = 129,
) -> np.ndarray:
    """Synchronous AM demod with carrier mixing and LPF."""

    n = np.arange(iq.size)
    mixer = np.exp(-1j * 2.0 * np.pi * carrier_hz * n / sample_rate)
    mixed = np.real(iq * mixer)
    mixed = mixed - np.mean(mixed)
    taps = design_lowpass_fir(lpf_cutoff_hz, sample_rate, num_taps=num_taps)
    return apply_fir(mixed, taps)
