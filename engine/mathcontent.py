"""
Mathematical content for the atom fixture -- a SIDECAR, deliberately.

The RDF stays pure structure (the two-strata rule): this module attaches, per
inference token of examples/bohr-atom.ttl, an EXECUTABLE derivation, and per
derived record its stored FORM (a sympy expression -- the form as held, which
is what a Record is). The content question is now DECIDED (ROOT.md §15):
`rec:formulation` carries the form as held in the graph, and EXECUTION stays
here in the engine stratum -- the reasoner never evaluates a formulation.
Migrating this module's CONTENT dict into the atom fixture as formulation
literals is the open follow-up; the derivations stay engine-side regardless.

What this buys (scripts/bohr_math_demo.py exercises it):

* Formal warrant made executable (§2): a truth-preserving inference whose
  content is real mathematics is checkable by RUNNING it -- "internally
  completable" stops being a metaphor. The derivations below re-derive the
  stored forms from the postulates and machinery alone.
* §14 puncturing demonstrated: delete the derived records' content, keep the
  non-derivable residue (postulates, machinery, DATA), regenerate the
  interior by computation. `regenerate()` is that operation.
* Corroboration with teeth: the Rydberg constant computed from e, m, h;
  the reduced-mass answer to Fowler; and the Sommerfeld coincidence made
  exact -- the 1916 and Dirac-form spectra are IDENTICAL under k = j + 1/2.

Constants are CODATA-2018; the historical agreements they reproduce were, of
course, made with the era's cruder values -- the point is the structure of
the agreement, not anachronistic precision.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping

import sympy as sp

# -- symbols ------------------------------------------------------------------
n, k, j, r = sp.symbols("n k j r", positive=True)
m_e, e, eps0, h, hbar, c = sp.symbols("m_e e epsilon_0 h hbar c", positive=True)
alpha, mc2 = sp.symbols("alpha m_ec2", positive=True)
HALF = sp.Rational(1, 2)

# -- numeric constants (SI, CODATA 2018) ---------------------------------------
NUM = {
    "m_e": 9.1093837015e-31,     # electron mass, kg
    "e": 1.602176634e-19,        # elementary charge, C
    "eps0": 8.8541878128e-12,    # vacuum permittivity, F/m
    "h": 6.62607015e-34,         # Planck constant, J s
    "c": 2.99792458e8,           # speed of light, m/s
    "M_p": 1.67262192369e-27,    # proton mass, kg
    "M_he": 6.6446573357e-27,    # helium-4 nucleus mass, kg
}

# -- the empirical side (the fixture's DATA leaves, as numbers) -----------------
# Balmer's own constant and the visible hydrogen lines he fitted (nm, in air).
BALMER_B_NM = 364.56
BALMER_LINES_NM = {3: 656.28, 4: 486.13, 5: 434.05, 6: 410.17}
# The empirical hydrogen Rydberg constant (spectroscopy), 1/m.
RYDBERG_H_MEASURED = 1.0967758e7
# Fowler's objection, quantified: the He+/H series ratio he measured was
# 4.0016, not 4 -- exactly what the reduced-mass correction predicts.
FOWLER_RATIO_MEASURED = 4.0016


# ---------------------------------------------------------------------------
# Machinery: the derivations (each re-derives a stored form from postulates)
# ---------------------------------------------------------------------------

def derive_bohr_levels() -> sp.Expr:
    """Inf_BohrHydrogen, run: quantized angular momentum (m v r = n hbar)
    + the Coulomb orbit (m v^2 / r = e^2 / 4 pi eps0 r^2)  =>  E_n."""
    v = n * hbar / (m_e * r)                                   # the postulate
    r_n = sp.solve(sp.Eq(m_e * v**2 / r,
                         e**2 / (4 * sp.pi * eps0 * r**2)), r)[0]
    v_n = v.subs(r, r_n)
    E = m_e * v_n**2 / 2 - e**2 / (4 * sp.pi * eps0 * r_n)
    return sp.simplify(E.subs(hbar, h / (2 * sp.pi)))


def derive_balmer_from_levels() -> sp.Expr:
    """Inf_RydbergDerivation, run: the frequency condition over E_n gives
    1/lambda for the n -> 2 series -- Balmer's regularity, with the Rydberg
    constant now an expression in e, m, h, c."""
    E = CONTENT["HydrogenEnergyLevels"]
    return sp.simplify((E - E.subs(n, 2)) / (h * c))


def sommerfeld_exact() -> sp.Expr:
    """Sommerfeld 1916, exact: E/(m c^2) for quantum numbers n, k."""
    return (1 + (alpha / (n - k + sp.sqrt(k**2 - alpha**2)))**2)**(-HALF) - 1


def dirac_exact() -> sp.Expr:
    """The Dirac-form levels: same functional shape in n, j + 1/2 -- but j
    is angular momentum WITH spin; the labels and degeneracies differ."""
    kap = j + HALF
    return (1 + (alpha / (n - kap + sp.sqrt(kap**2 - alpha**2)))**2)**(-HALF) - 1


def _alpha4_term(expr: sp.Expr) -> sp.Expr:
    return sp.simplify(expr.series(alpha, 0, 6).removeO().coeff(alpha, 4)) * alpha**4


def derive_fine_structure_sommerfeld() -> sp.Expr:
    """Inf_FineStructureSommerfeld, run: expand the exact 1916 formula; the
    alpha^4 term is the fine-structure splitting -- no spin anywhere in it."""
    return sp.simplify(mc2 * _alpha4_term(sommerfeld_exact()))


def derive_fine_structure_qm() -> sp.Expr:
    """Inf_FineStructureQM, run: the same splitting from the Dirac-form
    levels (spin built in), re-labelled by k = j + 1/2 for comparison. That
    the result is IDENTICAL to Sommerfeld's is the coincidence."""
    term = sp.simplify(mc2 * _alpha4_term(dirac_exact()))
    return sp.simplify(term.subs(j, k - HALF))


def derive_correspondence_limit() -> sp.Expr:
    """Inf_CorrespondenceLimit, run: emitted frequency (E_{n+1}-E_n)/h over
    the classical orbital frequency v/(2 pi r) of the n-th orbit -> 1."""
    v = n * hbar / (m_e * r)
    r_n = sp.solve(sp.Eq(m_e * v**2 / r,
                         e**2 / (4 * sp.pi * eps0 * r**2)), r)[0]
    f_classical = (v.subs(r, r_n) / (2 * sp.pi * r_n)).subs(hbar, h / (2 * sp.pi))
    E = CONTENT["HydrogenEnergyLevels"]
    nu = (E.subs(n, n + 1) - E) / h
    return sp.limit(sp.simplify(nu / f_classical), n, sp.oo)


# ---------------------------------------------------------------------------
# Stored content: the FORM each derived record holds
# ---------------------------------------------------------------------------

CONTENT: Mapping[str, sp.Expr] = {
    # E_n = -m e^4 / (8 eps0^2 h^2 n^2)
    "HydrogenEnergyLevels": -m_e * e**4 / (8 * eps0**2 * h**2 * n**2),
    # 1/lambda = R (1/4 - 1/n^2), R = m e^4 / (8 eps0^2 h^3 c).
    # (Held since 1885 with an EMPIRICAL constant B; 1913 re-expresses the
    # same regularity with R now derived -- the content's constant changes
    # warrant, the regularity does not.)
    "BalmerFormula": (m_e * e**4 / (8 * eps0**2 * h**3 * c))
                     * (sp.Rational(1, 4) - 1 / n**2),
    # the alpha^4 fine-structure term: -(m c^2) (alpha^4 / 2 n^4)(n/k - 3/4)
    "FineStructureSplitting": -mc2 * alpha**4 / (2 * n**4) * (n / k - sp.Rational(3, 4)),
    # the correspondence ratio: quantum emission frequency / classical
    # orbital frequency -> exactly 1
    "BohrModelAsLimit": sp.Integer(1),
}


# ---------------------------------------------------------------------------
# The joints: inference token -> executable derivation
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class MathJoint:
    inference: str                    # short name of the inference token
    concludes: str                    # short name of the concluded record
    title: str
    derive: Callable[[], sp.Expr]     # re-derives the concluded form


JOINTS = (
    MathJoint("Inf_BohrHydrogen", "HydrogenEnergyLevels",
              "E_n from quantized action + the Coulomb orbit",
              derive_bohr_levels),
    MathJoint("Inf_RydbergDerivation", "BalmerFormula",
              "Balmer's regularity from E_n; Rydberg constant from e, m, h, c",
              derive_balmer_from_levels),
    MathJoint("Inf_FineStructureSommerfeld", "FineStructureSplitting",
              "fine structure from relativistic ellipses (1916, no spin)",
              derive_fine_structure_sommerfeld),
    MathJoint("Inf_FineStructureQM", "FineStructureSplitting",
              "the same splitting from Dirac-form levels (spin built in)",
              derive_fine_structure_qm),
    MathJoint("Inf_CorrespondenceLimit", "BohrModelAsLimit",
              "quantum/classical frequency ratio -> 1 as n -> oo",
              derive_correspondence_limit),
)


def regenerate(record: str) -> list:
    """§14, run: re-derive a punctured record's content from the machinery.
    Returns one regenerated expression per joint concluding the record --
    FineStructureSplitting gets TWO (Sommerfeld's and the QM one), and their
    equality is the coincidence, visible in the regeneration table itself."""
    return [sp.simplify(jt.derive()) for jt in JOINTS if jt.concludes == record]


def regeneration_ok(record: str) -> bool:
    stored = CONTENT[record]
    outs = regenerate(record)
    return bool(outs) and all(sp.simplify(out - stored) == 0 for out in outs)
