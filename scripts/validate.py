#!/usr/bin/env python3
"""
Validation script for the Record Ontology.

Validates:
1. OWL/Turtle syntax (ontology + example).
2. DEFINED-CLASS ENTAILMENT via an OWL 2 RL reasoner (owlrl): the `Inference`
   class is *defined* (Record + hasPremise + concludes), never asserted as a
   primitive kind (ROOT.md §8). This check strips every asserted
   `a rec:Inference` from the example, runs the reasoner, and confirms the
   definition RE-DERIVES them -- with a negative control that a premise-less
   formal object (the "triangle" face) is NOT classified as an Inference.
3. Logical consistency: Record and Continuum are disjoint (ROOT.md §5); no
   individual may land in owl:Nothing.
4. Sub-property entailment: metadataOf ⊑ directedToward (ROOT.md §9).
5. Basic metrics.

Run:  python scripts/validate.py
Deps: pip install -r requirements-dev.txt   (rdflib, owlrl)
"""

import sys
from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.namespace import OWL, RDF

try:
    import owlrl
    HAVE_OWLRL = True
except ImportError:
    HAVE_OWLRL = False

REC = Namespace("https://www.epistemic-ontology.net/record#")


def _short(uri):
    s = str(uri)
    return s.rsplit("#", 1)[-1] if "#" in s else s.rsplit("/", 1)[-1]


def load_graph(path, fmt="turtle"):
    g = Graph()
    try:
        g.parse(path, format=fmt)
    except Exception as e:  # noqa: BLE001
        print(f"❌ Error loading {path}: {e}")
        sys.exit(1)
    return g


def validate_syntax(path):
    print(f"🔍 Validating RDF syntax: {path.name} ...")
    g = load_graph(path)
    print(f"✅ Syntax valid: {len(g)} triples loaded")
    return g


# ---------------------------------------------------------------------------
# Reasoner-backed checks
# ---------------------------------------------------------------------------

def _closure(g):
    """Return a reasoned copy of g under OWL 2 RL (in place on a fresh copy)."""
    r = Graph()
    for t in g:
        r.add(t)
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(r)
    return r


def check_inference_definition(ont_graph, ex_graph):
    """The headline check: `Inference` is a DEFINED class, not a stipulated kind.

    Remove every asserted `a rec:Inference`, run the reasoner, and require the
    definition (Record ⊓ ∃hasPremise.Record ⊓ ∃concludes.Record) to re-derive
    exactly those individuals. Negative control: a record with no premises (the
    formal-object / 'triangle' face) must NOT be classified as an Inference.
    """
    print("\n🔍 Checking the DEFINED class `Inference` (reasoner re-derivation)...")
    if not HAVE_OWLRL:
        print("⚠️  owlrl not installed -- skipping reasoner check (pip install owlrl)")
        return True

    merged = ont_graph + ex_graph
    asserted = set(merged.subjects(RDF.type, REC.Inference))
    if not asserted:
        print("⚠️  No example individuals asserted as rec:Inference; nothing to test.")
        return True

    probe = Graph()
    for t in merged:
        probe.add(t)
    for s in asserted:
        probe.remove((s, RDF.type, REC.Inference))

    reasoned = _closure(probe)
    derived = set(reasoned.subjects(RDF.type, REC.Inference))

    ok = True
    missing = asserted - derived
    if missing:
        ok = False
        print("❌ definition failed to re-derive:", ", ".join(sorted(map(_short, missing))))
    else:
        print(f"✅ definition re-derives all {len(asserted)} inference(s): "
              + ", ".join(sorted(map(_short, asserted))))

    # Negative control: formally-warranted records with no premises must stay out.
    formal_objects = {
        s for s in merged.subjects(REC.hasWarrant, REC.Formal)
        if not any(merged.objects(s, REC.hasPremise))
    }
    leaked = {s for s in formal_objects if (s, RDF.type, REC.Inference) in reasoned}
    if leaked:
        ok = False
        print("❌ formal object(s) misclassified as Inference:",
              ", ".join(sorted(map(_short, leaked))))
    elif formal_objects:
        print(f"✅ negative control: {len(formal_objects)} premise-less formal "
              f"object(s) correctly NOT inferences ({', '.join(sorted(map(_short, formal_objects)))})")
    return ok


def check_consistency(ont_graph, ex_graph):
    """Disjointness consistency (ROOT.md §5: Record ⊓ Continuum = ∅).

    After OWL RL closure, no named individual may be typed by both sides of any
    owl:disjointWith pair. (owlrl does not materialise owl:Nothing for a clash,
    so we detect shared instances directly -- this keeps the check with teeth.)
    """
    print("\n🔍 Checking logical consistency (disjointness)...")
    if not HAVE_OWLRL:
        print("⚠️  owlrl not installed -- skipping consistency check")
        return True
    from rdflib import URIRef
    reasoned = _closure(ont_graph + ex_graph)
    pairs = set(reasoned.subject_objects(OWL.disjointWith))
    if not pairs:
        print("⚠️  No owl:disjointWith axioms found; nothing to check.")
        return True
    ok = True
    for c1, c2 in pairs:
        shared = {s for s in (set(reasoned.subjects(RDF.type, c1))
                              & set(reasoned.subjects(RDF.type, c2)))
                  if isinstance(s, URIRef)}
        for s in sorted(shared):
            ok = False
            print(f"❌ inconsistency: {_short(s)} is both {_short(c1)} and {_short(c2)}")
    if ok:
        print(f"✅ consistent: no individual violates any of {len(pairs)} "
              "disjointness axiom(s)")
    return ok


def check_metadata_subproperty(ont_graph, ex_graph):
    """metadataOf ⊑ directedToward (ROOT.md §9): every metadataOf assertion must
    entail a directedToward edge under the reasoner."""
    print("\n🔍 Checking metadataOf ⊑ directedToward entailment...")
    if not HAVE_OWLRL:
        print("⚠️  owlrl not installed -- skipping sub-property check")
        return True
    merged = ont_graph + ex_graph
    pairs = set(merged.subject_objects(REC.metadataOf))
    if not pairs:
        print("⚠️  No metadataOf assertions present; nothing to test.")
        return True
    reasoned = _closure(merged)
    ok = True
    for s, o in pairs:
        if (s, REC.directedToward, o) not in reasoned:
            ok = False
            print(f"❌ {_short(s)} metadataOf {_short(o)} did NOT entail directedToward")
    if ok:
        print(f"✅ all {len(pairs)} metadataOf edge(s) entail directedToward "
              "(metadata is a record about a record)")
    return ok


def check_cogito(ont_graph, ex_graph):
    """The defined Carrier classes (ROOT.md §11). `Cogito` (Record borne by an
    Agent AND held with self-verifying warrant) and `FoundationalCarrier`
    (Carrier ⊓ Agent) are DEFINED, not asserted. Require the reasoner to derive
    Cogito for exactly the agent-borne + self-verifying records, derive the
    carrier as a FoundationalCarrier, and -- the negative controls -- NOT classify
    (a) a record on a non-agent carrier, nor (b) a MEMORY that is agent-borne but
    merely empirical. Also confirm the cogito's for/by/of coincide on one agent.
    """
    print("\n🔍 Checking the DEFINED Carrier classes (Cogito / FoundationalCarrier)...")
    if not HAVE_OWLRL:
        print("⚠️  owlrl not installed -- skipping cogito check")
        return True

    reasoned = _closure(ont_graph + ex_graph)
    cogitos = set(reasoned.subjects(RDF.type, REC.Cogito))
    foundational = set(reasoned.subjects(RDF.type, REC.FoundationalCarrier))

    # Expected = agent-borne AND self-verifying warrant; the rest of the carried
    # records are negative controls (non-agent carrier, OR agent-borne-but-empirical).
    carried = set(reasoned.subjects(REC.borneBy, None))
    expected = {r for r in carried
                if any((c, RDF.type, REC.Agent) in reasoned
                       for c in reasoned.objects(r, REC.borneBy))
                and (r, REC.hasWarrant, REC.SelfVerifying) in reasoned}
    negatives = carried - expected

    if not expected:
        print("⚠️  No agent-borne self-verifying records present; nothing to test.")
        return True

    ok = True
    missing = expected - cogitos
    if missing:
        ok = False
        print("❌ self-verifying agent-borne record(s) NOT derived as Cogito:",
              ", ".join(sorted(map(_short, missing))))
    else:
        print(f"✅ definition derives Cogito for all {len(expected)} self-verifying "
              f"agent-borne record(s): {', '.join(sorted(map(_short, expected)))}")

    leaked = negatives & cogitos
    if leaked:
        ok = False
        print("❌ record(s) wrongly classified as Cogito:",
              ", ".join(sorted(map(_short, leaked))))
    elif negatives:
        print(f"✅ negative controls correctly NOT Cogito "
              f"({', '.join(sorted(map(_short, negatives)))}) — incl. the "
              "agent-borne-but-empirical memory the warrant clause excludes")

    if foundational:
        print(f"✅ foundational carrier(s) derived (Carrier ⊓ Agent): "
              f"{', '.join(sorted(map(_short, foundational)))}")
    else:
        ok = False
        print("❌ no FoundationalCarrier derived (expected the agent qua carrier)")

    # the fixed point: for-whom == carrier == intentional object, on one agent
    for c in sorted(cogitos):
        fa = set(reasoned.objects(c, REC.forAgent))
        bb = set(reasoned.objects(c, REC.borneBy))
        dt = set(reasoned.objects(c, REC.directedToward))
        coincide = fa and (fa == bb == dt)
        if coincide:
            print(f"✅ fixed point on {_short(c)}: for-whom = carrier = "
                  f"intentional-object = {_short(next(iter(fa)))}")
        else:
            print(f"⚠️  {_short(c)} does not show full for/by/of coincidence "
                  "(definition still holds; coincidence is the full cogito pattern)")
    return ok


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def print_metrics(ont_graph, ex_graph):
    print("\n📊 Metrics:")
    merged = ont_graph + ex_graph
    reasoned = _closure(merged) if HAVE_OWLRL else merged
    counts = [
        ("Classes (ontology)", set(ont_graph.subjects(RDF.type, OWL.Class))),
        ("Object properties", set(ont_graph.subjects(RDF.type, OWL.ObjectProperty))),
        ("Records (examples)", set(ex_graph.subjects(RDF.type, REC.Record))),
        ("Inferences (reasoned)", set(reasoned.subjects(RDF.type, REC.Inference))),
        ("Cogitos (reasoned)", set(reasoned.subjects(RDF.type, REC.Cogito))),
    ]
    for label, s in counts:
        print(f"   {label}: {len(s)}")


def main():
    repo_root = Path(__file__).parent.parent
    ont_path = repo_root / "ontology" / "record-ontology.ttl"
    examples_dir = repo_root / "examples"

    if not ont_path.exists():
        print(f"❌ Ontology not found: {ont_path}")
        sys.exit(1)

    print("=" * 60)
    print("Record Ontology Validation")
    print("=" * 60)
    if not HAVE_OWLRL:
        print("⚠️  owlrl missing -- reasoner checks will be SKIPPED. "
              "Install: pip install -r requirements-dev.txt")

    ont_graph = validate_syntax(ont_path)
    # Merge every example so the defined classes are exercised across them all.
    ex_graph = Graph()
    ex_files = sorted(examples_dir.rglob("*.ttl")) if examples_dir.exists() else []
    if ex_files:
        for p in ex_files:
            ex_graph += validate_syntax(p)
    else:
        print("⚠️  No example files found; skipping example-backed checks.")

    ok = True
    ok &= check_inference_definition(ont_graph, ex_graph)
    ok &= check_cogito(ont_graph, ex_graph)
    ok &= check_consistency(ont_graph, ex_graph)
    ok &= check_metadata_subproperty(ont_graph, ex_graph)
    print_metrics(ont_graph, ex_graph)

    print("\n" + "=" * 60)
    if ok:
        print("✅ All validations passed!")
    else:
        print("❌ Validation failed (see above)")
        sys.exit(1)
    print("=" * 60)


if __name__ == "__main__":
    main()
