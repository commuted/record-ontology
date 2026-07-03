# The Record Ontology

A small OWL 2 DL ontology of the **Record** — the structure of warranted
knowledge as agents build it.

[![Version](https://img.shields.io/badge/version-0.4.0-blue.svg)](ontology/record-ontology.ttl)
[![OWL 2 DL](https://img.shields.io/badge/OWL-2%20DL-green.svg)](https://www.w3.org/TR/owl2-overview/)
[![Reasoner-validated](https://img.shields.io/badge/owlrl-validated-green.svg)](scripts/validate.py)

> **Status:** a seed/base (v0.4.0). The conceptual source of truth is
> [`ROOT.md`](ROOT.md); this README summarises it. Born at a permanent namespace
> (`https://www.epistemic-ontology.net/record#`) but not yet hosted.

## Scope

This is a **domain-neutral ontology of warranted record-structure**: how agents
**warrant, compose, ground, and revise** records — the connective grammar of
knowledge, *not the things known*.

- **In scope:** records, their warrants, how they compose into discoveries and
  narratives, how evidence grounds claims, how "metadata" and inference fit. It
  applies wherever agents build knowledge from evidence — scientific discovery
  above all (the motivating case), but equally history, scholarship, law,
  intelligence analysis.
- **Out of scope:** the domains themselves. It models neither electrons nor
  organisms nor battles — only the *records* of them and how they are held. This
  is the same refusal as `directedness`: a record is never named by the
  world-object it is "of." Domain ontologies and vocabularies (SKOS thesauri,
  scientific term-sets) **plug in through `warrant`** — attached, never absorbed.

It is **constrained to agents** (a person or an AI): it is built *for* an agent
and never steps outside one. The founding rule is that *no class may be defined
by a relation to an object that lies outside all records.*

## Core design

- **One class: `Record`** — a form, in a carrier, for an agent, at a level of
  abstraction. There is no separate `Form` class (that would be the "formal
  apple"); everything an agent holds is a Record, and Records are made of Records.
- **Attributes, not kinds** (so patchworks decompose):
  - **`warrant`** — a **triad, one value per limit**: `Formal` (true in virtue of
    form; → the form-in-itself), `Empirical` (true by givenness, defeasible; → the
    world-in-itself), `SelfVerifying` (true in virtue of the act of recording —
    the cogito; → the Agent-in-itself, the one limit *not* excluded).
  - **`atLevelOfAbstraction`**, **`directedToward`** (the intentional object),
    **`hasProvenance`**, **`pragmaticAdequacy`**. Fidelity/completeness are
    *entailed* by warrant, not primitive.
- **Inference** — the operational face of the formal: a `Record` with
  `hasPremise` / `concludes`, surfaced as a **defined** class (never a primitive
  kind). Inference carries a **force** (truth-preserving ↔ ampliative). Chains of
  inference form a derivation DAG.
- **Carrier (dissolved) & the cogito** — there is no `Carrier` class: the carrier
  dissolves into `hasProvenance` (whence) + `hasLocus` (where/when). The regress
  "what carries the carrier?" halts in the **self-verifying warrant** — the cogito
  is a *pattern* (self-verifying + reflexive provenance + self-directedness), not
  a class. Credit Descartes (existence) and Hintikka (the warrant).
- **No metadata** — `metadataOf` is a defined role (sub-property of
  `directedToward`): a record *about* a record, never a separate layer.
- **The Continuum** — the one thing that is *not* a Record: the undivided ground
  carriers are individuated from (disjoint from `Record`).
- **Two excluded limits** — the world-in-itself and the form-in-itself are
  recorded as commentary only, *never* instantiated as classes.

### Stance: between the OWL/DL and SKOS camps

The ontology is **DL-in-form** (defined classes, a reasoner, disjointness, no
SKOS import — SKOS is OWL Full) but **ecumenical-in-content**: the standing
OWL/DL ↔ SKOS/thesaurus schism is demoted from a *choice of framework* to the
**`warrant`** attribute (formal = DL/subsumption; empirical/given =
SKOS/convention). A real artifact is both. See `ROOT.md` §12.

## Repository structure

```
record-ontology/
├── ontology/
│   └── record-ontology.ttl        # the OWL 2 DL ontology (v0.4.0)
├── examples/
│   ├── historical-narrative.ttl   # a derivation DAG (sources → ampliative inferences)
│   ├── neptune-discovery.ttl      # the §10 flagship: a real discovery with a fork
│   │                              #   (engine fixture — fork collapse as oracle)
│   ├── cogito.ttl                 # the cogito as a self-verifying pattern (+ a promise)
│   └── minimal/                   # eyeball-sized examples, one feature each
│       ├── minimal-empirical.ttl      # empirical warrant, directedness, provenance
│       ├── minimal-formal.ttl         # formal warrant (the triangle)
│       ├── minimal-inference.ttl      # truth-preserving inference (syllogism)
│       ├── minimal-ampliative.ttl     # ampliative inference → revisability
│       ├── minimal-metadata.ttl       # metadata as record-about-record
│       ├── minimal-carrier.ttl        # carrier dissolved into provenance + locus
│       ├── minimal-cogito.ttl         # the cogito as a self-verifying pattern
│       ├── minimal-composition.ttl    # a record composed of records (compound)
│       └── minimal-level.ttl          # level of abstraction + pragmatic adequacy
├── scripts/
│   └── validate.py                # syntax + OWL 2 RL reasoner checks + metrics
├── requirements-dev.txt           # rdflib + owlrl
├── ROOT.md                        # the conceptual source of truth (read this)
├── LICENSE                        # CC BY 4.0 (ontology + docs) · MIT (scripts)
└── README.md
```

## Quick start

```bash
pip install -r requirements-dev.txt
python scripts/validate.py
```

`validate.py` runs a pure-Python OWL 2 RL reasoner (`owlrl`, no Java) and checks:

- **Defined-class entailment** — strips the asserted `Inference` type and confirms
  the *definition* re-derives it, with a negative control (a premise-less formal
  object is not an inference).
- **Cogito pattern** — confirms the cogito pattern (self-verifying + for=of) holds
  and that a self-verifying *promise* is correctly **not** conflated with it.
- **Consistency** — no individual is both `Record` and `Continuum`.
- **Sub-property entailment** — every `metadataOf` edge entails `directedToward`.

Load it yourself with [rdflib](https://rdflib.readthedocs.io/):

```python
from rdflib import Graph
g = Graph().parse("ontology/record-ontology.ttl", format="turtle")
```

## Open items

- **Composition transitivity** — `partOf`/`composedOf` left non-transitive on
  purpose (cf. the sibling, which dropped `buildsUpon` transitivity for OWL 2 DL).
- **Namespace** — confirm `epistemic-ontology.net/record#` before external
  adopters rely on the IRIs; hosting under `epistemic-ontology.net` (slug
  `record`) is pending.
- **Non-monotonic propagation** — fidelity propagation, forks, and stubs are an
  unbuilt *computational layer over* the static ontology (`ROOT.md` §10).

## License

The ontology and documentation are licensed **[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)** —
permissive, reuse and adapt freely (including commercially), with attribution:

> "The Record Ontology — epistemic-ontology.net" — https://www.epistemic-ontology.net/record

The scripts (`scripts/`) are additionally available under the **MIT License**.
See [LICENSE](LICENSE). Copyright © 2026 Ron Hinchley / epistemic-ontology.net.

## Related

- **record-harm** — models how a Record is *damaged*; intended to source its
  `Record` and `Agent` from this ontology once it stabilises.
