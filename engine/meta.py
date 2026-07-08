"""
The meta layer: reasoning ABOUT the web's open items -- "observe X to resolve Y".

Everything below is read off structure the engine already computes; nothing
here adds vocabulary or events. Three instruments:

1. PLANS (stubs and explananda). A stub is support that fell; an explanandum
   is support that never rose past observation (fidelity.explananda). Both
   are HOLES with a shape: the record's ATMS label says exactly which
   minimal environments would carry it, and the state says which grounds
   each environment still lacks. The DEFICIT of an environment is that gap,
   and a deficit's members sort by warrant into
       observe (empirical -- only the world supplies these),
       derive  (formal   -- an agent can supply these by derivation/exercise),
       secure  (everything else -- conventions, unmarked grounds).
   A plan is a minimal deficit, ranked smallest-first: the cheapest route to
   resolution the web itself licenses. An environment touching an exorcised
   ground is BLOCKED, not deficient -- repair is a new record (§15.3), so no
   plan is issued for it. For an explanandum the label is filtered to its
   THEORETICAL environments (fidelity.theoretical): the plan names what would
   let support rise past observation -- and when no theoretical environment
   exists at all, the honest plan is "discovery needed": the web contains no
   route, and only new records (a new abduction) can supply one. That absence
   is the discovery signal, stated rather than hidden.

2. DISCRIMINATORS (open forks). forks.corroborations is retrospective --
   evidence that HAS arrived. Its mirror image is prospective: for each
   unsupported empirical ground g, would asserting g NOW corroborate a rival,
   under exactly the retrospective rule (outside the rival's ancestry and
   downstream, feeding an inference that consumes the rival's downstream and
   would go live)? Freshness is automatic -- a future assertion's moment is
   later than the fork's. A ground that would corroborate EXACTLY ONE rival
   discriminates: observing it resolves the fork whichever way it lands
   (arrival collapses it one way; its absence, §13's skips aside, leaves the
   other standing). This is experiment design as a query over the DAG --
   what the engine would have told Le Verrier: point a telescope HERE.

3. THE PUNCTURE REPORT (grooming, §14.2). The §14.2 partition, computed:
     kept, constituted -- supported grounds whose warrant is provenance-
                          constituted (empirical / self-verifying / unmarked):
                          no derivation regenerates them; they ARE the asset.
     kept, pointers    -- supported FORMAL grounds: machinery. Regenerable in
                          principle from outside the web, kept as pointers.
     regenerable       -- supported derived records with a live amp-free
                          environment: deduction replays them exactly, with
                          or without the trail. Puncture freely.
     drift-risk        -- supported derived records whose every live
                          environment crosses an ampliative joint. STILL
                          PUNCTURED -- the decision trail is kept regardless,
                          and replay over trail + statics regenerates them --
                          but they are the decision-PINNED interior: re-run
                          the abductive process without its trail and a
                          different fork may come back. Drift-risk annotates
                          the punctured class; it does not shrink it.
     decisions         -- the escalation trail: every non-seed log event
                          (arrivals, retractions, rivalries, identifications,
                          exorcisms, exercise acts). Never punctured: the
                          trail is at once the reconstruction recipe and the
                          audit (§14.4 -- compression and integrity are one
                          requirement).
   The compression ratio is punctured / supported, and §14.2's "the ratio is
   the warrant profile" shows up in the SPLIT of the punctured interior:
   formal-heavy webs puncture losslessly, ampliative-heavy webs puncture
   decision-pinned -- compressible only because the trail is kept.

No sympy here: this module is engine-proper (the sidecar rule applies to
execution of content, and the meta layer never runs a formulation -- it
reasons about which ones are missing).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Optional, Sequence

from .core import Event, REC, State, Web, short
from .fidelity import labels as atms_labels
from .fidelity import explananda, theoretical
from .forks import Rivalry, ancestors, downstream, fork_report


# ---------------------------------------------------------------------------
# Plans -- deficits of minimal environments
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Plan:
    """One route to resolving one open item, read off one minimal
    environment. `observe` + `derive` + `secure` together are the deficit;
    empty deficit never occurs (a live environment is not a hole)."""
    target: object          # the stub / explanandum record
    kind: str               # "repair" (stub) | "explain" (explanandum)
                            # | "discover" (explanandum, no theoretical route)
    env: frozenset          # the environment this plan completes
    observe: frozenset      # empirical grounds still missing
    derive: frozenset       # formal grounds still missing
    secure: frozenset       # other grounds still missing
    rationale: str = ""

    @property
    def cost(self) -> int:
        return len(self.observe) + len(self.derive) + len(self.secure)


def _deficit(web: Web, state: State, env) -> Optional[tuple]:
    """(observe, derive, secure) for one environment, or None if blocked
    (an exorcised member: no assertion completes it, §15.3)."""
    if env & state.exorcised:
        return None
    missing = frozenset(g for g in env if g not in state.asserted
                        and g in web.grounds)
    observe = frozenset(g for g in missing
                        if REC.Empirical in web.warrants.get(g, ()))
    derive = frozenset(g for g in missing
                       if REC.Formal in web.warrants.get(g, ()))
    secure = missing - observe - derive
    return observe, derive, secure


def plans_for(web: Web, state: State, record,
              label_map: Optional[Mapping] = None) -> tuple:
    """Plans for one open record, cheapest first. Stubs get every unblocked
    environment; explananda only their theoretical ones (the point is to
    raise support past observation, not to re-observe)."""
    label_map = label_map if label_map is not None else atms_labels(web)
    is_stub = not state.supported.get(record, False)
    envs = label_map.get(record, frozenset())
    if not is_stub:
        envs = frozenset(e for e in envs if theoretical(web, e))
        if not envs:
            return (Plan(target=record, kind="discover", env=frozenset(),
                         observe=frozenset(), derive=frozenset(),
                         secure=frozenset(),
                         rationale="no theoretical environment exists in the "
                                   "web -- no plan completes one; a NEW "
                                   "abduction is required (discovery)"),)
    out = []
    for e in envs:
        d = _deficit(web, state, e)
        if d is None:
            continue
        observe, derive, secure = d
        if not (observe or derive or secure):
            continue  # live (or about to be): not a hole via this env
        out.append(Plan(
            target=record,
            kind="repair" if is_stub else "explain",
            env=e, observe=observe, derive=derive, secure=secure,
            rationale="completes a minimal environment of the record's label"))
    return tuple(sorted(out, key=lambda p: (p.cost, sorted(map(str, p.env)))))


def observation_plans(web: Web, state: State,
                      label_map: Optional[Mapping] = None) -> Mapping:
    """Every open item's plans: stubs (support fell) and explananda (support
    never rose), each mapped to its ranked plans. Quarantined records are
    NOT open items (§17): a conclusion visible only from a scaffold is a
    view, not a hole -- the planner does not propose repairing what was
    never held."""
    label_map = label_map if label_map is not None else atms_labels(web)
    quarantine = state.quarantined(web.universe)
    open_items = tuple(sorted(
        (n for n in web.derived
         if not state.supported.get(n, False) and n not in quarantine),
        key=str)) + explananda(web, state, label_map)
    return {r: plans_for(web, state, r, label_map) for r in open_items}


# ---------------------------------------------------------------------------
# Discriminators -- prospective corroboration for open forks
# ---------------------------------------------------------------------------

def _would_corroborate(web: Web, state: State, rival, g,
                       label_map: Mapping) -> bool:
    """forks.corroborations run forward: would asserting g corroborate
    `rival`? Same rule, hypothetical assertion, freshness automatic."""
    if REC.Empirical not in web.warrants.get(g, ()):
        return False
    anc = ancestors(web, rival) | {rival}
    down = downstream(web, rival)
    if g in anc or g in down:
        return False
    hyp = state.asserted | {g}

    def live(env) -> bool:
        return env <= hyp and not (env & state.exorcised)

    for concl, js in web.justifications_of.items():
        for j in js:
            if g not in j.premises or not (j.premises & down):
                continue
            if any(live(e) for e in label_map.get(concl, ())):
                return True
    return False


@dataclass(frozen=True)
class Discriminator:
    """One prospective observation and what it would decide."""
    ground: object          # the unobserved empirical ground
    corroborates: tuple     # the rival(s) it would corroborate, sorted
    decisive: bool          # exactly one rival -> observing it resolves


def fork_discriminators(web: Web, state: State, rivalry: Rivalry,
                        label_map: Optional[Mapping] = None) -> tuple:
    """All unsupported empirical grounds that would corroborate at least one
    rival if observed, decisive ones first. Empty for a fork the web gives
    no experiment for -- itself worth knowing."""
    label_map = label_map if label_map is not None else atms_labels(web)
    candidates = sorted(
        (g for g in web.grounds
         if not state.supported.get(g, False)
         and REC.Empirical in web.warrants.get(g, ())),
        key=str)
    out = []
    for g in candidates:
        hits = tuple(sorted(
            (r for r in (rivalry.a, rivalry.b)
             if _would_corroborate(web, state, r, g, label_map)), key=str))
        if hits:
            out.append(Discriminator(ground=g, corroborates=hits,
                                     decisive=len(hits) == 1))
    return tuple(sorted(out, key=lambda d: (not d.decisive, str(d.ground))))


def open_fork_plans(web: Web, state: State,
                    label_map: Optional[Mapping] = None) -> Mapping:
    """Discriminators for every fork not yet settled (open or contested).
    Resolved, identified and moot forks need no experiment."""
    label_map = label_map if label_map is not None else atms_labels(web)
    out = {}
    for rv in state.rivalries:
        report = fork_report(web, state, rv)
        if report.status in ("open", "contested"):
            out[rv] = fork_discriminators(web, state, rv, label_map)
    return out


# ---------------------------------------------------------------------------
# The puncture report -- §14.2, computed
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PunctureReport:
    kept_constituted: frozenset   # empirical / self-verifying / unmarked grounds
    kept_pointers: frozenset      # formal grounds (machinery)
    regenerable: frozenset        # derived, a live amp-free environment
    drift_risk: frozenset         # derived, live only through ampliative joints
    decisions: tuple              # non-seed events: the escalation trail

    @property
    def punctured(self) -> frozenset:
        """The whole derivable interior -- lossless and decision-pinned
        together: the decision trail is kept regardless, so both regenerate
        on replay."""
        return self.regenerable | self.drift_risk

    @property
    def supported_total(self) -> int:
        return (len(self.kept_constituted) + len(self.kept_pointers)
                + len(self.regenerable) + len(self.drift_risk))

    @property
    def ratio(self) -> float:
        """Fraction of the supported web that punctures away (§14.2). The
        warrant profile lives in the SPLIT: regenerable is the lossless
        share, drift_risk the decision-pinned share."""
        total = self.supported_total
        return len(self.punctured) / total if total else 0.0


def puncture_report(web: Web, state: State, events: Sequence[Event],
                    label_map: Optional[Mapping] = None) -> PunctureReport:
    from .fidelity import amp  # local: keep the module head declarative
    label_map = label_map if label_map is not None else atms_labels(web)

    kept_constituted, kept_pointers = set(), set()
    for g in web.grounds:
        if not state.supported.get(g, False):
            continue
        if REC.Formal in web.warrants.get(g, ()):
            kept_pointers.add(g)
        else:
            kept_constituted.add(g)

    regenerable, drift_risk = set(), set()
    for r in web.derived:
        if not state.supported.get(r, False):
            continue
        live = [e for e in label_map[r] if state.env_live(e)]
        if any(amp(web, e) == 0 for e in live):
            regenerable.add(r)
        else:
            drift_risk.add(r)

    decisions = tuple(ev for ev in events
                      if not ev.note.startswith("seed:"))

    return PunctureReport(
        kept_constituted=frozenset(kept_constituted),
        kept_pointers=frozenset(kept_pointers),
        regenerable=frozenset(regenerable),
        drift_risk=frozenset(drift_risk),
        decisions=decisions,
    )


# ---------------------------------------------------------------------------
# Scaffold verdicts -- the force asymmetry, computed (§17)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ConsequenceVerdict:
    """One tested consequence of one scaffold."""
    consequence: object
    passed: bool
    tp_only: bool       # every promontory path from scaffold to consequence
                        # is free of ampliative joints
    verdict: str        # "refutes (formal)" | "impugns (defeasible)"
                        # | "corroborates (defeasible)"


@dataclass(frozen=True)
class ScaffoldReport:
    """One scaffold's standing, read off its tested consequences.

    THE FORCE ASYMMETRY (§2, cashed out): refutation flows truth-preservingly
    -- a consequence failing its exercise, reached from the scaffold by
    deduction alone, is modus tollens, and what propagates back is FORMAL
    (relative to the test): the scaffold is refuted with the certainty of the
    derivation. Confirmation flows ampliatively no matter the path's force --
    a passing consequence corroborates, defeasibly, full stop. You learn
    more, at higher grade, from the scaffold's death than from its survival;
    the false record is the one place deduction points outward. And the
    verdict is the WEB's, not the agent's: Saccheri's conviction that the
    acute hypothesis was absurd never entered this computation -- conviction
    is content, and it was wrong."""
    scaffold: object
    consequences: tuple    # ConsequenceVerdicts, refutations first

    @property
    def refuted(self) -> bool:
        return any(v.verdict == "refutes (formal)" for v in self.consequences)

    @property
    def corroborated(self) -> int:
        return sum(1 for v in self.consequences
                   if v.verdict == "corroborates (defeasible)")


def scaffold_report(web: Web, state: State, scaffold,
                    label_map: Optional[Mapping] = None) -> ScaffoldReport:
    """Verdicts for one supposed ground, from the exercised records among
    its quarantined downstream. A consequence counts only if it PINS on the
    scaffold: every promontory-live environment contains it (otherwise the
    outcome is evidence about something else the agent already holds)."""
    from .fidelity import amp  # local: keep the module head declarative
    label_map = label_map if label_map is not None else atms_labels(web)
    out = []
    for c in sorted(web.derived, key=str):
        if c not in state.exercised:
            continue
        envs = [e for e in label_map[c] if state.env_on_promontory(e)]
        if not envs or not all(scaffold in e for e in envs):
            continue
        passed = state.exercised[c][1]
        tp_only = all(amp(web, e) == 0 for e in envs)
        if passed:
            verdict = "corroborates (defeasible)"
        elif tp_only:
            verdict = "refutes (formal)"
        else:
            verdict = "impugns (defeasible)"
        out.append(ConsequenceVerdict(consequence=c, passed=passed,
                                      tp_only=tp_only, verdict=verdict))
    out.sort(key=lambda v: (v.passed, str(v.consequence)))
    return ScaffoldReport(scaffold=scaffold, consequences=tuple(out))


def scaffold_reports(web: Web, state: State,
                     label_map: Optional[Mapping] = None) -> Mapping:
    """Every current scaffold's report."""
    label_map = label_map if label_map is not None else atms_labels(web)
    return {s: scaffold_report(web, state, s, label_map)
            for s in sorted(state.supposed, key=str)}


def describe_plan(web: Web, plan: Plan, label_of=None) -> str:
    """One line of English per plan, for demos and reports."""
    name = label_of or (lambda n: short(n))
    bits = []
    if plan.observe:
        bits.append("observe " + ", ".join(sorted(map(name, plan.observe))))
    if plan.derive:
        bits.append("derive " + ", ".join(sorted(map(name, plan.derive))))
    if plan.secure:
        bits.append("secure " + ", ".join(sorted(map(name, plan.secure))))
    action = "; ".join(bits) if bits else plan.rationale
    verb = {"repair": "to repair", "explain": "to explain",
            "discover": "to explain"}[plan.kind]
    return f"{action} — {verb} {name(plan.target)}"
