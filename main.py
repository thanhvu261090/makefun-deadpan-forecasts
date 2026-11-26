#!/usr/bin/env python3
"""Deadpan forecast for a city that does not exist.

Writes one line, at most 160 characters, to /output/entry.txt.
"""

import argparse
import os
import sys

ENTRY = (
    "In Port Unlikely, expect 11 mm of sideways rain, winds of 40 km/h "
    "from the northeast, and a 90% chance the sea politely declines to arrive."
)


def validate(text):
    """Return True only if text is a valid gate entry: 1-160 chars, not blank."""
    if not isinstance(text, str):
        return False
    if not text.strip():
        return False
    if "\n" in text or "\r" in text:
        return False
    if text != text.strip():
        return False
    return 1 <= len(text) <= 160


def write_entry(text, path):
    """Write the single-line entry to path, with a trailing newline."""
    if not validate(text):
        raise ValueError("entry failed validation")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text + "\n")
    return path


def describe(text):
    """One-line summary of the entry for logs."""
    return "deadpan forecast: %d chars for Port Unlikely" % len(text)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Write the deadpan forecast entry.")
    parser.add_argument("--self-test", action="store_true",
                        help="validate the entry and exit 0 on success")
    parser.add_argument("--out", default=None,
                        help="output path (default: $MAKEFUN_OUTPUT_DIR/entry.txt)")
    args = parser.parse_args(argv)

    if args.self_test:
        ok = validate(ENTRY)
        print(describe(ENTRY))
        print("self-test: %s" % ("PASS" if ok else "FAIL"))
        return 0 if ok else 1

    if not validate(ENTRY):
        print("entry failed validation", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = args.out or os.path.join(out_dir, "entry.txt")
    write_entry(ENTRY, path)
    print(describe(ENTRY))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
