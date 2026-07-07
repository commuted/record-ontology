#!/usr/bin/env python3
"""
Exercise the fidelity calculus (engine/fidelity.py) and verify its claims:

  A. AGREEMENT / CONFLUENCE -- support recomputed from ATMS labels alone must
     equal the engine's fixpoint at EVERY moment of the Neptune replay, and
     the grade projection must equal the engine's Level for every supported
     record (Level is the calculus's coarsest projection, as promised).
  B. §2 BOUNDARY CONDITIONS -- formal pass-through mints certainty only over
     formal leaves; attenuation (amp) and leaf profile are separate
     dimensions; the punctual leaf grades only itself.
  C. NEPTUNE STRUCTURAL TRUTHS -- convergence adds little (the two
     predictions' environments differ only in their inference tokens: it
     corroborates the execution, not the premises); Galle adds much (the
     corroborating environment contains evidence in NO base environment of
     the hypothesis); corroboration is temporal (§13.3) through the calculus.

Doubles as the calculus's test: prints per-check results, exits nonzero on
failure.  Run:  python scripts/fidelity_demo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from engine import (Engine, Level, fidelity, fork_fidelity, grade, labels,  # noqa: E402
                    short, supported_by_labels)

REPO = Path(__file__).parent.parent
FAILURES = []


def check(ok, msg):
    print(("✅" if ok else "❌"), msg)
    if not ok:
        FAILURES.append(msg)


def names(nodes):
    return ", ".join(sorted(short(n) for n in nodes))


def agree(eng, lab, moment=None):
    """Label-support == fixpoint support; grade projection == engine Level."""
    s = eng.state(moment)
    by_labels = supported_by_labels(eng.web, s, lab)
    for n in eng.web.universe:
        if by_labels[n] != s.supported[n]:
            return f"support disagrees on {short(n)} at moment {s.moment}"
        if s.supported[n]:
            best = max(grade(eng.web, e) for e in lab[n] if e <= s.asserted)
            if best != s.level[n]:
                return f"grade disagrees on {short(n)} at moment {s.moment}"
    return None


def main():
    print("=" * 60)
    print("Fidelity Calculus — structure, projections, agreement")
    print("=" * 60)

    # Re-enact the Neptune history exactly as engine_demo does.
    eng = Engine(REPO / "ontology" / "record-ontology.ttl",
                 REPO / "examples" / "neptune-discovery.ttl",
                 defer=["GalleObservation"])
    eng.declare_rivals("UnseenPlanetClaim", "ModifiedGravityClaim",
                       note="the §12 fork, declared")
    rivalry = eng.state().rivalries[0]
    m_1845 = eng.log.now
    eng.assert_ground("GalleObservation", note="1846-09-23")
    eng.retract("LawOfGravitation", note="counterfactual")
    eng.assert_ground("LawOfGravitation", note="reinstated")
    lab = labels(eng.web)

    # -- A. agreement at every moment of the replay ----------------------------
    print("\n🔍 A. Agreement with the engine at every moment...")
    problems = [p for m in range(eng.log.now + 1) if (p := agree(eng, lab, m))]
    check(not problems,
          f"labels ⇔ fixpoint support and grade ⇔ Level across all "
          f"{eng.log.now + 1} moments" + (f" — {problems[0]}" if problems else ""))

    # ... and across every fixture in the repository merged.
    all_paths = [REPO / "ontology" / "record-ontology.ttl",
                 *sorted((REPO / "examples").rglob("*.ttl"))]
    eng_all = Engine(*all_paths)
    lab_all = labels(eng_all.web)
    p = agree(eng_all, lab_all)
    check(not p, f"same agreement over all fixtures merged "
                 f"({len(eng_all.web.universe)} records)" + (f" — {p}" if p else ""))

    # -- B. §2 boundary conditions ---------------------------------------------
    print("\n🔍 B. §2 boundary conditions...")
    s_all = eng_all.state()
    socrates = fidelity(eng_all.web, s_all, eng_all.resolve("SocratesMortal"), lab_all)
    check(socrates.best_grade == Level.CERTAIN and socrates.base[0].amp == 0,
          "SocratesMortal: CERTAIN — truth-preserving over formal leaves "
          "passes completeness through")
    cogito = fidelity(eng_all.web, s_all, eng_all.resolve("Cogito"), lab_all)
    check(cogito.best_grade == Level.PUNCTUAL
          and cogito.base[0].env == frozenset({eng_all.resolve("Cogito")}),
          "Cogito: PUNCTUAL, and only over the environment that is exactly "
          "itself — §2's zero amplification as the min-law")

    s_now = eng.state()
    residuals = fidelity(eng.web, s_now, eng.resolve("UranusResiduals"), lab)
    check(residuals.base[0].amp == 0 and residuals.best_grade == Level.DEFEASIBLE,
          "UranusResiduals: amp=0 yet DEFEASIBLE — attenuation and leaf "
          "profile are separate dimensions (empirical leaves decide)")
    neptune = fidelity(eng.web, s_now, eng.resolve("NeptuneExists"), lab)
    check(neptune.base[0].amp == 3,
          f"NeptuneExists: {neptune.base[0].amp} ampliative joints crossed "
          "(abduction, prediction, identification) — set semantics, no "
          "double-counting of shared ancestry")

    # -- C. Neptune structural truths -------------------------------------------
    print("\n🔍 C. Neptune structural truths...")
    lv = lab[eng.resolve("LeVerrierPredictedPosition")]
    ad = lab[eng.resolve("AdamsPredictedPosition")]
    (lv_env,), (ad_env,) = lv, ad
    diff = lv_env ^ ad_env
    check(diff == {eng.resolve("Inf_LeVerrierPrediction"),
                   eng.resolve("Inf_AdamsPrediction")},
          "convergence adds little: the two predictions' environments differ "
          "ONLY in their inference tokens — it corroborates the execution, "
          "not the premises")

    ff = fork_fidelity(eng.web, s_now, rivalry, lab)
    upc = ff[eng.resolve("UnseenPlanetClaim")]
    mgc = ff[eng.resolve("ModifiedGravityClaim")]
    galle = eng.resolve("GalleObservation")
    base_grounds = {g for v in upc.base for g in v.env}
    corr_grounds = {g for v in upc.corroborating for g in v.env}
    check(len(upc.corroborating) == 1 and galle in corr_grounds
          and galle not in base_grounds,
          "Galle adds much: the corroborating environment holds evidence "
          "absent from EVERY base environment of the hypothesis")
    check(not mgc.corroborating,
          "ModifiedGravityClaim: no corroborating environment — the fork's "
          "resolution, seen as environments")
    shared = upc.shared_grounds & (mgc.shared_grounds or set())
    check(eng.resolve("LawOfGravitation") in upc.shared_grounds
          and eng.resolve("UranusResiduals") in upc.base[0].via
          and shared,
          f"common fate: both rivals rest on [{names(shared)}] — why "
          "retracting the law felled BOTH forks (oracle 3)")

    upc_1845 = fidelity(eng.web, eng.state(m_1845), eng.resolve("UnseenPlanetClaim"), lab)
    check(not upc_1845.corroborating,
          "as-of moment '1845' the hypothesis has NO corroborating "
          "environment — the temporal rule (§13.3), through the calculus")

    # -- a human-readable glimpse of the object ---------------------------------
    print("\n📊 The fidelity object of UnseenPlanetClaim (now):")
    for kind, views in (("base", upc.base), ("corroborating", upc.corroborating)):
        for v in views:
            print(f"   {kind}: grade={v.grade.name} amp={v.amp} "
                  f"leaves=[{names(v.leaves)}]")
    print(f"   breadth={upc.breadth}  shared grounds=[{names(upc.shared_grounds)}]")

    print("\n" + "=" * 60)
    if FAILURES:
        print(f"❌ {len(FAILURES)} calculus check(s) failed")
        sys.exit(1)
    print("✅ All fidelity-calculus checks passed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
