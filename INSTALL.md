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

- Python 3.10+ with `numpy` for the novelty gate; `model2vec` for the full embedding ensemble:
  `pip install model2vec numpy`
- Without the embedding models, the gate degrades to lexical checks inside `novelty.py`. Still better than vibes.

## Verify the install

```bash
cd skills/typhon
python learn.py          # expect: self-check passed
```

Then fire `/typhon` on one open problem and check the output carries MODE, SLATE, BRED, KILLED, WINNER, BEATS-MODE, CHEAPEST TEST.
