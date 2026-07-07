# The Record Ontology

A small OWL 2 DL ontology of the **Record** — the structure of warranted
knowledge as agents build it.

[![Version](https://img.shields.io/badge/version-0.6.0-blue.svg)](ontology/record-ontology.ttl)
[![OWL 2 DL](https://img.shields.io/badge/OWL-2%20DL-green.svg)](https://www.w3.org/TR/owl2-overview/)
[![Reasoner-validated](https://img.shields.io/badge/owlrl-validated-green.svg)](scripts/validate.py)

> **Status:** a seed/base (v0.6.0). The conceptual source of truth is
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
  - **`formulation`** — the *form as held*, the first datatype property
    (`ROOT.md` §15): a formula, a constraint list, a text. Opaque to the
    reasoner by design; for formal records it should suffice to **exercise**
    them (warrant earned by running the description, withdrawn by exorcism —
    engine events, never OWL vocabulary).
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
│   ├── record-ontology.ttl        # the OWL 2 DL ontology (v0.6.0)
│   └── arith.ttl                  # the arithmetic COMPANION (§15): the formal
│                                  #   object face, representative, attached
├── examples/
│   ├── historical-narrative.ttl   # a derivation DAG (sources → ampliative inferences)
│   ├── neptune-discovery.ttl      # the §10 flagship: a real discovery with a fork
│   │                              #   (engine fixture — fork collapse as oracle)
│   ├── bohr-atom.ttl              # chained model succession 1885–1927: explananda,
│   │                              #   environment swap, identification (matrix ≡ wave)
│   ├── triangle-described.ttl     # the 3-4-5 relation as an expression subgraph
│   │                              #   (described in full; compiler-exercised)
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
│       ├── minimal-level.ttl          # level of abstraction + pragmatic adequacy
│       └── minimal-exorcism.ttl       # a pseudo-proof: exercise fails → exorcise
├── engine/                        # the DYNAMIC stratum (ROOT.md §10): a
│   ├── __init__.py                #   computational layer OVER the ontology —
│   ├── core.py                    #   revision log (moments), support/level
│   ├── forks.py                   #   propagation, forks & corroboration,
│   ├── fidelity.py                #   the fidelity calculus (ATMS labels),
│   ├── mathcontent.py             #   executable math for the atom fixture,
│   ├── exercise.py                #   exercise-or-exorcise (§15.3),
│   └── compile.py                 #   + the formulation compiler (arith → sympy)
├── scripts/
│   ├── validate.py                # syntax + OWL 2 RL reasoner checks + metrics
│   ├── engine_demo.py             # runs the engine against the Neptune oracle
│   ├── fidelity_demo.py           # exercises the calculus + agreement checks
│   ├── bohr_demo.py               # the atom arc: succession, explananda, identity
│   ├── bohr_math_demo.py          # the arc's mathematics, executed (sympy)
│   ├── exercise_demo.py           # the triangle run; the pseudo-proof expelled
│   └── arith_demo.py              # the companion: description → compiled exercise
├── requirements-dev.txt           # rdflib + owlrl
├── ROOT.md                        # the conceptual source of truth (read this)
├── LICENSE                        # CC BY 4.0 (ontology + docs) · MIT (scripts + engine)
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

## The propagation engine (prototype)

OWL DL is monotonic — it cannot retract — so all dynamics live in a
**computational layer over** the static ontology (`ROOT.md` §10), implemented
as the `engine/` package (kin: de Kleer's assumption-based truth maintenance):

- **Revision log = the carrier of moments** (`ROOT.md` §13.3): an append-only
  event stream of ground assertions, retractions, and decisions; log position
  is order-derived time, and any state is computable **as-of any moment**.
  Derived records never enter the log — they regenerate by replay (§14's
  puncturing: the log holds only leaves + the escalation trail).
- **Support & re-leveling:** grounds are asserted; conclusions hold iff a live
  inference yields them; levels are warrant-entailed (formal → certain,
  ampliative force caps at defeasible). Withdrawn conclusions surface as
  **open stubs**.
- **Forks:** structural detection deliberately over-detects (convergence looks
  like rivalry), so a rivalry is **declared** — a logged decision, i.e. an
  escalation (§13). **Corroboration is temporal:** only empirical evidence
  first-asserted *after* the fork opened can collapse it; the losing branch is
  eclipsed, never deleted.
- **Fidelity calculus** (`engine/fidelity.py`): fidelity is *not*
  probability-of-truth (that would be the apple in numeric dress) but a
  structured, web-internal measure of **invariance under the web's own
  dynamics**. The object is the ATMS **label** — a record's minimal
  environments (sets of grounds, inference tokens included); everything else
  is *entailed* from the environment: ampliative attenuation (`amp`), leaf
  warrant profile, fork variables (`via`). Backward **corroborating
  environments** flow from fresh downstream successes (the temporal rule).
  Scalars are purpose-relative *projections* — the engine's `Level` is
  provably the coarsest one (the demo asserts grade ⇔ Level agreement at
  every moment). Verified structural truths: the Adams/Le Verrier convergence
  corroborates the *execution*, not the premises (their environments differ
  only in inference tokens); Galle's corroboration is genuinely new evidence
  (in no base environment of the hypothesis).

- **Identification** (`Engine.identify`): rivals proven equivalent — the fork
  **dissolves** rather than collapsing (status `identified`, no winner, no
  eclipsed; pre-empts eclipse), and the pair's environments **pool** in the
  fidelity view: corroboration earned by either formulation accrues to both.
  Matrix vs wave mechanics (1926) is the type case.
- **Explananda** (`fidelity.explananda`): the second stub species — phenomena
  *supported but only observationally*, no live theoretical environment
  (convention: a theoretical environment carries a formally-warranted
  machinery leaf). `stubs()` is support that fell (drives repair);
  `explananda()` is support that never rose past observation (drives
  discovery). Fine structure 1891–1916 is the type case.

- **Executable mathematics** (`engine/mathcontent.py`, a deliberate *sidecar*
  — content now enters the graph as **`rec:formulation`**, the form as held,
  decided in `ROOT.md` §15; *execution* stays engine-side, since the reasoner
  never evaluates a formulation): the atom fixture's key inference tokens carry
  runnable sympy derivations, making three claims demonstrable rather than
  asserted. **Formal warrant, run** (§2): E_n and the Balmer formula are
  re-derived from the postulates; the Rydberg constant computed from e, m, h,
  c matches spectroscopy to ~10⁻⁸; the reduced-mass answer to Fowler lands on
  his measured 4.0016. **The Sommerfeld coincidence, exact**: the 1916 and
  Dirac-form spectra are *identical* under k = j + ½ — same conclusion,
  disjoint premises. **§14 puncturing, run**: delete the derived records'
  content and it regenerates from postulates + machinery alone; the data
  leaves do not — the punctured core is exactly the non-derivable residue.

- **Exercise-or-exorcise** (`engine/exercise.py` + `Engine.exorcise`,
  `ROOT.md` §15.3): formal warrant is **earned, not stipulated** — a formal
  record's `formulation` is a description (sides, angles, relationships) that
  can be *run*; exercising it confirms the warrant, and a failed exercise
  **exorcises** it: a log event with a moment that expels the *pretender*
  (the record stays — history keeps the document; records about it survive —
  but it can no longer transmit support, and everything resting on it
  cascades away). Never-exercised = testimonially held, stated honestly.
  Kempe/Heawood in miniature: the demo pair is the triangle (passes) and the
  2 = 1 pseudo-proof (fails at its hidden division by zero).
- **The arithmetic companion + the formulation compiler**
  (`ontology/arith.ttl` + `engine/compile.py`): full structural description —
  "the whole thing: sides, and all, coming together." The companion lays out
  the formal *object* face at representative scope: four operations in a
  **definitional hierarchy** bottoming at the Peano ground (mathematics' own
  derivation web, all formal — §14's limiting case), and **expressions as
  formal Records composed of Records** (`arith:Expression ⊑ rec:Record`,
  operands ⊑ `composedOf`). Described records are exercised by a *compiler*
  that walks the subgraph into sympy — exercise derived from the description,
  not hand-written beside it; closed-world well-formedness (a missing operand)
  is a `CompileError`, since OWL cannot see absence. **Performative
  provenance**: every exercise act is logged at a moment
  (`Engine.log_exercise`), so earned warrant has a genealogy and each record
  carries a lifecycle **standing**: unexercised → confirmed / failed →
  exorcised.

```bash
python scripts/engine_demo.py     # runs the Neptune fixture's fork-collapse oracle
python scripts/fidelity_demo.py   # exercises the calculus; agreement + §2 checks
python scripts/bohr_demo.py       # the atom 1885–1927: explananda resolved one per
                                  #   era; the Sommerfeld coincidence as environment
                                  #   swap; matrix ≡ wave as fork dissolution
python scripts/bohr_math_demo.py  # the same arc's mathematics, executed: Bohr's
                                  #   derivation run, Rydberg recomputed, the
                                  #   coincidence exact, puncturing demonstrated
python scripts/exercise_demo.py   # the triangle verified by running it; the 2=1
                                  #   pseudo-proof exorcised; the cascade + the
                                  #   surviving publication
python scripts/arith_demo.py      # the companion: the triangle exercised FROM its
                                  #   description (compiled, act logged at a moment);
                                  #   the pretender fails by derivation
```

```python
from engine import Engine, fork_report
eng = Engine("ontology/record-ontology.ttl",
             "examples/neptune-discovery.ttl", defer=["GalleObservation"])
eng.declare_rivals("UnseenPlanetClaim", "ModifiedGravityClaim")
eng.assert_ground("GalleObservation")      # evidence arrives → fork resolves
eng.retract("LawOfGravitation")            # cascade: both forks re-level out
state = eng.state()                        # or eng.state(moment) — as-of views
```

## Open items

- **Composition transitivity** — `partOf`/`composedOf` left non-transitive on
  purpose (cf. the sibling, which dropped `buildsUpon` transitivity for OWL 2 DL).
- **Namespace** — confirm `epistemic-ontology.net/record#` before external
  adopters rely on the IRIs; hosting under `epistemic-ontology.net` (slug
  `record`) is pending.
- **Non-monotonic propagation** — a working **prototype** now exists
  (`engine/`, validated against the Neptune oracle by `scripts/engine_demo.py`),
  including the **fidelity calculus** (`engine/fidelity.py`: exact ATMS
  semantics at exemplar scale; approximation at scale is a known open
  problem). Still open from §10: the what-if visual explorer.
- **Escalations, formation, and the moment** — the decision layer (trade-offs
  between objectives replacing punitive calculus; escalation history *forming*
  the agent) and order-derived time (moments as positions in the
  happened-before order; the clock as a defeasible overlay) are recorded as
  horizon in `ROOT.md` §13, not yet vocabulary.
- **The knowledge-automaton** — a groomed record web as a generative asset:
  subsumption creates redundancy, warrant entails the puncturing map (formal
  interior regenerates by deduction; empirical leaves and the escalation trail
  must be kept), regeneration is replay. Recorded as horizon in `ROOT.md` §14;
  engine/asset layer, no vocabulary proposed.

## License

The ontology and documentation are licensed **[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)** —
permissive, reuse and adapt freely (including commercially), with attribution:

> "The Record Ontology — epistemic-ontology.net" — https://www.epistemic-ontology.net/record

The software (`scripts/`, `engine/`) is additionally available under the
**MIT License**. See [LICENSE](LICENSE). Copyright © 2026 Ron Hinchley / epistemic-ontology.net.

## Related

- **record-harm** — models how a Record is *damaged*; intended to source its
  `Record` and `Agent` from this ontology once it stabilises.
