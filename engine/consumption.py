"""
The consumption check: a third detector for fabrication (§15.3 extended).

§15.3 gave fabrication two detectors -- empirical fabrication exposed by
incoherence with the web, formal fabrication (the pretender) exposed by an
exercise that FAILS. A review of an external contribution exposed a third
shape: the exercise that passes VACUOUSLY. A derivation that restates its
stored conclusion closes trivially -- regeneration_ok compares x with x --
and formal warrant is worn without the form while every green light stays
green. Kempe's pretender failed when Heawood ran it; the restating
pretender cannot fail, which is worse.

The mechanical test is counterfactual: POISON a premise and re-derive.

  * For each joint (an inference token in the fixture graph), find its
    premises. Poison every premise the sidecar can express: its CONTENT
    entry is replaced with a sentinel symbol, and -- because honest
    derivations often RECOMPUTE their premises rather than read them --
    any derive function that concludes a poisoned premise is replaced by
    one returning the sentinel.
  * Re-run the joint's derivation.
      - output changed, or the derivation RAISED (its own asserts noticed
        the poison): the joint CONSUMES its premises. Genuine.
      - output identical: the derivation never touched what it claims to
        depend on. If the joint is not declared in STATED_JOINTS, that is
        the ALARM: a restatement wearing derivational warrant.

Honest limits, stated: a joint whose premises are all GROUNDS (concluded
by no joint, their content embedded in the derivation's own machinery --
the Binet ODE just IS Newton's law in u-substitution) cannot be poisoned
at the content level; it is reported as ground-embedded, not alarmed, and
its warrant rests on the internal asserts of its own exercise. A stated
joint declared in STATED_JOINTS is the honest stub (§13.1): reported as
testimonial, never alarmed -- the declaration is exactly what separates
it from the pretender.

Sidecar-facing (imports sympy through the modules it inspects); the demo
is scripts/consumption_demo.py.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import rdflib
from rdflib.namespace import RDF

REC = rdflib.Namespace("https://www.epistemic-ontology.net/record#")

CONSUMES = "consumes"            # output changed (or derivation raised) under poison
STATED = "stated"                # declared testimonial -- the honest stub
GROUND_EMBEDDED = "ground-embedded"  # only ground premises; content-level poison impossible
ALARM = "ALARM: restates"        # undeclared, derived premises poisoned, output unchanged
NO_PREMISES = "no-premises"      # nothing to consume (definitional token)


@dataclass(frozen=True)
class Verdict:
    inference: str
    concludes: str
    category: str
    detail: str


def _local(uri) -> str:
    s = str(uri)
    for sep in ("#", "/"):
        if sep in s:
            s = s.rsplit(sep, 1)[1]
    return s


def _premises_by_inference(ttl_path: Path) -> Dict[str, List[str]]:
    g = rdflib.Graph()
    g.parse(ttl_path, format="turtle")
    out: Dict[str, List[str]] = {}
    for s, _, o in g.triples((None, REC.hasPremise, None)):
        out.setdefault(_local(s), []).append(_local(o))
    return out


def analyze(module, ttl_path: Path) -> List[Verdict]:
    """Run the consumption check over one sidecar module + its fixture."""
    import sympy as sp

    premises_of = _premises_by_inference(Path(ttl_path))
    joints = list(module.JOINTS)
    stated = getattr(module, "STATED_JOINTS", frozenset())
    concluder = {}          # premise short-name -> derive function name
    for jt in joints:
        concluder[jt.concludes] = jt.derive.__name__

    sentinel = sp.Symbol("POISON__sentinel", positive=True)
    verdicts: List[Verdict] = []

    for jt in joints:
        prem = premises_of.get(jt.inference, [])
        if jt.inference in stated:
            verdicts.append(Verdict(jt.inference, jt.concludes, STATED,
                                    "declared in STATED_JOINTS -- testimonial, the honest stub"))
            continue
        if not prem:
            verdicts.append(Verdict(jt.inference, jt.concludes, NO_PREMISES,
                                    "no premises in the fixture graph"))
            continue

        poisonable_content = [p for p in prem if p in module.CONTENT]
        poisonable_derives = [p for p in prem if p in concluder]
        if not poisonable_content and not poisonable_derives:
            verdicts.append(Verdict(jt.inference, jt.concludes, GROUND_EMBEDDED,
                                    f"premises {prem} are grounds outside CONTENT; "
                                    f"warrant rests on the exercise's own asserts"))
            continue
        # If every poisonable premise is a pure ground (in CONTENT but not
        # concluded by any joint) AND the derivation neither reads CONTENT
        # nor calls a premise derive, poisoning may be inert for honest
        # machinery-level derivations. Distinguish: ground-only joints are
        # reported, mixed/derived-premise joints are alarmed on inertness.
        has_derived_premise = bool(poisonable_derives)

        baseline = sp.simplify(jt.derive())

        saved_content = {p: module.CONTENT[p] for p in poisonable_content}
        saved_fns = {}
        try:
            for p in poisonable_content:
                module.CONTENT[p] = sentinel
            for p in poisonable_derives:
                name = concluder[p]
                try:
                    saved_fns[name] = getattr(module, name)
                except AttributeError:
                    continue    # derive fn not module-bound; CONTENT poison only
                setattr(module, name, lambda _s=sentinel: _s)
            try:
                poisoned = sp.simplify(jt.derive())
                changed = bool(sp.simplify(poisoned - baseline) != 0) \
                    if poisoned.free_symbols == baseline.free_symbols \
                    else poisoned != baseline
            except Exception as e:      # the derivation NOTICED the poison
                verdicts.append(Verdict(jt.inference, jt.concludes, CONSUMES,
                                        f"derivation raised under poison ({type(e).__name__}) "
                                        f"-- its own asserts consumed the premises"))
                continue
        finally:
            for p, v in saved_content.items():
                module.CONTENT[p] = v
            for name, fn in saved_fns.items():
                setattr(module, name, fn)

        if changed:
            verdicts.append(Verdict(jt.inference, jt.concludes, CONSUMES,
                                    f"output changed under poisoned {poisonable_content + poisonable_derives}"))
        elif has_derived_premise:
            verdicts.append(Verdict(jt.inference, jt.concludes, ALARM,
                                    f"premises {prem} poisoned (incl. derived premises "
                                    f"{poisonable_derives}); output UNCHANGED -- the "
                                    f"derivation restates its conclusion"))
        else:
            verdicts.append(Verdict(jt.inference, jt.concludes, GROUND_EMBEDDED,
                                    f"ground premises {poisonable_content} poisoned without "
                                    f"effect; consumption is at machinery level (untestable "
                                    f"here) -- warrant rests on the exercise's own asserts"))

    return verdicts


def alarms(verdicts: Sequence[Verdict]) -> List[Verdict]:
    return [v for v in verdicts if v.category == ALARM]
