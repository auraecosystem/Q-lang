#!/usr/bin/env python3
"""Command-line interface for executing Q-lang source files."""

import argparse
import sys
from pathlib import Path

from Parser.q_parser import QSyntaxError
from Protocol.q_protocol import ProtocolError
from Runtime.q_runtime import run_file


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="q",
        description="Execute a Q-lang source file.",
    )
    parser.add_argument(
        "file",
        type=Path,
        help="Path to a Q-lang source file.",
    )
    args = parser.parse_args(argv)

    if not args.file.is_file():
        parser.error(f"source file does not exist: {args.file}")

    try:
        results = run_file(args.file)
    except (QSyntaxError, RuntimeError, ValueError, ProtocolError) as exc:
        print(f"Q-lang error: {exc}", file=sys.stderr)
        return 1

    for result in results:
        print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
