# Pulling KiwiSDR IQ Data

Wrapper: `scripts/kiwi_fetch_iq.py` → drives `kiwiclient/kiwirecorder.py`.

## Working command (verified)

Run from `project/` directory:

```bash
../.venv/bin/python scripts/kiwi_fetch_iq.py \
  --host kiwisdr.yo3bn.ro --port 8073 \
  --freq 855 --low -6000 --high 6000 \
  --tlimit 5 \
  --out /home/atom/Programming/DSP/project/data/am_855khz
```

Writes `data/am_855khz.wav` (IQ, 2-channel, ~12 kHz sample rate).

## Args

| Flag | Meaning | Notes |
|------|---------|-------|
| `--host` | KiwiSDR address | find public ones at rx.linkfanel.net |
| `--port` | usually `8073` | |
| `--freq` | tune frequency in **kHz** | 855 = MW broadcast |
| `--low` / `--high` | passband cutoffs in Hz | audio filter only — does NOT change IQ rate |
| `--tlimit` | record length in **seconds** | |
| `--out` | output prefix (no extension) | use absolute path; `.wav` appended |

## Gotchas

- **Use an absolute `--out` path.** Relative `../data` resolves wrong from the subprocess cwd → `FileNotFoundError`.
- **One connection per IP.** `KiwiConnectionError: No multiple connections from the same IP address` = close any browser tab / other recorder pointed at the same Kiwi.
- **IQ bandwidth is fixed ~12 kHz (±6 kHz).** `--low/--high` only move the audio filter inside that band; widening them does NOT raise the IQ sample rate. Verified: `-L -10000 -H 10000` still yields sr = 11999 Hz. Multi-channel MW capture needs a wideband SDR (RTL-SDR V3 direct-sampling, Airspy HF+, SDRplay), not KiwiSDR.

## Audio mode (demod on the server)

For a ready-to-play AM WAV instead of raw IQ:

```bash
../.venv/bin/python kiwiclient/kiwirecorder.py \
  -s kiwisdr.yo3bn.ro -p 8073 -f 855 -m am \
  --tlimit 5 --filename /home/atom/Programming/DSP/project/data/am_855khz_audio
```

`-m iq` = raw IQ (notebook §6 demodulates it yourself) · `-m am` = server-side AM audio.
