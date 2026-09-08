#!/usr/bin/env python3
"""Q-lang command-line interface."""
import argparse
from Runtime.q_runtime import run_file


def main():
    parser = argparse.ArgumentParser(prog="q", description="Q-lang Universal Semantic Language")
    parser.add_argument("file", help="Q-lang source file (.q)")
    args = parser.parse_args()
    run_file(args.file)


if __name__ == "__main__":
    main()
