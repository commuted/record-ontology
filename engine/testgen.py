"""
Generated suites: the web's own machinery, read back as test cases.

The engine's disciplines each IMPLY a family of checks, and a loaded web
supplies the instances mechanically -- nothing here is written per fixture.
The suite is derived from the web the way the arith compiler derives an
exercise from a description (§15): generation, not enumeration. Six families:

  replay       (§13.3)  every log prefix recomputes to the same state, and
                        the label calculus agrees with the fixpoint at every
                        moment -- determinism and confluence, per moment.
  sufficiency  (§10)    every minimal environment in a record's label, when
                        asserted alone, carries the record. The label's
                        promise, tested environment by environment.
  minimality   (§10)    no environment stays sufficient with any member
                        removed -- asserted with one member withheld, the
                        record must fall. Minimal means minimal.
  level        (§10)    the engine's Level equals the calculus's best live
                        grade for every supported record -- the coarsest-
                        projection theorem, asserted record by record.
  category     (§14)    asserting or retracting any DERIVED record raises:
                        derived records regenerate, they are never asserted.
                        The API's contract, tried against every derived node.
  exercise     (§15.3)  every record with a runnable description (an arith
                        subgraph or a hand-registered exercise) runs to a
                        result; where the log already records a standing,
                        the fresh run must AGREE with it. And the PRETENDER
                        ALARM: a record whose exercise FAILS while it stands
                        unexorcised in the current state is formal warrant
                        worn without the form -- the §15.3 detector firing
                        from a generated case, no hand-written test naming
                        the culprit.

A generated suite is a tuple of Cases; `run_suite` executes them. Sidecar,
like compile.py and exercise.py: imports sympy through them, so the engine
package never imports this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping, Optional

from .compile import equations_of, exercise_description
from .core import Engine, State, compute_state, short
from .exercise import EXERCISES, exercise as registry_exercise
from .fidelity import grade, labels as atms_labels, supported_by_labels


@dataclass(frozen=True)
class CaseResult:
    ok: bool
    detail: str = ""


@dataclass(frozen=True)
class Case:
    kind: str
    subject: str
    run: Callable[[], CaseResult]


# ---------------------------------------------------------------------------
# Families
# ---------------------------------------------------------------------------

def _replay_cases(eng: Engine, label_map: Mapping) -> list:
    def probe(moment: int) -> Callable[[], CaseResult]:
        def run() -> CaseResult:
            events = eng.log.upto(moment)
            s1 = compute_state(eng.web, events)
            s2 = compute_state(eng.web, events)
            if s1 != s2:
                return CaseResult(False, "recomputation disagreed with itself")
            via_labels = supported_by_labels(eng.web, s1, label_map)
            bad = [n for n in eng.web.universe
                   if via_labels[n] != s1.supported[n]]
            if bad:
                return CaseResult(
                    False, "fixpoint/calculus split on "
                    + ", ".join(sorted(map(short, bad))))
            return CaseResult(True, "deterministic; calculus agrees")
        return run

    return [Case("replay", f"moment {m}", probe(m))
            for m in range(eng.log.now + 1)]


def _assert_exactly(eng: Engine, grounds) -> Optional[State]:
    """A synthetic state in which precisely these grounds are asserted --
    or None when the environment is not directly assertable (a member is
    itself derived, e.g. an inference token something concludes)."""
    if any(g not in eng.web.grounds for g in grounds):
        return None
    log_cls = type(eng.log)
    log = log_cls()
    for g in sorted(grounds, key=str):
        log.append("assert", g, note="testgen: synthetic environment")
    return compute_state(eng.web, log.upto())


def _label_cases(eng: Engine, label_map: Mapping) -> list:
    cases: list = []
    for r in sorted(eng.web.derived, key=str):
        for i, env in enumerate(sorted(label_map[r], key=lambda e: sorted(map(str, e)))):
            def suff(r=r, env=env) -> CaseResult:
                s = _assert_exactly(eng, env)
                if s is None:
                    return CaseResult(True, "environment not directly "
                                            "assertable; vacuous")
                return (CaseResult(True, "environment carries the record")
                        if s.supported[r]
                        else CaseResult(False, "asserted whole, it does not"))
            cases.append(Case("sufficiency", f"{short(r)} env#{i}", suff))

            for g in sorted(env, key=str):
                def minim(r=r, env=env, g=g) -> CaseResult:
                    s = _assert_exactly(eng, env - {g})
                    if s is None:
                        return CaseResult(True, "not directly assertable; "
                                                "vacuous")
                    return (CaseResult(False,
                            f"still supported without {short(g)} -- "
                            "the environment was not minimal")
                            if s.supported[r]
                            else CaseResult(True, f"falls without {short(g)}"))
                cases.append(Case("minimality",
                                  f"{short(r)} env#{i} − {short(g)}", minim))
    return cases


def _level_cases(eng: Engine, label_map: Mapping) -> list:
    state = eng.state()

    def probe(r) -> Callable[[], CaseResult]:
        def run() -> CaseResult:
            live = [e for e in label_map[r] if state.env_live(e)]
            best = max((grade(eng.web, e) for e in live), default=None)
            if best == state.level[r]:
                return CaseResult(True, f"Level == best grade ({best})")
            return CaseResult(False, f"engine {state.level[r]} vs "
                                     f"calculus {best}")
        return run

    return [Case("level", short(r), probe(r))
            for r in sorted(eng.web.universe, key=str)
            if state.supported[r]]


def _category_cases(eng: Engine) -> list:
    def probe(r) -> Callable[[], CaseResult]:
        def run() -> CaseResult:
            for op in (eng.assert_ground, eng.retract):
                try:
                    op(r)
                except ValueError:
                    continue
                return CaseResult(False, f"{op.__name__} accepted a "
                                         "derived record")
            return CaseResult(True, "assert and retract both refuse")
        return run

    return [Case("category", short(r), probe(r))
            for r in sorted(eng.web.derived, key=str)]


def _exercisable(eng: Engine):
    """Every record with a runnable description: arith subgraph (compiler),
    orbital model (orbits sidecar), hand registry. Yields (record, runner)."""
    from .core import REC
    from .orbits import exercise_model, parse_model
    seen = set()
    for r in sorted(eng.web.universe, key=str):
        if equations_of(eng.web.graph, r):
            seen.add(short(r))
            yield r, (lambda r=r: exercise_description(eng, r))
            continue
        lit = next(eng.web.graph.objects(r, REC.formulation), None)
        if lit is not None and parse_model(str(lit)) is not None:
            seen.add(short(r))
            yield r, (lambda r=r: exercise_model(eng, r))
    for name in sorted(EXERCISES):
        if name in seen:
            continue
        try:
            r = eng.resolve(name)
        except KeyError:
            continue  # registry entry for a fixture not in this web
        yield r, (lambda name=name: registry_exercise(name))


def _exercise_cases(eng: Engine) -> list:
    state = eng.state()
    cases: list = []
    for r, runner in _exercisable(eng):
        def closes(r=r, runner=runner) -> CaseResult:
            res = runner()
            if res is None:
                return CaseResult(False, "described yet not runnable")
            standing = state.standing(r)
            if standing == "confirmed" and not res.passed:
                return CaseResult(False, "log says confirmed; fresh run fails")
            if standing in ("failed", "exorcised") and res.passed:
                return CaseResult(False, f"log says {standing}; fresh run "
                                         "passes")
            return CaseResult(True, f"runs; outcome "
                                    f"{'passes' if res.passed else 'fails'}, "
                                    f"standing '{standing}' consistent")
        cases.append(Case("exercise", short(r), closes))

        def alarm(r=r, runner=runner) -> CaseResult:
            res = runner()
            pretender = (res is not None and not res.passed
                         and state.supported.get(r, False)
                         and r not in state.exorcised)
            if pretender:
                return CaseResult(False, "PRETENDER: exercise fails while "
                                         "the record stands unexorcised "
                                         "(§15.3) -- expel or repair")
            return CaseResult(True, "no pretense: outcome and standing agree")
        cases.append(Case("alarm", short(r), alarm))
    return cases


# ---------------------------------------------------------------------------
# The suite
# ---------------------------------------------------------------------------

def generate(eng: Engine, label_map: Optional[Mapping] = None) -> tuple:
    """The full generated suite for one engine as it currently stands."""
    label_map = label_map if label_map is not None else atms_labels(eng.web)
    return tuple(
        _replay_cases(eng, label_map)
        + _label_cases(eng, label_map)
        + _level_cases(eng, label_map)
        + _category_cases(eng)
        + _exercise_cases(eng)
    )


def run_suite(cases) -> tuple:
    """(passures, failures) -- each a list of (case, result)."""
    passed, failed = [], []
    for c in cases:
        res = c.run()
        (passed if res.ok else failed).append((c, res))
    return passed, failed


def counts_by_kind(cases) -> Mapping:
    out: dict = {}
    for c in cases:
        out[c.kind] = out.get(c.kind, 0) + 1
    return out
