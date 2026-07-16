"""
Escalation dynamics over a record web -- the engine stratum (§13, run).

ROOT.md §6 leaves escalation VOCABULARY deliberately uncommitted, so
everything here is computation over existing structure: no OWL terms, no
new properties -- the strata rule, fourth time. What §13 narrates, this
module computes for a two-or-more-agent web:

  * AS-OF-MOMENT VIEWS -- which records were extant when a decision was
    taken (§13.3: retrospection is as-of-moment, never as-of-hindsight);
  * OMISSION, MEASURED -- for an inference, the records extant at its
    moment that impugn its premises and are absent from its premise-set.
    §18's Omission ("the unrecorded skip") as a computable set difference:
    the edge that is not there;
  * CORROBORATION CONTRAST -- impugners per record at a moment, so a
    weakly-held record standing next to a well-held one is visible as a
    number, not a feeling;
  * VELOCITY -- §13.1's irrevocability ladder (notice < record < rank <
    act) with timestamps: rungs climbed per day, review time granted
    between a requested evaluation and the action that outran it;
  * COUNTERFACTUAL RESTORATION -- re-assemble an inference's premise-set
    with the omitted impugners restored, and report what the consent
    would then have had to carry openly.

First fixture: examples/tonkin-consent.ttl -- consent to war assembled
from a curated premise-set while the impugning records (Herrick's own
review cable) sat extant in the web. The 2005 NSA study is the oracle in
the Saccheri/Beltrami sense: it confirms what the as-of-moment web
already impugned. The registries below (extancy times, impugnment
valence) are CONTENT, engine-side, exactly as planetary elements are in
perturbation.py; the graph stays pure structure.

Times are fractional days from 1964-08-01 00:00 Washington time,
approximate to the hour where the sources allow (flagged inline).

Sidecar-facing (rdflib only; no sympy); demo: scripts/tonkin_demo.py.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import rdflib

REC = rdflib.Namespace("https://www.epistemic-ontology.net/record#")


# -- generic machinery -----------------------------------------------------------

def _local(uri) -> str:
    s = str(uri)
    for sep in ("#", "/"):
        if sep in s:
            s = s.rsplit(sep, 1)[1]
    return s


@dataclass(frozen=True)
class Web:
    """A fixture graph plus the engine-side content registries."""
    graph: rdflib.Graph
    extant_at: Dict[str, float]          # record -> moment it entered the web
    impugns: Dict[str, List[str]]        # record -> records it counts against

    @classmethod
    def load(cls, ttl_path: Path, extant_at, impugns) -> "Web":
        g = rdflib.Graph()
        g.parse(ttl_path, format="turtle")
        return cls(g, dict(extant_at), {k: list(v) for k, v in impugns.items()})

    def premises_of(self, inference: str) -> List[str]:
        return sorted({_local(o) for s, _, o in
                       self.graph.triples((None, REC.hasPremise, None))
                       if _local(s) == inference})

    def as_of(self, moment: float) -> List[str]:
        return sorted(r for r, t in self.extant_at.items() if t <= moment)

    def impugners_of(self, record: str, moment: Optional[float] = None) -> List[str]:
        out = [r for r, targets in self.impugns.items() if record in targets]
        if moment is not None:
            out = [r for r in out if self.extant_at.get(r, float("inf")) <= moment]
        return sorted(out)

    def omitted_impugners(self, inference: str, moment: float) -> Dict[str, List[str]]:
        """§18's Omission, computed: for each premise of the inference, the
        records extant at the inference's moment that impugn that premise
        (or the inference's other premises) and are NOT in the premise-set.
        The edge that is not there."""
        premises = set(self.premises_of(inference))
        omitted: Dict[str, List[str]] = {}
        for p in premises:
            for imp in self.impugners_of(p, moment):
                if imp not in premises:
                    omitted.setdefault(p, []).append(imp)
        return omitted

    def corroboration_contrast(self, records: Sequence[str],
                               moment: float) -> Dict[str, int]:
        """Impugners extant per record at the moment: the weakly-held record
        next to the well-held one, as numbers."""
        return {r: len(self.impugners_of(r, moment)) for r in records}


@dataclass(frozen=True)
class Ladder:
    """§13.1's irrevocability ladder with timestamps (fractional days)."""
    notice: Tuple[str, float]            # the triggering report
    record: Tuple[str, float]            # the review/evaluation record
    rank: Tuple[str, float]              # the decision
    act: Tuple[str, float]               # the irrevocable action
    consent: Tuple[str, float]           # the widened commitment

    def rungs(self) -> List[Tuple[str, str, float]]:
        return [("notice",) + self.notice, ("record",) + self.record,
                ("rank",) + self.rank, ("act",) + self.act,
                ("consent",) + self.consent]

    def notice_to_act_days(self) -> float:
        return self.act[1] - self.notice[1]

    def notice_to_consent_days(self) -> float:
        return self.consent[1] - self.notice[1]

    def review_time_granted_days(self) -> float:
        """Between the record rung (the requested evaluation) and the rank
        rung (the decision). Negative or near-zero = the ladder was climbed
        over its own review."""
        return self.rank[1] - self.record[1]


# -- the Tonkin registries (content, engine-side) ---------------------------------
# Fractional days from 1964-08-01 00:00 Washington time; hour-level values
# are approximations consistent with the documentary record.

TONKIN_EXTANT: Dict[str, float] = {
    "Oplan34ARaids":       0.0,     # ongoing before the window
    "DesotoPatrol":        0.0,
    "Aug2Engagement":      2.5,
    "Aug4AttackReport":    4.45,    # flash reports, morning/midday DC
    "HerrickDoubtCable":   4.70,    # evening DC, before the strike order
    "NoVisualSightings":   4.70,
    "PierceArrowStrikes":  5.30,    # strikes flown Aug 5 (announced ~23:36 Aug 4 DC)
    "ExecutiveTestimony":  6.50,
    "TonkinResolution":    7.50,
    "PublicConsentRecord": 7.60,
    "HanyokStudy":         15128.0, # declassified 2005 -- ~41.4 years on
}

TONKIN_IMPUGNS: Dict[str, List[str]] = {
    "HerrickDoubtCable":  ["Aug4AttackReport"],
    "NoVisualSightings":  ["Aug4AttackReport"],
    "Oplan34ARaids":      ["ExecutiveTestimony"],   # against 'unprovoked'
    "HanyokStudy":        ["Aug4AttackReport", "ExecutiveTestimony"],
}

TONKIN_LADDER = Ladder(
    notice=("Aug4AttackReport", 4.45),
    record=("HerrickDoubtCable", 4.70),   # the review REQUESTED, on the record
    rank=("strike order", 4.95),          # ~23:36 Aug 4 DC announcement
    act=("PierceArrowStrikes", 5.30),
    consent=("TonkinResolution", 7.50),
)

# For contrast: the Cuban Missile Crisis climbed notice (Oct 16, U-2 photos)
# to resolution (Oct 28) in 13 days -- and the maximal rung (the airstrike)
# was never taken. Same ladder, different velocity, different century of
# consequences.
CUBAN_MISSILE_NOTICE_TO_RESOLUTION_DAYS = 13.0

DECISION_MOMENT = 4.95      # the strike order
CONSENT_MOMENT = 7.50       # the resolution vote


def load_tonkin(repo_root: Optional[Path] = None) -> Web:
    root = repo_root or Path(__file__).resolve().parent.parent
    return Web.load(root / "examples" / "tonkin-consent.ttl",
                    TONKIN_EXTANT, TONKIN_IMPUGNS)


def counterfactual_restoration(web: Web, inference: str,
                               moment: float) -> Dict[str, List[str]]:
    """Re-assemble the inference's premise-set with the omitted impugners
    restored, and report the conflict the curated set kept invisible."""
    premises = web.premises_of(inference)
    omitted = web.omitted_impugners(inference, moment)
    restored = sorted(set(premises) | {i for imps in omitted.values() for i in imps})
    visible_conflicts = {
        p: imps for p, imps in omitted.items()
    }
    return {
        "original_premises": premises,
        "restored_premises": restored,
        "conflicts_made_visible": visible_conflicts,
    }
