"""
novelty.py — the measurement substrate for the divergence harness.

You cannot make an agent "think outside the box" unless you can *measure* how far outside the box
a given candidate is. This module gives the harness three primitives, all from the
Novelty-Search / Quality-Diversity literature:

  1. novelty_vs_archive(c, archive)  — how new is candidate c relative to everything tried so far?
                                        (Novelty Search: reward distance-to-k-nearest in behavior space.)
  2. set_diversity(candidates)        — how structurally spread-out is a *set* of candidates?
                                        (Are stage-1's N ideas actually different, or N paraphrases?)
  3. select_diverse(candidates, k)    — greedy max-min pick of k maximally-different candidates.
                                        (MAP-Elites-style: keep a spread, not k near-duplicates.)

ponytail: distance is LEXICAL (character n-gram Jaccard) by default — zero dependencies,
          runs anywhere, deterministic. Set TYPHON_EMBEDDINGS=1 with model2vec installed
          to use embedding cosine instead (semantic novelty: paraphrases read as CLOSE).
          Report distance_backend() alongside every score; never assume which metric ran.
          Ceiling (lexical): measures *surface* novelty — a pure-paraphrase set scores
          ~0.69 and clears naive 0.5 gates. Treat the gate as a tripwire, not proof.
TYPHON hardening: optional embedding backend + backend reporter. Diverges from upstream;
          everything else below is verbatim.
"""

from __future__ import annotations
from itertools import combinations

_EMBED_MODEL = None


def _embed_model():
    """Optional semantic backend, loaded once. Active only when TYPHON_EMBEDDINGS=1
    and model2vec is importable; otherwise None (lexical default)."""
    import os
    if os.environ.get("TYPHON_EMBEDDINGS") != "1":
        return None
    global _EMBED_MODEL
    if _EMBED_MODEL is None:
        try:
            from model2vec import StaticModel
        except ImportError:
            return None
        _EMBED_MODEL = StaticModel.from_pretrained("minishlab/potion-base-8M")
    return _EMBED_MODEL


def distance_backend() -> str:
    """Which metric distance() is using RIGHT NOW. Print it with every score."""
    return "embedding:potion-base-8M" if _embed_model() else "lexical:char-4gram-jaccard"


def _embed_distance(a: str, b: str) -> float:
    """1 - cosine over static embeddings. Pure-stdlib math (no numpy needed)."""
    import math
    m = _embed_model()
    va, vb = (list(v) for v in m.encode([a, b]))
    dot = sum(x * y for x, y in zip(va, vb))
    na = math.sqrt(sum(x * x for x in va))
    nb = math.sqrt(sum(y * y for y in vb))
    if na == 0 or nb == 0:
        return 0.0 if a == b else 1.0
    return 1.0 - (dot / (na * nb))


def _ngrams(text: str, n: int = 4) -> set[str]:
    """Character n-grams. Character-level is robust to tokenization and tiny inputs."""
    t = " ".join(text.lower().split())  # normalize whitespace
    if len(t) < n:
        return {t} if t else set()
    return {t[i:i + n] for i in range(len(t) - n + 1)}


def distance(a: str, b: str, n: int = 4) -> float:
    """1 - Jaccard(n-grams), or 1 - cosine when the embedding backend is active.
    0.0 == identical, 1.0 == nothing shared. Check distance_backend()."""
    if _embed_model() is not None:
        return _embed_distance(a, b)
    ga, gb = _ngrams(a, n), _ngrams(b, n)
    if not ga and not gb:
        return 0.0
    inter = len(ga & gb)
    union = len(ga | gb)
    return 1.0 - (inter / union if union else 0.0)


def novelty_vs_archive(candidate: str, archive: list[str], k: int = 3, n: int = 4) -> float:
    """Novelty Search score: mean distance to the k nearest neighbors in the archive.
    High == candidate sits in a sparse, under-explored region (genuinely new).
    Empty archive == maximally novel by definition (1.0)."""
    if not archive:
        return 1.0
    dists = sorted(distance(candidate, a, n) for a in archive)
    knn = dists[:k] if len(dists) >= k else dists
    return sum(knn) / len(knn)


def set_diversity(candidates: list[str], n: int = 4) -> float:
    """Mean pairwise distance across a set. The stage-1 gate: if generation produced N ideas but
    set_diversity is low, they are paraphrases of the mode — regenerate with harder constraints."""
    if len(candidates) < 2:
        return 0.0
    pairs = list(combinations(candidates, 2))
    return sum(distance(a, b, n) for a, b in pairs) / len(pairs)


def select_diverse(candidates: list[str], k: int, n: int = 4) -> list[int]:
    """Greedy max-min diversity selection (farthest-point sampling). Returns indices of k
    candidates chosen to maximize the minimum pairwise distance — a spread, not a cluster.
    Seeds with the single most-novel-vs-the-rest item, then repeatedly adds the item farthest
    from everything already chosen."""
    if k >= len(candidates):
        return list(range(len(candidates)))
    if k <= 0 or not candidates:
        return []
    # seed: the candidate with the highest mean distance to all others
    seed = max(range(len(candidates)),
               key=lambda i: novelty_vs_archive(candidates[i],
                                                 [c for j, c in enumerate(candidates) if j != i], n=n))
    chosen = [seed]
    while len(chosen) < k:
        rest = [i for i in range(len(candidates)) if i not in chosen]
        # pick the item whose nearest already-chosen neighbor is farthest away (max-min)
        nxt = max(rest, key=lambda i: min(distance(candidates[i], candidates[c], n) for c in chosen))
        chosen.append(nxt)
    return chosen


if __name__ == "__main__":
    # Runnable self-check (ponytail: one assert-based check, no framework).
    obvious = "use a for loop to iterate over the list and sum the values"
    paraphrase = "use a loop to go through the list and add up the values"
    novel = "exploit the closed-form n(n+1)/2 and skip iteration entirely"
    wild = "offload the reduction to the GPU with a parallel scan kernel"

    # paraphrase must be closer to obvious than the novel approach is
    assert distance(obvious, paraphrase) < distance(obvious, novel), "paraphrase should be near-duplicate"

    # novelty vs an archive containing only the obvious answer: paraphrase low, wild high
    arch = [obvious]
    assert novelty_vs_archive(paraphrase, arch) < novelty_vs_archive(wild, arch), "wild idea must read as more novel"

    # a set of distinct ideas is more diverse than a set of paraphrases
    distinct_set = [obvious, novel, wild]
    paraphrase_set = [obvious, paraphrase, "iterate the list and total the values up"]
    assert set_diversity(distinct_set) > set_diversity(paraphrase_set), "distinct set should score higher"

    # select_diverse should never return the two closest items together when it can avoid it
    pool = [obvious, paraphrase, novel, wild]
    picks = select_diverse(pool, 2)
    assert 0 not in picks or 1 not in picks, "should not pick both obvious+paraphrase as the diverse-2"
    assert len(picks) == 2 and len(set(picks)) == 2

    print("novelty.py self-check passed:",
          f"backend={distance_backend()}",
          f"div(distinct)={set_diversity(distinct_set):.3f}",
          f"div(paraphrase)={set_diversity(paraphrase_set):.3f}",
          f"diverse-2 picks={picks}")
