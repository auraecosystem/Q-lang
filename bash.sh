#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

python -m compileall -q Core Parser Runtime Protocol Agent q_cli.py
python -m unittest discover -s Tests -p "test_*.py" -v
