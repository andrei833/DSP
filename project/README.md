# DSP Project: AM/FM Pipeline

This folder contains a modular DSP pipeline for AM/FM modulation and
demodulation using explicit NumPy/SciPy operations. The project uses real IQ
recordings for validation and synthetic signals for clean demonstrations.

## Requirements

- Python 3.9+
- NumPy
- SciPy
- Matplotlib

## Project Files

- PLAN.md: project plan and checklist
- src/: core DSP modules
  - data_tools/: data loaders (KiwiSDR, SDRangel, RadioML)
  - modulation/: synthetic modulation + AM/FM demod
  - signal/: channel selection, decimation, noise
  - analysis/: metrics + plotting
- scripts/: runnable examples and demos
- data/: local IQ recordings (optional)

## Quick Start

### Plot spectrum for a KiwiSDR IQ WAV

```bash
python scripts/example_plot_spectrum.py --source kiwi --path /path/to/kiwi_iq.wav
```

### Plot spectrum for an SDRangel IQ WAV

```bash
python scripts/example_plot_spectrum.py --source sdrangel --path /path/to/sdrangel_iq.wav
```

### Plot spectrum for RadioML 2016.10A

```bash
python scripts/example_plot_spectrum.py --source radioml --path /path/to/RML2016.10a_dict.pkl --mod AM-DSB --snr 10 --index 0
```

Notes:

- RadioML is optional and synthetic (CC BY-NC-SA 4.0). Use it only as labeled
  benchmark data.
- If the RadioML sample rate is unknown, the spectrum uses a normalized
  frequency axis.

## Main Demo Examples

### Synthetic AM demo

```bash
python scripts/main_demo.py --demo synthetic-am --sample-rate 8000
```

### Synthetic FM demo

```bash
python scripts/main_demo.py --demo synthetic-fm --sample-rate 8000
```

### KiwiSDR AM envelope demo

```bash
python scripts/main_demo.py --demo kiwi-am --path /path/to/kiwi_iq.wav --sample-rate 12000 --cutoff-hz 5000
```

### SDRangel FM demo

```bash
python scripts/main_demo.py --demo sdrangel-fm --path /path/to/sdrangel_iq.wav --sample-rate 4000000 --center-hz 0 --bandwidth-hz 200000
```

## Data Sources (Planned)

- AM live IQ: KiwiSDR via kiwirecorder.py
- FM real IQ: SDRangel broadcast FM IQ (bfm.zip)
- Optional labeled benchmark: RadioML 2016.10A

## Status

- Channel selection and frequency shifting: done
- Decimation/resampling with anti-alias filtering: done
- AM envelope demod and FM discriminator: done
- Reproducible plotting and evaluation scripts: done
