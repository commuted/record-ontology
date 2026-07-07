#!/usr/bin/env python3
"""
The mathematics of the atom fixture, executed (engine/mathcontent.py):

  1. Balmer's formula against his own lines -- the 1885 induction's data.
  2. Bohr's derivation, run: E_n from the postulates; the Rydberg constant
     computed from e, m, h, c against spectroscopy -- the 1913 thunderclap.
  3. The reduced-mass answer to Fowler: 4 R_He/R_H = 4.0016, not 4.
  4. The Sommerfeld coincidence, exact: the 1916 and Dirac-form spectra are
     IDENTICAL under k = j + 1/2 -- numerically right, wrong premises.
  5. The correspondence limit: quantum/classical frequency ratio -> 1.

Plus: sidecar <-> fixture consistency (every joint names a real inference
edge in examples/bohr-atom.ttl), and the §14 puncturing demonstration (the
derived interior regenerates from postulates + machinery; the data cannot).

Doubles as the sidecar's test: prints per-check results, exits nonzero on
failure.  Run:  python scripts/bohr_math_demo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import sympy as sp  # noqa: E402

from engine import load_web, short  # noqa: E402
from engine.mathcontent import (BALMER_B_NM, BALMER_LINES_NM, CONTENT,  # noqa: E402
                                FOWLER_RATIO_MEASURED, JOINTS, NUM,
                                RYDBERG_H_MEASURED, dirac_exact, e, eps0, h, j,
                                k, m_e, c, n, regenerate, regeneration_ok,
                                sommerfeld_exact, HALF)

REPO = Path(__file__).parent.parent
FAILURES = []


def check(ok, msg):
    print(("✅" if ok else "❌"), msg)
    if not ok:
        FAILURES.append(msg)


def main():
    print("=" * 60)
    print("The atom's mathematics, executed")
    print("=" * 60)

    # -- 0. sidecar <-> fixture consistency -------------------------------------
    print("\n🔍 Sidecar ⇔ fixture consistency...")
    web = load_web([REPO / "ontology" / "record-ontology.ttl",
                    REPO / "examples" / "bohr-atom.ttl"])
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

    # -- 1. Balmer, 1885 ---------------------------------------------------------
    print("\n🔍 1. Balmer's induction against his lines...")
    worst = max(abs(BALMER_B_NM * nn**2 / (nn**2 - 4) - lam) / lam
                for nn, lam in BALMER_LINES_NM.items())
    check(worst < 5e-4, f"lambda = B n²/(n²−4) fits Halpha..Hdelta to "
                        f"{worst:.2e} relative — the regularity is real, "
                        "the mechanism absent (the 1885 explanandum)")

    # -- 2. Bohr, 1913, run ------------------------------------------------------
    print("\n🔍 2. Bohr's derivation, executed...")
    jt = JOINTS[0]
    derived = sp.simplify(jt.derive() - CONTENT["HydrogenEnergyLevels"])
    check(derived == 0, "E_n = −m e⁴/8ε₀²h²n² re-derived from quantized "
                        "action + the Coulomb orbit (formal warrant, run)")
    inv_lambda = sp.simplify(JOINTS[1].derive() - CONTENT["BalmerFormula"])
    check(inv_lambda == 0, "the Balmer formula re-derived via the frequency "
                           "condition — explanandum #1 resolved by computation")
    R_expr = m_e * e**4 / (8 * eps0**2 * h**3 * c)
    R_inf = float(R_expr.subs({m_e: NUM["m_e"], e: NUM["e"], eps0: NUM["eps0"],
                               h: NUM["h"], c: NUM["c"]}))
    R_H = R_inf / (1 + NUM["m_e"] / NUM["M_p"])
    rel = abs(R_H - RYDBERG_H_MEASURED) / RYDBERG_H_MEASURED
    check(rel < 1e-4, f"Rydberg constant from e, m, h, c: {R_H:.6e} 1/m vs "
                      f"measured {RYDBERG_H_MEASURED:.6e} ({rel:.1e} relative) "
                      "— the 1913 corroboration, recomputed")
    B_bohr_nm = 4 / R_H * 1e9
    relB = abs(B_bohr_nm - BALMER_B_NM) / BALMER_B_NM
    check(relB < 1e-3, f"Balmer's empirical constant B = {BALMER_B_NM} nm "
                       f"becomes 4/R_H = {B_bohr_nm:.2f} nm ({relB:.1e}; "
                       "residue is air-vs-vacuum wavelengths) — the content's "
                       "constant changes WARRANT, the regularity stands")

    # -- 3. the reduced-mass answer to Fowler ------------------------------------
    print("\n🔍 3. Fowler's objection, answered to four decimals...")
    ratio = 4 * (1 + NUM["m_e"] / NUM["M_p"]) / (1 + NUM["m_e"] / NUM["M_he"])
    check(abs(ratio - FOWLER_RATIO_MEASURED) < 2e-4,
          f"4·R_He/R_H = {ratio:.5f} vs Fowler's measured "
          f"{FOWLER_RATIO_MEASURED} — the corroboration that arrived through "
          "an objection")

    # -- 4. the Sommerfeld coincidence, exact -------------------------------------
    print("\n🔍 4. The Sommerfeld coincidence...")
    fs_somm = sp.simplify(JOINTS[2].derive() - CONTENT["FineStructureSplitting"])
    check(fs_somm == 0, "1916: the alpha^4 splitting −(mc²α⁴/2n⁴)(n/k − 3/4) "
                        "from relativistic ellipses — NO spin in the premises")
    fs_qm = sp.simplify(JOINTS[3].derive() - CONTENT["FineStructureSplitting"])
    check(fs_qm == 0, "the SAME splitting from Dirac-form levels (spin built "
                      "in), under k = j + 1/2 — same conclusion, disjoint "
                      "premises: the environment swap, now exact")
    ident = sp.simplify(sommerfeld_exact().subs(k, j + HALF) - dirac_exact())
    check(ident == 0, "and not just to alpha^4: the EXACT spectra coincide "
                      "under k = j + 1/2 (labels and degeneracies differ — "
                      "which is why it is a coincidence, not a duplication)")

    # -- 5. the correspondence limit ----------------------------------------------
    print("\n🔍 5. The correspondence principle, as a symbolic limit...")
    lim = JOINTS[4].derive()
    check(sp.simplify(lim - 1) == 0,
          "lim n→∞ [ (E_{n+1}−E_n)/h ] / f_classical = 1 — the eclipsed "
          "model persists as a limit, by computation (LoA, §14's textbook)")

    # -- §14: puncture and regenerate ----------------------------------------------
    print("\n🔍 §14 puncturing: the derived interior regenerates...")
    for rec in ("HydrogenEnergyLevels", "BalmerFormula",
                "FineStructureSplitting", "BohrModelAsLimit"):
        outs = regenerate(rec)
        check(regeneration_ok(rec),
              f"{rec}: content deleted, regenerated from machinery alone "
              f"({len(outs)} derivation{'s' if len(outs) > 1 else ''})")
    check(not regenerate("BalmerMeasurements"),
          "BalmerMeasurements: NO derivation regenerates the data — the "
          "empirical leaves are exactly what the punctured core must keep")

    print("\n" + "=" * 60)
    if FAILURES:
        print(f"❌ {len(FAILURES)} check(s) failed")
        sys.exit(1)
    print("✅ All executable-mathematics checks passed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
