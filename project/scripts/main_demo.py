"""Main demo runner for synthetic and real IQ processing."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.modulation.am_demod import coherent_demod, envelope_demod
from src.signal.channel_select import channel_select
from src.data_tools.data_loaders import load_kiwisdr_iq, load_sdrangel_iq
from src.modulation.fm_demod import fm_demod
from src.analysis.metrics import compute_snr_db
from src.modulation.modulation import generate_baseband_tone, am_modulate, fm_modulate
from src.analysis.plotting import plot_spectrum, plot_time_compare

def _align_gain(reference: np.ndarray, estimate: np.ndarray) -> np.ndarray:
    """Scale estimate to best match reference in least-squares sense."""

    n = min(reference.size, estimate.size)
    ref = reference[:n]
    est = estimate[:n]
    denom = np.dot(est, est)
    if denom == 0:
        return estimate
    scale = np.dot(ref, est) / denom
    return estimate * scale

def run_synthetic_am(sample_rate: float, duration_s: float) -> None:
    baseband = generate_baseband_tone(sample_rate, duration_s, freq_hz=50.0)
    carrier_hz = 1000.0
    am = am_modulate(baseband, carrier_hz, modulation_index=0.6)
    recovered = coherent_demod(am.astype(np.complex64), sample_rate, carrier_hz, lpf_cutoff_hz=200.0)
    recovered = recovered[: baseband.m.size]
    recovered = _align_gain(baseband.m, recovered)
    snr_db = compute_snr_db(baseband.m, recovered)
    plot_time_compare(baseband.t, baseband.m, recovered, f"Synthetic AM Demod (SNR={snr_db:.2f} dB)")
    plot_spectrum(am, sample_rate, "Synthetic AM Spectrum")


def run_synthetic_fm(sample_rate: float, duration_s: float) -> None:
    baseband = generate_baseband_tone(sample_rate, duration_s, freq_hz=50.0)
    carrier_hz = 1000.0
    fm = fm_modulate(baseband, carrier_hz, kf=50.0)
    recovered = fm_demod(fm.astype(np.complex64), sample_rate, lpf_cutoff_hz=200.0)
    t = baseband.t[:-1]
    recovered = recovered[: t.size]
    recovered = _align_gain(baseband.m[: t.size], recovered)
    snr_db = compute_snr_db(baseband.m[: t.size], recovered)
    plot_time_compare(t, baseband.m[: t.size], recovered, f"Synthetic FM Demod (SNR={snr_db:.2f} dB)")
    plot_spectrum(fm, sample_rate, "Synthetic FM Spectrum")


def run_kiwi_am(path: str, sample_rate: float, cutoff_hz: float) -> None:
    data = load_kiwisdr_iq(path, sample_rate=sample_rate)
    audio = envelope_demod(data.iq, data.sample_rate, lpf_cutoff_hz=cutoff_hz)
    t = np.arange(audio.size) / data.sample_rate
    plot_time_compare(t, audio, audio, "KiwiSDR AM Envelope", label_a="Envelope", label_b="Envelope")
    plot_spectrum(data.iq, data.sample_rate, "KiwiSDR IQ Spectrum")


def run_sdrangel_fm(path: str, sample_rate: float, channel_hz: float, bw_hz: float) -> None:
    data = load_sdrangel_iq(path, sample_rate=sample_rate)
    chan = channel_select(data.iq, data.sample_rate, center_hz=channel_hz, bandwidth_hz=bw_hz, decim_factor=4)
    audio = fm_demod(chan.iq, chan.sample_rate, lpf_cutoff_hz=15000.0, de_emphasis_tau=50e-6)
    t = np.arange(audio.size) / chan.sample_rate
    plot_time_compare(t, audio, audio, "SDRangel FM Demod", label_a="Audio", label_b="Audio")
    plot_spectrum(chan.iq, chan.sample_rate, "SDRangel Channel Spectrum")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run DSP pipeline demos.")
    parser.add_argument("--demo", choices=["synthetic-am", "synthetic-fm", "kiwi-am", "sdrangel-fm"], required=True)
    parser.add_argument("--path", default=None, help="IQ WAV path for real-data demos")
    parser.add_argument("--sample-rate", type=float, default=12000.0)
    parser.add_argument("--cutoff-hz", type=float, default=5000.0)
    parser.add_argument("--center-hz", type=float, default=0.0, help="Channel center offset (Hz)")
    parser.add_argument("--bandwidth-hz", type=float, default=200000.0)
    args = parser.parse_args()

    if args.demo == "synthetic-am":
        run_synthetic_am(args.sample_rate, duration_s=1.0)
        return 0
    if args.demo == "synthetic-fm":
        run_synthetic_fm(args.sample_rate, duration_s=1.0)
        return 0
    if args.demo == "kiwi-am":
        if args.path is None:
            print("--path is required for kiwi-am")
            return 2
        run_kiwi_am(args.path, args.sample_rate, cutoff_hz=args.cutoff_hz)
        return 0
    if args.demo == "sdrangel-fm":
        if args.path is None:
            print("--path is required for sdrangel-fm")
            return 2
        run_sdrangel_fm(args.path, args.sample_rate, channel_hz=args.center_hz, bw_hz=args.bandwidth_hz)
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
