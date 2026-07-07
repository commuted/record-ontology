"""
Exercise-or-exorcise (ROOT.md §15.3): formal warrant earned, not stipulated.

A formally-warranted record's `rec:formulation` is a DESCRIPTION -- the
triangle's three sides, its angles, their relationships -- and a description
can be RUN. Exercising a record executes its description and checks it
closes; §2's "the triangle verifies itself" becomes an operation with a
result. The lifecycle:

    claim (assert formal) -> exercise (run the description)
        -> confirmed (warrant earned)  |  exorcised (warrant withdrawn)

with the common third state BEFORE the fork: never exercised = testimonially
held (§15.2) -- `exercise()` returns None for a record with no registered
exercise, which is most of them, honestly.

Exorcism is `Engine.exorcise` (core.py): a log event with a moment; the
record stays in the graph (history keeps the document -- records ABOUT it
are untouched) but can no longer stand or transmit support. What is expelled
is a pretender: formal warrant worn without the form. The demo pair below is
Kempe/Heawood in miniature -- a triangle that verifies itself when run, and
a pseudo-proof (the classic 2=1 fallacy) whose exercise fails at the hidden
division by a-b = 0.

Like mathcontent.py this is a SIDECAR keyed to fixture records by short
name; the engine package never imports it (sympy stays a demo-only
dependency).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping, Optional

import sympy as sp


@dataclass(frozen=True)
class ExerciseResult:
    passed: bool
    detail: str


@dataclass(frozen=True)
class Exercise:
    record: str                          # short name of the fixture record
    title: str
    run: Callable[[], ExerciseResult]


# ---------------------------------------------------------------------------
# The triangle: sides, angles, relationships -- run (minimal-formal.ttl)
# ---------------------------------------------------------------------------

def _run_pythagorean() -> ExerciseResult:
    """Exercise the formulation of ex:PythagoreanTheorem: token sides 3,4,5;
    the Pythagorean relation; the right angle; the angle sum closing."""
    a, b, c = sp.Integer(3), sp.Integer(4), sp.Integer(5)
    checks = []
    # relationship: a^2 + b^2 = c^2
    checks.append(a**2 + b**2 == c**2)
    # angles by the law of cosines (exact rational cosines)
    cos_A = sp.Rational(b**2 + c**2 - a**2, 2 * b * c)   # 4/5
    cos_B = sp.Rational(a**2 + c**2 - b**2, 2 * a * c)   # 3/5
    cos_C = sp.Rational(a**2 + b**2 - c**2, 2 * a * b)   # 0 -> right angle
    checks.append(cos_C == 0)
    # the angle sum closes: cos(A + B) = 0 exactly, so A + B = pi/2 = pi - C
    A, B = sp.acos(cos_A), sp.acos(cos_B)
    checks.append(sp.simplify(sp.expand_trig(sp.cos(A + B))) == 0)
    ok = all(checks)
    return ExerciseResult(ok, "sides 3,4,5: a²+b²=c² holds; angle opposite 5 "
                              "is right; angle sum closes to π — the triangle "
                              "verifies itself, when run"
                          if ok else "a check on the 3-4-5 description failed")


# ---------------------------------------------------------------------------
# The pretender: the 2 = 1 pseudo-proof -- run (minimal-exorcism.ttl)
# ---------------------------------------------------------------------------

def _run_pseudoproof() -> ExerciseResult:
    """Exercise the formulation of ex:PseudoProofTwoEqualsOne. Each step is
    checked as an identity UNDER THE PREMISE a = b; the cancellation step
    silently divides by a - b = 0 and fails."""
    a, b = sp.symbols("a b", positive=True)
    steps = [
        ("a^2 = ab", a**2, a * b),
        ("a^2 - b^2 = ab - b^2", a**2 - b**2, a * b - b**2),
        ("(a+b)(a-b) = b(a-b)", (a + b) * (a - b), b * (a - b)),
        ("a + b = b   [cancels a-b]", a + b, b),
        ("2 = 1", sp.Integer(2), sp.Integer(1)),
    ]
    for name, lhs, rhs in steps:
        holds = sp.simplify((lhs - rhs).subs(a, b)) == 0
        if not holds:
            return ExerciseResult(False, f"fails at step '{name}': the "
                                         "cancellation divides by a-b, which "
                                         "the premise a=b makes zero")
    return ExerciseResult(True, "all steps held (they must not!)")


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

EXERCISES: Mapping[str, Exercise] = {
    ex.record: ex for ex in (
        Exercise("PythagoreanTheorem",
                 "the triangle's description, run", _run_pythagorean),
        Exercise("PseudoProofTwoEqualsOne",
                 "the 2=1 pseudo-proof, run", _run_pseudoproof),
    )
}


def exercise(record_short_name: str) -> Optional[ExerciseResult]:
    """Run a record's registered exercise. None means NO exercise is
    registered: the record is formally warrantABLE at best, testimonially
    held in fact (§15.2) -- which is the honest status of most mathematics
    in most heads."""
    ex = EXERCISES.get(record_short_name)
    return ex.run() if ex else None
