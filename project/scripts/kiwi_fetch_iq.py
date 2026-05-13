"""Fetch KiwiSDR IQ data using kiwirecorder.py from the kiwiclient repo."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def _find_kiwirecorder(explicit_path: str | None) -> Path:
    if explicit_path:
        return Path(explicit_path).expanduser().resolve()

    project_root = Path(__file__).resolve().parents[1]
    repo_paths = [
        (project_root / "kiwiclient/kiwirecorder.py").resolve(),
        Path("./kiwiclient/kiwirecorder.py").resolve(),
        Path("../kiwiclient/kiwirecorder.py").resolve(),
    ]
    for repo_path in repo_paths:
        if repo_path.exists():
            return repo_path

    found = shutil.which("kiwirecorder.py")
    if found:
        return Path(found).resolve()

    raise FileNotFoundError(
        "kiwirecorder.py not found. Clone https://github.com/jks-prv/kiwiclient "
        "or pass --kiwirecorder-path."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Record KiwiSDR IQ samples.")
    parser.add_argument("--host", required=True, help="KiwiSDR host")
    parser.add_argument("--port", type=int, default=8073)
    parser.add_argument("--freq", type=float, required=True, help="Frequency in kHz")
    parser.add_argument("--tlimit", type=int, default=30, help="Seconds to record")
    parser.add_argument("--low", type=int, default=-5000, help="Low cutoff (Hz)")
    parser.add_argument("--high", type=int, default=5000, help="High cutoff (Hz)")
    parser.add_argument("--out", required=True, help="Output filename prefix")
    parser.add_argument("--kiwirecorder-path", default=None)
    args = parser.parse_args()

    try:
        kiwirecorder = _find_kiwirecorder(args.kiwirecorder_path)
    except FileNotFoundError as exc:
        print(str(exc))
        return 2

    cmd = [
        sys.executable,
        str(kiwirecorder),
        "-s",
        args.host,
        "-p",
        str(args.port),
        "-f",
        str(args.freq),
        "-m",
        "iq",
        "-L",
        str(args.low),
        "-H",
        str(args.high),
        "--tlimit",
        str(args.tlimit),
        "--filename",
        args.out,
    ]

    print("Running:", " ".join(cmd))
    result = subprocess.run(cmd)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
