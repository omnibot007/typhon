"""
diff_test.py â€” differential testing: use DIVERSITY as a correctness oracle (no reference solution needed).

The fuzz benchmark (RESULTS.md Benchmark 5) measured a real win: a single forward pass ships a subtly-buggy
solution ~1 in 36 times (passes weak tests, fails fuzzing), but generating DIVERSE solutions and running
them against many random inputs exposes the bug as a DISAGREEMENT â€” and majority-vote over the diverse set
recovers the correct answer (383/383 disagreement cases in the benchmark). This module is that mechanism,
made reusable: the cognitive engine's `convergent_verify` mode should run it on any code task.

Honest scope: this catches IDIOSYNCRATIC (minority) bugs. If most candidates share the SAME wrong belief
(a systematic error), the majority is wrong and diversity cannot save you â€” so disagreements are a strong
bug signal but agreement is NOT a correctness proof. We flag that explicitly. ponytail: stdlib only.

TYPHON hardening: type-preserving votes (1 vs "1" disagree), ties / unanimous-errors /
empty-inputs resolve to INCONCLUSIVE (never shipped), wrong majorities are reported with
named suspects instead of silently shipped. Diverges from upstream; see SKILL.md Stage 5B.
"""
import sys, os, json, subprocess, tempfile, re
from collections import Counter


def _run(fn, code, inputs, timeout=12):
    if "```" in code:
        m = re.search(r"```(?:python)?\s*(.*?)```", code, re.DOTALL)
        if m: code = m.group(1)
    runner = (code.strip() + "\n\nimport json\n"
              f"_inp=json.loads(r'''{json.dumps(inputs)}''')\n"
              "res=[]\n"
              f"for a in _inp:\n    try: res.append({fn}(*a))\n    except Exception: res.append('__ERR__')\n"
              "print(json.dumps(res, default=str))\n")
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as fh:
            fh.write(runner); path = fh.name
        out = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=timeout,
                             cwd=tempfile.gettempdir())
        line = out.stdout.strip().splitlines()[-1] if out.stdout.strip() else ""
        return json.loads(line)
    except Exception:
        return None
    finally:
        try: os.unlink(path)
        except Exception: pass


def _vote_key(value):
    """Type-preserving ballot: 1 and "1" must never share a box. None (crash in
    transport, not a vote) is unvotable and filtered before counting."""
    return json.dumps(value, sort_keys=True, default=str)


def differential_test(fn_name, codes, inputs):
    """Run every candidate (each defining `fn_name`) on `inputs`. Returns a report:
      consensus      : per-input majority output, TYPED values (None == inconclusive there)
      disagreements  : input indices where candidates differ (someone is buggy there)
      inconclusive   : input indices with NO shippable answer (tie / unanimous errors)
      suspect_idx    : candidate indices that ever differ from a decided consensus
      agreement      : fraction of inputs with unanimous NON-ERROR agreement
      warning        : agreement != correctness (a wrong majority survives voting)
    """
    if not inputs:
        return {"error": "empty input set: agreement over nothing proves nothing", "runnable": 0}
    outs = [_run(fn_name, c, inputs) for c in codes]
    ok_idx = [ci for ci, o in enumerate(outs) if o is not None and len(o) == len(inputs)]
    ok = [outs[ci] for ci in ok_idx]
    if len(ok) < 2:
        return {"error": "need >=2 runnable candidates", "runnable": len(ok)}
    consensus, disagreements, inconclusive = [], [], []
    for i in range(len(inputs)):
        votes = Counter(_vote_key(o[i]) for o in ok)
        top = votes.most_common(2)
        if len(top) > 1 and top[0][1] == top[1][1]:
            consensus.append(None); disagreements.append(i); inconclusive.append(i); continue
        key = top[0][0]
        if key == _vote_key("__ERR__") and len(votes) == 1:
            consensus.append(None); inconclusive.append(i); continue
        consensus.append(json.loads(key))
        if len(votes) > 1:
            disagreements.append(i)
    suspect = []
    for ci, o in enumerate(outs):
        if o is None or len(o) != len(inputs):
            suspect.append(ci); continue
        if any(consensus[i] is not None and _vote_key(o[i]) != _vote_key(consensus[i])
               for i in range(len(inputs))):
            suspect.append(ci)
    return {
        "consensus": consensus,
        "disagreements": disagreements,
        "inconclusive": inconclusive,
        "suspect_candidate_idx": suspect,
        "agreement": 1.0 - (len(disagreements) + len(inconclusive)) / len(inputs),
        "runnable": len(ok),
        "warning": "disagreement => >=1 candidate is buggy; unanimous error or tie => "
                   "INCONCLUSIVE, never a pass; a wrong majority still outvotes the truth â€” "
                   "investigate suspects against the spec, do not ship the vote.",
    }


if __name__ == "__main__":
    # self-check: 3 correct candidates + 1 with a planted off-by-one bug; the bug must be caught.
    good = "def f(xs):\n return sorted(set(xs))"
    good2 = "def f(xs):\n out=[]\n for x in sorted(xs):\n  if x not in out: out.append(x)\n return out"
    good3 = "def f(xs):\n return sorted(list(dict.fromkeys(xs)))"
    buggy = "def f(xs):\n s=sorted(set(xs))\n return s[1:] if s else s   # planted bug: drops the smallest"
    inputs = [[[3, 1, 2, 1]], [[5]], [[]], [[2, 2, 2]], [[9, 1, 9, 4]]]
    rep = differential_test("f", [good, good2, good3, buggy], inputs)
    assert rep["disagreements"], "should have caught the planted bug via disagreement"
    assert 3 in rep["suspect_candidate_idx"], "the buggy candidate (idx 3) must be flagged"
    assert 0 not in rep["suspect_candidate_idx"], "a correct candidate must not be flagged"
    # consensus should equal the correct answer (buggy is outvoted 3-to-1)
    assert rep["consensus"][0] == [1, 2, 3], rep["consensus"][0]
    assert not rep["inconclusive"], "clean run must have no inconclusive inputs"
    print(f"diff_test self-check passed: caught planted bug at candidate {rep['suspect_candidate_idx']}, "
          f"consensus correct, agreement={rep['agreement']:.2f}")
    # --- TYPHON hardening regressions ---
    # 1. typed votes: int 1 vs str "1" must disagree, and the 1-1 tie is inconclusive (never first-wins)
    r1 = differential_test("f", ["def f(x):\n return 1", "def f(x):\n return '1'"], [[0]])
    assert 0 in r1["disagreements"] and 0 in r1["inconclusive"], "typed tie must disagree AND be inconclusive"
    assert r1["consensus"] == [None], "tie must ship nothing"
    # 2. unanimous errors are inconclusive, never consensus-by-agreement
    r2 = differential_test("f", ["def f(x):\n raise ValueError('x')", "def f(x):\n 1/0"], [[0]])
    assert r2["consensus"] == [None] and not r2["disagreements"] and r2["inconclusive"] == [0], \
        "unanimous errors must be inconclusive, not agreement"
    # 3. empty input set errors instead of vacuous agreement
    r3 = differential_test("f", ["def f(x):\n return x"], [])
    assert "error" in r3, "empty inputs must error"
    # 4. wrong majority: consensus follows the crowd but the correct minority is named, not buried
    r4 = differential_test("f", ["def f(x):\n return x + 1", "def f(x):\n return x + 1",
                                 "def f(x):\n return x * 2"], [[3]])
    assert r4["consensus"] == [4], "majority rules the vote (investigate vs spec before shipping)"
    assert 2 in r4["suspect_candidate_idx"] and "warning" in r4, "minority suspect must be named"
    print("diff_test hardening regressions passed: typed-tie, unanimous-error, empty-input, wrong-majority")
