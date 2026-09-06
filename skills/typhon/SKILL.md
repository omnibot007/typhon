---
name: typhon
description: Force wild alternatives and outside-box thinking with a bounded divergence engine. Names the modal answer, tail-samples structurally distinct candidates, dedupes against a novelty archive, breeds distant hybrids, verifies adversarially, selects rare-and-good. Use when the user says be creative, think outside the box, wild ideas, innovate, surprise me, brainstorm, diverge, or invokes typhon.
argument-hint: [the problem to set on fire]
effort: max
---

# /typhon -- The Divergence Engine (thinking lives in the loop)

Run the divergence loop; do not promise that novelty wins.
Mission: $ARGUMENTS
Respect host permissions. Ideation may use approved scratch JSON and reviewed
helper execution; never modify the target project without a commissioned build.
Persistent playbook writes need separate authorization. If execution is unavailable,
continue as a clearly labeled UNVERIFIED proposal; never invent gate results.
Resolve this skill's absolute directory before invoking its bundled Python files.

Credit: engine adapted from `SritejBommaraju/divergent-agents` (MIT, 2026).
Bundled `novelty.py`, `diff_test.py`, `modes.json`, and `learn.py` derive from that project.
On-top additions (grader verify, cheap-model mapping, ledger archive, stakes gate,
router wiring) are ours. Preserve all MIT notices and upstream attribution.
Full method: https://github.com/SritejBommaraju/divergent-agents/blob/main/METHOD.md

Evidence scope: the maintainer reports reproducing upstream DAT p=0.84
(within-response prompting comparison) and +0.229 (archive population spread).
These do not establish a universal prompting null, code quality, or this 0.5 gate.
The full TYPHON workflow and upstream ~9x/~28x claims are not locally validated here.

## LAW 0 -- THE STAKES GATE (fire costs; matches are free)

Trivial task: take the direct gate; do not manufacture a slate. Otherwise use the engine.
Keep user constraints and plugin settings intact. Constraint-removal lenses are
counterfactuals, not permission to violate the final requirements or add dependencies.
Conventionality probabilities are uncalibrated self-estimates, not measured likelihoods.
Default budget: five initial candidates, two regeneration rounds, three survivors,
one hybrid, and search depth two. Stop at the cap; report unresolved gates.
Reserve time for verification. Increase the budget only with explicit authorization.
If subagents or model tiers are unavailable, work serially and disclose that limitation;
role-switching is not independent verification. Do not invent models or tool runs.

## STAGE 0 -- NAME THE MODE (anti-typicality framing)

State the strongest reasonable conventional answer as MODE, not a straw baseline.
Before sampling, fix hard constraints, the quality floor, the comparison metric,
and the available test budget. Apply the same checks to MODE and challengers.
Beating MODE is a hypothesis to test, not a conclusion the output must manufacture.

## STAGE 1 -- TAIL SAMPLING (verbalized + lensed divergence)

Generate candidates that are STRUCTURALLY distinct, never paraphrases.
Two mechanisms stacked:
- Verbalized sampling: each candidate carries a self-estimated conventionality
  probability. Work the low-probability tail deliberately.
- Forced lenses, one per candidate minimum: invert it (do the opposite), steal it
  (mechanism analogized from a distant domain: biology, heists, kitchens,
  warfare), remove the loudest constraint, rederive from first principles,
  step back to a higher abstraction, blend two unrelated concepts.
If two candidates share a skeleton, kill one and regenerate with a ban-list of
what exists plus a harder constraint, within the LAW 0 budget.

## STAGE 2 -- NOVELTY ARCHIVE (quality-diversity dedupe gate)

Represent each idea as mechanism | representation/state | decisive assumption.
Merge mechanism-equivalent ideas even if their wording differs; document the shared skeleton.
The archive is MODE plus earlier ideas from THIS run, snapshotted before scoring.
playbook.json contains routing statistics, not candidate memories; do not feed it to novelty.
Use approved scratch files: cands.json is a JSON list of at least four nonblank strings;
archive.json is a JSON string list. Neither file belongs in the installed skill folder.
Run from the resolved skill directory, replacing placeholders with absolute scratch paths:
```
python -B -c "import json,novelty,sys; c=json.load(open(sys.argv[1],encoding='utf-8')); a=json.load(open(sys.argv[2],encoding='utf-8')); d=novelty.set_diversity(c); print('set_diversity',d,'gate',d>=0.5); print('archive',[novelty.novelty_vs_archive(x,a) for x in c]); print('spread_indices',novelty.select_diverse(c,3))" "<SCRATCH>/cands.json" "<SCRATCH>/archive.json"
```
Keep the 0.5 threshold as an uncalibrated lexical tripwire, not proof of structural novelty.
Below it, regenerate within the budget. Above it, still reject structural duplicates;
a high set average cannot excuse a duplicate pair. Never pad wording to raise the score.
Keep up to three distinct survivors using the returned indices, preserving their IDs.
Append all attempted ideas and rejection reasons to the session archive after scoring.
At the retry cap, report the gate failure and use the Stage-6 fallback; do not fake a pass.

## STAGE 3 -- RECOMBINATION (breed the distant)

Take the two MOST distant survivors and breed them. Hybrids no single candidate
contained are routinely the winners. Ideation is a population that breeds, not a
one-shot. One hybrid minimum, state its parents.

## STAGE 4 -- DEEPEN BY SEARCH (backtrack, don't chain)

Expand survivors into small reasoning trees with backtracking and value
estimates, within the LAW 0 depth budget. Pour compute into promising branches.
Never commit to a greedy chain that kills a good branch early. For diagnosis use
abduction, for proof deduction, for estimates decomposition -- match the mode to
the problem (see bundled `modes.json`), not always diverge.

## STAGE 5 -- ADVERSARIAL VERIFY (novel AND correct)

Refute every survivor, hybrid, and MODE against the same specification and quality floor.
Record a concrete failure probe, observed result, evidence location, and residual risk.
A refuter proposes attacks; only a relevant external check supports VERIFIED.
Classify outcomes as failed, verified within stated test scope, or UNVERIFIED;
missing tools or evidence are not a correctness failure and never a pass.
Keep feasibility separate from unusualness. Dedupe hybrids against the session archive.
Retest any later graft before selection.

STAGE 5B -- DIFFERENTIAL TESTING (for commissioned code with costly subtle bugs).
Fix the signature, input domain, expected types, and error semantics before generation.
Use five structurally different implementations, including a small reference checked
against independent examples/properties; record the random seed and edge-case inputs.
Run generated code only in an approved isolated environment; a temporary directory
and subprocess timeout are NOT a sandbox. No suitable runner means NOT RUN.
Treat diff_test.py as a disagreement diagnostic, never a shipping oracle: its current
string conversion loses types and its exception sentinel can receive unanimous votes.
Independently check typed outputs and reference properties; reject ties, unexpected
exceptions, missing candidates, malformed results, and empty test sets as inconclusive.
Investigate disagreements against the spec, not by outvoting the reference.
Select and rerun one actual implementation; a list of consensus outputs is not a program.
Agreement does not rule out a shared misconception. No ~28x claim from this run.

## STAGE 6 -- FRONTIER SELECT (rare-and-good beats common-and-good)

Apply the declared quality floor first, then compare novelty and demonstrated value
on the surviving frontier. Give the winner's parents, measured advantage, and evidence.
Novelty is not permission to miss constraints or hide cost. Do not graft after verification.
If no challenger demonstrably beats MODE, retain a verified MODE and say so.
If nothing is verified, WINNER is NONE or explicitly provisional; BEATS-MODE is
not demonstrated. A failed diversity gate cannot support a novelty claim.

## LAW 5 -- LEDGER ARCHIVE (the learning loop)

Keep task type, mode-plan, winner, failures, and evidence in the session record.
playbook.json stores aggregate routing scores only: it does not remember dead ideas.
An empty playbook means NO LEARNED PRIORS; use modes.json without pretending otherwise.
learn.py currently averages score sources together. Keep self-scores in the report only.
After authorization, back up playbook.json and serialize writes; use
learn.record(task_type, plan, score, source="external") with a finite score in [0,1]
from the predeclared, comparable rubric. Never substitute zero for an unmeasured result.
Use learn.recommend(task_type) only as advice: require uses >= 2, all recorded sources
external, and compatible task/rubric context; otherwise fall back to the static router.
Do not claim persistent candidate dedupe or out-of-sample improvement without evidence.

## LAW 6 -- CHEAP-MODEL MAPPING (AlphaEvolve ensemble pattern)

Breadth is cheap, depth is dear. Default mapping: fast models (flash/nano tier)
propose the population and run refuters in parallel where subagents exist; otherwise
work serially and disclose it. The strong model judges the frontier and writes the
synthesis. Declare tiers per summon. Never spend oracle tokens on paraphrase generation.

## LAW 7 -- ROUTER + ESCALATION (don't always diverge, know when to call the army)

Divergence is ONE mode, not every mode. Diagnose first using the bundled
`modes.json` (12 operators with trigger + protocol + verify_with + grounding):
divergent for open design, abductive for diagnosis, deductive for proof,
decompose for big builds, bayesian for estimates, dialectic for trade-offs,
analogical when stuck, first_principles when the obvious smells, causal for
interventions, metacognitive when uncertain -- then always close with
convergent_verify. Compose the minimal sequence per task, never the full menu.
A router that brainstorms a rename is a clown with a flamethrower.
Escalate when high-stakes or the inline run keeps collapsing: fan out real
parallel subagents per lens plus per refuter where the harness supports it.
Say you're escalating and why.

## FINAL OUTPUT

```
# TYPHON: <mission>
GATE: <engine | direct; budget and capability limits>
MODE: <strong conventional baseline and acceptance test>
SLATE: <candidate IDs, lenses, self-estimated conventionality, mechanisms, gate evidence>
BRED: <hybrid and parent IDs, or why breeding was blocked>
KILLED: <candidate IDs and observed failures; separate unverified candidates>
WINNER: <candidate | MODE | NONE; verification scope or provisional status>
BEATS-MODE: <metric, difference, evidence | not demonstrated>
PLAYBOOK NOTE: <recorded with permission | not recorded; no priors if empty>
CHEAPEST TEST: <next falsifier, expected failure signal, and cost>
```
Preserve every label; use N/A with a reason for direct or blocked stages.
Report outcomes and evidence, not private deliberation. No bulk code or uncommissioned
project edits. CHEAPEST TEST is always the last output line.

## Forbidden acts

- Inventing a win over MODE or declaring an untested idea verified.
- Treating lexical spread, conventionality guesses, or consensus as correctness proof.
- Repeating a dead mechanism without naming changed evidence or assumptions.
- Exceeding the search budget, disabling constraints, or inventing unavailable subagents.
- Treating scratch-execution permission as permission to edit projects or persist learning.
