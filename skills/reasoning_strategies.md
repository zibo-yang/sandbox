# Reasoning Strategies

Guidelines for composing reasoning tools into effective proof workflows. Organized by phase.

---

## Phase 1: Exploration — Figuring Out the Approach

Use these strategies when you don't yet have a solution and need to find the right direction.

### Brainstorming

```
reasoning_assistant ×N (multiple models) → compare ideas → pick direction
```

**When to use:** The problem is hard and you don't know where to start, or the generator keeps going down the wrong path. Also useful for investigating related literature and known results.

**Flow:**
1. Use **reasoning_assistant** to sample proof sketches and ideas from different models (`--model openai` and `--model gemini`), multiple times. No full solutions needed — just high-level directions and key insights.
2. Compare and critique the ideas to identify the most promising approach.
3. Once a direction emerges, feed it to the **generator** as context in the problem file to produce a full solution.

### Divide and Verify

```
decompose → logic_verifier → solve each piece → verify each → assemble → verify whole
```

**When to use:** The problem is too large or complex for the generator to solve in one shot. Also use when the generator produces incomplete or fundamentally flawed solutions.

**Flow:**
1. Decompose the proof into subproblems. Run **logic_verifier** to confirm the decomposition is sound — i.e., solving these subproblems actually resolves the original problem.
2. Once the structure passes, use **generator** to solve each subproblem individually.
3. Run **proof_verifier** on each subproblem's proof to check correctness.
4. Run **improver** only on the failed sections.
5. Re-verify the fixed sections with **proof_verifier**.
6. Once all sections pass, run **proof_verifier** on the full assembled proof end-to-end.

---

## Phase 2: Generation — Producing Solutions

Use these strategies when generating candidate solutions for a (sub)problem.

### Best-of-N (initial generation)

```
generator ×N (different models) → verifier ×N → pick best or merge
```

**When to use:** The problem is hard and you want to explore multiple proof strategies in parallel rather than committing to one.

**Flow:**
1. Run **generator** N times (e.g., N=2–3) using different models (`--model gemini` and `--model openai`) to increase diversity.
2. Run **verifier** on each candidate.
3. Use the **verifier**'s bug reports to judge which solution is best and what problems each one has.
4. Either pick the best solution, or merge the strengths of multiple solutions — e.g., take the best lemma from solution A and the cleaner main argument from solution B.
5. Optionally feed the result into a Generate-Verify-Improve Loop.

---

## Phase 3: Iteration — Fixing and Improving

Use these strategies when you have a solution that needs to be refined.

### Generate-Verify-Improve Loop

```
generator → verifier → improver → verifier → ... (until clean or max iterations)
```

**When to use:** The default strategy. The initial solution from the generator is roughly on the right track, and you want to iteratively refine it.

**Watch out:** If the loop is not making progress after 3 rounds (e.g., the same issues keep appearing), stop looping. Either re-generate a fresh solution with the generator, or decompose the problem into smaller subproblems. Do not waste tokens going in circles on a bad initial solution.

**Flow:**
1. Run **generator** to produce an initial solution.
2. Run **proof_verifier** to produce a bug report.
3. If the bug report says the solution is correct, stop.
4. Otherwise, run **improver** with the solution and bug report to produce a refined solution.
5. Go back to step 2 with the refined solution.
6. Set a max iteration limit (3–5 rounds) to avoid infinite loops.

### Partial Acceptance

```
solution partially wrong → extract correct parts → save and reuse → re-generate broken parts
```

**When to use:** A solution is not fully correct, but parts are valuable — correct lemmas, valid computations, sound case analysis. Don't discard good work.

**Flow:**
1. Run **proof_verifier** on the full solution.
2. Save the correct parts into `.tex` section files. Mark broken parts with `\textcolor{red}{TODO:}`.
3. Only re-generate or improve the broken parts — keep everything that already works.

### Fresh Restart + Merge

```
loop not converging → generator from scratch → merge with old good parts
```

**When to use:** The improve loop has stalled (3+ rounds, same issues recurring). The solution needs a fundamentally different approach, not incremental fixes.

**Flow:**
1. Save verified parts from the old solution.
2. Run **generator** from scratch on the problematic subproblem (possibly with a different approach hint in the problem file).
3. Merge the new solution's strengths with the old verified parts.

---

## Phase 4: Verification — Confirming Correctness

Use these strategies to gain confidence that the proof is actually correct.

### Pessimistic Verification

```
proof_verifier ×N (multiple OpenAI runs) → any failure = proof is wrong
```

**When to use:** When you need high confidence that a proof is correct. A single verifier call can miss issues — multiple runs catch issues from sampling variance.

**Flow:**
1. Run **proof_verifier** multiple times (e.g., 2–3 runs) on the same proof. The verifier is OpenAI-only; do not substitute Gemini.
2. If **any** run reports an issue, treat the proof as incorrect.
3. Feed the bug reports into the **improver** and repeat.

### Final Verification

```
all sections pass → assemble full proof → proof_verifier on the whole thing
```

**When to use:** Always, as the last step. Even if every subproblem has individually passed verification, you must still run **proof_verifier** on the complete assembled proof before declaring it done. Individual sections may be correct on their own but fail to connect properly. This is your last line of defense. Combine with Pessimistic Verification for extra confidence.
