"""
The fidelity calculus (prototype) -- ROOT.md §10's combinatorial quantity.

Stance: fidelity is NOT probability-of-truth (a god's-eye measure of
confirmation would be the apple in numeric dress). It is a structured,
web-internal measure of INVARIANCE UNDER THE WEB'S OWN DYNAMICS -- how a
record's support survives re-derivation, retraction, transmission, replay.
That single stance unifies §2 (transmissibility), §10 (robustness under
revision) and §14 (rate-distortion / puncturing).

The object, not a scalar:
  label(r)  = the set of MINIMAL ENVIRONMENTS deriving r -- minimal sets of
              grounds (inference tokens included) sufficient to re-derive it.
              Classic ATMS (de Kleer). Everything else is a FUNCTION of the
              environment -- entailed, not stipulated:
    amp(e)        -- ampliative joints crossed = ampliative inference tokens
                     in e (set semantics de-duplicates shared ancestry, so
                     this is exact, not an upper bound)
    leaves(e)     -- e minus inference tokens: what must actually be believed
    grade(e)      -- the coarsest projection: DEFEASIBLE if any ampliative
                     joint, else the weakest leaf warrant. This is provably
                     the engine's Level (the demo asserts agreement), which
                     makes Level the calculus's coarsest projection, as
                     promised.
    via(e)        -- derived intermediates the environment passes through
                     (recovered from its inference tokens): where fork
                     variables live.

Two flows:
  forward   -- environments compose premises->conclusions; truth-preserving
               tokens are free, ampliative tokens attenuate; the punctual
               leaf obeys §2's zero-amplification by the min-law (it can
               anchor only the environment consisting of itself; in any
               larger environment it never raises the grade).
  backward  -- corroboration: a rival's fidelity gains the live environments
               of its downstream successes that contain FRESH empirical
               evidence, under forks.py's temporal rule (first-asserted
               after the rivalry opened). Evidence-for, kept distinct from
               derivations-of.

Scalars (counts, grades) are purpose-relative PROJECTIONS of this structure;
numeric plug-ins (priors etc.) are content -- records in the web -- never
framework. Known cliff: label size can blow up combinatorially at scale;
this prototype fixes the exact semantics at exemplar scale and lets any
future approximation be judged against it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Optional

from .core import REC, Level, State, WARRANT_LEVEL, Web, short
from .forks import Rivalry, corroborations, identity_partners


# ---------------------------------------------------------------------------
# Structural labels (state-independent)
# ---------------------------------------------------------------------------

def inference_tokens(web: Web) -> frozenset:
    return frozenset(j.inference for j in web.justifications())


def _forces(web: Web) -> Mapping:
    return {j.inference: j.force for j in web.justifications()}


def _minimize(envs) -> frozenset:
    """Keep only subset-minimal environments. Minimality is Pareto-complete
    here: e1 <= e2 implies amp(e1) <= amp(e2), so no dominated environment
    hides a better attenuation."""
    kept: list = []
    for e in sorted(envs, key=len):
        if not any(k <= e for k in kept):
            kept.append(e)
    return frozenset(kept)


def labels(web: Web) -> Mapping:
    """ATMS labels for every record: record -> frozenset of minimal
    environments (each a frozenset of grounds, inference tokens included).
    Structural -- independent of any state; support at a state is
    'some environment is a subset of the asserted grounds'."""
    memo: dict = {}
    in_progress: set = set()

    def lab(n):
        if n in memo:
            return memo[n]
        if n in web.grounds:
            memo[n] = frozenset({frozenset({n})})
            return memo[n]
        if n in in_progress:
            raise ValueError(f"cycle through {short(n)}: labels need a DAG")
        in_progress.add(n)
        envs: set = set()
        for j in web.justifications_of.get(n, ()):
            combos = [frozenset({j.inference})]
            for p in j.premises:
                combos = [c | e for c in combos for e in lab(p)]
            envs.update(combos)
        in_progress.discard(n)
        memo[n] = _minimize(envs)
        return memo[n]

    for n in web.universe:
        lab(n)
    return memo


# ---------------------------------------------------------------------------
# Entailed annotations (functions of an environment)
# ---------------------------------------------------------------------------

def amp(web: Web, env) -> int:
    forces = _forces(web)
    return sum(1 for g in env if forces.get(g) == REC.Ampliative)


def leaves(web: Web, env) -> frozenset:
    return frozenset(env - inference_tokens(web))


def _ground_level(web: Web, g) -> Level:
    ws = [WARRANT_LEVEL[w] for w in web.warrants.get(g, ()) if w in WARRANT_LEVEL]
    return min(ws) if ws else Level.DEFEASIBLE


def leaf_level(web: Web, env) -> Level:
    """The weakest leaf warrant in the environment (unmarked leaves default
    to defeasible).

    A subtlety the engine's semantics dictates: an inference token counts as
    a leaf in ITS OWN singleton environment (accepting the inference is a
    defeasible commitment like any unmarked ground), but in a composite
    environment it contributes through amp() only -- its FORCE gates the
    conclusion, its own acceptance-level does not. This mirrors
    core.compute_state exactly, which is what keeps grade ⇔ Level agreement.
    A composite environment with no leaves at all (premise-less machinery)
    is vacuously certain."""
    if len(env) == 1:
        (g,) = env
        return _ground_level(web, g)
    lvls = [_ground_level(web, leaf) for leaf in leaves(web, env)]
    return min(lvls) if lvls else Level.CERTAIN


def grade(web: Web, env) -> Level:
    """The coarsest projection: one ampliative joint caps the environment at
    defeasible (§2, force as the hinge); otherwise the weakest leaf decides.
    The punctual leaf's zero-amplification is the min-law: it can be the
    grade only of the environment that is exactly itself."""
    if amp(web, env) > 0:
        return Level.DEFEASIBLE
    return leaf_level(web, env)


def via(web: Web, env) -> frozenset:
    """Derived intermediates this environment passes through, recovered from
    its inference tokens. Fork variables live here: if a declared rival is in
    via(e), then e depends on that fork's choice."""
    return frozenset(
        c for c, js in web.justifications_of.items()
        if any(j.inference in env for j in js)
    )


# ---------------------------------------------------------------------------
# The fidelity object (state-relative)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class EnvView:
    """One environment, fully annotated, as of a state."""
    env: frozenset
    live: bool          # env subset of the asserted grounds
    amp: int
    leaves: frozenset
    grade: Level
    via: frozenset


@dataclass(frozen=True)
class FidelityReport:
    """The fidelity of one record as of one state: its derivations (base) and
    its evidence-for (corroborating), kept distinct. Scalars below are
    projections; the environments are the quantity."""
    record: object
    base: tuple            # EnvViews of the record's own label
    corroborating: tuple   # EnvViews of fresh downstream successes (backward flow)

    @property
    def breadth(self) -> int:
        return sum(1 for v in self.base if v.live)

    @property
    def best_grade(self) -> Optional[Level]:
        live = [v.grade for v in self.base if v.live]
        return max(live) if live else None

    @property
    def shared_grounds(self) -> frozenset:
        """The common fate: grounds every live derivation rests on. Retract
        one of these and the record falls with no fallback."""
        live = [v.env for v in self.base if v.live]
        if not live:
            return frozenset()
        out = set(live[0])
        for e in live[1:]:
            out &= e
        return frozenset(out)


def _view(web: Web, state: State, env) -> EnvView:
    return EnvView(env=env, live=state.env_live(env), amp=amp(web, env),
                   leaves=leaves(web, env), grade=grade(web, env),
                   via=via(web, env))


def fidelity(web: Web, state: State, record,
             label_map: Optional[Mapping] = None) -> FidelityReport:
    """The fidelity object of one record as of one state.

    IDENTITY POOLING: if the record has been identified with others
    (Engine.identify -- rivals proven one), the report pools the whole
    equivalence class: base environments of every partner (breadth genuinely
    increases -- the one case where 'two derivations' means independent
    support, because the environments differ in nearly everything except the
    conclusion) and corroborating environments earned by any partner.

    Backward corroboration is currently defined only through DECLARED
    rivalries (the temporal freshness rule needs a fork-opening moment to be
    relative to); a record that is no rivalry's rival gets an empty
    corroborating tuple. Generalising freshness to non-fork records is an
    open question for the calculus, not an oversight of the code."""
    label_map = label_map if label_map is not None else labels(web)
    partners = identity_partners(state, record)
    base_envs: set = set()
    for p in partners:
        base_envs.update(label_map.get(p, ()))
    base = tuple(sorted((_view(web, state, e) for e in base_envs),
                        key=lambda v: sorted(map(str, v.env))))
    corr_envs: set = set()
    for rivalry in state.rivalries:
        for p in partners:
            if p not in (rivalry.a, rivalry.b):
                continue
            for c in corroborations(web, state, p, rivalry.moment):
                for e in label_map.get(c.conclusion, ()):
                    if state.env_live(e):
                        corr_envs.add(e)
    corroborating = tuple(sorted((_view(web, state, e) for e in corr_envs),
                                 key=lambda v: sorted(map(str, v.env))))
    return FidelityReport(record=record, base=base, corroborating=corroborating)


def fork_fidelity(web: Web, state: State, rivalry: Rivalry,
                  label_map: Optional[Mapping] = None) -> Mapping:
    """Both rivals' fidelity objects side by side. Structural dominance --
    one rival holding a live corroborating environment the other has no
    counterpart to -- is what forks.fork_report reads as 'resolved'; this
    view shows the environments behind that verdict."""
    label_map = label_map if label_map is not None else labels(web)
    return {r: fidelity(web, state, r, label_map) for r in (rivalry.a, rivalry.b)}


def supported_by_labels(web: Web, state: State,
                        label_map: Optional[Mapping] = None) -> Mapping:
    """Support recomputed from labels alone: some environment is live.
    Must agree with core.compute_state's fixpoint for every record at every
    moment -- the calculus's confluence check (the demo asserts it).
    (Deliberately un-pooled: identity affects the fidelity VIEW, never
    support -- each formulation still stands on its own derivation.)"""
    label_map = label_map if label_map is not None else labels(web)
    return {n: any(state.env_live(e) for e in label_map[n]) for n in web.universe}


# ---------------------------------------------------------------------------
# Explananda -- the second stub species (support that never rose)
# ---------------------------------------------------------------------------

def theoretical(web: Web, env) -> bool:
    """An environment is THEORETICAL iff it carries at least one formally
    warranted leaf -- the mathematical machinery a derivation runs on.

    This is a modelling CONVENTION, not metaphysics: theory derivations in
    the fixtures carry a formal-machinery record (perturbation theory, the
    phase-integral method, the wave equation's mathematics); observation
    reports run leaf -> report with no formal leaf. The convention has a
    known limit -- observation is theory-laden (instruments embed formalism)
    -- which a finer model may some day represent; at that point this
    predicate, not the callers, is what changes."""
    return any(REC.Formal in web.warrants.get(leaf, ())
               for leaf in leaves(web, env))


def explananda(web: Web, state: State,
               label_map: Optional[Mapping] = None) -> tuple:
    """The open questions of the era: derived records that are SUPPORTED but
    only observationally -- no live environment is theoretical. The second
    stub species, complementing Engine.stubs():

      stubs()      -- withdrawn conclusions: support that FELL   (drives repair)
      explananda() -- unexplained phenomena: support that never  (drives
                      ROSE past observation                       discovery)

    Fine structure 1891-1916 is the type case: empirically live the whole
    time, flagged here until Sommerfeld's derivation goes live, at which
    point it resolves -- refinement = a stub resolving (§10), visible.
    Disjoint from stubs() by construction (supported vs unsupported)."""
    label_map = label_map if label_map is not None else labels(web)
    out = []
    for r in sorted(web.derived, key=str):
        if not state.supported.get(r, False):
            continue
        live = [e for e in label_map[r] if state.env_live(e)]
        if live and not any(theoretical(web, e) for e in live):
            out.append(r)
    return tuple(out)
