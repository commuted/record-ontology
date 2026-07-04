"""
The propagation engine -- the computational layer OVER the static ontology.

ROOT.md §10's architectural rule, implemented: OWL DL is monotonic and cannot
retract, so all dynamics (support withdrawal, re-leveling, forks, moments) live
here, never as axioms. The engine reads the ontology + example graphs as
read-only structure and computes over them. Kin: assumption-based truth
maintenance (de Kleer).

Strata contract:
  static  (ontology/*.ttl, examples/*.ttl) -- structure: the derivation DAG
          (hasPremise / concludes), warrants, forces. Never mutated.
  dynamic (this package) -- an append-only REVISION LOG of ground assertions,
          retractions, and decisions; log position = MOMENT (ROOT.md §13.3).
          Every state is computed from a log prefix, so as-of-moment views and
          replay/regeneration (§14) come for free.

The log stores only the non-derivable residue: ground records and decisions
(a rivalry declaration is a §13 escalation, recorded as such). Derived records
never enter the log -- they regenerate by re-derivation on replay. That is
§14's puncturing map, running.
"""

from .core import Engine, Event, Level, RevisionLog, State, Web, load_web, short
from .forks import Corroboration, ForkReport, Rivalry, fork_report, structural_candidates

__all__ = [
    "Engine", "Event", "Level", "RevisionLog", "State", "Web", "load_web", "short",
    "Corroboration", "ForkReport", "Rivalry", "fork_report", "structural_candidates",
]
