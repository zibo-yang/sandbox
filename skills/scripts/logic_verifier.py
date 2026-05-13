#!/usr/bin/env python3
"""Logic verifier agent: checks if the proof structure is sound."""

import argparse
import importlib
from prompts import LOGIC_VERIFIER_PROMPT


def verify_logic(problem, outline):
    import api_oai as api
    prompt = LOGIC_VERIFIER_PROMPT.format(problem=problem, outline=outline)
    return api.call_llm("", prompt)


def main():
    parser = argparse.ArgumentParser(description="Verify the logical structure of a proof plan")
    parser.add_argument("problem_file", help="Path to file containing the problem statement")
    parser.add_argument("outline_file", help="Path to file containing the proof outline")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    args = parser.parse_args()

    with open(args.problem_file, "r") as f:
        problem = f.read()
    with open(args.outline_file, "r") as f:
        outline = f.read()

    result = verify_logic(problem, outline)

    if result is None:
        print("Error: API call failed.")
        return

    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
        print(f"Logic verification written to {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
