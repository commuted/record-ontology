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
# Saccheri (saccheri.ttl): two hypotheses stood on, three descriptions run
# ---------------------------------------------------------------------------

def _run_bounded_lines() -> ExerciseResult:
    """Exercise ex:BoundedLines -- 'on the obtuse hypothesis every straight
    line closes on itself'. The obtuse model is the sphere: run it. A
    geodesic's total length computes to 2*pi*R -- finite; prolonging past it
    revisits every point. The description CLOSES internally, and precisely
    thereby contradicts the held axiom of indefinite prolongation (Euclid
    post. 2), which is the datum the exercise tests against -- adequacy
    against what is held, exactly as the orbit models test against
    observations."""
    t = sp.symbols("t", real=True)
    # unit-sphere great circle through the poles, arc-length parameter t
    point = sp.Matrix([sp.cos(t), sp.sin(t), 0])
    speed = sp.sqrt(sum(c.diff(t) ** 2 for c in point))
    total = sp.integrate(speed, (t, 0, 2 * sp.pi))   # closes at 2*pi
    revisits = sp.simplify(point.subs(t, 0) - point.subs(t, total)) == sp.zeros(3, 1)
    if sp.simplify(total - 2 * sp.pi) == 0 and revisits:
        return ExerciseResult(
            False,
            "the obtuse model's straights close at length 2π and revisit — "
            "prolongation is bounded, contradicting the indefinite-"
            "prolongation axiom held since Euclid: the consequence fails "
            "against the held web")
    return ExerciseResult(True, "the geodesic did not close (it must!)")


def _run_angle_sum_deficit() -> ExerciseResult:
    """Exercise ex:AngleSumDeficit -- 'on the acute hypothesis a triangle's
    angles fall short of two right angles, the deficit growing with the
    triangle'. Run the acute model (hyperbolic law of cosines, equilateral
    triangles of side 1 and 2): both sums under pi, the deficit strictly
    growing. Saccheri derived this to find an absurdity; it verifies."""
    sums = []
    for side in (sp.Integer(1), sp.Integer(2)):
        cos_angle = sp.cosh(side) / (sp.cosh(side) + 1)
        sums.append(3 * sp.acos(cos_angle))
    below_pi = all(sp.simplify(s - sp.pi) < 0 for s in sums)
    growing_deficit = sp.simplify((sp.pi - sums[1]) - (sp.pi - sums[0])) > 0
    ok = bool(below_pi and growing_deficit)
    return ExerciseResult(
        ok,
        "equilateral sides 1 and 2: angle sums "
        f"{float(sums[0]):.4f} and {float(sums[1]):.4f} rad, both < π, "
        "deficit growing with the triangle — the description closes"
        if ok else "an angle-sum check failed")


def _run_repugnance() -> ExerciseResult:
    """Exercise ex:SaccheriRepugnance -- Proposition XXXIII's 'refutation'
    of the acute hypothesis: asymptotic straights 'meet at infinity and
    there share a common perpendicular', which he declares repugnant. Run
    the step his argument needs: the angle between the asymptote and the
    perpendicular, acos(tanh x), has limit 0 at infinity -- but ATTAINS 0
    at no point. The argument treats the limit as a point; the description
    does not close. His conviction was content; this is the computation."""
    x = sp.symbols("x", real=True)
    angle = sp.acos(sp.tanh(x))
    limit_ok = sp.limit(angle, x, sp.oo) == 0
    attained = sp.solveset(sp.Eq(angle, 0), x, domain=sp.S.Reals)
    if limit_ok and attained is sp.S.EmptySet:
        return ExerciseResult(
            False,
            "the perpendicularity his argument needs is approached "
            "(limit 0) but attained at NO point — 'at infinity' is not a "
            "place where lines meet; the refutation fails at its own step")
    return ExerciseResult(True, "the limit is attained (it must not be!)")


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

EXERCISES: Mapping[str, Exercise] = {
    ex.record: ex for ex in (
        Exercise("PythagoreanTheorem",
                 "the triangle's description, run", _run_pythagorean),
        Exercise("PseudoProofTwoEqualsOne",
                 "the 2=1 pseudo-proof, run", _run_pseudoproof),
        Exercise("BoundedLines",
                 "the obtuse hypothesis's closed straights, run",
                 _run_bounded_lines),
        Exercise("AngleSumDeficit",
                 "the acute hypothesis's angle deficit, run",
                 _run_angle_sum_deficit),
        Exercise("SaccheriRepugnance",
                 "Saccheri's refutation of the acute, run", _run_repugnance),
    )
}


def exercise(record_short_name: str) -> Optional[ExerciseResult]:
    """Run a record's registered exercise. None means NO exercise is
    registered: the record is formally warrantABLE at best, testimonially
    held in fact (§15.2) -- which is the honest status of most mathematics
    in most heads."""
    ex = EXERCISES.get(record_short_name)
    return ex.run() if ex else None
