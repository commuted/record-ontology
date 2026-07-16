#!/usr/bin/env python3
"""
The fundamental arithmetic properties, executed (engine/arith_properties.py):

  1. Associativity of addition and multiplication
  2. Commutativity of addition and multiplication
  3. Distributivity of multiplication over addition
  4. Identity elements (additive and multiplicative)
  5. Zero property of multiplication
  6. Additive inverse (for integers)
  7. Sidecar ↔ fixture consistency validation
  8. Regeneration test: derived properties regenerate from axioms

Doubles as the sidecar's test: prints per-check results, exits nonzero on
failure.  Run:  python scripts/arith_properties_demo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import sympy as sp  # noqa: E402

from engine import load_web, short  # noqa: E402
from engine.arith_properties import (  # noqa: E402
    CONTENT, JOINTS, a, b, c,
    regenerate, regeneration_ok
)

REPO = Path(__file__).parent.parent
FAILURES = []


def check(ok, msg):
    print(("✅" if ok else "❌"), msg)
    if not ok:
        FAILURES.append(msg)


def main():
    print("=" * 60)
    print("Fundamental Arithmetic Properties: Executable Mathematics")
    print("=" * 60)

    # -- 0. sidecar <-> fixture consistency -----------------------------------
    print("\n🔍 Sidecar ⇔ fixture consistency...")
    web = load_web([REPO / "ontology" / "record-ontology.ttl",
                    REPO / "ontology" / "arith.ttl",
                    REPO / "examples" / "arith-properties.ttl"])
    by_short = {short(node): node for node in web.universe}
    bad = []
    for jt in JOINTS:
        concl = by_short.get(jt.concludes)
        js = web.justifications_of.get(concl, ())
        if not any(short(x.inference) == jt.inference for x in js):
            bad.append(jt.inference)
    check(not bad, f"every executable joint names a real (inference ⊸ concludes) "
                   f"edge in the fixture ({len(JOINTS)} joints)"
                   + (f" — missing: {bad}" if bad else ""))

    # -- 1. Associativity -----------------------------------------------------
    print("\n🔍 1. Associativity properties...")
    
    # Addition associativity
    jt_add = next(jt for jt in JOINTS if jt.concludes == "AdditionAssociativity")
    derived_add = jt_add.derive()
    stored_add = CONTENT["AdditionAssociativity"]
    check(sp.simplify(derived_add - stored_add) == 0,
          "(a + b) + c = a + (b + c) verified symbolically")
    
    # Multiplication associativity
    jt_mul = next(jt for jt in JOINTS if jt.concludes == "MultiplicationAssociativity")
    derived_mul = jt_mul.derive()
    stored_mul = CONTENT["MultiplicationAssociativity"]
    check(sp.simplify(derived_mul - stored_mul) == 0,
          "(a × b) × c = a × (b × c) verified symbolically")

    # -- 2. Commutativity -----------------------------------------------------
    print("\n🔍 2. Commutativity properties...")
    
    # Addition commutativity
    jt_add_comm = next(jt for jt in JOINTS if jt.concludes == "AdditionCommutativity")
    derived_add_comm = jt_add_comm.derive()
    stored_add_comm = CONTENT["AdditionCommutativity"]
    check(sp.simplify(derived_add_comm - stored_add_comm) == 0,
          "a + b = b + a verified symbolically")
    
    # Multiplication commutativity
    jt_mul_comm = next(jt for jt in JOINTS if jt.concludes == "MultiplicationCommutativity")
    derived_mul_comm = jt_mul_comm.derive()
    stored_mul_comm = CONTENT["MultiplicationCommutativity"]
    check(sp.simplify(derived_mul_comm - stored_mul_comm) == 0,
          "a × b = b × a verified symbolically")

    # -- 3. Distributivity ----------------------------------------------------
    print("\n🔍 3. Distributivity properties...")
    
    # Left distributivity
    jt_left = next(jt for jt in JOINTS if jt.concludes == "LeftDistributivity")
    derived_left = jt_left.derive()
    stored_left = CONTENT["LeftDistributivity"]
    check(sp.simplify(derived_left - stored_left) == 0,
          "a × (b + c) = (a × b) + (a × c) verified symbolically")
    
    # Right distributivity
    jt_right = next(jt for jt in JOINTS if jt.concludes == "RightDistributivity")
    derived_right = jt_right.derive()
    stored_right = CONTENT["RightDistributivity"]
    check(sp.simplify(derived_right - stored_right) == 0,
          "(a + b) × c = (a × c) + (b × c) derived from left distributivity")

    # -- 4. Identity elements -------------------------------------------------
    print("\n🔍 4. Identity elements...")
    
    # Additive identity
    jt_add_id = next(jt for jt in JOINTS if jt.concludes == "AdditiveIdentity")
    derived_add_id = jt_add_id.derive()
    stored_add_id = CONTENT["AdditiveIdentity"]
    check(sp.simplify(derived_add_id - stored_add_id) == 0,
          "a + 0 = a verified symbolically")
    
    # Multiplicative identity
    jt_mul_id = next(jt for jt in JOINTS if jt.concludes == "MultiplicativeIdentity")
    derived_mul_id = jt_mul_id.derive()
    stored_mul_id = CONTENT["MultiplicativeIdentity"]
    check(sp.simplify(derived_mul_id - stored_mul_id) == 0,
          "a × 1 = a verified symbolically")

    # -- 5. Zero property -----------------------------------------------------
    print("\n🔍 5. Zero property...")
    
    jt_zero = next(jt for jt in JOINTS if jt.concludes == "MultiplicativeZero")
    derived_zero = jt_zero.derive()
    stored_zero = CONTENT["MultiplicativeZero"]
    check(sp.simplify(derived_zero - stored_zero) == 0,
          "a × 0 = 0 verified symbolically")

    # -- 6. Additive inverse --------------------------------------------------
    print("\n🔍 6. Additive inverse (integers)...")
    
    jt_inv = next(jt for jt in JOINTS if jt.concludes == "AdditiveInverse")
    derived_inv = jt_inv.derive()
    stored_inv = CONTENT["AdditiveInverse"]
    check(sp.simplify(derived_inv - stored_inv) == 0,
          "a + (-a) = 0 verified symbolically (requires integer extension)")

    # -- 7. Numerical verification --------------------------------------------
    print("\n🔍 7. Numerical verification with concrete values...")
    
    # Test associativity with a=2, b=3, c=5
    test_vals = {a: 2, b: 3, c: 5}
    
    add_assoc_lhs = ((a + b) + c).subs(test_vals)
    add_assoc_rhs = (a + (b + c)).subs(test_vals)
    check(add_assoc_lhs == add_assoc_rhs,
          f"Addition associativity: (2+3)+5 = 2+(3+5) = {add_assoc_lhs}")
    
    mul_assoc_lhs = ((a * b) * c).subs(test_vals)
    mul_assoc_rhs = (a * (b * c)).subs(test_vals)
    check(mul_assoc_lhs == mul_assoc_rhs,
          f"Multiplication associativity: (2×3)×5 = 2×(3×5) = {mul_assoc_lhs}")
    
    # Test distributivity
    dist_lhs = (a * (b + c)).subs(test_vals)
    dist_rhs = ((a * b) + (a * c)).subs(test_vals)
    check(dist_lhs == dist_rhs,
          f"Distributivity: 2×(3+5) = (2×3)+(2×5) = {dist_lhs}")

    # -- 8. Regeneration test -------------------------------------------------
    print("\n🔍 8. Regeneration: derived properties regenerate from axioms...")
    
    # Properties that can be regenerated (proven from axioms)
    derived_properties = [
        "AdditionAssociativity",
        "MultiplicationAssociativity",
        "AdditionCommutativity",
        "MultiplicationCommutativity",
        "LeftDistributivity",
        "RightDistributivity",
        "AdditiveIdentity",
        "MultiplicativeIdentity",
        "MultiplicativeZero",
        "AdditiveInverse",
    ]
    
    for rec in derived_properties:
        outs = regenerate(rec)
        check(regeneration_ok(rec),
              f"{rec}: content deleted, regenerated from machinery alone "
              f"({len(outs)} derivation{'s' if len(outs) > 1 else ''})")
    
    # Definitional extensions (have derivations but are axiomatic)
    definitional_records = [
        "AdditionDefinition",
        "MultiplicationDefinition",
        "IntegerExtension",
    ]
    
    for rec in definitional_records:
        outs = regenerate(rec)
        check(len(outs) > 0,
              f"{rec}: has derivation (definitional extension from axioms)")
    
    # Ground cannot be regenerated
    check(not regenerate("PeanoAxioms"),
          "PeanoAxioms: NO derivation regenerates this ground — "
          "foundational axioms must be given")

    print("\n" + "=" * 60)
    if FAILURES:
        print(f"❌ {len(FAILURES)} check(s) failed")
        for failure in FAILURES:
            print(f"   - {failure}")
        sys.exit(1)
    print("✅ All arithmetic property checks passed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
