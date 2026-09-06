# Install Typhon

## Claude Code

```bash
cp -r skills/typhon ~/.claude/skills/typhon
```

Then invoke with `/typhon`. Restart the session so the skill registers.

## OpenCode

```bash
cp -r skills/typhon ~/.config/opencode/skills/typhon
```

Or point your `opencode.json` skills paths at this repo's `skills/` directory.

## Requirements

- Python 3.10+. The bundled helpers (`novelty.py`, `diff_test.py`, `learn.py`)
  are standard-library only: no install needed to run the gates.

## Optional: semantic backend

- `pip install model2vec`, then `TYPHON_EMBEDDINGS=1`. The novelty gate switches
  from lexical to embedding cosine: paraphrase sets that pass lexical (0.693)
  get rejected (0.279). The active backend prints in every self-check; report
  `distance_backend()` with scores, never assume it.

## Verify the install

```bash
cd skills/typhon
python learn.py          # expect: self-check passed
```

Then fire `/typhon` on one open problem and check the output carries MODE, SLATE, BRED, KILLED, WINNER, BEATS-MODE, CHEAPEST TEST.
