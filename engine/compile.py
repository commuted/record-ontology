"""
The formulation compiler: exercise DERIVED from description (§15 + arith).

With the arithmetic companion, a record's description is an expression
subgraph -- numerals, applications, equations, every node a formal Record,
every operand a part. This module walks that subgraph, builds the
corresponding sympy expressions mechanically, and runs them: any record
described in the companion becomes exercisable for free, replacing the
hand-written registry (engine/exercise.py) for structured formulations.
The formulation literal remains the RENDERING; the subgraph is the
DESCRIPTION, and this compiler treats the subgraph as authoritative.

Division of labour, per the strata rule:
  * OWL (arith.ttl)  -- shape, decidable face: functional operands, typing.
  * this compiler    -- CLOSED-WORLD well-formedness (a missing operand is
    open-world-invisible to OWL; here it is a CompileError) and VALUE
    (2+2=4 is engine work, never a DL entailment).

PERFORMATIVE PROVENANCE (§15.2/.3): exercising is an act of derivation --
exactly what a formal genealogy bottoms out in -- so `exercise_and_log`
appends the act to the revision log at a moment. The earned warrant thereby
HAS a genealogy ('exercised at m, passed'), and the event's record is its
own evidence that the run happened: the act attests itself (the performative
face), while what it confirms is formal (the content). Two warrants, stacked.

Sidecar like mathcontent.py: the engine package never imports this (sympy
stays a demo-only dependency).
"""

from __future__ import annotations

from typing import Optional

import sympy as sp
from rdflib import Graph, Namespace
from rdflib.namespace import RDF

from .core import Engine, REC, short
from .exercise import ExerciseResult

ARITH = Namespace("https://www.epistemic-ontology.net/arith#")

_BUILDERS = {
    ARITH.Addition: lambda a, b: a + b,
    ARITH.Subtraction: lambda a, b: a - b,
    ARITH.Multiplication: lambda a, b: a * b,
    ARITH.Division: lambda a, b: a / b,
}


class CompileError(ValueError):
    """Closed-world well-formedness failure: the description does not parse
    as an expression. OWL cannot see absence; the compiler can."""


def compile_expression(g: Graph, node) -> sp.Expr:
    """Walk one expression subgraph into a sympy expression."""
    if (node, RDF.type, ARITH.Numeral) in g:
        v = next(g.objects(node, ARITH.numericValue), None)
        if v is None:
            raise CompileError(f"{short(node)}: numeral without a numericValue")
        return sp.Integer(int(v))
    if (node, RDF.type, ARITH.Variable) in g:
        s = next(g.objects(node, ARITH.symbol), None)
        if s is None:
            raise CompileError(f"{short(node)}: variable without a symbol")
        return sp.Symbol(str(s))
    if (node, RDF.type, ARITH.Application) in g:
        op = next(g.objects(node, ARITH.operator), None)
        first = next(g.objects(node, ARITH.firstOperand), None)
        second = next(g.objects(node, ARITH.secondOperand), None)
        if op not in _BUILDERS:
            raise CompileError(f"{short(node)}: unknown or missing operator")
        if first is None or second is None:
            raise CompileError(f"{short(node)}: missing operand")
        return _BUILDERS[op](compile_expression(g, first),
                             compile_expression(g, second))
    raise CompileError(f"{short(node)}: not a compilable expression")


def equations_of(g: Graph, record) -> tuple:
    """Every arith:Equation among the record's parts (composedOf-descendants,
    the record itself included -- an equation record describes itself)."""
    seen, frontier, eqs = set(), [record], []
    while frontier:
        node = frontier.pop()
        if node in seen:
            continue
        seen.add(node)
        if (node, RDF.type, ARITH.Equation) in g:
            eqs.append(node)
        frontier.extend(g.objects(node, REC.composedOf))
    return tuple(sorted(eqs, key=str))


def exercise_description(engine: Engine, name) -> Optional[ExerciseResult]:
    """Exercise a record from its DESCRIPTION: compile every equation among
    its parts and check both sides agree. None = nothing described (the
    record may still have a hand-registered exercise, or be testimonial)."""
    g = engine.web.graph
    record = engine.resolve(name)
    eqs = equations_of(g, record)
    if not eqs:
        return None
    for eq in eqs:
        lhs = next(g.objects(eq, ARITH.lhs), None)
        rhs = next(g.objects(eq, ARITH.rhs), None)
        if lhs is None or rhs is None:
            return ExerciseResult(False, f"{short(eq)}: equation missing a side")
        try:
            left, right = compile_expression(g, lhs), compile_expression(g, rhs)
        except CompileError as e:
            return ExerciseResult(False, f"{short(eq)}: {e}")
        if sp.simplify(left - right) != 0:
            return ExerciseResult(
                False, f"fails at {short(eq)}: {left} ≠ {right} — the "
                       "description does not come together")
    return ExerciseResult(True, f"all {len(eqs)} described equation(s) close "
                                "— compiled from the subgraph, not hand-written")


def exercise_and_log(engine: Engine, name) -> Optional[ExerciseResult]:
    """Exercise from description AND log the act -- performative provenance:
    the run enters the revision log at a moment, so the warrant's lifecycle
    state (State.standing) is henceforth backed by a recorded act."""
    result = exercise_description(engine, name)
    if result is not None:
        engine.log_exercise(name, result.passed, note=result.detail)
    return result
