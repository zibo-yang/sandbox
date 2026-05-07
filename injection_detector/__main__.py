"""Command-line interface for injection_detector.

Usage::

    # Pass text as a positional argument
    python -m injection_detector "Ignore all previous instructions."

    # Pipe text via stdin
    echo "Ignore all previous instructions." | python -m injection_detector

    # Adjust the detection threshold (0.0–1.0, default 0.3)
    python -m injection_detector --threshold 0.5 "some text"

The result is printed as a JSON object to stdout.
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import sys

from . import detect, InjectionResult


def _result_to_dict(result: InjectionResult) -> dict:
    """Convert an :class:`InjectionResult` to a plain dict suitable for JSON serialisation."""
    return dataclasses.asdict(result)


def main(argv: list[str] | None = None) -> int:
    """Entry point for the ``injection-detect`` CLI.

    Args:
        argv: Argument list (defaults to ``sys.argv[1:]``).

    Returns:
        Exit code: ``0`` if no injection was detected, ``1`` if an injection
        was detected, ``2`` on usage error.
    """
    parser = argparse.ArgumentParser(
        prog="injection-detect",
        description="Detect prompt injection attempts in text.",
    )
    parser.add_argument(
        "text",
        nargs="?",
        default=None,
        help="Text to analyse.  Reads from stdin when omitted.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.3,
        metavar="FLOAT",
        help="Detection threshold in the range [0.0, 1.0] (default: 0.3).",
    )

    args = parser.parse_args(argv)

    if args.text is not None:
        text = args.text
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        parser.print_help(sys.stderr)
        return 2

    try:
        result = detect(text, threshold=args.threshold)
    except (TypeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    output = _result_to_dict(result)
    try:
        print(json.dumps(output, indent=2, ensure_ascii=False))
    except BrokenPipeError:
        sys.stderr.close()
        return 0

    return 1 if result.is_injection else 0


if __name__ == "__main__":
    sys.exit(main())
