"""Concept demos: aliasing, spectral copies, Gibbs, windowing, and LPF in frequency domain."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.analysis.plotting import plot_spectrum


def demo_aliasing(sample_rate: float, tone_hz: float, duration_s: float) -> None:
    n = int(round(sample_rate * duration_s))
    t = np.arange(n) / sample_rate
    x = np.cos(2.0 * np.pi * tone_hz * t)
    plot_spectrum(x, sample_rate, f"Aliasing Demo: tone={tone_hz} Hz, fs={sample_rate} Hz")


def demo_spectral_copies(sample_rate: float, baseband_hz: float, duration_s: float) -> None:
    n = int(round(sample_rate * duration_s))
    t = np.arange(n) / sample_rate
    x = np.cos(2.0 * np.pi * baseband_hz * t)
    plot_spectrum(x, sample_rate, f"Spectral Copies: baseband={baseband_hz} Hz")


def demo_gibbs(sample_rate: float, duration_s: float) -> None:
    n = int(round(sample_rate * duration_s))
    t = np.linspace(-0.5, 0.5, n, endpoint=False)
    x = np.sign(t)
    spectrum = np.fft.fftshift(np.fft.fft(x))
    freqs = np.fft.fftshift(np.fft.fftfreq(n, d=1.0 / sample_rate))
    mag_db = 20 * np.log10(np.maximum(np.abs(spectrum), 1e-12))

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(freqs, mag_db, linewidth=1.0)
    ax.set_title("Gibbs Phenomenon: Square Wave Spectrum")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude (dB)")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def demo_windowing(sample_rate: float, tone_hz: float, duration_s: float) -> None:
    n = int(round(sample_rate * duration_s))
    t = np.arange(n) / sample_rate
    x = np.cos(2.0 * np.pi * tone_hz * t)

    windows = {
        "Rect": np.ones(n),
        "Hann": np.hanning(n),
        "Hamming": np.hamming(n),
    }

    fig, ax = plt.subplots(figsize=(10, 3))
    for name, w in windows.items():
        spectrum = np.fft.fftshift(np.fft.fft(x * w))
        freqs = np.fft.fftshift(np.fft.fftfreq(n, d=1.0 / sample_rate))
        mag_db = 20 * np.log10(np.maximum(np.abs(spectrum), 1e-12))
        ax.plot(freqs, mag_db, linewidth=1.0, label=name)

    ax.set_title("Windowing Leakage Tradeoff")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude (dB)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.show()


def demo_lowpass_freq_domain(sample_rate: float, cutoff_hz: float, duration_s: float) -> None:
    n = int(round(sample_rate * duration_s))
    t = np.arange(n) / sample_rate
    x = np.cos(2.0 * np.pi * 200.0 * t) + 0.4 * np.cos(2.0 * np.pi * 1200.0 * t)

    freqs = np.fft.fftshift(np.fft.fftfreq(n, d=1.0 / sample_rate))
    spectrum = np.fft.fftshift(np.fft.fft(x))
    lpf = np.abs(freqs) <= cutoff_hz
    filtered = np.fft.ifft(np.fft.ifftshift(spectrum * lpf)).real

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(t, x, label="Original", linewidth=1.0)
    ax.plot(t, filtered, label="LPF (freq-domain)", linewidth=1.0, alpha=0.7)
    ax.set_title("Lowpass Filtering in Frequency Domain")
    ax.set_xlabel("Time (s)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.show()


def main() -> int:
    parser = argparse.ArgumentParser(description="DSP concept demos.")
    parser.add_argument(
        "--demo",
        choices=["aliasing", "copies", "gibbs", "windowing", "lpf"],
        required=True,
    )
    parser.add_argument("--sample-rate", type=float, default=2000.0)
    parser.add_argument("--tone-hz", type=float, default=1200.0)
    parser.add_argument("--duration", type=float, default=1.0)
    parser.add_argument("--cutoff-hz", type=float, default=400.0)
    args = parser.parse_args()

    if args.demo == "aliasing":
        demo_aliasing(args.sample_rate, args.tone_hz, args.duration)
        return 0
    if args.demo == "copies":
        demo_spectral_copies(args.sample_rate, args.tone_hz, args.duration)
        return 0
    if args.demo == "gibbs":
        demo_gibbs(args.sample_rate, args.duration)
        return 0
    if args.demo == "windowing":
        demo_windowing(args.sample_rate, args.tone_hz, args.duration)
        return 0
    if args.demo == "lpf":
        demo_lowpass_freq_domain(args.sample_rate, args.cutoff_hz, args.duration)
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
