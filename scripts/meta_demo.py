#!/usr/bin/env python3
"""
The meta layer (engine/meta.py), run end to end -- "observe X to resolve Y":

  * THE NEPTUNE ORACLE, PROSPECTIVE -- as of 1845 (fork open, Berlin not yet
    pointed), the planner's one DECISIVE discriminator is GalleObservation:
    the engine reproduces history's experiment before history runs it. After
    the observation arrives, no experiments remain -- the planner knows a
    settled fork needs none;
  * PLANS FROM DEFICITS -- the stub NeptuneExists is repairable by exactly
    that observation, read off its label's minimal environments;
  * EXPLANANDA PLANS (Bohr, 1885) -- fine structure's plan is "derive": the
    theoretical route exists in the web with formal machinery missing, and
    the planner names Sommerfeld's ingredients three decades early;
  * THE PUNCTURE REPORT (§14.2) -- the partition computes, the classes are
    disjoint and exhaustive over the supported web, and the ratio moves the
    right way when evidence arrives (more derivable interior => more
    compressible);
  * the escalation trail is exactly the non-seed events -- what grooming
    must keep is what audit must keep (§14.4).

Doubles as the extension's test: prints per-check results, exits nonzero on
failure.  Run:  python scripts/meta_demo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from engine import Engine, labels, short  # noqa: E402
from engine.meta import (describe_plan, fork_discriminators,  # noqa: E402
                         observation_plans, open_fork_plans, plans_for,
                         puncture_report)

REPO = Path(__file__).parent.parent
FAILURES = []


def check(ok, msg):
    print(("✅" if ok else "❌"), msg)
    if not ok:
        FAILURES.append(msg)


def main():
    print("=" * 60)
    print("The meta layer — observe X to resolve Y")
    print("=" * 60)

    # ------------------------------------------------------------------ #
    # A. Neptune, prospective: the planner reproduces history's experiment
    # ------------------------------------------------------------------ #
    print("\n🔍 A. The Neptune oracle, run forward (1845)...")
    eng = Engine(REPO / "ontology" / "record-ontology.ttl",
                 REPO / "examples" / "neptune-discovery.ttl",
                 defer=["GalleObservation"])
    eng.declare_rivals("UnseenPlanetClaim", "ModifiedGravityClaim",
                       note="1845: two explanations of the residuals")
    lab = labels(eng.web)
    s_1845 = eng.state()

    forks_open = open_fork_plans(eng.web, s_1845, lab)
    check(len(forks_open) == 1, "as of 1845: one fork awaits an experiment")

    (rv, ds), = forks_open.items()
    decisive = [d for d in ds if d.decisive]
    check(len(decisive) == 1
          and short(decisive[0].ground) == "GalleObservation",
          f"the one decisive discriminator is GalleObservation — point the "
          f"telescope HERE (corroborates "
          f"{short(decisive[0].corroborates[0])} only)")

    neptune = eng.resolve("NeptuneExists")
    plans = plans_for(eng.web, s_1845, neptune, lab)
    check(bool(plans) and plans[0].kind == "repair"
          and {short(g) for g in plans[0].observe} == {"GalleObservation"}
          and not plans[0].derive,
          f"cheapest plan: {describe_plan(eng.web, plans[0])}")

    # the observation arrives; the planner stands down
    eng.assert_ground("GalleObservation", note="Berlin, 1846-09-23")
    s_1846 = eng.state()
    check(not open_fork_plans(eng.web, s_1846, lab),
          "after Berlin: no open forks — a settled fork needs no experiment")
    check(not plans_for(eng.web, s_1846, neptune, lab),
          "and NeptuneExists needs no plan — the hole closed")

    # ------------------------------------------------------------------ #
    # B. Bohr 1885: explananda plans (derive, not observe)
    # ------------------------------------------------------------------ #
    print("\n🔍 B. Explananda plans (the atom, as of 1885)...")
    deferred = ["GoldFoilScattering", "Inf_NuclearAtom", "Inf_RadiativeCollapse",
                "BohrEscalation", "BohrPostulates", "Inf_BohrHydrogen",
                "Inf_RydbergDerivation", "Inf_HeliumReattribution",
                "FranckHertzExperiment", "Inf_DiscreteLevelsConfirmed",
                "PhaseIntegralMethod", "SommerfeldPostulates",
                "Inf_FineStructureSommerfeld", "PaschenMeasurements",
                "Inf_PaschenAgreement", "DeBroglieHypothesis", "SpinHypothesis",
                "MatrixAlgebraFormalism", "Inf_MatrixMechanics",
                "WaveEquationFormalism", "Inf_WaveMechanics",
                "EquivalenceProof", "Inf_HydrogenFromQM", "Inf_FineStructureQM",
                "Inf_ZeemanFromSpin", "Inf_CorrespondenceLimit",
                "LargeNumberLimitGrain", "DavissonGermerExperiment",
                "Inf_MatterWaveConfirmed"]
    atom = Engine(REPO / "ontology" / "record-ontology.ttl",
                  REPO / "examples" / "bohr-atom.ttl", defer=deferred)
    lab_a = labels(atom.web)
    s_1885 = atom.state()

    fine = atom.resolve("FineStructureSplitting")
    fs_plans = plans_for(atom.web, s_1885, fine, lab_a)
    check(bool(fs_plans) and all(p.kind == "explain" for p in fs_plans),
          "fine structure (supported, unexplained): plans are 'explain', "
          "not 'repair' — the two stub species stay distinct")
    best = fs_plans[0]
    check("PhaseIntegralMethod" in {short(g) for g in best.derive},
          f"the plan names Sommerfeld's machinery, thirty years early: "
          f"{describe_plan(atom.web, best)}")
    check("PhaseIntegralMethod" not in {short(g) for g in best.observe},
          "the deficit sorts by warrant: the formal machinery lands under "
          "'derive', never 'observe' — no telescope finds a method")

    # every open item gets ranked plans; cheapest first
    all_plans = observation_plans(atom.web, s_1885, lab_a)
    ranked_ok = all(
        tuple(p.cost for p in ps) == tuple(sorted(p.cost for p in ps))
        for ps in all_plans.values())
    check(ranked_ok, f"{len(all_plans)} open items as of 1885, every plan "
                     "list ranked cheapest-first")

    # ------------------------------------------------------------------ #
    # C. The puncture report (§14.2) -- grooming, computed
    # ------------------------------------------------------------------ #
    print("\n🔍 C. The puncture report (grooming as §14.2's partition)...")
    pr_1845 = puncture_report(eng.web, s_1845, eng.log.upto(), lab)
    pr_1846 = puncture_report(eng.web, s_1846, eng.log.upto(), lab)

    classes = (pr_1846.kept_constituted, pr_1846.kept_pointers,
               pr_1846.regenerable, pr_1846.drift_risk)
    disjoint = all(not (a & b) for i, a in enumerate(classes)
                   for b in classes[i + 1:])
    supported_all = frozenset(
        n for n in eng.web.universe if s_1846.supported[n])
    check(disjoint and frozenset().union(*classes) == supported_all,
          "the partition is disjoint and exhaustive over the supported web")

    # §14.2: "a web's compression ratio is its warrant profile." The
    # profile lives in the SPLIT of the punctured interior: Neptune's
    # resolution is AMPLIATIVE, so the arrival grows the decision-PINNED
    # share (drift-risk) while the lossless share stands still --
    # compressible only because the fork's resolution stays in the trail.
    check(len(pr_1846.drift_risk) > len(pr_1845.drift_risk)
          and len(pr_1846.regenerable) == len(pr_1845.regenerable)
          and pr_1846.ratio > pr_1845.ratio,
          f"the interior grew {len(pr_1845.punctured)} → "
          f"{len(pr_1846.punctured)} records (ratio {pr_1845.ratio:.2f} → "
          f"{pr_1846.ratio:.2f}), and ALL of the growth is decision-pinned "
          f"(drift {len(pr_1845.drift_risk)} → {len(pr_1846.drift_risk)}, "
          f"lossless unchanged) — an ampliative web compresses only "
          "because its decisions are kept")

    check(all(not ev.note.startswith("seed:") for ev in pr_1846.decisions)
          and any(ev.kind == "rivals" for ev in pr_1846.decisions),
          f"the escalation trail keeps {len(pr_1846.decisions)} non-seed "
          "events (the 1845 fork declaration among them) — reconstruction "
          "recipe and audit are the same list (§14.4)")

    drift_names = {short(r) for r in pr_1846.drift_risk}
    check("UnseenPlanetClaim" in drift_names,
          "the abduced claim is drift-risk: replay regenerates it only "
          "defeasibly — puncture it only alongside its resolution")

    print()
    if FAILURES:
        print(f"❌ {len(FAILURES)} check(s) failed")
        return 1
    print("✅ all checks passed — the web plans its own observations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
