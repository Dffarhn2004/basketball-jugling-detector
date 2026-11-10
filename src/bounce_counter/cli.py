"""Command-line interface for the project skeleton."""

from __future__ import annotations

import argparse
import importlib.util
import platform
import shutil
import sys


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="bounce_counter")
    subparsers = parser.add_subparsers(dest="command")
    doctor = subparsers.add_parser("doctor", help="report local environment availability")
    doctor.add_argument("--json", action="store_true", help="emit JSON-like machine-readable output")
    for name in ("video-info", "extract-frames", "validate-data", "detect", "train", "track", "count", "evaluate", "render"):
        command = subparsers.add_parser(name, help=f"Phase 0 stub for {name}")
        command.add_argument("--config", help="configuration path")
        command.add_argument("--input", help="input path")
        command.add_argument("--output", help="output path")
        command.add_argument("--run-id", help="run identifier")
    return parser


def doctor() -> int:
    print(f"python={sys.version.split()[0]}")
    print(f"platform={platform.platform()}")
    for package in ("torch", "ultralytics", "cv2", "yaml", "pytest"):
        available = importlib.util.find_spec(package) is not None
        print(f"{package}={'available' if available else 'missing'}")
    print(f"ffmpeg={'available' if shutil.which('ffmpeg') else 'missing'}")
    try:
        import torch
        print(f"torch_device={'cuda' if torch.cuda.is_available() else 'cpu'}")
    except ImportError:
        print("torch_device=unknown (torch missing)")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "doctor":
        return doctor()
    if args.command:
        print(f"{args.command}: not implemented in Phase 0; no data or model operation performed")
        return 0
    build_parser().print_help()
    return 0
