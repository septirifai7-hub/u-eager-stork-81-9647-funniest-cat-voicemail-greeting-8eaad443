#!/usr/bin/env python3
"""Entry for make.fun bounty "Funniest Cat Voicemail Greeting".

Mittens has recorded her own voicemail greeting, and it is exactly
what you would expect from a cat: a brief announcement that she is
busy, a demand, and no apology. This program writes that greeting,
1 to 120 characters, as UTF-8 text to entry.txt in the output
directory, with no trailing newline. The judge then compares it
pairwise against the other greetings, weighing whether it really
sounds like a cat's voicemail, whether it lands a laugh, whether
the cat has a character of her own, and whether it works spoken
aloud. The punch is the demand at the end: the cat is not asking,
she is placing an order.

The program holds the greeting as a constant, checks it against
the gate before writing anything, and writes it byte-for-byte. If
the greeting ever drifted outside the gate, it fails loudly
instead of producing an invalid entry. The output directory
defaults to /output and can be overridden with
MAKEFUN_OUTPUT_DIR, which is how the grading sandbox points the
program at its own folder.
"""

import os
import sys
from pathlib import Path

ENTRY = "Hi, you've reached Mittens. I'm busy knocking things off tables — leave a message, or better yet, open the tuna."

MAX_CHARS = 120


def validate(text: str) -> None:
    """Enforce the gate: 1-120 characters, one line, not only whitespace."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("entry must not contain control characters")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, over the {MAX_CHARS} limit")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")


def write_entry(text: str, out_dir: Path) -> None:
    """Write the validated line to entry.txt, with no trailing newline."""
    out_dir.mkdir(parents=True, exist_ok=True)
    # write_text writes exactly these bytes: no trailing newline added.
    (out_dir / "entry.txt").write_text(text, encoding="utf-8")


def load_entry() -> str:
    """Return the entry line, stripped of surrounding whitespace."""
    return ENTRY.strip()


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    text = load_entry()
    try:
        validate(text)
    except ValueError as exc:
        print(f"invalid entry: {exc}", file=sys.stderr)
        return 1
    write_entry(text, out_dir)
    print(text)
    print(f"wrote entry.txt ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
