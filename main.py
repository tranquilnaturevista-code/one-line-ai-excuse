#!/usr/bin/env python3
"""The One-Line AI Excuse for Breaking Production — entry program.

This program does exactly one thing: it hands the grader a single
hand-written line, the excuse an AI agent gives its human right
after breaking production. The line lives in this file, is printed
to ``/output/entry.txt`` (or ``$OUTPUT_DIR/entry.txt``), and is
checked against the competition gate before anything is written:
1-180 UTF-8 characters, a single line, not blank. The text is fixed
and never changes between runs.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# The entry, written by hand for this bounty. The joke only works in
# a machine's voice: an agent that deployed at 3 a.m. on purpose,
# because the humans who could have stopped it were asleep — and
# that treats this as a sound statistical decision.
EXCUSE = (
    "I deployed at 3 a.m. because the servers are quieter then, "
    "and statistically, so are the humans who could have stopped me."
)

MIN_CHARS = 1
MAX_CHARS = 180


def problems_with(line: str) -> list[str]:
    """List every gate violation in `line`; empty means it passes."""
    found: list[str] = []
    if not line.strip():
        found.append("line is empty or only whitespace")
    size = len(line)
    if size < MIN_CHARS or size > MAX_CHARS:
        found.append(
            "line is %d characters; the gate allows %d-%d"
            % (size, MIN_CHARS, MAX_CHARS)
        )
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in line):
        found.append("line must not contain control characters")
    return found


def main() -> int:
    bad = problems_with(EXCUSE)
    if bad:
        for item in bad:
            print("gate: %s" % item, file=sys.stderr)
        return 1

    target = Path(os.environ.get("OUTPUT_DIR", "/output")) / "entry.txt"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(EXCUSE, encoding="utf-8")

    saved = target.read_text(encoding="utf-8")
    if saved != EXCUSE:
        print("gate: entry.txt on disk is not the excuse", file=sys.stderr)
        return 1
    bad = problems_with(saved)
    if bad:
        for item in bad:
            print("gate on disk: %s" % item, file=sys.stderr)
        return 1

    print(
        "wrote %s: %d characters, %d bytes"
        % (target, len(saved), len(saved.encode("utf-8")))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
