#!/usr/bin/env python3
"""Reasoning assistant: general-purpose LLM query for any reasoning task."""

import argparse
import importlib


def ask(question, context=None, model="openai"):
    api = importlib.import_module("api_google" if model == "gemini" else "api_oai")
    prompt = question
    if context:
        prompt = f"{context}\n\n{question}"
    return api.call_llm("", prompt)


def main():
    parser = argparse.ArgumentParser(description="Ask LLM any reasoning question")
    parser.add_argument("question", help="The question to ask (string or file path)")
    parser.add_argument("--context", "-c", help="Optional context file")
    parser.add_argument("--model", choices=["gemini", "openai"], default="openai")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    parser.add_argument("--file", "-f", action="store_true", help="Read question from file instead of string")
    args = parser.parse_args()

    if args.file:
        with open(args.question, "r") as f:
            question = f.read()
    else:
        question = args.question

    context = None
    if args.context:
        with open(args.context, "r") as f:
            context = f.read()

    result = ask(question, context=context, model=args.model)

    if result is None:
        print("Error: API call failed.")
        return

    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
        print(f"Response written to {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
