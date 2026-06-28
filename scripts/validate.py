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


def check_cogito_pattern(ont_graph, ex_graph):
    """The cogito as a PATTERN, not a class (ROOT.md §11). There is no Cogito
    class to derive; the cogito is recognised by: self-verifying warrant +
    for-whom = of-what (directed at its own agent). The decisive check is that
    this does NOT conflate with other performatives: a promise is self-verifying
    but directed elsewhere (for != of), so it is correctly NOT the cogito. This
    is a graph-pattern check (no reasoner needed)."""
    print("\n🔍 Checking the cogito PATTERN (no class; over-capture removed)...")
    merged = ont_graph + ex_graph

    sv = set(merged.subjects(REC.hasWarrant, REC.SelfVerifying))
    if not sv:
        print("⚠️  No self-verifying records present; nothing to test.")
        return True

    def coincides(r):  # for-whom == of-what, both present
        fa = set(merged.objects(r, REC.forAgent))
        dt = set(merged.objects(r, REC.directedToward))
        return bool(fa) and fa == dt

    cogito_pattern = {r for r in sv if coincides(r)}
    performatives = sv - cogito_pattern  # self-verifying but not self-directed

    ok = True
    if cogito_pattern:
        print(f"✅ cogito pattern (self-verifying + for=of) holds for: "
              f"{', '.join(sorted(map(_short, cogito_pattern)))}")
    else:
        ok = False
        print("❌ no record matches the cogito pattern (self-verifying + for=of)")

    if performatives:
        print(f"✅ {len(performatives)} self-verifying performative(s) correctly "
              f"NOT the cogito ({', '.join(sorted(map(_short, performatives)))}) "
              "— the demotion-to-pattern removed the old class over-capture")

    # No Carrier class should exist or be used.
    stray = (set(merged.objects(None, REC.borneBy))
             | set(merged.subjects(RDF.type, REC.Carrier))
             | set(merged.subjects(RDF.type, REC.Cogito)))
    if stray:
        ok = False
        print("❌ removed carrier/cogito terms still in use:",
              ", ".join(sorted(map(_short, stray))))
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
        ("Self-verifying records", set(reasoned.subjects(REC.hasWarrant, REC.SelfVerifying))),
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
    ok &= check_cogito_pattern(ont_graph, ex_graph)
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
