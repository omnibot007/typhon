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
- The upstream full-ensemble scorer optionally uses `model2vec` embeddings;
  that is upstream's rig, not this skill's requirement. Do not install it
  for TYPHON.

## Verify the install

```bash
cd skills/typhon
python learn.py          # expect: self-check passed
```

Then fire `/typhon` on one open problem and check the output carries MODE, SLATE, BRED, KILLED, WINNER, BEATS-MODE, CHEAPEST TEST.
