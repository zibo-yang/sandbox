# Experience

Practical experience distilled from past proving sessions. Each entry is general-purpose (not problem-specific) and has been validated in practice. When you discover a new general-purpose technique that works well, add it here.

---

## Parallel Launches

**When:** Generating or verifying — any time you call a reasoning tool.

**How:** For tools that support `--model` (generator, reasoning_assistant), launch with both `--model openai` and `--model gemini` simultaneously. Most effective patterns:
- Generator: best-of-2 with both models
- Brainstorming: diverse ideas from both models

---

## Numerical Verification with Python

**When:** You suspect a claimed result is wrong, need to check a specific value, or want to explore a parameter space before committing to a proof approach.

**How:** Use Python with `mpmath` (arbitrary precision) to:
- Check matrix rank at specific parameter values
- Verify that a claimed root/solution actually satisfies the equation
- Scan parameter grids to find or rule out solutions
- Confirm algebraic identities to 50+ digits

Numerical checks are not proofs, but they reveal errors early and guide the proof strategy.

---

## Escape Plateaus by Decomposing

**When:** The verify → fix → re-verify loop is not converging (3+ rounds, same issues keep reappearing or new issues replace old ones).

**How:** The section is too large for the improver to fix coherently. Decompose it into smaller `.tex` files, verify each independently, then reassemble. Smaller pieces converge faster.

---

## Verifier Annotations Are User-Facing

**When:** Every time `proof_verifier` returns ISSUES_FOUND.

**How:** The `\verifierissue{...}` annotations you insert into section files are not internal scratch notes — they appear inline in red in the PDF the user reads in the Reports panel. They are the user's primary signal of *where* and *why* a section is currently failing. Place each one at the anchor the verifier names; getting the location wrong is worse than not annotating at all (the user reads "Step 4 has a problem" while staring at Step 1 and loses trust). Treat them like commit messages: precise, faithful to the verifier's actual finding, and short enough to read at a glance. Don't soften, paraphrase, or bundle issues. And don't leave stale annotations on a section that has since passed CLEAN — the user will think the proof is in worse shape than it is.

---

## Improver Output May Need Format Conversion

**When:** The improver returns raw markdown instead of compilable LaTeX.

**How:** Either:
- Write a problem file containing the markdown and ask the **generator** to convert it to LaTeX, or
- Use the improved content as reference and incorporate key fixes into your existing `.tex` file via the generator.
