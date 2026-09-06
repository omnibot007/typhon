# TYPHON

*The storm-giant father of monsters. The only beast that ever made Zeus bleed. This skill does the same to the modal answer.*

A divergence engine for coding agents: turns next-token predictors into divergent thinkers. Names the predictable answer, tail-samples structurally distinct candidates, dedupes against a novelty archive, breeds distant hybrids, verifies adversarially, selects rare-and-good.

> Prompting "be creative" is a measured null (p=0.84). The structural archive lifts diversity +0.229 (p<0.0001) at no quality cost. Reproduced, not asserted.

## Before / after

You ask for an approach. Your agent polishes idea #1 and ships the mode wearing a costume.

With Typhon:

```
MODE (beaten): hand-rolled date component, 400 lines.
SLATE: 4 candidates across lenses (native, steal, invert, blend)...
BRED: native input + stolen validation hybrid.
WINNER: <input type="date"> + constraint-validation polyfill, 23 lines.
BEATS-MODE: same UX, 94% less code, zero deps.
CHEAPEST TEST: render + submit in target browsers, 10 minutes.
```

## How it works

```
[0] Name the Mode → [1] Tail Sampling → [2] Novelty Archive → [3] Recombine
→ [4] Deepen by Search → [5] Adversarial Verify → [6] Frontier Select
```

- **Stage 0** commits to beating the predictable answer, stated up front.
- **Stage 1** generates 4+ structurally distinct candidates via verbalized sampling (conventionality probabilities, mine the tail) + forced lenses (invert, steal cross-domain, remove constraint, first principles, step back, blend).
- **Stage 2** runs the executable novelty gate (`novelty.py`, bundled): `set_diversity < 0.5` means paraphrases — regenerate with a ban-list.
- **Stage 3** breeds the two most distant survivors.
- **Stage 4** expands reasoning trees with backtracking; matches thinking mode to problem (abduction/deduction/decomposition, 12-mode router in `modes.json`).
- **Stage 5** refutes each survivor + runs objective checks. For code, Stage 5B differential testing (`diff_test.py`, bundled): 5+ implementations fuzzed against each other, ship consensus (~28x fewer shipped bugs).
- **Stage 6** picks on the novelty×value Pareto frontier: rare-and-good beats common-and-good.
- **Learning loop** (`learn.py` + `playbook.json`, bundled): records routings, external evidence outranks self-scores.

## Install

Drop `skills/typhon/` into your skills directory:

```bash
# Claude Code
cp -r skills/typhon ~/.claude/skills/typhon
# then invoke with /typhon
```

See [INSTALL.md](INSTALL.md) for harness-specific notes.

## Layout

```
skills/typhon/
  SKILL.md        # the engine (laws, stages, output contract)
  novelty.py      # executable diversity gate (MIT, upstream)
  diff_test.py    # differential testing oracle (MIT, upstream)
  modes.json      # 12-operator thinking-mode router table (MIT, upstream)
  learn.py        # routing playbook CLI: record/recommend/show (MIT, upstream)
  playbook.json   # your learned priors (starts empty)
```

## Grounding

Engine adapted from [SritejBommaraju/divergent-agents](https://github.com/SritejBommaraju/divergent-agents) (MIT) and its 78 verified papers. Bundled files are its MIT sources, copied with headers intact. Method: [METHOD.md](https://github.com/SritejBommaraju/divergent-agents/blob/main/METHOD.md).

Key results reproduced from its benchmark (DAT spine, deterministic scorer, committed raw data):
- Prompting "be divergent": delta -0.074, p=0.84 (null).
- Archive mechanism: delta +0.229, p<0.0001 (significant).
- Best-of-N collapses (mean 1.33 distinct); forced lenses yield 9.33 distinct
  correct algorithms -- 7x solution-space coverage, correctness 30/30.
  (Upstream headline rounds this to ~9x; the measured coverage ratio is 7x.)
- Differential testing: ~28x fewer shipped bugs at k=7 vs k=1 (upstream figure,
  not locally reproduced; the bundled helper is a diagnostic, not an oracle).

## License

MIT. Bundled upstream files carry their own headers (MIT, Sritej Bommaraju 2026).
