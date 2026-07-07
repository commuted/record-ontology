#!/usr/bin/env python3
"""
Generated suites (engine/testgen.py), run end to end:

  * the suite is DERIVED from the web -- replay, sufficiency, minimality,
    level-agreement, category-error and exercise cases enumerated from the
    merged fixtures' own structure, none written by hand;
  * every structural case passes -- the labels keep their promises
    (sufficient AND minimal, environment by environment), the fixpoint is
    deterministic, the calculus agrees at every moment, the API refuses
    category errors for every derived record;
  * THE PLANTED PRETENDER IS FOUND MECHANICALLY -- the 2=1 pseudo-proof
    stands unexorcised in the raw merged web, and the generated alarm case
    catches it with no test naming it anywhere;
  * exorcism CLEARS the alarm -- regenerate after Engine.exorcise and the
    suite goes green: the suite tracks the lifecycle, because it is
    generated from it.

Doubles as the extension's test: prints per-check results, exits nonzero on
failure.  Run:  python scripts/testgen_demo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from engine import Engine, labels, short  # noqa: E402
from engine.testgen import counts_by_kind, generate, run_suite  # noqa: E402

REPO = Path(__file__).parent.parent
FAILURES = []


def check(ok, msg):
    print(("✅" if ok else "❌"), msg)
    if not ok:
        FAILURES.append(msg)


def main():
    print("=" * 60)
    print("Generated suites — the web tests itself")
    print("=" * 60)

    eng = Engine(REPO / "ontology" / "record-ontology.ttl",
                 *sorted((REPO / "examples").rglob("*.ttl")))
    lab = labels(eng.web)

    print("\n🔍 Generating the suite from the merged web...")
    cases = generate(eng, lab)
    kinds = counts_by_kind(cases)
    print("   " + ", ".join(f"{k}: {n}" for k, n in sorted(kinds.items())))
    check(len(cases) > 300 and
          {"replay", "sufficiency", "minimality", "level", "category",
           "exercise", "alarm"} <= set(kinds),
          f"{len(cases)} cases generated across {len(kinds)} families — "
          "no fixture-specific test was written")

    print("\n🔍 Running it...")
    passed, failed = run_suite(cases)

    structural = [(c, r) for c, r in failed if c.kind != "alarm"]
    check(not structural,
          "every structural case passes: labels sufficient and minimal "
          "env-by-env, replay deterministic, calculus agrees at every "
          "moment, category errors refused for every derived record"
          if not structural else
          f"structural failures: "
          + "; ".join(f"{c.kind}/{c.subject}: {r.detail}"
                      for c, r in structural[:5]))

    alarms = {c.subject for c, r in failed if c.kind == "alarm"}
    check(alarms == {"PseudoProofTwoEqualsOne", "TwoEqualsOneEquation",
                     "VicariousPostulates"},
          f"the alarms are exactly the planted failures — the registry "
          f"fallacy, its arith-described equation, and the equant model "
          f"that cannot match the octants ({', '.join(sorted(alarms))}) — "
          "found by generation, not by any test naming them")

    print("\n🔍 Expelling and deprecating, each by its own discipline...")
    # formal fabrication -> exorcise (the description does not close, §15.3)
    for name in ("PseudoProofTwoEqualsOne", "TwoEqualsOneEquation"):
        eng.log_exercise(name, passed=False,
                         note="generated alarm: fails at the hidden "
                              "division by a-b")
        eng.exorcise(name, note="expelled on the generated suite's finding")
    # jurisdictional failure -> retract (the geometry runs; adequacy fell,
    # §15.2 -- the same act kepler_demo performs as deprecation)
    eng.log_exercise("VicariousPostulates", passed=False,
                     note="generated alarm: 8.96' > 2' at the octants")
    eng.retract("VicariousPostulates",
                note="deprecated on the generated suite's finding")
    cases2 = generate(eng, lab)
    _, failed2 = run_suite(cases2)
    check(not [f for f in failed2 if f[0].kind == "alarm"],
          "every alarm clears — exorcism for the broken form, deprecation "
          "for the fallen jurisdiction; the suite tracks the lifecycle "
          "because it is generated from it")
    check(not [f for f in failed2 if f[0].kind != "alarm"],
          "and every structural case still passes afterwards "
          "(the cascade is consistent at every moment)")

    print()
    if FAILURES:
        print(f"❌ {len(FAILURES)} check(s) failed")
        return 1
    print("✅ all checks passed — the machinery implies its own suite")
    return 0


if __name__ == "__main__":
    sys.exit(main())
