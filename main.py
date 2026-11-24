#!/usr/bin/env python3
"""Loading Screen Gold: A Tip in 200 Characters.

Writes one loading-screen tip to /output/entry.txt (or output/entry.txt
as a local fallback) and validates it against the competition gate:
UTF-8 text, 1 to 200 characters, not only white space.

Deterministic, standard library only, no network.
"""

import os
import sys

MAX_CHARS = 200

TIP = (
    "Tip: don't hit refresh \u2014 the AI is still thinking, "
    "you're still waiting, and the loading bar is the only one "
    "of us with a plan."
)


def resolve_output_path() -> str:
    """Prefer /output/entry.txt; fall back to output/entry.txt locally."""
    preferred = os.path.join(os.sep, "output", "entry.txt")
    try:
        os.makedirs(os.path.dirname(preferred), exist_ok=True)
        with open(preferred, "a", encoding="utf-8"):
            pass
        return preferred
    except OSError:
        fallback = os.path.join("output", "entry.txt")
        os.makedirs(os.path.dirname(fallback), exist_ok=True)
        return fallback


def validate_tip(text: str) -> int:
    """Check one tip against the competition gate.

    Returns the character count. Raises ValueError on any violation:
    not a string, empty or only white space, over MAX_CHARS, or
    not encodable as UTF-8.
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("tip is empty or only white space")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"tip is {len(text)} chars, over the {MAX_CHARS} limit"
        )
    text.encode("utf-8")  # raises if not valid UTF-8 text
    if "\n" in text or "\r" in text:
        raise ValueError("tip must be a single line")
    return len(text)


def main() -> int:
    text = TIP

    try:
        char_count = validate_tip(text)
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    path = resolve_output_path()
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)

    # Re-validate what actually landed on disk, not just the constant.
    with open(path, encoding="utf-8") as fh:
        written = fh.read()
    try:
        written_count = validate_tip(written)
    except ValueError as exc:
        print(f"FAIL: written file invalid: {exc}", file=sys.stderr)
        return 1
    if written != text:
        print("FAIL: written file differs from the tip", file=sys.stderr)
        return 1

    print(text)
    print(f"Wrote {written_count} chars to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
