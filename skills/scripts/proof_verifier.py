#!/usr/bin/env python3
"""Verifier agent: reads a problem and solution, produces a bug report."""

import argparse
import importlib
from prompts import PROOF_VERIFIER_PROMPT


def verify(problem, solution):
    import api_oai as api
    prompt = PROOF_VERIFIER_PROMPT.format(problem=problem, solution=solution)
    return api.call_llm("", prompt)


def main():
    parser = argparse.ArgumentParser(description="Verify a solution and produce a bug report")
    parser.add_argument("problem_file", help="Path to file containing the problem statement")
    parser.add_argument("solution_file", help="Path to file containing the solution")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    args = parser.parse_args()

    with open(args.problem_file, "r") as f:
        problem = f.read()
    with open(args.solution_file, "r") as f:
        solution = f.read()

    result = verify(problem, solution)

    if result is None:
        print("Error: API call failed.")
        return

    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
        print(f"Bug report written to {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
