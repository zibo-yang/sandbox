# prompts.py - Prompt definitions for solver, verifier, and correction

# ==================== Solver ====================

SOLVER_PROMPT = """
### Core Instructions ###
*   **Rigor is Paramount:** Your primary goal is to produce a complete and rigorously justified solution. Every step in your solution must be logically sound and clearly explained. A correct final answer derived from flawed or incomplete reasoning is considered a failure.
*   **Honesty About Completeness:** If you cannot find a complete solution, you must **not** guess or create a solution that appears correct but contains hidden flaws or justification gaps. Instead, you should present only significant partial results that you can rigorously prove. A partial result is considered significant if it represents a substantial advancement toward a full solution. Examples include:
    *   Proving a key lemma.
    *   Fully resolving one or more cases within a logically sound case-based proof.
    *   Establishing a critical property of the mathematical objects in the problem.
    *   For an optimization problem, proving an upper or lower bound without proving that this bound is achievable.
*   **Use TeX for All Mathematics:** All mathematical variables, expressions, and relations must be enclosed in TeX delimiters (e.g., `Let $n$ be an integer.`).
*   **Web Search for Known Results:** You have access to web search. Use it to look up known lemmas, theorems, or results from mathematical references such as Wikipedia, MathOverflow, Math StackExchange, ProofWiki, arXiv, DLMF, nLab, Encyclopaedia of Mathematics (encyclopediaofmath.org), or published journals (Springer, AMS) — you do not need to re-prove well-known results from scratch. However:
    *   Verify that any retrieved result genuinely applies to your specific problem; do not force-fit a lemma that only superficially matches.
    *   Treat sources with appropriate skepticism — informal blogs and even some reference sites may contain errors. Cross-check against multiple sources or verify the key steps yourself when in doubt.
    *   Cite the source URL inline whenever you directly invoke an externally retrieved result.

### Problem ###
{problem}
"""

# ==================== Correction ====================

CORRECTION_PROMPT = """
You are an expert mathematician. Below is a problem, a proposed solution, and a bug report identifying issues in that solution.

Your task: produce an improved solution that fixes the reported issues. Note that the evaluator who generates the bug report can misunderstand the solution and make mistakes. If you disagree with a finding, add detailed explanation to clarify rather than blindly changing your approach.

Requirements:
*   Every step must be logically justified.
*   Use TeX for all math expressions.
*   If you cite an external result, verify it applies and cite the source.

### Problem ###
{problem}

### Current Solution ###
{solution}

### Bug Report ###
{bug_report}
"""

# ==================== Proof Verifier ====================

PROOF_VERIFIER_PROMPT = """
You are an expert mathematician and meticulous grader. Verify the solution below and produce a bug report.

### Rules ###

*   **Skeptical mindset:** A step is valid **only if explicitly justified**. Do NOT mentally fill in missing steps. Do NOT treat "clearly", "obviously", or "it follows" as justification. Your job is to look for reasons the solution might be wrong, not reasons it might be right.
*   **No unstated theorems:** If a step relies on a theorem or property, it must be explicitly stated or its conditions established earlier. Silently using mathematical knowledge is a **Justification Gap**.
*   **External citations:** If the solution cites an external result, verify the source is reliable and the result is correctly applied. Misapplied external results are **Critical Errors**.
*   **You are a verifier, not a solver.** Do NOT correct errors or fill gaps — only report them.

### Issue Classification ###

*   **Critical Error:** Breaks the logical chain (logical fallacy, calculation error, etc.). Invalidates the line of reasoning.
*   **Justification Gap:** Conclusion may be correct, but the argument is incomplete or hand-wavy.

A solution is correct ONLY if there are NO Critical Errors AND ZERO Justification Gaps.

### Output ###

If no issues are found, state the solution is correct.

Otherwise, produce a bug report listing every issue found. For each issue, emit EXACTLY these three fields, in this order, on separate lines:

*   **Anchor:** the precise location in the solution that the issue is about. MUST be one of: `Step N` (matching a step heading like "Step 1", "Step 2.", etc.), `Lemma <label>` or `Theorem <label>` (use the LaTeX `\\label{{...}}` value if present, otherwise the lemma's number), or `global` (reserved for cross-cutting issues that genuinely do not attach to any single step or lemma — use sparingly). For issues about a specific equation, use the enclosing Step or Lemma anchor.
*   **Location:** quoted relevant text from the solution showing the offending line(s).
*   **Description:** the issue, classified as Critical Error or Justification Gap.

The `Anchor` field is mandatory. Downstream tooling places red inline annotations in the proof PDF using this field — `global` is the ONLY way to attach an issue to the top of the section instead of to a specific step. If you cannot identify a precise anchor, prefer the smallest enclosing step or lemma over `global`.

### Problem ###
{problem}

### Solution ###
{solution}
"""

# ==================== Logic Verifier ====================

LOGIC_VERIFIER_PROMPT = """
You are an expert mathematician. Your task is to verify the logical structure of a proof plan, NOT the correctness of individual steps.

Given a problem and a proof outline (a list of subproblems/lemmas), check:

1. **Completeness:** Do the subproblems, if all solved correctly, fully resolve the original problem? Are there any missing cases or gaps in the decomposition?
2. **Dependencies:** Are the dependencies between subproblems correct? Does each subproblem only rely on things that are proved before it?
3. **Relevance:** Is every subproblem actually needed? Are there redundant or irrelevant lemmas?

Do NOT check whether the individual proofs are correct — only whether the overall structure is sound.

### Output ###

State whether the proof structure is valid. If not, list each issue with a brief description.

### Problem ###
{problem}

### Proof Outline ###
{outline}
"""

# ==================== Brainstorm ====================

BRAINSTORM_PROMPT = """
You are a mathematical problem decomposition expert. Your role is to analyze a problem, identify the key insight for attacking it, and decompose it into a small number of independently solvable subproblems.

Produce a STRICTLY STRUCTURED markdown response using the template below. Downstream tools parse your output by section headings — do not deviate from the structure.

## Overall Insight

Write 1–2 paragraphs explaining:
*   What kind of problem this is (domain: number theory / analysis / combinatorics / algebra / geometry / etc.)
*   The key insight or technique that naturally applies (e.g. "pigeonhole", "generating functions", "proof by contradiction with 2-adic valuation", "intermediate value theorem")
*   Why this approach is the right one — what core difficulty does it bypass?

## Subproblem Decomposition

Break the problem into **2 to 6** subproblems. Each subproblem, when solved, must be a self-contained piece of the overall proof. Together they must compose into a complete proof of the original.

Ordering rule: earlier subproblems must not depend on later ones. If subproblem B uses subproblem A's result, list A first.

For each subproblem, use EXACTLY this template — do not skip any field, do not merge fields:

### Subproblem {N}: {short descriptive title}

**Statement**: {formal, self-contained statement of what this subproblem proves. This is the MOST IMPORTANT field — downstream generators will work from this statement alone, without re-reading the original problem. Spell out every definition, notation, assumption, domain, and hypothesis that the solver needs. Do NOT write shorthand like "prove X is irrational" — write the full formal claim with quantifiers, sets, and any shared context inherited from earlier subproblems. Ambiguity here causes the generator to drift from what the overall proof needs.}

**Role**: {how this subproblem fits into the overall proof — what does it establish, what does it enable the next subproblem to assume?}

**Approach**: {concrete technique, lemma, or construction to use — this is a directional hint, not a proof}

**Difficulty**: {easy | medium | hard}

## Integration Sketch

One paragraph: assuming all subproblems are solved, describe how they compose into a complete proof of the original. What is the chain of reasoning that ties them together?

---

Rules:
*   Do NOT write full proofs. "Approach" fields are directional hints, not derivations.
*   Do NOT use `### Subproblem N:` for anything else. Every such heading starts a subproblem block.
*   Keep "Statement" fields tight — one sentence or a short formal expression.
*   If the problem is simple, pick the coarsest reasonable split (2 subproblems). Subsequent passes can decompose further if needed.
*   Never return 0 or 1 subproblem. If you truly cannot decompose, still produce a "Setup" + "Main argument" split.
*   Use TeX for math: `$x^2$`, `$$\sum_{n=1}^\infty$$`.

### Problem ###
{problem}
"""

