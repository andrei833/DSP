"""Evaluation metrics for signal recovery."""

from __future__ import annotations

import numpy as np


def compute_snr_db(reference: np.ndarray, estimate: np.ndarray) -> float:
    """Compute SNR in dB using reference as the clean signal."""

    n = min(reference.size, estimate.size)
    ref = reference[:n]
    est = estimate[:n]
    noise = ref - est

    signal_power = np.mean(ref**2)
    noise_power = np.mean(noise**2)
    if noise_power <= 0:
        return float("inf")

    return 10.0 * np.log10(signal_power / noise_power)


def compute_mse(reference: np.ndarray, estimate: np.ndarray) -> float:
    """Mean squared error between reference and estimate."""

    n = min(reference.size, estimate.size)
    ref = reference[:n]
    est = estimate[:n]
    return float(np.mean((ref - est) ** 2))
