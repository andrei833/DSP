"""Noise and channel impairment utilities."""

from __future__ import annotations

from typing import Iterable, Tuple

import numpy as np


def add_awgn(iq: np.ndarray, snr_db: float, rng_seed: int | None = None) -> np.ndarray:
    """Add complex AWGN to reach a target SNR (dB) based on signal power."""

    rng = np.random.default_rng(rng_seed)
    signal_power = np.mean(np.abs(iq) ** 2)
    snr_linear = 10.0 ** (snr_db / 10.0)
    noise_power = signal_power / snr_linear

    noise = (
        rng.normal(scale=np.sqrt(noise_power / 2.0), size=iq.size)
        + 1j * rng.normal(scale=np.sqrt(noise_power / 2.0), size=iq.size)
    )
    return iq + noise


def add_frequency_offset(iq: np.ndarray, sample_rate: float, offset_hz: float) -> np.ndarray:
    """Apply a frequency offset by complex mixing."""

    n = np.arange(iq.size)
    mixer = np.exp(1j * 2.0 * np.pi * offset_hz * n / sample_rate)
    return iq * mixer


def add_phase_noise(iq: np.ndarray, std_rad: float, rng_seed: int | None = None) -> np.ndarray:
    """Apply sample-wise phase noise with zero-mean Gaussian distribution."""

    rng = np.random.default_rng(rng_seed)
    phase = rng.normal(scale=std_rad, size=iq.size)
    return iq * np.exp(1j * phase)


def add_multipath(
    iq: np.ndarray,
    sample_rate: float,
    paths: Iterable[Tuple[float, complex]],
) -> np.ndarray:
    """Apply a simple multipath channel model.

    paths: iterable of (delay_seconds, complex_gain)
    """

    max_delay = max(delay for delay, _ in paths)
    max_samples = int(round(max_delay * sample_rate))
    h = np.zeros(max_samples + 1, dtype=np.complex64)
    for delay, gain in paths:
        idx = int(round(delay * sample_rate))
        h[idx] += gain

    return np.convolve(iq, h, mode="same")
