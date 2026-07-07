#!/usr/bin/env python3
"""
The war on Mars (examples/kepler-mars.ttl): the full
DISCOVERY / GROOMING / DEPRECATION cycle, run end to end.

  * THE FORK OPENS on Tycho's quadrant longitudes: circle-with-equant (the
    vicarious hypothesis) and ellipse-with-area-law both fit within 2' --
    both models EXERCISED against the asserted data, both pass, both acts
    logged (performative provenance);
  * THE META LAYER DESIGNS KEPLER'S EXPERIMENT -- before the octants exist
    in the log, the one decisive discriminator is OctantObservations:
    "observe the octants to resolve the fork", computed, not narrated;
  * DISCOVERY -- the octants arrive; the ellipse passes at 0.0', the equant
    model fails at 8.96': THE EIGHT MINUTES, run and printed. Corroboration
    is temporal (the octants arrived after the fork opened) and the fork
    resolves for the ellipse;
  * DEPRECATION -- the vicarious hypothesis is retracted as a JURISDICTION
    (§15.2, the Sommerfeld pattern): its geometry still runs; its adequacy
    fell. Retraction, not exorcism -- and the record ABOUT it (Astronomia
    Nova) keeps the history (§9), while the generated suite's pretender
    alarm, which fired while the failed model still stood, goes quiet;
  * GROOMING -- the puncture report across the three moments: evidence
    grows the punctured interior, deprecation shrinks the decision-pinned
    share, and the minimal asset ends as §14.2 promises: leaves, decisions,
    pointers.

Doubles as the extension's test: prints per-check results, exits nonzero on
failure.  Run:  python scripts/kepler_demo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from engine import Engine, fork_report, labels, short  # noqa: E402
from engine.meta import open_fork_plans, puncture_report  # noqa: E402
from engine.orbits import exercise_and_log_model  # noqa: E402
from engine.testgen import generate, run_suite  # noqa: E402

REPO = Path(__file__).parent.parent
FAILURES = []


def check(ok, msg):
    print(("✅" if ok else "❌"), msg)
    if not ok:
        FAILURES.append(msg)


def alarms(eng, lab):
    cases = [c for c in generate(eng, lab) if c.kind == "alarm"]
    _, failed = run_suite(cases)
    return {c.subject for c, _r in failed}


def main():
    print("=" * 60)
    print("The war on Mars — discovery, grooming, deprecation")
    print("=" * 60)

    eng = Engine(REPO / "ontology" / "record-ontology.ttl",
                 REPO / "examples" / "kepler-mars.ttl",
                 defer=["OctantObservations"])
    lab = labels(eng.web)

    # ------------------------------------------------------------------ #
    # 1. The fork opens on shared evidence
    # ------------------------------------------------------------------ #
    print("\n🔍 1. Two hypotheses over the quadrant longitudes...")
    eng.declare_rivals("VicariousOrbitClaim", "EllipseOrbitClaim",
                       note="1600: the war on Mars opens")
    s0 = eng.state()
    check(s0.supported[eng.resolve("VicariousOrbitClaim")]
          and s0.supported[eng.resolve("EllipseOrbitClaim")],
          "both claims stand on the quadrant data — a real fork, not a "
          "strawman")

    res_v = exercise_and_log_model(eng, "VicariousPostulates", "quadrants")
    res_e = exercise_and_log_model(eng, "EllipsePostulates", "quadrants")
    check(res_v.passed and res_e.passed,
          f"both models pass at the quadrants — vicarious: {res_v.detail}")
    m_quadrants = eng.log.now

    # ------------------------------------------------------------------ #
    # 2. The meta layer designs Kepler's experiment
    # ------------------------------------------------------------------ #
    print("\n🔍 2. What would resolve it? Ask the web...")
    forks = open_fork_plans(eng.web, eng.state(), lab)
    check(len(forks) == 1, "one open fork awaits an experiment")
    (rv, ds), = forks.items()
    decisive = [d for d in ds if d.decisive]
    check(len(decisive) == 1
          and short(decisive[0].ground) == "OctantObservations",
          "the decisive observation is the OCTANTS — the engine designs "
          "the experiment Kepler ran")

    # ------------------------------------------------------------------ #
    # 3. Discovery: the eight minutes
    # ------------------------------------------------------------------ #
    print("\n🔍 3. The octants arrive...")
    eng.assert_ground("OctantObservations", note="Tycho's octant longitudes")
    res_v2 = exercise_and_log_model(eng, "VicariousPostulates", "octants")
    res_e2 = exercise_and_log_model(eng, "EllipsePostulates", "octants")
    print(f"   vicarious: {res_v2.detail}")
    print(f"   ellipse:   {res_e2.detail}")
    check(res_e2.passed and not res_v2.passed
          and "8.9" in res_v2.detail,
          "the ellipse holds; the equant model fails by ~8.96 arcminutes — "
          "the EIGHT MINUTES, computed from the descriptions")

    s1 = eng.state()
    rep = fork_report(eng.web, s1, s1.rivalries[0])
    check(rep.status == "resolved"
          and short(rep.winner) == "EllipseOrbitClaim",
          "fresh octant evidence corroborates the ellipse alone — the fork "
          "RESOLVES (temporal rule: the octants arrived after it opened)")

    fired = alarms(eng, lab)
    check("VicariousPostulates" in fired,
          "the generated suite raises the pretender alarm: a model failing "
          "its own exercise still stands and transmits (§15.3's detector)")

    # ------------------------------------------------------------------ #
    # 4. Deprecation: a jurisdiction suspended, not a form expelled
    # ------------------------------------------------------------------ #
    print("\n🔍 4. Deprecating the vicarious hypothesis...")
    eng.retract("VicariousPostulates",
                note="deprecated: adequacy fell at the octants (8.96' > 2'); "
                     "the geometry is untouched — jurisdiction, not form "
                     "(§15.2)")
    s2 = eng.state()
    check(not s2.supported[eng.resolve("VicariousOrbitClaim")]
          and not s2.supported[eng.resolve("VicariousEphemeris")],
          "the claim and its ephemeris cascade away with the postulates")
    check(eng.resolve("VicariousPostulates") not in s2.exorcised
          and s2.standing(eng.resolve("VicariousPostulates")) == "failed",
          "retracted, NOT exorcised: the description still runs (Sommerfeld "
          "pattern) — standing stays 'failed', the geometry stays a form")
    check(s2.supported[eng.resolve("AstronomiaNova")],
          "Astronomia Nova — the record ABOUT the vicarious hypothesis — "
          "survives its subject's deprecation (§9: history keeps the "
          "document)")
    check(not alarms(eng, lab),
          "and the pretender alarm goes quiet: deprecation groomed the web "
          "back to consistency")

    # ------------------------------------------------------------------ #
    # 5. Grooming: the puncture report across the three moments
    # ------------------------------------------------------------------ #
    print("\n🔍 5. The puncture report (§14.2), before / after / groomed...")
    pr0 = puncture_report(eng.web, eng.state(m_quadrants),
                          eng.log.upto(m_quadrants), lab)
    pr1 = puncture_report(eng.web, s1, eng.log.upto(), lab)
    pr2 = puncture_report(eng.web, s2, eng.log.upto(), lab)
    for tag, pr in (("quadrants", pr0), ("octants", pr1), ("deprecated", pr2)):
        print(f"   {tag:11s} kept {len(pr.kept_constituted)}+"
              f"{len(pr.kept_pointers)}p, punctured {len(pr.punctured)} "
              f"(lossless {len(pr.regenerable)}, pinned "
              f"{len(pr.drift_risk)}), ratio {pr.ratio:.2f}, "
              f"decisions {len(pr.decisions)}")
    check(len(pr1.punctured) > len(pr0.punctured),
          "evidence GREW the punctured interior — accuracy creates "
          "compressibility (§14.2)")
    check(len(pr2.drift_risk) < len(pr1.drift_risk),
          "deprecation SHRANK the decision-pinned share — grooming is "
          "recompression")
    check(all(ev.note and not ev.note.startswith("seed:")
              for ev in pr2.decisions)
          and any(ev.kind == "retract" for ev in pr2.decisions),
          f"the trail keeps every decision, deprecation included "
          f"({len(pr2.decisions)} events) — the recipe for replay is the "
          "audit (§14.4)")

    # the minimal asset, stated
    ephemeris = eng.resolve("MarsEphemeris")
    check(ephemeris in pr2.punctured,
          "the surviving ephemeris is punctured interior: predictions are "
          "never stored, they regenerate from laws + elements on demand")

    print()
    if FAILURES:
        print(f"❌ {len(FAILURES)} check(s) failed")
        return 1
    print("✅ all checks passed — discovered, groomed, deprecated, "
          "and the history kept")
    return 0


if __name__ == "__main__":
    sys.exit(main())
