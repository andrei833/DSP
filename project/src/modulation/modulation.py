"""Synthetic baseband generation and AM/FM modulation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np


@dataclass
class BasebandSignal:
    """Container for baseband message signal and time axis."""

    t: np.ndarray
    m: np.ndarray
    sample_rate: float


def generate_baseband_tone(
    sample_rate: float,
    duration_s: float,
    freq_hz: float,
    amplitude: float = 1.0,
) -> BasebandSignal:
    """Generate a simple sinusoidal baseband message."""

    n = int(round(sample_rate * duration_s))
    t = np.arange(n) / sample_rate
    m = amplitude * np.cos(2.0 * np.pi * freq_hz * t)
    return BasebandSignal(t=t, m=m, sample_rate=sample_rate)


def generate_baseband_multitone(
    sample_rate: float,
    duration_s: float,
    tones: Tuple[Tuple[float, float], ...],
) -> BasebandSignal:
    """Generate a multitone baseband message.

    tones: tuple of (freq_hz, amplitude)
    """

    n = int(round(sample_rate * duration_s))
    t = np.arange(n) / sample_rate
    m = np.zeros_like(t)
    for freq_hz, amplitude in tones:
        m += amplitude * np.cos(2.0 * np.pi * freq_hz * t)
    return BasebandSignal(t=t, m=m, sample_rate=sample_rate)


def am_modulate(
    baseband: BasebandSignal,
    carrier_hz: float,
    modulation_index: float = 0.5,
) -> np.ndarray:
    """AM modulation: x(t) = [1 + mu*m(t)] cos(2pi f_c t)."""

    m = baseband.m / np.max(np.abs(baseband.m))
    t = baseband.t
    return (1.0 + modulation_index * m) * np.cos(2.0 * np.pi * carrier_hz * t)


def fm_modulate(
    baseband: BasebandSignal,
    carrier_hz: float,
    kf: float,
) -> np.ndarray:
    """FM modulation: x(t) = cos(2pi f_c t + 2pi kf integral m(t) dt)."""

    t = baseband.t
    integral = np.cumsum(baseband.m) / baseband.sample_rate
    phase = 2.0 * np.pi * carrier_hz * t + 2.0 * np.pi * kf * integral
    return np.cos(phase)
