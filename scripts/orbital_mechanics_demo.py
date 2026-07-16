#!/usr/bin/env python3
"""Orbital mechanics: the Layer-2 derivations, run -- and the consumption
check, run against every sidecar in the repo.

Three acts:
  1. regeneration -- every joint of examples/orbital-mechanics.ttl re-derived
     (dsolve, solve, cancellation-asserts) and compared with the stored form;
  2. corroboration -- Earth's sidereal year from the DERIVED harmonic law,
     perihelion two ways;
  3. the consumption check (engine/consumption.py) across orbital, trig and
     arith sidecars, plus a synthetic restatement joint as the negative
     control: the third fabrication detector, demonstrated on the pattern
     that motivated it.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import sympy as sp

from engine import consumption
from engine import orbital_mechanics as om


def act_1_regeneration() -> bool:
    print("=" * 72)
    print("1. REGENERATION -- every joint re-derived, compared with stored form")
    print("=" * 72)
    ok_all = True
    for jt in om.JOINTS:
        ok = om.regeneration_ok(jt.concludes)
        ok_all &= ok
        mark = "OK " if ok else "FAIL"
        print(f"  [{mark}] {jt.inference:28s} -> {jt.concludes:24s} {jt.title}")
    return ok_all


def act_2_corroboration() -> bool:
    print()
    print("=" * 72)
    print("2. CORROBORATION -- the derived laws against Earth's orbit")
    print("=" * 72)
    P_calc, P_obs, err = om.validate_keplers_third_law()
    print(f"  Kepler III (derived): sidereal year = {P_calc / 86400:.5f} d")
    print(f"  observed:                             {P_obs / 86400:.5f} d")
    print(f"  relative error: {err:.2e}")
    r1, r2 = om.validate_perihelion()
    print(f"  perihelion, r(θ=0) via first law:  {r1:.6e} m")
    print(f"  perihelion, derived a(1-e):        {r2:.6e} m")
    same = abs(r1 - r2) < 1.0
    return err < 1e-4 and same


class _RestatementFixture:
    """The negative control: the pattern the detector exists to catch.
    A 'derivation' over a DERIVED premise that simply returns its stored
    conclusion -- Bob's orbital draft, distilled to one joint."""

    def __init__(self):
        from dataclasses import make_dataclass
        x = sp.symbols("x", positive=True)
        self.CONTENT = {"Base": x + 1, "Derived": (x + 1) ** 2}
        J = make_dataclass("J", ["inference", "concludes", "title", "derive"],
                           frozen=True)

        def derive_base():
            return self.CONTENT["Base"]

        def restate():                      # never touches Base
            return (x + 1) ** 2

        self.derive_base = derive_base      # module-style attribute binding
        self.restate = restate
        self.JOINTS = [
            J("Inf_Base", "Base", "ground-ish", derive_base),
            J("Inf_Restate", "Derived", "restates its conclusion", restate),
        ]
        self.STATED_JOINTS = frozenset()
        self.__name__ = "synthetic_restatement"


def act_3_consumption() -> bool:
    print()
    print("=" * 72)
    print("3. THE CONSUMPTION CHECK -- poison a premise, re-derive")
    print("=" * 72)
    repo = Path(__file__).resolve().parent.parent
    from engine import trig_basics, arith_properties

    total_alarms = {}
    for mod, ttl in [(om, "examples/orbital-mechanics.ttl"),
                     (trig_basics, "examples/trig-basics.ttl"),
                     (arith_properties, "examples/arith-properties.ttl")]:
        vs = consumption.analyze(mod, repo / ttl)
        als = consumption.alarms(vs)
        total_alarms[mod.__name__] = len(als)
        print(f"\n  {mod.__name__}  ({ttl})")
        for v in vs:
            flag = " <-- " if v.category == consumption.ALARM else "     "
            print(f"   {flag}{v.category:16s} {v.inference}")
    print()
    print("  NOTE: arith_properties' alarms are a live finding, not a demo")
    print("  artifact -- those joints restate their conclusions and should be")
    print("  either genuinely derived or declared in STATED_JOINTS (the")
    print("  honest stub). The detector reports the repo's true condition.")

    # -- negative control ------------------------------------------------------
    print()
    print("  negative control (synthetic restatement over a derived premise):")
    fx = _RestatementFixture()
    import tempfile, textwrap
    with tempfile.NamedTemporaryFile("w", suffix=".ttl", delete=False) as f:
        f.write(textwrap.dedent("""\
            @prefix rec: <https://www.epistemic-ontology.net/record#> .
            @prefix ex:  <https://example.org/synth#> .
            ex:Inf_Base    rec:hasPremise ex:Peano .
            ex:Inf_Restate rec:hasPremise ex:Base .
        """))
        tmp = f.name
    vs = consumption.analyze(fx, Path(tmp))
    Path(tmp).unlink()
    control = {v.inference: v.category for v in vs}
    caught = control.get("Inf_Restate") == consumption.ALARM
    print(f"   Inf_Restate -> {control.get('Inf_Restate')}   "
          f"({'caught' if caught else 'MISSED'})")

    return total_alarms["engine.orbital_mechanics"] == 0 and caught


def main() -> int:
    ok1 = act_1_regeneration()
    ok2 = act_2_corroboration()
    ok3 = act_3_consumption()
    print()
    print("=" * 72)
    verdict = ok1 and ok2 and ok3
    print(f"VERDICT: regeneration={'OK' if ok1 else 'FAIL'}  "
          f"corroboration={'OK' if ok2 else 'FAIL'}  "
          f"consumption={'OK' if ok3 else 'FAIL'}")
    print("=" * 72)
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
