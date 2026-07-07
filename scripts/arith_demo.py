#!/usr/bin/env python3
"""
The arithmetic companion + the formulation compiler, run end to end:

  * the DEFINITIONAL HIERARCHY -- division ← multiplication ← addition ←
    successor: mathematics' own derivation web, all formal, bottoming at the
    Peano ground;
  * the triangle DESCRIBED IN FULL -- the 3-4-5 relation as an expression
    subgraph (Records composed of Records); its exercise is COMPILED from
    the description, agrees with the hand registry, and the act is LOGGED
    at a moment (performative provenance, §15.2);
  * the pretender's final step compiled too -- 1+1=1 fails by derivation,
    not by hand; the §15.3 lifecycle runs to the end with a standing at
    every stage: unexercised → confirmed / failed → exorcised;
  * closed-world WELL-FORMEDNESS -- a malformed application (missing
    operand) is invisible to open-world OWL and a CompileError here;
  * agreement regression, exercise events included.

Doubles as the companion's test: prints per-check results, exits nonzero on
failure.  Run:  python scripts/arith_demo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from rdflib import Graph, Namespace, URIRef  # noqa: E402
from rdflib.namespace import RDF  # noqa: E402

from engine import Engine, grade, labels, short, supported_by_labels  # noqa: E402
from engine.compile import (ARITH, CompileError, compile_expression,  # noqa: E402
                            exercise_and_log)
from engine.exercise import exercise as hand_exercise  # noqa: E402

REPO = Path(__file__).parent.parent
FAILURES = []


def check(ok, msg):
    print(("✅" if ok else "❌"), msg)
    if not ok:
        FAILURES.append(msg)


def main():
    print("=" * 60)
    print("The arithmetic companion — described in full, compiled")
    print("=" * 60)

    eng = Engine(REPO / "ontology" / "record-ontology.ttl",
                 REPO / "ontology" / "arith.ttl",
                 *sorted((REPO / "examples").rglob("*.ttl")))
    g = eng.web.graph

    # -- the definitional hierarchy ----------------------------------------------
    print("\n🔍 The definitional hierarchy (all formal, Peano at the root)...")
    chain, node = [], ARITH.Division
    while node is not None:
        chain.append(short(node))
        node = next(g.objects(node, ARITH.inverseOperationOf),
                    next(g.objects(node, ARITH.iterates), None))
    check(chain == ["Division", "Multiplication", "Addition", "Successor"],
          "division ← multiplication ← addition ← successor: mathematics' "
          "own derivation web, bottoming at the Peano ground "
          "(the §14 limiting case: everything regenerates from this core)")

    # -- the triangle, described and compiled -------------------------------------
    print("\n🔍 The triangle, exercised FROM ITS DESCRIPTION...")
    m_before = eng.log.now
    res = exercise_and_log(eng, "PythagoreanTheorem")
    check(res is not None and res.passed,
          f"PythagoreanTheorem: PASSED — {res.detail}")
    hand = hand_exercise("PythagoreanTheorem")
    check(hand.passed == res.passed,
          "the compiled exercise agrees with the hand registry — the "
          "registry generalizes into a compiler")
    s = eng.state()
    ev = eng.log.upto()[-1]
    check(ev.kind == "exercise" and ev.moment > m_before
          and s.standing(eng.resolve("PythagoreanTheorem")) == "confirmed",
          f"PERFORMATIVE PROVENANCE: the act is logged at moment {ev.moment}; "
          "standing = confirmed — the earned warrant now has a genealogy, "
          "and the act's record attests itself")

    # -- the pretender's final step, compiled --------------------------------------
    print("\n🔍 The pretender, compiled and expelled...")
    pseudo = eng.resolve("PseudoProofTwoEqualsOne")
    check(eng.state().standing(pseudo) == "unexercised",
          "before: standing = unexercised (claimed; testimonially held)")
    res = exercise_and_log(eng, "PseudoProofTwoEqualsOne")
    check(res is not None and not res.passed and "2 ≠ 1" in res.detail,
          f"compiled exercise FAILS by derivation, not by hand — {res.detail}")
    check(eng.state().standing(pseudo) == "failed",
          "after the failed act: standing = failed (expulsion pending — a "
          "separate §13 decision)")
    eng.exorcise("PseudoProofTwoEqualsOne", note=res.detail)
    s_end = eng.state()
    check(s_end.standing(pseudo) == "exorcised"
          and not s_end.supported[eng.resolve("BogusCorollary")],
          "exorcised, corollary cascades — the full lifecycle ran with a "
          "moment at every stage: unexercised → failed → exorcised")
    check(s_end.standing(eng.resolve("PhaseIntegralMethod")) == "unexercised",
          "PhaseIntegralMethod: still unexercised — testimonial holding "
          "stays visible, per record")

    # -- closed-world well-formedness ----------------------------------------------
    print("\n🔍 Well-formedness is the compiler's job (OWL cannot see absence)...")
    broken = Graph()
    node = URIRef("urn:test:half-formed")
    broken.add((node, RDF.type, ARITH.Application))
    broken.add((node, ARITH.operator, ARITH.Addition))
    broken.add((node, ARITH.firstOperand, URIRef("urn:test:orphan")))
    try:
        compile_expression(broken, node)
        check(False, "a half-formed application should not compile")
    except CompileError as e:
        check("missing operand" in str(e),
              f"a half-formed application raises CompileError ({e}) — "
              "closed-world shape checking, engine stratum")

    # -- agreement regression, exercise events included -----------------------------
    print("\n🔍 Calculus ⇔ engine agreement, exercise events included...")
    lab = labels(eng.web)
    problems = []
    for m in range(eng.log.now + 1):
        st = eng.state(m)
        by_labels = supported_by_labels(eng.web, st, lab)
        for n in eng.web.universe:
            if by_labels[n] != st.supported[n]:
                problems.append(f"support: {short(n)} @ {m}")
            elif st.supported[n]:
                best = max(grade(eng.web, e) for e in lab[n] if st.env_live(e))
                if best != st.level[n]:
                    problems.append(f"grade: {short(n)} @ {m}")
    check(not problems,
          f"labels ⇔ fixpoint and grade ⇔ Level across all {eng.log.now + 1} "
          "moments" + (f" — first: {problems[0]}" if problems else ""))

    print("\n" + "=" * 60)
    if FAILURES:
        print(f"❌ {len(FAILURES)} check(s) failed")
        sys.exit(1)
    print("✅ All companion checks passed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
