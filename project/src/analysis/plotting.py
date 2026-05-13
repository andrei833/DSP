"""Plotting helpers for evaluation and comparisons."""

from __future__ import annotations

from typing import Optional

import matplotlib.pyplot as plt
import numpy as np


def plot_time_compare(
    t: np.ndarray,
    original: np.ndarray,
    recovered: np.ndarray,
    title: str,
    label_a: str = "Original",
    label_b: str = "Recovered",
) -> None:
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(t, original, label=label_a, linewidth=1.0)
    ax.plot(t, recovered, label=label_b, linewidth=1.0, alpha=0.7)
    ax.set_title(title)
    ax.set_xlabel("Time (s)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_spectrum(
    x: np.ndarray,
    sample_rate: float,
    title: str,
    window_sec: Optional[float] = None,
) -> None:
    n = x.size
    if window_sec is None:
        window_samples = n
    else:
        window_samples = max(1, int(round(window_sec * sample_rate)))
        window_samples = min(window_samples, n)

    window = np.hanning(window_samples)
    segment = x[:window_samples]
    spectrum = np.fft.fftshift(np.fft.fft(segment * window))
    freqs = np.fft.fftshift(np.fft.fftfreq(window_samples, d=1.0 / sample_rate))
    mag_db = 20 * np.log10(np.maximum(np.abs(spectrum), 1e-12))

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(freqs, mag_db, linewidth=1.0)
    ax.set_title(title)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude (dB)")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
