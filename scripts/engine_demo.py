#!/usr/bin/env python3
"""
Run the propagation engine against the Neptune fixture's ORACLE -- the
contract written into the header of examples/neptune-discovery.ttl:

  1. With Galle's observation in: the unseen-planet fork dominates
     ("the discovery pops out"); the modified-gravity rival is eclipsed.
  2. Retract the observation: the fork REOPENS.
  3. Retract the law of gravitation: the tables, the residuals, and BOTH
     forks re-level out -- fork B is self-undermining.

Plus the §13/§14 machinery the engine carries: moments and as-of views
(retrospection without hindsight), open stubs, and the puncturing property
(the log holds only grounds + decisions; the derived interior regenerates).

Doubles as the engine's test: prints per-check results, exits nonzero on
failure.  Run:  python scripts/engine_demo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from engine import Engine, Level, fork_report, short, structural_candidates  # noqa: E402

REPO = Path(__file__).parent.parent
EX = "https://www.epistemic-ontology.net/record/examples/neptune-discovery#"

FAILURES = []


def check(ok, msg):
    print(("✅" if ok else "❌"), msg)
    if not ok:
        FAILURES.append(msg)


def names(nodes):
    return ", ".join(sorted(short(n) for n in nodes))


def main():
    print("=" * 60)
    print("Propagation Engine — Neptune oracle")
    print("=" * 60)

    # History re-enacted: every ground is seeded EXCEPT Galle's observation,
    # which arrives later -- evidence after the fork opens (§13.3).
    eng = Engine(REPO / "ontology" / "record-ontology.ttl",
                 REPO / "examples" / "neptune-discovery.ttl",
                 defer=["GalleObservation"])

    # -- structural candidates over-detect; rivalry is declared ---------------
    print("\n🔍 Fork candidates (structural — deliberately over-detects)...")
    cands = {pair for pair, _shared in structural_candidates(eng.web)}
    real = tuple(sorted((eng.resolve("UnseenPlanetClaim"),
                         eng.resolve("ModifiedGravityClaim")), key=str))
    parallel = tuple(sorted((eng.resolve("LeVerrierPredictedPosition"),
                             eng.resolve("AdamsPredictedPosition")), key=str))
    check(real in cands, "candidate: unseen planet vs modified gravity (the real fork)")
    check(parallel in cands,
          "candidate: Le Verrier vs Adams predictions — NOT rivals (convergence); "
          "why rivalry must be declared, not derived")

    eng.declare_rivals("UnseenPlanetClaim", "ModifiedGravityClaim",
                       note="escalation: rivalry is content-level, so declaring "
                            "it is a decision, logged")
    rivalry = eng.state().rivalries[0]

    # -- 1845: the fork is open; the planet is a stub --------------------------
    print("\n🔍 Moment '1845' (before the observation arrives)...")
    m_1845 = eng.log.now
    s = eng.state()
    rep = fork_report(eng.web, s, rivalry)
    check(rep.status == "open", f"fork status: {rep.status} (expected open)")
    neptune = eng.resolve("NeptuneExists")
    check(not s.supported[neptune], "NeptuneExists is unsupported (not yet observed)")
    check(neptune in eng.stubs(s),
          f"open stubs = [{names(eng.stubs(s))}] — the first-class hole (§10)")
    check(s.level[eng.resolve("UranusResiduals")] == Level.DEFEASIBLE,
          "UranusResiduals is DEFEASIBLE despite truth-preserving force "
          "(deduction over empirical leaves mints no certainty)")
    check(s.level[eng.resolve("PerturbationMathematics")] == Level.CERTAIN,
          "PerturbationMathematics is CERTAIN (formal ground)")

    # -- 1846-09-23: the observation arrives; the fork collapses ---------------
    print("\n🔍 The observation arrives (oracle 1: the discovery pops out)...")
    eng.assert_ground("GalleObservation",
                      note="Berlin, 1846-09-23 — evidence arriving AFTER the fork opened")
    s = eng.state()
    rep = fork_report(eng.web, s, rivalry)
    check(rep.status == "resolved" and short(rep.winner) == "UnseenPlanetClaim",
          f"fork resolved, winner: {short(rep.winner) if rep.winner else None}")
    check(short(rep.eclipsed) == "ModifiedGravityClaim"
          and s.supported[eng.resolve("ModifiedGravityClaim")],
          "ModifiedGravityClaim is ECLIPSED, not deleted — the losing branch "
          "stays in the history")
    fresh = {leaf for c in rep.corroborations[rep.winner] for leaf in c.fresh_leaves}
    check(fresh == {eng.resolve("GalleObservation")},
          f"corroborating fresh evidence: [{names(fresh)}] — Bode's law (seeded "
          "before the fork) correctly does NOT corroborate")
    check(s.supported[neptune] and s.level[neptune] == Level.DEFEASIBLE,
          "NeptuneExists supported at DEFEASIBLE (ampliative identification — "
          "revisability entailed; the Vulcan coda stays possible)")
    check(not eng.stubs(s), "no open stubs remain")

    # -- retrospection without hindsight (§13.3) -------------------------------
    print("\n🔍 As-of-moment view (retrospection without hindsight)...")
    rep_then = fork_report(eng.web, eng.state(m_1845), rivalry)
    check(rep_then.status == "open",
          "as-of moment '1845' the fork is still OPEN — judging Airy by the "
          "sub-DAG of his moment, not ours")

    # -- oracle 2: retract the observation, the fork reopens -------------------
    print("\n🔍 Oracle 2: retract GalleObservation...")
    m_before = eng.log.now
    eng.retract("GalleObservation", note="suppose the observation withdrawn")
    s = eng.state()
    rep = fork_report(eng.web, s, rivalry)
    check(rep.status == "open", f"fork status: {rep.status} (reopened)")
    withdrawn = {n for n, _old, new in eng.diff(m_before) if not new[0]}
    check(withdrawn == {eng.resolve("GalleObservation"), neptune},
          f"withdrawn by propagation: [{names(withdrawn)}]")
    eng.assert_ground("GalleObservation", note="reinstated")
    rep = fork_report(eng.web, eng.state(), rivalry)
    check(rep.status == "resolved", "reinstated: fork resolves again "
          "(first-assertion moment survives retraction)")

    # -- oracle 3: retract the law; fork B is self-undermining -----------------
    print("\n🔍 Oracle 3: retract LawOfGravitation...")
    m_before = eng.log.now
    eng.retract("LawOfGravitation", note="suppose the law withdrawn")
    s = eng.state()
    withdrawn = {n for n, _old, new in eng.diff(m_before) if not new[0]}
    expected = {eng.resolve(n) for n in (
        "LawOfGravitation", "BouvardTables", "UranusResiduals",
        "UnseenPlanetClaim", "ModifiedGravityClaim",
        "LeVerrierPredictedPosition", "AdamsPredictedPosition", "NeptuneExists")}
    check(withdrawn == expected,
          f"cascade re-levels {len(withdrawn)} records: [{names(withdrawn)}]")
    check(not s.supported[eng.resolve("ModifiedGravityClaim")],
          "fork B is SELF-UNDERMINING: it contested the very premise its own "
          "evidence (the residuals) was computed from, so it falls too")
    check(s.supported[eng.resolve("GalleObservation")],
          "GalleObservation itself stays in (a leaf, not derived)")
    rep = fork_report(eng.web, s, rivalry)
    check(rep.status == "moot", f"fork status: {rep.status} (both rivals down)")
    eng.assert_ground("LawOfGravitation", note="reinstated")
    check(fork_report(eng.web, eng.state(), rivalry).status == "resolved",
          "reinstated: the whole web regenerates and the fork resolves again")

    # -- §14: the log is the punctured core -----------------------------------
    print("\n🔍 Puncturing property (§14: the log holds only the non-derivable residue)...")
    logged = {r for ev in eng.log.upto() for r in ev.subjects if ev.kind != "rivals"}
    check(not (logged & eng.web.derived),
          f"no derived record ever enters the log ({len(eng.web.derived)} derived "
          f"records regenerate by replay; {len(eng.log.upto())} events cover "
          f"{len(logged)} grounds + 1 decision)")

    print("\n" + "=" * 60)
    if FAILURES:
        print(f"❌ {len(FAILURES)} oracle check(s) failed")
        sys.exit(1)
    print("✅ All oracle checks passed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
