# Reasoning Tools

A collection of sub-agents to assist with mathematical reasoning, including solution generation, verification, and iterative improvement.

**IMPORTANT: Input quality matters.** When calling any tool, describe the problem, conditions, and context precisely and rigorously. Vague or incomplete inputs lead to vague or incorrect outputs. State all assumptions, include relevant definitions, and specify exactly what you need. The tools are only as good as the prompts you give them.

**IMPORTANT: Long-running tasks.** These tools can take up to 30 minutes for hard problems. Always use `-o` to write results to a file and run in background mode (`run_in_background: true`). Do NOT wait synchronously — launch the task in background and continue with other work while it completes.

## Generator

Generate a solution for a math problem. Tip: explicitly request LaTeX output in the problem file if you need compilable `.tex`, otherwise you may get markdown.

```bash
python skills/scripts/generator.py <problem_file> [--model gemini|openai] [-o output_file]
```

| Argument | Required | Description |
|----------|----------|-------------|
| `problem_file` | Yes | Path to file containing the problem statement |
| `--model` | No | `gemini` or `openai` (default: `openai`) |
| `-o` | No | Output file path (default: stdout) |

## Proof Verifier

Verify a solution's correctness step by step and produce a bug report. The verifier is thorough and reliable — take its findings seriously. Every flagged issue should be addressed. Verify each section independently first, then verify the full assembled proof end-to-end.

```bash
python skills/scripts/proof_verifier.py <problem_file> <solution_file> [-o output_file]
```

| Argument | Required | Description |
|----------|----------|-------------|
| `problem_file` | Yes | Path to file containing the problem statement |
| `solution_file` | Yes | Path to file containing the solution |
| `-o` | No | Output file path (default: stdout) |

## Logic Verifier

Verify the logical structure of a proof plan — checks whether solving the subproblems actually resolves the original problem, without checking individual proof correctness. Use this right after decomposing a problem, before spending tokens on solving subproblems.

```bash
python skills/scripts/logic_verifier.py <problem_file> <outline_file> [--model gemini|openai] [-o output_file]
```

| Argument | Required | Description |
|----------|----------|-------------|
| `problem_file` | Yes | Path to file containing the problem statement |
| `outline_file` | Yes | Path to file containing the proof outline (list of subproblems/lemmas) |
| `--model` | No | `gemini` or `openai` (default: `openai`) |
| `-o` | No | Output file path (default: stdout) |

## Improver

Improve a solution based on a bug report. The improver's output must still be verified — always run `proof_verifier` on the result (see the Generate-Verify-Improve Loop in `reasoning_strategies.md`).

```bash
python skills/scripts/improver.py <problem_file> <solution_file> <bug_report_file> [--model gemini|openai] [-o output_file]
```

| Argument | Required | Description |
|----------|----------|-------------|
| `problem_file` | Yes | Path to file containing the problem statement |
| `solution_file` | Yes | Path to file containing the solution |
| `bug_report_file` | Yes | Path to file containing the bug report |
| `--model` | No | `gemini` or `openai` (default: `openai`) |
| `-o` | No | Output file path (default: stdout) |

## Reasoning Assistant

General-purpose LLM query for any reasoning task — subproblem decomposition, strategy decisions, brainstorming, literature investigation, or any other question. Use `-c` to pass context files (e.g., existing lemmas, the problem statement) — this significantly improves output quality.

```bash
# Ask a question with problem file as context
python skills/scripts/reasoning_assistant.py "What proof strategy should I use?" -c problem.txt

# Both question and context from files
python skills/scripts/reasoning_assistant.py question.txt -f -c problem.txt
```

| Argument | Required | Description |
|----------|----------|-------------|
| `question` | Yes | The question string, or file path if `-f` is used |
| `-f` | No | Read question from file instead of string |
| `-c` / `--context` | No | Context file to provide background |
| `--model` | No | `gemini` or `openai` (default: `openai`) |
| `-o` | No | Output file path (default: stdout) |

## Matlas Search

Search the [matlas.ai](https://matlas.ai) mathematical literature database for theorems, lemmas, definitions, and examples. Results include source title, authors, journal, year, DOI, and the mathematical statement (often with inline LaTeX). Save results to JSONL for later reference. Use this to look up known results, find related work, or gather citations before proving.

\`\`\`bash
# Search and save to file (append mode — safe to call multiple times)
python skills/scripts/matlas_search.py "Kakeya conjecture" -n 20 -o proof/references.jsonl

# Search and print to stdout
python skills/scripts/matlas_search.py "irrationality of sqrt 2" -n 10

# Read saved results
python skills/scripts/matlas_search.py --read proof/references.jsonl

# Read and filter by query substring
python skills/scripts/matlas_search.py --read proof/references.jsonl --query "Kakeya"
\`\`\`

| Argument | Required | Description |
|----------|----------|-------------|
| \`query\` | Yes (search mode) | Search query string |
| \`-n\` | No | Number of results, 10-200 (default: 10) |
| \`-o\` | No | Output JSONL file (append mode, creates parent dirs) |
| \`--read\` | No | Read mode: path to existing .jsonl file to display |
| \`--query\` | No | Filter \\--read results by query substring |

