"""Small example: load IQ data and plot its spectrum."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.data_tools.data_loaders import load_kiwisdr_iq, load_sdrangel_iq, load_radioml_2016_10a


def _plot_time_domain(
    iq: np.ndarray,
    sample_rate: float,
    title: str,
    max_samples: int = 5000,
) -> None:
    """Plot I/Q, magnitude, and phase in the time domain."""

    n = min(iq.size, max_samples)
    t = np.arange(n) / sample_rate
    i = np.real(iq[:n])
    q = np.imag(iq[:n])
    mag = np.abs(iq[:n])
    phase = np.angle(iq[:n])

    fig, axes = plt.subplots(2, 2, figsize=(10, 6), sharex=True)
    fig.suptitle(title)

    axes[0, 0].plot(t, i, linewidth=0.9)
    axes[0, 0].set_ylabel("I")
    axes[0, 0].grid(True, alpha=0.3)

    axes[0, 1].plot(t, q, linewidth=0.9)
    axes[0, 1].set_ylabel("Q")
    axes[0, 1].grid(True, alpha=0.3)

    axes[1, 0].plot(t, mag, linewidth=0.9)
    axes[1, 0].set_ylabel("Magnitude")
    axes[1, 0].set_xlabel("Time (s)")
    axes[1, 0].grid(True, alpha=0.3)

    axes[1, 1].plot(t, phase, linewidth=0.9)
    axes[1, 1].set_ylabel("Phase (rad)")
    axes[1, 1].set_xlabel("Time (s)")
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def _plot_spectrum(
    iq: np.ndarray,
    sample_rate: float,
    title: str,
    window_sec: float | None = None,
    freq_offset_hz: float = 0.0,
) -> None:
    """Plot a magnitude spectrum; optionally add a time slider."""

    n = iq.size
    if window_sec is None:
        window_samples = n
    else:
        window_samples = max(1, int(round(window_sec * sample_rate)))
        window_samples = min(window_samples, n)

    window = np.hanning(window_samples)
    freqs = np.fft.fftshift(np.fft.fftfreq(window_samples, d=1.0 / sample_rate))
    freqs = freqs + freq_offset_hz

    def compute_mag_db(start_idx: int) -> np.ndarray:
        segment = iq[start_idx : start_idx + window_samples]
        spectrum = np.fft.fftshift(np.fft.fft(segment * window))
        return 20 * np.log10(np.maximum(np.abs(spectrum), 1e-12))

    fig, ax = plt.subplots(figsize=(10, 4))
    plt.subplots_adjust(bottom=0.25)

    start_idx = 0
    mag_db = compute_mag_db(start_idx)
    (line,) = ax.plot(freqs, mag_db, linewidth=1.0)
    ax.set_title(title)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude (dB)")
    ax.grid(True, alpha=0.3)

    if window_samples < n:
        max_start = (n - window_samples) / sample_rate
        slider_ax = fig.add_axes([0.2, 0.08, 0.6, 0.03])
        slider = Slider(
            slider_ax,
            "Start (s)",
            0.0,
            max_start,
            valinit=0.0,
            valstep=1.0 / sample_rate,
        )

        def on_change(val: float) -> None:
            idx = int(round(val * sample_rate))
            line.set_ydata(compute_mag_db(idx))
            ax.set_title(f"{title} (t={val:.2f}s)")
            fig.canvas.draw_idle()

        slider.on_changed(on_change)

    plt.show()


def main() -> int:
    parser = argparse.ArgumentParser(description="Load IQ data and plot spectrum.")
    parser.add_argument("--source", choices=["kiwi", "sdrangel", "radioml"], required=True)
    parser.add_argument("--path", required=True, help="Path to WAV or RadioML pickle file")
    parser.add_argument("--sample-rate", type=float, default=None)
    parser.add_argument("--mod", default=None, help="RadioML modulation (e.g., AM-DSB, WBFM)")
    parser.add_argument("--snr", type=int, default=None, help="RadioML SNR level")
    parser.add_argument("--index", type=int, default=0, help="RadioML sample index")
    parser.add_argument(
        "--window-sec",
        type=float,
        default=None,
        help="FFT window length in seconds (enables time slider if shorter than data)",
    )
    parser.add_argument(
        "--freq-offset",
        type=float,
        default=0.0,
        help="Frequency axis offset in Hz (e.g., RF center frequency)",
    )
    parser.add_argument(
        "--show-time",
        action="store_true",
        help="Show time-domain I/Q, magnitude, and phase plots",
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=5000,
        help="Max samples for time-domain plots",
    )
    args = parser.parse_args()

    if args.source == "kiwi":
        data = load_kiwisdr_iq(args.path, sample_rate=args.sample_rate)
        if args.show_time:
            _plot_time_domain(data.iq, data.sample_rate, "KiwiSDR IQ Time", args.max_samples)
        _plot_spectrum(
            data.iq,
            data.sample_rate,
            "KiwiSDR IQ Spectrum",
            args.window_sec,
            args.freq_offset,
        )
        return 0

    if args.source == "sdrangel":
        data = load_sdrangel_iq(args.path, sample_rate=args.sample_rate)
        if args.show_time:
            _plot_time_domain(data.iq, data.sample_rate, "SDRangel IQ Time", args.max_samples)
        _plot_spectrum(
            data.iq,
            data.sample_rate,
            "SDRangel IQ Spectrum",
            args.window_sec,
            args.freq_offset,
        )
        return 0

    if args.source == "radioml":
        if args.mod is None or args.snr is None:
            print("RadioML requires --mod and --snr.")
            return 2
        x, labels = load_radioml_2016_10a(args.path, mods=[args.mod], snrs=[args.snr])
        if x.size == 0:
            print("No samples found for the given modulation/SNR.")
            return 2
        if args.index >= x.shape[0]:
            print(f"Index {args.index} out of range (0..{x.shape[0]-1}).")
            return 2
        iq = x[args.index]
        sample_rate = args.sample_rate or 1.0
        if args.show_time:
            _plot_time_domain(
                iq,
                sample_rate,
                f"RadioML IQ Time: {args.mod} @ {args.snr} dB",
                args.max_samples,
            )
        _plot_spectrum(
            iq,
            sample_rate,
            f"RadioML Spectrum: {args.mod} @ {args.snr} dB",
            args.window_sec,
            args.freq_offset,
        )
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
