#!/usr/bin/env python3
"""Generator agent: reads a problem and produces a solution."""

import argparse
import importlib
from prompts import SOLVER_PROMPT


def generate(problem, model="openai"):
    api = importlib.import_module("api_google" if model == "gemini" else "api_oai")
    prompt = SOLVER_PROMPT.format(problem=problem)
    return api.call_llm("", prompt)


def main():
    parser = argparse.ArgumentParser(description="Generate a solution for a math problem")
    parser.add_argument("problem_file", help="Path to file containing the problem statement")
    parser.add_argument("--model", choices=["gemini", "openai"], default="openai")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    args = parser.parse_args()

    with open(args.problem_file, "r") as f:
        problem = f.read()

    result = generate(problem, model=args.model)

    if result is None:
        print("Error: API call failed.")
        return

    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
        print(f"Solution written to {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
