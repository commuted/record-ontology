"""
Forks: competing abductive explanations, their detection, corroboration, and
collapse (ROOT.md §10, exercised by the Neptune fixture's oracle).

Three commitments:

1. Fork-ness is structural but rivalry is content-level. Two ampliative
   inferences sharing a premise and concluding different records LOOK like a
   fork, yet the same shape covers independent convergence (Adams and
   Le Verrier both predicting the planet are not rivals). Incompatibility of
   content is not OWL-visible, so `structural_candidates` deliberately
   over-detects and an actual rivalry must be DECLARED -- a decision, logged
   as an escalation event (§13).

2. Corroboration is temporal (§13.3). A rival is corroborated by evidence
   that (a) arrived AFTER the fork opened (first-asserted at a later moment
   than the rivalry declaration), (b) is an empirical ground outside the
   rival's own ancestry, and (c) feeds a live inference consuming the rival's
   downstream. Without (a), an assumption baked into the rival's own
   derivation (Bode's law in the predictions) would masquerade as
   confirmation. "Forks collapse as observations ARRIVE" -- arrival is a
   moment, and the moment is load-bearing.

3. Collapse is an engine event over static structure. The losing branch stays
   in the graph (the history keeps it; nothing is deleted); the fork report
   marks it ECLIPSED. The static stratum never changes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Optional

from .core import REC, State, Web


@dataclass(frozen=True)
class Rivalry:
    """A declared fork between two conclusions. `moment` is the declaration's
    log position -- the moment the fork opened for the engine."""
    a: object
    b: object
    moment: int
    note: str = ""


@dataclass(frozen=True)
class Identity:
    """A declared equivalence between two records -- rivals proven one.
    Content-level like Rivalry (the proof is a record; declaring is a
    decision), logged with its moment. Identification PRE-EMPTS eclipse: a
    fork between identified records is 'identified', never 'resolved', even
    if fresh evidence later corroborates one formulation's downstream --
    that evidence accrues to the pair (fidelity pooling)."""
    a: object
    b: object
    moment: int
    note: str = ""


def identity_partners(state, record) -> frozenset:
    """The record plus everything identified with it (transitive closure)."""
    partners = {record}
    changed = True
    while changed:
        changed = False
        for ident in state.identities:
            pair = {ident.a, ident.b}
            if partners & pair and not pair <= partners:
                partners |= pair
                changed = True
    return frozenset(partners)


@dataclass(frozen=True)
class Corroboration:
    """One piece of fork-relevant support: a live inference whose premises
    join the rival's downstream with fresh empirical evidence."""
    inference: object
    conclusion: object
    fresh_leaves: frozenset


@dataclass(frozen=True)
class ForkReport:
    rivalry: Rivalry
    status: str        # "open" | "resolved" | "contested" | "moot" | "identified"
    winner: Optional[object]
    eclipsed: Optional[object]
    corroborations: Mapping        # rival -> tuple[Corroboration, ...]


# ---------------------------------------------------------------------------
# Structural closures
# ---------------------------------------------------------------------------

def ancestors(web: Web, r) -> frozenset:
    """The support closure above r: every inference and premise its derivation
    rests on (structurally -- independent of current support)."""
    seen: set = set()
    frontier = [r]
    while frontier:
        node = frontier.pop()
        for j in web.justifications_of.get(node, ()):
            for up in (j.inference, *j.premises):
                if up not in seen:
                    seen.add(up)
                    frontier.append(up)
    return frozenset(seen)


def downstream(web: Web, r) -> frozenset:
    """r plus everything derivable through it: conclusions of inferences that
    consume r or anything already downstream of it."""
    seen = {r}
    changed = True
    while changed:
        changed = False
        for concl, js in web.justifications_of.items():
            if concl not in seen and any(j.premises & seen for j in js):
                seen.add(concl)
                changed = True
    return frozenset(seen)


# ---------------------------------------------------------------------------
# Candidates, corroboration, and the fork report
# ---------------------------------------------------------------------------

def structural_candidates(web: Web) -> tuple:
    """Pairs of conclusions that LOOK like forks: distinct ampliative
    inferences sharing at least one premise, concluding different records.
    Over-detects on purpose (see module docstring); rivalry is declared, not
    derived."""
    amp = [(j, c) for c, js in web.justifications_of.items()
           for j in js if j.force == REC.Ampliative]
    found = {}
    for i, (j1, c1) in enumerate(amp):
        for j2, c2 in amp[i + 1:]:
            if j1.inference == j2.inference or c1 == c2:
                continue
            shared = j1.premises & j2.premises
            if shared:
                key = frozenset((c1, c2))
                found.setdefault(key, shared)
    return tuple((tuple(sorted(k, key=str)), v) for k, v in
                 sorted(found.items(), key=lambda kv: sorted(map(str, kv[0]))))


def corroborations(web: Web, state: State, rival, since_moment: int) -> tuple:
    """Evidence for one rival, per the temporal rule (module docstring)."""
    anc = ancestors(web, rival) | {rival}
    down = downstream(web, rival)
    out = []
    for concl, js in web.justifications_of.items():
        for j in js:
            if not state.is_live(j) or not state.supported.get(concl, False):
                continue
            if not (j.premises & down):
                continue
            fresh = frozenset(
                p for p in j.premises
                if p in web.grounds
                and REC.Empirical in web.warrants.get(p, ())
                and state.supported.get(p, False)
                and p not in anc and p not in down
                and state.first_asserted.get(p, -1) > since_moment
            )
            if fresh:
                out.append(Corroboration(inference=j.inference,
                                         conclusion=concl, fresh_leaves=fresh))
    return tuple(out)


def fork_report(web: Web, state: State, rivalry: Rivalry) -> ForkReport:
    """The fork's standing as of this state.

    identified -- the rivals were declared equivalent (Identity): the fork
                  DISSOLVES rather than collapsing. No winner, no eclipsed;
                  the incompatibility was an artifact of presentation.
                  Checked first: identification pre-empts eclipse.
    moot      -- neither rival is supported (e.g. the shared ancestry fell).
    resolved  -- exactly one rival stands, or exactly one is corroborated by
                 evidence that arrived after the fork opened. The loser is
                 ECLIPSED, not deleted.
    contested -- both corroborated (the calculus, §10, will have to weigh).
    open      -- both stand on the shared evidence alone.
    """
    a, b = rivalry.a, rivalry.b
    corr = {r: corroborations(web, state, r, rivalry.moment) for r in (a, b)}

    pair = frozenset((a, b))
    if any(frozenset((i.a, i.b)) == pair for i in state.identities):
        return ForkReport(rivalry, "identified", None, None, corr)

    standing = [r for r in (a, b) if state.supported.get(r, False)]

    if not standing:
        return ForkReport(rivalry, "moot", None, None, corr)
    if len(standing) == 1:
        winner = standing[0]
        loser = b if winner == a else a
        return ForkReport(rivalry, "resolved", winner, loser, corr)
    corroborated = [r for r in (a, b) if corr[r]]
    if len(corroborated) == 1:
        winner = corroborated[0]
        loser = b if winner == a else a
        return ForkReport(rivalry, "resolved", winner, loser, corr)
    if len(corroborated) == 2:
        return ForkReport(rivalry, "contested", None, None, corr)
    return ForkReport(rivalry, "open", None, None, corr)
