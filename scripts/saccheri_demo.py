#!/usr/bin/env python3
"""
The promontory (ROOT.md §17), run end to end on Saccheri (1733-1868):

  * TWO SCAFFOLDS ERECTED -- the obtuse and acute hypotheses SUPPOSED, not
    asserted: the agent's conviction ("false, erected to explode") goes in
    the note as content; the register records only that they are stood on.
    Their deductive downstream is QUARANTINED -- reachable, exercisable,
    transmitting nothing into the held web, invisible to the planner;
  * THE REFUTATION EXIT -- the obtuse consequence (straights close on
    themselves) runs and FAILS against the held prolongation axiom; the
    path is truth-preserving, so modus tollens returns a FORMAL verdict:
    "refutes (formal)". The scaffold is dismantled; the episode stays in
    the trail;
  * THE FORCE ASYMMETRY -- the acute consequence (angle-sum deficit) runs
    and PASSES, and passing only ever CORROBORATES, defeasibly, though the
    path is exactly as truth-preserving: you learn more, at higher grade,
    from a scaffold's death than from its survival;
  * THE CLEANUP THAT FAILED -- Saccheri's published refutation exercises
    and fails at its own step (the limit treated as a point): the pretender
    was the cleanup, not the scaffold; it is exorcised (§15.3);
  * THE LANDING -- Beltrami's model arrives (1868) and the acute hypothesis
    CONVERTS: the same record, re-asserted as held at a moment, its
    quarantined theorem now held knowledge, its provenance forever reading
    "born on the promontory". What he was convinced was false was found
    true -- conviction is content, and it was wrong;
  * the generated suite ends green: every standing consistent, no alarms.

Doubles as the extension's test: prints per-check results, exits nonzero on
failure.  Run:  python scripts/saccheri_demo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from engine import Engine, labels, short  # noqa: E402
from engine.exercise import exercise  # noqa: E402
from engine.meta import (observation_plans, puncture_report,  # noqa: E402
                         scaffold_reports)
from engine.testgen import generate, run_suite  # noqa: E402

REPO = Path(__file__).parent.parent
FAILURES = []


def check(ok, msg):
    print(("✅" if ok else "❌"), msg)
    if not ok:
        FAILURES.append(msg)


def main():
    print("=" * 60)
    print("Saccheri — the promontory, both exits")
    print("=" * 60)

    eng = Engine(REPO / "ontology" / "record-ontology.ttl",
                 REPO / "examples" / "saccheri.ttl",
                 defer=["HypObtuseAngle", "HypAcuteAngle",
                        "BeltramiConsistency"])
    lab = labels(eng.web)

    # ------------------------------------------------------------------ #
    # 1. Erect the scaffolds: supposed, not held
    # ------------------------------------------------------------------ #
    print("\n🔍 1. Two hypotheses, stood on to be exploded (1733)...")
    eng.suppose("HypObtuseAngle",
                note="convinced it is false; erected to explode it")
    eng.suppose("HypAcuteAngle",
                note="convinced it is false; erected to explode it — "
                     "beyond the Hail Mary, to see what the cat drags in")
    s = eng.state()
    hyp_a = eng.resolve("HypAcuteAngle")
    deficit = eng.resolve("AngleSumDeficit")
    bounded = eng.resolve("BoundedLines")

    check(s.standing(hyp_a) == "supposed"
          and not s.supported[hyp_a] and s.reachable[hyp_a],
          "standing 'supposed': stood on, not held — worn openly, unlike "
          "the pretender")
    check(not s.supported[deficit] and s.reachable[deficit]
          and not s.supported[bounded] and s.reachable[bounded],
          "the deductive downstream is QUARANTINED: visible from the "
          "promontory, transmitting nothing held")
    quarantined = s.quarantined(eng.web.universe)
    plans = observation_plans(eng.web, s, lab)
    check(not (set(plans) & quarantined),
          "and the planner ignores it — a view from a scaffold is not a "
          "hole to repair")

    # ------------------------------------------------------------------ #
    # 2. Run the consequences; the verdicts split by force
    # ------------------------------------------------------------------ #
    print("\n🔍 2. Exercising the quarantined consequences...")
    res_b = exercise("BoundedLines")
    eng.log_exercise("BoundedLines", res_b.passed, note=res_b.detail)
    res_d = exercise("AngleSumDeficit")
    eng.log_exercise("AngleSumDeficit", res_d.passed, note=res_d.detail)
    print(f"   obtuse ⇒ {res_b.detail[:74]}...")
    print(f"   acute  ⇒ {res_d.detail[:74]}...")

    reports = scaffold_reports(eng.web, eng.state(), lab)
    rep_o = reports[eng.resolve("HypObtuseAngle")]
    rep_a = reports[hyp_a]
    check(rep_o.refuted
          and rep_o.consequences[0].verdict == "refutes (formal)",
          "OBTUSE: the failing consequence, reached by deduction alone, "
          "REFUTES — formal, by modus tollens: falsification pays certain "
          "coin")
    check(not rep_a.refuted and rep_a.corroborated == 1
          and rep_a.consequences[0].verdict == "corroborates (defeasible)",
          "ACUTE: the passing consequence only CORROBORATES — defeasible "
          "though the path is equally truth-preserving: the force "
          "asymmetry, computed")

    # ------------------------------------------------------------------ #
    # 3. The cleanup that failed: the refutation is the pretender
    # ------------------------------------------------------------------ #
    print("\n🔍 3. Saccheri's own refutation, run...")
    res_r = exercise("SaccheriRepugnance")
    eng.log_exercise("SaccheriRepugnance", res_r.passed, note=res_r.detail)
    check(not res_r.passed,
          f"Prop. XXXIII fails at its own step — {res_r.detail[:80]}...")
    eng.exorcise("SaccheriRepugnance",
                 note="the cleanup was the pretender: formal warrant worn "
                      "without the form (§15.3)")
    check(eng.state().standing(eng.resolve("SaccheriRepugnance"))
          == "exorcised"
          and eng.state().standing(hyp_a) == "supposed",
          "the refutation is exorcised; the scaffold stands untouched — "
          "his conviction was content, and it was wrong")

    # ------------------------------------------------------------------ #
    # 4. The refutation exit: dismantle the obtuse scaffold
    # ------------------------------------------------------------------ #
    print("\n🔍 4. Cleanup (the obtuse promontory served its purpose)...")
    eng.retract("HypObtuseAngle",
                note="dismantled: refuted formally via BoundedLines — the "
                     "discovery is the refutation")
    s4 = eng.state()
    check(not s4.reachable[bounded]
          and eng.resolve("HypObtuseAngle") not in s4.supposed,
          "scaffold down, quarantine gone — nothing held was ever touched")

    # ------------------------------------------------------------------ #
    # 5. The landing: 1868
    # ------------------------------------------------------------------ #
    print("\n🔍 5. Beltrami's model arrives; the guess lands...")
    eng.assert_ground("BeltramiConsistency", note="1868")
    eng.convert("HypAcuteAngle",
                note="1868: the promontory is territory — consistent "
                     "geometry, not absurdity")
    s5 = eng.state()
    check(s5.supported[hyp_a] and s5.supported[deficit],
          "the acute hypothesis is HELD and its quarantined theorem is now "
          "held knowledge — the angle-sum deficit, believed by nobody in "
          "1733, supported in 1868")
    first_event = next(ev for ev in eng.log.upto()
                       if ev.subjects == (hyp_a,))
    check(first_event.kind == "suppose"
          and s5.first_asserted[hyp_a] > first_event.moment,
          "provenance keeps the birth: first event 'suppose' (1733), held "
          "only from the convert moment (1868) — the temporal apple stays "
          "in order")
    check(s5.supported[eng.resolve("EuclidesVindicatus")],
          "and the book survives everything — refutation exorcised, "
          "scaffold converted, the record about them untouched (§9)")

    # ------------------------------------------------------------------ #
    # 6. Trail + generated suite
    # ------------------------------------------------------------------ #
    print("\n🔍 6. The trail and the suite...")
    pr = puncture_report(eng.web, s5, eng.log.upto(), lab)
    kinds = {ev.kind for ev in pr.decisions}
    check({"suppose", "convert", "retract", "exorcise"} <= kinds,
          "the whole episode is escalation trail: suppose, convert, "
          "dismantle, exorcise — kept for replay, kept for audit (§14.4)")

    _, failed = run_suite(generate(eng, lab))
    check(not failed,
          "the generated suite ends green — every standing consistent, "
          "no alarms: the promontory left the web clean")

    print()
    if FAILURES:
        print(f"❌ {len(FAILURES)} check(s) failed")
        return 1
    print("✅ all checks passed — falsification instrumental to discovery, "
          "and the unexpected guess landed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
