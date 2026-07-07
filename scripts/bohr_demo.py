#!/usr/bin/env python3
"""
Run the engine + fidelity calculus against the atom fixture
(examples/bohr-atom.ttl): chained model succession 1885-1927, exercising the
two extensions the arc demanded:

  A. EXPLANANDA -- the second stub species: supported phenomena no live
     theoretical environment reaches. The arc resolves one per era:
     Balmer's formula (1913), fine structure (1916), anomalous Zeeman (1926).
  B. ENVIRONMENT SWAP -- the Sommerfeld coincidence: fine structure's
     conclusion stands while its entire environment is replaced; hydrogen's
     levels survive the retraction of the postulates that first derived them.
  C. IDENTIFICATION -- matrix vs wave mechanics: declared rivals, then
     proven one; the fork DISSOLVES (no winner, no eclipsed), and
     Davisson-Germer's later corroboration accrues to the POOLED pair.
  D. AGREEMENT -- the calculus still matches the engine at every moment
     (regression for both extensions).

Doubles as the extensions' test: prints per-check results, exits nonzero on
failure.  Run:  python scripts/bohr_demo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from engine import (Engine, fidelity, fork_report, grade, explananda,  # noqa: E402
                    labels, short, structural_candidates, supported_by_labels)

REPO = Path(__file__).parent.parent
FAILURES = []

# Everything that arrives AFTER the 1885-1912 stratum, in historical order.
ERAS = [
    ("1909-11", ["GoldFoilScattering", "Inf_NuclearAtom", "Inf_RadiativeCollapse"]),
    ("1913", ["BohrEscalation", "BohrPostulates", "Inf_BohrHydrogen",
              "Inf_RydbergDerivation", "Inf_HeliumReattribution"]),
    ("1914", ["FranckHertzExperiment", "Inf_DiscreteLevelsConfirmed"]),
    ("1916", ["PhaseIntegralMethod", "SommerfeldPostulates",
              "Inf_FineStructureSommerfeld", "PaschenMeasurements",
              "Inf_PaschenAgreement"]),
    ("1924-25", ["DeBroglieHypothesis", "SpinHypothesis",
                 "MatrixAlgebraFormalism", "Inf_MatrixMechanics"]),
    ("early 1926", ["WaveEquationFormalism", "Inf_WaveMechanics"]),
    # mid 1926 and 1927 are scripted by hand below (rivalry, identify,
    # retractions, Davisson-Germer).
]
DEFERRED = ([n for _era, ns in ERAS for n in ns]
            + ["EquivalenceProof", "Inf_HydrogenFromQM", "Inf_FineStructureQM",
               "Inf_ZeemanFromSpin", "Inf_CorrespondenceLimit",
               "LargeNumberLimitGrain", "DavissonGermerExperiment",
               "Inf_MatterWaveConfirmed"])


def check(ok, msg):
    print(("✅" if ok else "❌"), msg)
    if not ok:
        FAILURES.append(msg)


def names(nodes):
    return ", ".join(sorted(short(n) for n in nodes))


def live_envs(eng, lab, state, name):
    return [e for e in lab[eng.resolve(name)] if e <= state.asserted]


def main():
    print("=" * 60)
    print("The Atom, 1885-1927 — succession, explananda, identification")
    print("=" * 60)

    eng = Engine(REPO / "ontology" / "record-ontology.ttl",
                 REPO / "examples" / "bohr-atom.ttl", defer=DEFERRED)
    lab = labels(eng.web)
    m = {"1885": eng.log.now}

    for era, ns in ERAS:
        for n in ns:
            eng.assert_ground(n, note=era)
        m[era] = eng.log.now
    eng.declare_rivals("MatrixMechanics", "WaveMechanics",
                       note="early 1926: two formalisms, open hostility")
    rivalry = eng.state().rivalries[0]
    m["rivals"] = eng.log.now
    eng.assert_ground("EquivalenceProof", note="Schroedinger 1926")
    eng.identify("MatrixMechanics", "WaveMechanics",
                 note="proven one theory — warrant: EquivalenceProof")
    for n in ["Inf_HydrogenFromQM", "Inf_FineStructureQM", "Inf_ZeemanFromSpin",
              "Inf_CorrespondenceLimit", "LargeNumberLimitGrain"]:
        eng.assert_ground(n, note="1926")
    eng.retract("BohrPostulates", note="1926: the old quantum theory falls")
    eng.retract("SommerfeldPostulates", note="1926: the old quantum theory falls")
    m["1926"] = eng.log.now
    eng.assert_ground("DavissonGermerExperiment", note="1927")
    eng.assert_ground("Inf_MatterWaveConfirmed", note="1927")

    # -- A. the explananda arc: one resolved per era ----------------------------
    print("\n🔍 A. Explananda (the open questions of each era)...")
    expect = {
        "1885": {"BalmerFormula", "FineStructureSplitting", "AnomalousZeemanEffect"},
        "1913": {"FineStructureSplitting", "AnomalousZeemanEffect"},
        "1916": {"AnomalousZeemanEffect"},
    }
    for era, want in expect.items():
        got = {short(r) for r in explananda(eng.web, eng.state(m[era]), lab)}
        check(got == want, f"as of {era}: explananda = [{', '.join(sorted(got))}]")
    got_end = explananda(eng.web, eng.state(), lab)
    check(not got_end, "as of 1927: no explananda remain — each era resolved one")
    s_1885 = eng.state(m["1885"])
    overlap = set(explananda(eng.web, s_1885, lab)) & set(eng.stubs(s_1885))
    check(not overlap, "explananda ∩ stubs = ∅ — support that never rose vs "
                       "support that fell are disjoint species")

    # -- B. environment swap under standing conclusions -------------------------
    print("\n🔍 B. The Sommerfeld coincidence (environment swap)...")
    somm, spin = eng.resolve("SommerfeldPostulates"), eng.resolve("SpinHypothesis")
    fs_1916 = live_envs(eng, lab, eng.state(m["1916"]), "FineStructureSplitting")
    fs_end = live_envs(eng, lab, eng.state(), "FineStructureSplitting")
    check(any(somm in e for e in fs_1916) and not any(spin in e for e in fs_1916),
          "1916: fine structure's theoretical environment rests on Sommerfeld's "
          "postulates — numerically right, no spin in it")
    check(fs_end and not any(somm in e for e in fs_end)
          and any(spin in e for e in fs_end),
          "1927: the conclusion STANDS while its environment is replaced "
          "(spin + wave mechanics) — right result, re-warranted")
    s_end = eng.state()
    survivors = ["HydrogenEnergyLevels", "BalmerFormula", "IonizedHeliumOrigin",
                 "DiscreteEnergyLevelsReal"]
    check(all(s_end.supported[eng.resolve(n)] for n in survivors)
          and eng.resolve("BohrPostulates") not in s_end.asserted,
          f"results outlive their model: [{', '.join(survivors)}] all stand "
          "after the Bohr postulates are retracted (re-derived from QM)")
    check(s_end.supported[eng.resolve("BohrModelAsLimit")],
          "the eclipsed model persists as a limiting case at a coarser grain "
          "(correspondence as level of abstraction)")
    check(s_end.supported[eng.resolve("RadiativeInstability")],
          "the classical reductio still stands — 1913 suspended the law's "
          "jurisdiction, not the law")

    # -- C. identification: the fork that dissolved -----------------------------
    print("\n🔍 C. Matrix vs wave mechanics (resolution by equivalence)...")
    mm, wm = eng.resolve("MatrixMechanics"), eng.resolve("WaveMechanics")
    cands = {pair for pair, _ in structural_candidates(eng.web)}
    check(tuple(sorted((mm, wm), key=str)) not in cands,
          "the 1926 fork was not even structurally detectable (no shared "
          "premise) — declaration was the only route to it")
    check(fork_report(eng.web, eng.state(m["rivals"]), rivalry).status == "open",
          "declared rivals, pre-equivalence: fork open")
    rep = fork_report(eng.web, s_end, rivalry)
    check(rep.status == "identified" and rep.winner is None and rep.eclipsed is None,
          f"post-equivalence: fork {rep.status} — dissolved, no winner, "
          "no eclipsed")
    check(bool(rep.corroborations[wm]) and not rep.corroborations[mm],
          "Davisson-Germer corroborates only wave's downstream — without the "
          "identification, wave would have ECLIPSED matrix")
    fid_mm = fidelity(eng.web, s_end, mm, lab)
    dg = eng.resolve("DavissonGermerExperiment")
    check(any(dg in v.env for v in fid_mm.corroborating),
          "pooling: matrix mechanics' fidelity object now carries the "
          "Davisson-Germer corroborating environment, gained through identity")
    check(fid_mm.breadth >= 2,
          f"pooled breadth = {fid_mm.breadth}: the pair's environments differ "
          "in nearly everything except the conclusion — here convergence IS "
          "independent support (contrast Adams/Le Verrier)")
    fid_mm_before = fidelity(eng.web, eng.state(m["rivals"]), mm, lab)
    check(not fid_mm_before.corroborating,
          "as-of early 1926 (pre-identity): matrix mechanics had no "
          "corroborating environments — pooling is moment-indexed too")

    # -- D. agreement regression --------------------------------------------------
    print("\n🔍 D. Calculus ⇔ engine agreement at every moment...")
    problems = []
    for mm_i in range(eng.log.now + 1):
        s = eng.state(mm_i)
        by_labels = supported_by_labels(eng.web, s, lab)
        for n in eng.web.universe:
            if by_labels[n] != s.supported[n]:
                problems.append(f"support: {short(n)} @ {mm_i}")
            elif s.supported[n]:
                best = max(grade(eng.web, e) for e in lab[n] if e <= s.asserted)
                if best != s.level[n]:
                    problems.append(f"grade: {short(n)} @ {mm_i}")
    check(not problems, f"labels ⇔ fixpoint and grade ⇔ Level across all "
          f"{eng.log.now + 1} moments"
          + (f" — first: {problems[0]}" if problems else ""))

    print("\n" + "=" * 60)
    if FAILURES:
        print(f"❌ {len(FAILURES)} check(s) failed")
        sys.exit(1)
    print("✅ All atom-arc checks passed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
