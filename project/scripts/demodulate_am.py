"""Demodulate KiwiSDR AM IQ WAV into audio WAV."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from scipy.io import wavfile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.data_tools.data_loaders import load_kiwisdr_iq
from src.modulation.am_demod import envelope_demod
from src.signal.channel_select import channel_select
from src.signal.decimation import resample_rational


def _normalize_audio(x: np.ndarray) -> np.ndarray:
    peak = np.max(np.abs(x))
    if peak == 0:
        return x.astype(np.float32)
    return (x / peak).astype(np.float32)


def main() -> int:
    parser = argparse.ArgumentParser(description="Demodulate AM IQ to audio WAV.")
    parser.add_argument("--path", required=True, help="Path to KiwiSDR IQ WAV")
    parser.add_argument("--out", required=True, help="Output audio WAV path")
    parser.add_argument("--sample-rate", type=float, default=None, help="Override IQ sample rate")
    parser.add_argument("--lpf-cutoff", type=float, default=5000.0)
    parser.add_argument("--freq-offset", type=float, default=0.0, help="Frequency offset to remove (Hz)")
    parser.add_argument("--bandwidth", type=float, default=10000.0, help="AM channel bandwidth (Hz)")
    parser.add_argument("--decim", type=int, default=1, help="Optional decimation factor before demod")
    parser.add_argument("--trim-sec", type=float, default=0.0, help="Trim leading seconds")
    parser.add_argument("--audio-rate", type=int, default=None, help="Optional output audio sample rate")
    args = parser.parse_args()

    data = load_kiwisdr_iq(args.path, sample_rate=args.sample_rate)
    iq = data.iq
    if args.trim_sec > 0:
        trim_samples = int(round(args.trim_sec * data.sample_rate))
        iq = iq[trim_samples:]

    if args.freq_offset != 0.0 or args.decim > 1:
        chan = channel_select(
            iq,
            data.sample_rate,
            center_hz=args.freq_offset,
            bandwidth_hz=args.bandwidth,
            decim_factor=args.decim,
        )
        iq = chan.iq
        sample_rate = chan.sample_rate
    else:
        sample_rate = data.sample_rate

    audio = envelope_demod(iq, sample_rate, lpf_cutoff_hz=args.lpf_cutoff)

    out_rate = int(sample_rate)
    if args.audio_rate is not None and args.audio_rate != out_rate:
        up = int(args.audio_rate)
        down = int(out_rate)
        audio, out_rate = resample_rational(audio, out_rate, up=up, down=down)
        out_rate = int(round(out_rate))

    audio = _normalize_audio(audio)
    wavfile.write(args.out, out_rate, (audio * 32767).astype(np.int16))
    print(f"Wrote {args.out} at {out_rate} Hz")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
