#!/usr/bin/env python3
"""Improver agent: reads a problem, solution, and bug report, produces an improved solution."""

import argparse
import importlib
from prompts import CORRECTION_PROMPT


def improve(problem, solution, bug_report, model="openai"):
    api = importlib.import_module("api_google" if model == "gemini" else "api_oai")
    prompt = CORRECTION_PROMPT.format(problem=problem, solution=solution, bug_report=bug_report)
    return api.call_llm("", prompt)


def main():
    parser = argparse.ArgumentParser(description="Improve a solution based on a bug report")
    parser.add_argument("problem_file", help="Path to file containing the problem statement")
    parser.add_argument("solution_file", help="Path to file containing the solution")
    parser.add_argument("bug_report_file", help="Path to file containing the bug report")
    parser.add_argument("--model", choices=["gemini", "openai"], default="openai")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    args = parser.parse_args()

    with open(args.problem_file, "r") as f:
        problem = f.read()
    with open(args.solution_file, "r") as f:
        solution = f.read()
    with open(args.bug_report_file, "r") as f:
        bug_report = f.read()

    result = improve(problem, solution, bug_report, model=args.model)

    if result is None:
        print("Error: API call failed.")
        return

    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
        print(f"Improved solution written to {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
