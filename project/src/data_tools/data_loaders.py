"""Data loading utilities for IQ datasets and WAV IQ recordings."""

from __future__ import annotations

from dataclasses import dataclass
import pickle
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
from scipy.io import wavfile


@dataclass
class IQData:
    """Container for complex IQ samples with metadata."""

    iq: np.ndarray
    sample_rate: Optional[float]
    meta: Dict[str, Any]


@dataclass
class SpectrumData:
    """Container for spectrum data with metadata."""

    freqs_hz: np.ndarray
    power_db: np.ndarray
    meta: Dict[str, Any]


def _normalize_iq(iq: np.ndarray) -> np.ndarray:
    """Normalize IQ to float32 in [-1, 1] based on dtype."""

    if np.issubdtype(iq.dtype, np.floating):
        return iq.astype(np.float32, copy=False)

    info = np.iinfo(iq.dtype)
    scale = max(abs(info.min), info.max)
    return iq.astype(np.float32) / scale


def read_wav_iq(path: str, sample_rate: Optional[float] = None) -> IQData:
    """Load interleaved IQ from a stereo WAV file.

    Assumes the WAV has shape (N, 2) with I in channel 0 and Q in channel 1.
    """

    wav_rate, data = wavfile.read(path)
    if data.ndim != 2 or data.shape[1] != 2:
        raise ValueError("Expected stereo WAV with I/Q channels.")

    i = _normalize_iq(data[:, 0])
    q = _normalize_iq(data[:, 1])
    iq = (i + 1j * q).astype(np.complex64)

    return IQData(iq=iq, sample_rate=sample_rate or float(wav_rate), meta={"path": path})


def load_kiwisdr_iq(path: str, sample_rate: Optional[float] = None) -> IQData:
    """Load KiwiSDR IQ WAV recordings from kiwirecorder.py."""

    data = read_wav_iq(path, sample_rate=sample_rate)
    data.meta["source"] = "kiwisdr"
    return data


def load_kiwisdr_spectrum_csv(
    path: str,
    freq_start_hz: Optional[float] = None,
    freq_step_hz: Optional[float] = None,
) -> SpectrumData:
    """Load a KiwiSDR spectrum snapshot saved as CSV.

    Supported formats:
    - Two columns: freq_hz, power_db
    - One column: power_db (requires freq_start_hz and freq_step_hz)
    """

    data = np.loadtxt(path, delimiter=",")
    if data.ndim == 1:
        power_db = data.astype(np.float32)
        if freq_start_hz is None or freq_step_hz is None:
            raise ValueError("freq_start_hz and freq_step_hz are required for 1-column CSV.")
        freqs_hz = freq_start_hz + freq_step_hz * np.arange(power_db.size)
    else:
        if data.shape[1] < 2:
            raise ValueError("CSV must have 1 or 2 columns.")
        freqs_hz = data[:, 0].astype(np.float32)
        power_db = data[:, 1].astype(np.float32)

    return SpectrumData(
        freqs_hz=freqs_hz,
        power_db=power_db,
        meta={"path": path, "source": "kiwisdr", "format": "csv"},
    )


def load_sdrangel_iq(path: str, sample_rate: Optional[float] = None) -> IQData:
    """Load SDRangel IQ WAV recordings (e.g., bfm.zip contents)."""

    data = read_wav_iq(path, sample_rate=sample_rate)
    data.meta["source"] = "sdrangel"
    return data


def load_radioml_2016_10a(
    path: str,
    mods: Optional[Sequence[str]] = None,
    snrs: Optional[Sequence[int]] = None,
    max_per_class: Optional[int] = None,
    shuffle: bool = True,
    rng_seed: int = 0,
) -> Tuple[np.ndarray, List[Dict[str, Any]]]:
    """Load RadioML 2016.10A (pickle) and return complex IQ samples.

    The pickle maps (modulation, snr) -> array with shape (N, 2, 128).
    This function returns X with shape (M, 128) complex64 and a list of labels.
    """

    with open(path, "rb") as f:
        dataset = pickle.load(f, encoding="latin1")

    xs: List[np.ndarray] = []
    labels: List[Dict[str, Any]] = []

    for (mod, snr), data in sorted(dataset.items()):
        if mods is not None and mod not in mods:
            continue
        if snrs is not None and snr not in snrs:
            continue

        if max_per_class is not None:
            data = data[:max_per_class]

        iq = data[:, 0, :] + 1j * data[:, 1, :]
        xs.append(iq.astype(np.complex64))
        labels.extend([{"mod": mod, "snr": snr}] * iq.shape[0])

    if not xs:
        return np.empty((0, 0), dtype=np.complex64), []

    x_all = np.concatenate(xs, axis=0)
    if shuffle:
        rng = np.random.default_rng(rng_seed)
        idx = rng.permutation(x_all.shape[0])
        x_all = x_all[idx]
        labels = [labels[i] for i in idx]

    return x_all, labels
