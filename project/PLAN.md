## Plan: Modular AM/FM DSP Pipeline with Synthetic Demonstrations and Real IQ Validation

Build a modular Python DSP pipeline (NumPy/SciPy/Matplotlib only) split into
data_tools, modulation, signal, and analysis modules. Use synthetic baseband
signals for clean modulation demonstrations and real IQ recordings for
validation of demodulation, filtering, and noise robustness.

- [x] Confirm datasets and licensing: primary FM = SDRangel broadcast FM IQ
      (bfm.zip); primary AM = KiwiSDR live IQ via kiwirecorder.py; AM spectrum
      via KiwiSDR API snapshots; optional benchmark = RadioML (synthetic, CC
      BY-NC-SA 4.0) only for labeled SNR/modulation tests.
- [x] Data module: loaders for KiwiSDR WAV IQ, KiwiSDR spectrum snapshots,
      SDRangel IQ WAV, and optional RadioML pickle/HDF5; normalization; metadata
      parsing; unified IQ sample interface.
- [x] Visualization module: time-domain I/Q, magnitude/phase, FFT spectrum with
      selectable windows (rect, Hann, Hamming).
- [x] Channel selection module: frequency shift to target station,
      bandpass/lowpass channel filter, then decimation prior to demodulation.
- [x] Decimation/resampling module: explicit rational resampler or FFT-based
      decimation with anti-alias filtering.
- [x] Modulation module (synthetic): create m(t) baseband signals; implement AM
      and FM modulation explicitly for demonstration plots.
- [x] AM demodulation module (real IQ): envelope detection for broadcast AM
      (magnitude + DC removal + LPF); optional coherent/synchronous demod for
      synthetic demos.
- [x] FM demodulation module (real IQ): phase discriminator angle(x[n] _
      x_[n-1]), then LPF, decimation, de-emphasis (50 us option) to audio.
- [x] Noise/impairments module: add AWGN and channel effects; use dataset SNR
      labels when available.
- [x] Concepts demos: Nyquist/aliasing, spectral copies, Gibbs, leakage vs.
      windowing, lowpass in frequency domain.
- [x] Evaluation: compute SNR before/after, spectral comparisons, and export
      figures for report/slides.
- [x] Script structure: clean modular functions with math-focused docstrings;
      single main script to reproduce all plots and figures.

**Decisions**

- Use only NumPy, SciPy, Matplotlib (no black-box SDR libs).
- Separate synthetic modulation demos from real-data demodulation to keep
  explanations clear.
- RadioML is optional and not the main real-data source due to its synthetic
  nature and CC BY-NC-SA 4.0 license.

**Verification**

- Validate IQ ingest by plotting spectra and confirming expected
  bandwidth/structure.
- Confirm AM and FM demod recover baseband signals on synthetic and real data
  when possible.
- Demonstrate windowing tradeoffs and aliasing with clear plots and captions.
- Reproduce key figures consistently via a single script entry point.

---

## Plan: Automatic Modulation Classification (AI Extension)

SVM classifier in `notebooks/classification_panoradio.ipynb`. No separate module files.

### Panoradio HF (`notebooks/classification_panoradio.ipynb`)

- [x] Downloaded Panoradio HF dataset: 18 HF signal classes, 9600 samples
      each, 2048 IQ samples/frame at 6 kHz, Watterson fading channel model.
      Stored at `data/dataset_panoradio_hf.npy` + `dataset_panoradio_hf_tags.csv`.
- [x] Same 8-feature SVM pipeline as RadioML notebook.
- [x] SVM trained: **66.7% test accuracy** on 18 classes (random = 5.6%,
      12× above chance).
- [x] Per-class highlights: MT63 96%, Morse 86.6%, USB 83.7%, AM 80.4%.
- [x] Real-world validation: KiwiSDR 153 kHz AM recording → **26/29 frames
      predict `am` (89.7%)** — validation works due to shared HF channel model.

**Decisions**

- SVM with RBF kernel, scikit-learn only — no deep learning frameworks.
- 8 features: amp variance/kurtosis, phase variance, freq variance/kurtosis,
  spectral symmetry, peak ratio, spectral entropy.
**Verification**

- 66.7% test accuracy on 18 classes, interactive 3D feature space, per-class bars.
- KiwiSDR AM validation: 89.7% frames predict `am`.
