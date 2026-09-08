#!/usr/bin/env python3
"""Q-lang command line launcher."""
import sys
from Runtime.q_runtime import run_file

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./q <file.q>", file=sys.stderr)
        raise SystemExit(2)
    run_file(sys.argv[1])
