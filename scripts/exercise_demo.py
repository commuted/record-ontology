#!/usr/bin/env python3
"""
Exercise-or-exorcise (ROOT.md §15.3), run end to end:

  * the triangle EXERCISED -- ex:PythagoreanTheorem's formulation (sides,
    angles, relationships) executes and closes: warrant earned;
  * the pretender EXERCISED and EXORCISED -- the 2=1 pseudo-proof fails at
    its hidden division by zero; Engine.exorcise withdraws the warrant claim
    at a moment; the corollary resting on it cascades away; the PUBLICATION
    (a record about the proof, §9) survives -- history keeps the document;
  * the honest third state -- a formal record with no registered exercise is
    testimonially held (most mathematics, in most heads);
  * agreement -- the calculus still matches the engine at every moment,
    exorcism included.

Doubles as the extension's test: prints per-check results, exits nonzero on
failure.  Run:  python scripts/exercise_demo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from engine import Engine, grade, labels, short, supported_by_labels  # noqa: E402
from engine.exercise import exercise  # noqa: E402

REPO = Path(__file__).parent.parent
FAILURES = []


def check(ok, msg):
    print(("✅" if ok else "❌"), msg)
    if not ok:
        FAILURES.append(msg)


def main():
    print("=" * 60)
    print("Exercise or exorcise — formal warrant, earned")
    print("=" * 60)

    eng = Engine(REPO / "ontology" / "record-ontology.ttl",
                 *sorted((REPO / "examples").rglob("*.ttl")))
    lab = labels(eng.web)

    # -- the triangle, run -------------------------------------------------------
    print("\n🔍 Exercising the triangle...")
    res = exercise("PythagoreanTheorem")
    check(res is not None and res.passed,
          f"PythagoreanTheorem: PASSED — {res.detail}")

    # -- the honest third state --------------------------------------------------
    res_none = exercise("PhaseIntegralMethod")
    check(res_none is None,
          "PhaseIntegralMethod: no exercise registered — formally "
          "warrantable, testimonially held (§15.2), stated rather than hidden")

    # -- the pretender, run and expelled ------------------------------------------
    print("\n🔍 Exercising the pseudo-proof...")
    res = exercise("PseudoProofTwoEqualsOne")
    check(res is not None and not res.passed,
          f"PseudoProofTwoEqualsOne: FAILED — {res.detail}")

    s_before = eng.state()
    bogus = eng.resolve("BogusCorollary")
    check(s_before.supported[bogus],
          "before exorcism: the corollary resting on it stands (the claim "
          "was trusted)")

    m_before = eng.log.now
    eng.exorcise("PseudoProofTwoEqualsOne", note=res.detail)
    s_after = eng.state()
    withdrawn = {n for n, _old, new in eng.diff(m_before) if not new[0]}
    check(withdrawn == {eng.resolve("PseudoProofTwoEqualsOne"), bogus},
          f"exorcism cascades: [{', '.join(sorted(short(n) for n in withdrawn))}] "
          "lose standing — a broken proof transmits nothing")
    check(bogus in eng.stubs(s_after),
          "the corollary reopens as a stub — exorcising Kempe reopens "
          "four-color, in miniature")
    check(s_after.supported[eng.resolve("PseudoProofPublication")],
          "the publication — a record ABOUT the proof — survives: history "
          "keeps the document; the warrant is what is expelled")
    check(s_after.supported[eng.resolve("PythagoreanTheorem")],
          "the exercised triangle is untouched")

    # -- guard: exorcism targets machinery, not conclusions ------------------------
    try:
        eng.exorcise("BogusCorollary")
        check(False, "exorcising a derived record should be refused")
    except ValueError:
        check(True, "guard: derived records cannot be exorcised — expel the "
                    "machinery they rest on (§15.3)")

    # -- agreement, exorcism included ----------------------------------------------
    print("\n🔍 Calculus ⇔ engine agreement, exorcism included...")
    problems = []
    for m in range(eng.log.now + 1):
        s = eng.state(m)
        by_labels = supported_by_labels(eng.web, s, lab)
        for n in eng.web.universe:
            if by_labels[n] != s.supported[n]:
                problems.append(f"support: {short(n)} @ {m}")
            elif s.supported[n]:
                best = max(grade(eng.web, e) for e in lab[n] if s.env_live(e))
                if best != s.level[n]:
                    problems.append(f"grade: {short(n)} @ {m}")
    check(not problems,
          f"labels ⇔ fixpoint and grade ⇔ Level across all {eng.log.now + 1} "
          "moments, before and after the exorcism"
          + (f" — first: {problems[0]}" if problems else ""))

    print("\n" + "=" * 60)
    if FAILURES:
        print(f"❌ {len(FAILURES)} check(s) failed")
        sys.exit(1)
    print("✅ All exercise-or-exorcise checks passed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
