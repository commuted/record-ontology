"""
Core of the propagation engine: structure extraction, the revision log
(moments), and support/level computation.

Design notes (the strata rule, ROOT.md §10):
- The RDF graphs are READ-ONLY structure. The engine never writes a triple.
- Support is computed from scratch for any log prefix (23-node exemplars make
  this trivially cheap and keeps the semantics transparent). A production
  engine would relabel incrementally, ATMS-style; the *semantics* is fixed
  here and any incremental version must agree with it.
- "Ground" is structural: a record no inference concludes. Grounds enter the
  web by log events (assert/retract); derived records enter only by
  re-derivation. Only grounds may be asserted or retracted -- retracting a
  derived record is a category error (retract its grounds instead; §14).
- rec:composedOf is deliberately NOT a support edge: composition is mereology,
  not justification. (Whether a composite should weaken when its parts go out
  belongs to the fidelity calculus, not this prototype.)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Iterable, Mapping, Optional, Sequence

from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, RDFS

REC = Namespace("https://www.epistemic-ontology.net/record#")


def short(node: URIRef) -> str:
    s = str(node)
    return s.rsplit("#", 1)[-1] if "#" in s else s.rsplit("/", 1)[-1]


# ---------------------------------------------------------------------------
# Levels -- the coarse, warrant-entailed grade used for re-leveling.
# ---------------------------------------------------------------------------
# NOT the fidelity calculus (that is a later, combinatorial quantity, §10);
# just enough grade structure to demonstrate re-leveling:
#   CERTAIN    -- formal: internally completable (§2).
#   PUNCTUAL   -- self-verifying: maximally certain, zero amplification (§2).
#                 Its non-extensibility (nothing may be *built* on it) belongs
#                 to the real calculus; no current fixture exercises it.
#   DEFEASIBLE -- empirical/given, and anything downstream of ampliative force.

class Level(IntEnum):
    DEFEASIBLE = 1
    PUNCTUAL = 2
    CERTAIN = 3


WARRANT_LEVEL = {
    REC.Formal: Level.CERTAIN,
    REC.SelfVerifying: Level.PUNCTUAL,
    REC.Empirical: Level.DEFEASIBLE,
}


# ---------------------------------------------------------------------------
# Static structure (read-only)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Justification:
    """One way a conclusion is supported: an inference record, its premises,
    and its force. A record is derived iff it has at least one of these."""
    inference: URIRef
    premises: frozenset
    force: URIRef  # REC.TruthPreserving | REC.Ampliative


@dataclass(frozen=True)
class Web:
    """The derivation web as read from RDF. Immutable; the engine's statics."""
    universe: frozenset            # every record node in play
    grounds: frozenset             # records no inference concludes
    derived: frozenset             # universe - grounds
    warrants: Mapping              # record -> frozenset of warrant IRIs
    justifications_of: Mapping     # conclusion -> tuple[Justification, ...]
    labels: Mapping                # record -> rdfs:label (for reporting)
    graph: Graph                   # the merged RDF, read-only (companion
                                   # vocabularies, formulations, descriptions)

    def justifications(self) -> Iterable[Justification]:
        for js in self.justifications_of.values():
            yield from js


def load_web(paths: Sequence) -> Web:
    g = Graph()
    for p in paths:
        g.parse(str(p), format="turtle")

    universe = set(g.subjects(RDF.type, REC.Record))
    # Anything used as a premise or conclusion is in play even if untyped.
    universe |= set(g.objects(None, REC.hasPremise))
    universe |= set(g.objects(None, REC.concludes))
    universe |= set(g.subjects(REC.hasPremise, None))
    universe |= set(g.subjects(REC.concludes, None))

    justifications_of: dict = {}
    for inf, concl in g.subject_objects(REC.concludes):
        premises = frozenset(g.objects(inf, REC.hasPremise))
        # No asserted force => treated as ampliative, the conservative reading
        # (an unmarked joint must not silently pass certainty through).
        force = next(g.objects(inf, REC.hasForce), REC.Ampliative)
        justifications_of.setdefault(concl, []).append(
            Justification(inference=inf, premises=premises, force=force))

    derived = frozenset(justifications_of)
    grounds = frozenset(universe - derived)
    warrants = {r: frozenset(g.objects(r, REC.hasWarrant)) for r in universe}
    labels = {r: str(next(g.objects(r, RDFS.label), short(r))) for r in universe}

    return Web(
        universe=frozenset(universe),
        grounds=grounds,
        derived=derived,
        warrants=warrants,
        justifications_of={c: tuple(js) for c, js in justifications_of.items()},
        labels=labels,
        graph=g,
    )


# ---------------------------------------------------------------------------
# The revision log -- the carrier of moments (ROOT.md §13.3)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Event:
    """One appended fact of the dynamics. moment = position in the log: the
    order-derived time. Clock time, if wanted, is content (a note), never the
    index -- the moment is load-bearing, the clock is overlay."""
    moment: int
    kind: str          # "assert" | "retract" | "rivals" | "identify"
                       #   | "exorcise" | "exercise"
    subjects: tuple    # (record,) or (a, b) for rivals/identify
    note: str = ""
    flag: Optional[bool] = None   # exercise outcome (passed?), else None


class RevisionLog:
    """Append-only. Never rewritten: a retraction is a NEW moment appended --
    'a record to amend rather than a thread to remember,' applied to time."""

    def __init__(self) -> None:
        self._events: list = []

    def append(self, kind: str, *subjects, note: str = "",
               flag: Optional[bool] = None) -> Event:
        ev = Event(moment=len(self._events), kind=kind,
                   subjects=tuple(subjects), note=note, flag=flag)
        self._events.append(ev)
        return ev

    @property
    def now(self) -> int:
        """The latest moment (-1 when empty)."""
        return len(self._events) - 1

    def upto(self, moment: Optional[int] = None) -> Sequence[Event]:
        if moment is None:
            return tuple(self._events)
        return tuple(self._events[: moment + 1])


# ---------------------------------------------------------------------------
# State -- everything true of the web as of a moment (computed, never stored)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class State:
    moment: int
    asserted: frozenset            # grounds currently in
    first_asserted: Mapping        # ground -> moment of first assertion
    rivalries: tuple               # forks declared so far (see forks.Rivalry)
    identities: tuple              # equivalences declared (see forks.Identity)
    exorcised: frozenset           # grounds whose warrant claim failed exercise
    exercised: Mapping             # record -> (moment, passed) of last exercise
    supported: Mapping             # record -> bool
    level: Mapping                 # record -> Level | None (None when out)

    def standing(self, record) -> str:
        """The §15.3 lifecycle state of a warrant claim:
        'exorcised'   -- expelled (a decision, after failure);
        'confirmed'   -- exercised and passed (warrant earned, at a moment);
        'failed'      -- exercised and did not pass; expulsion pending (§13);
        'unexercised' -- claimed only: testimonially held (§15.2)."""
        if record in self.exorcised:
            return "exorcised"
        if record in self.exercised:
            return "confirmed" if self.exercised[record][1] else "failed"
        return "unexercised"

    def is_live(self, j: Justification) -> bool:
        """A justification carries support iff its inference record is itself
        supported and every premise is supported."""
        return (self.supported.get(j.inference, False)
                and all(self.supported.get(p, False) for p in j.premises))

    def env_live(self, env) -> bool:
        """An environment carries support iff all its grounds are asserted
        and none is exorcised -- a broken proof transmits nothing (§15.3)."""
        return env <= self.asserted and not (env & self.exorcised)


def compute_state(web: Web, events: Sequence[Event]) -> State:
    from .forks import Identity, Rivalry  # local import to avoid a cycle

    asserted: set = set()
    first_asserted: dict = {}
    rivalries: list = []
    identities: list = []
    exorcised: set = set()
    exercised: dict = {}
    for ev in events:
        if ev.kind == "assert":
            (r,) = ev.subjects
            asserted.add(r)
            first_asserted.setdefault(r, ev.moment)
        elif ev.kind == "retract":
            (r,) = ev.subjects
            asserted.discard(r)
        elif ev.kind == "rivals":
            a, b = ev.subjects
            rivalries.append(Rivalry(a=a, b=b, moment=ev.moment, note=ev.note))
        elif ev.kind == "identify":
            a, b = ev.subjects
            identities.append(Identity(a=a, b=b, moment=ev.moment, note=ev.note))
        elif ev.kind == "exorcise":
            (r,) = ev.subjects
            exorcised.add(r)
        elif ev.kind == "exercise":
            (r,) = ev.subjects
            exercised[r] = (ev.moment, bool(ev.flag))

    # -- support: monotone fixpoint from all-False (recompute-from-scratch
    #    makes retraction trivially correct; see module docstring) -----------
    supported = {n: False for n in web.universe}
    changed = True
    while changed:
        changed = False
        for n in web.universe:
            if n in web.grounds:
                # An exorcised ground keeps its place in the graph and the
                # log, but its warrant claim failed exercise: it can no
                # longer stand or transmit support (§15.3).
                s = n in asserted and n not in exorcised
            else:
                s = any(
                    supported.get(j.inference, False)
                    and all(supported.get(p, False) for p in j.premises)
                    for j in web.justifications_of.get(n, ())
                )
            if s != supported[n]:
                supported[n] = s
                changed = True

    # -- levels: warrant-entailed for grounds; propagated through force ------
    level: dict = {n: None for n in web.universe}
    for n in web.grounds:
        if supported[n]:
            ws = [WARRANT_LEVEL[w] for w in web.warrants.get(n, ()) if w in WARRANT_LEVEL]
            # Patchwork grounds take their weakest warrant; unmarked grounds
            # default to defeasible.
            level[n] = min(ws) if ws else Level.DEFEASIBLE
    changed = True
    while changed:
        changed = False
        for n in web.derived:
            if not supported[n]:
                continue
            candidates = []
            for j in web.justifications_of[n]:
                if not (supported.get(j.inference, False)
                        and all(supported.get(p, False) for p in j.premises)):
                    continue
                if j.force == REC.TruthPreserving:
                    plevels = [level[p] for p in j.premises]
                    if any(l is None for l in plevels):
                        continue  # not yet computed this pass
                    # Truth-preserving passes through what the premises HAD --
                    # deduction over defeasible leaves does not mint certainty.
                    candidates.append(min(plevels) if plevels else Level.CERTAIN)
                else:
                    # Ampliative adds content: defeasible even from certain
                    # premises (§2, force as the hinge).
                    candidates.append(Level.DEFEASIBLE)
            best = max(candidates) if candidates else None
            if best != level[n]:
                level[n] = best
                changed = True

    return State(
        moment=events[-1].moment if events else -1,
        asserted=frozenset(asserted),
        first_asserted=dict(first_asserted),
        rivalries=tuple(rivalries),
        identities=tuple(identities),
        exorcised=frozenset(exorcised),
        exercised=dict(exercised),
        supported=supported,
        level=level,
    )


# ---------------------------------------------------------------------------
# Engine facade
# ---------------------------------------------------------------------------

class Engine:
    """Load the static web, seed the log with its grounds, then move through
    moments: assert/retract grounds, declare rivalries, view any state as-of
    any moment. `defer` names grounds present in the static graph that should
    NOT be seeded -- they arrive later, by explicit events (this is how a
    fixture re-enacts history: evidence arriving after a fork opens)."""

    def __init__(self, *paths, defer: Sequence[str] = ()) -> None:
        self.web = load_web(paths)
        self.log = RevisionLog()
        deferred = {self.resolve(name) for name in defer}
        for gnd in sorted(self.web.grounds, key=str):
            if gnd not in deferred:
                self.log.append("assert", gnd, note="seed: ground in the static graph")

    # -- naming ---------------------------------------------------------------
    def resolve(self, name) -> URIRef:
        """Accept a full IRI or a unique local name (#suffix)."""
        if isinstance(name, URIRef):
            return name
        if str(name).startswith("http"):
            return URIRef(name)
        matches = [n for n in self.web.universe if short(n) == str(name)]
        if len(matches) != 1:
            raise KeyError(f"{name!r} resolves to {len(matches)} records")
        return matches[0]

    # -- dynamics (all of it: append events) -----------------------------------
    def assert_ground(self, name, note: str = "") -> Event:
        r = self.resolve(name)
        if r not in self.web.grounds:
            raise ValueError(
                f"{short(r)} is derived; derived records regenerate by "
                "re-derivation and are never asserted (§14)")
        return self.log.append("assert", r, note=note)

    def retract(self, name, note: str = "") -> Event:
        r = self.resolve(name)
        if r not in self.web.grounds:
            raise ValueError(
                f"{short(r)} is derived; retract its grounds instead (§14)")
        return self.log.append("retract", r, note=note)

    def declare_rivals(self, a, b, note: str = "") -> Event:
        """Rivalry (fork-ness between two conclusions) is content-level: OWL
        cannot see it and structure alone over-detects it, so declaring it is
        a decision -- an escalation record in the log (§13)."""
        return self.log.append("rivals", self.resolve(a), self.resolve(b), note=note)

    def log_exercise(self, name, passed: bool, note: str = "") -> Event:
        """Record the ACT of exercising -- PERFORMATIVE PROVENANCE (§15.2/.3).
        A formal genealogy bottoms out in acts of derivation, and this is
        one, logged at a moment: the event is the act's own record, so the
        earned warrant now has a genealogy ('exercised at m, passed').
        Two warrants stack here: the exercise-event's record is
        performatively warranted (the run happened -- the log attests the
        act), while what it confirms is formal (the content). A failed
        exercise does NOT exorcise by itself -- expulsion is a separate
        decision (§13), taken by Engine.exorcise."""
        r = self.resolve(name)
        return self.log.append("exercise", r, note=note, flag=passed)

    def exorcise(self, name, note: str = "") -> Event:
        """Withdraw a ground's warrant claim after a failed exercise
        (ROOT.md §15.3). What is expelled is a PRETENDER -- formal warrant
        worn without the form -- not the record: the node stays in the graph
        and the log (history keeps the document; records ABOUT it are
        untouched), but it can no longer stand or transmit support, and
        everything resting on it cascades away. No reversal event exists on
        purpose: a repaired proof is a NEW record, not a restoration."""
        r = self.resolve(name)
        if r not in self.web.grounds:
            raise ValueError(
                f"{short(r)} is derived; exorcise the machinery it rests on "
                "instead (§15.3)")
        return self.log.append("exorcise", r, note=note)

    def identify(self, a, b, note: str = "") -> Event:
        """Declare two records equivalent -- rivals proven one (matrix vs
        wave mechanics, 1926). The mirror image of declare_rivals and equally
        content-level: equivalence takes a proof (itself a record, formally
        warranted), so the engine cannot derive it; an agent declares it and
        the declaration is logged with its moment. A fork between identified
        records DISSOLVES rather than collapsing: no winner, no eclipsed
        (forks.fork_report), and the pair's environments pool
        (fidelity.fidelity)."""
        return self.log.append("identify", self.resolve(a), self.resolve(b), note=note)

    # -- views ------------------------------------------------------------------
    def state(self, moment: Optional[int] = None) -> State:
        return compute_state(self.web, self.log.upto(moment))

    def stubs(self, state: State) -> tuple:
        """Open stubs (§10): conclusions whose support is currently withdrawn
        -- first-class holes, awaiting evidence."""
        return tuple(sorted((n for n in self.web.derived if not state.supported[n]),
                            key=str))

    def diff(self, m_old: int, m_new: Optional[int] = None) -> tuple:
        """What propagated between two moments: (record, (sup, lvl) old, new)."""
        a, b = self.state(m_old), self.state(m_new)
        out = []
        for n in sorted(self.web.universe, key=str):
            old = (a.supported[n], a.level[n])
            new = (b.supported[n], b.level[n])
            if old != new:
                out.append((n, old, new))
        return tuple(out)

    def label(self, node) -> str:
        return self.web.labels.get(node, short(node))
