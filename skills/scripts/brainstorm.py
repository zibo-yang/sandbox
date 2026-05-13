#!/usr/bin/env python3
"""Brainstorm agent: analyze a problem and produce a structured markdown
document with Overall Insight + Subproblem Decomposition + Integration Sketch.

Uses a dedicated prompt (BRAINSTORM_PROMPT in prompts.py) that forces the
output format, so downstream tools can parse subproblems by section heading.
"""

import argparse
import importlib
from prompts import BRAINSTORM_PROMPT


def brainstorm(problem, model="openai", feedback=None):
    api = importlib.import_module("api_google" if model == "gemini" else "api_oai")
    # BRAINSTORM_PROMPT contains template placeholders like {N}, {short title},
    # and TeX with braces — str.format() would try to parse all of them and
    # raise KeyError. Use literal replace for the single {problem} slot.
    prompt = BRAINSTORM_PROMPT.replace("{problem}", problem)
    if feedback:
        prompt += (
            "\n\n### Previous Attempt Was Rejected ###\n"
            "The logic_verifier reviewed your previous decomposition and "
            "flagged these issues:\n\n"
            + feedback
            + "\n\nProduce a revised decomposition that directly addresses "
            "each issue listed above. Keep the same structured markdown format."
        )
    return api.call_llm("", prompt)


def main():
    parser = argparse.ArgumentParser(
        description="Brainstorm and decompose a math problem into 2-6 subproblems"
    )
    parser.add_argument("problem_file", help="Path to file containing the problem")
    parser.add_argument("--model", choices=["gemini", "openai"], default="openai")
    parser.add_argument("--feedback", help="Path to logic_verifier feedback file (triggers revision mode)")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    args = parser.parse_args()

    with open(args.problem_file, "r") as f:
        problem = f.read()

    feedback = None
    if args.feedback:
        with open(args.feedback, "r") as f:
            feedback = f.read()

    result = brainstorm(problem, model=args.model, feedback=feedback)

    if result is None:
        print("Error: API call failed.")
        return

    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
        print(f"Brainstorm written to {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
