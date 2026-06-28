# The Record Ontology — Root

> A base, deliberately given wide berth. The concept is slippery and "can vanish
> without trace"; this document and its Turtle stub exist so the idea-record is
> not destroyed — the ontology applied, at once, to itself.

This file is the **faithful capture** of the root we settled in discussion. The
Turtle stub (`ontology/record-ontology.ttl`) encodes only what is settled here.
Everything is open to amendment; the point is to have a record to amend rather
than a thread to remember.

---

## 0. The constraint (what makes this ontology *this* ontology)

The ontology is **constrained to agents** — a person or an AI. It is built *for*
an agent and never steps outside one. This is not a limitation to be engineered
away; it is the founding discipline, influenced by the constraint at the heart
of Bonhoeffer's *Ethics*: the temptation is *sicut deus* — to know good and evil,
to occupy the standpoint that sees both the thing and its representation and
certifies the correspondence. That standpoint is the apple. We do not eat it.

**The rule that follows:** *no class may be defined by a relation to an object
that lies outside all records.* We name records by what the agent actually
holds — their form, the mode of their givenness, their relations to other
records, their pragmatic adequacy — **never** by a certified correspondence to a
thing-in-itself. (This is why an earlier "Representational Record / record *of*
the world" was rejected: "of" smuggles in an all-knowing observer who sees both
the shadow and its caster.)

## 1. The one class: **Record**

There is a single class. A **Record** is *a form, in a carrier, for an agent, at
a level of abstraction.*

We do **not** posit a separate `Form` class. The triangle-in-itself is no more
available to an agent than the thing-in-itself; we never hold the form
un-recorded — we hold a record warranted *formally*. A standalone `Form` class
would be the *formal* apple (an ideal object grasped from outside all records).
Same refusal, applied symmetrically to both sides.

## 2. Attributes (not kinds)

What used to look like *kinds* of record are **attributes**, because records are
**patchworks** — one paper carries equations (formal) and observations
(empirical) in one body. If these were disjoint subclasses, a single record
could not be both. As attributes they attach to a record's **grounds/parts**, so
one Record is formal here and empirical there.

- **warrant** — *formal ↔ empirical/given*. How the agent **holds/justifies** the
  record: formally (internal, deductive — the triangle verifies itself) or by
  **givenness** (arriving through the senses or an instrument; defeasible, never
  closed). Demoting "formal" from kind to attribute is the same move as not
  eating the apple, completed — it describes how the record is *warranted*, not a
  relation to a thing-in-itself.
    - The **formal** side itself has **two faces**: *formal objects* (the
      **triangle** — a self-standing structure, complete in itself) and *formal
      operations* (**inference** — a transition over records). This is the
      object/morphism (term/rule, formula/derivation) duality, and is plausibly
      *exhaustive* of formal content. See §8.
    - Inference carries a second parameter, its **force**: *truth-preserving*
      (deductive — passes a triangle's completeness through unchanged) or
      *ampliative* (abductive/inductive — adds content, hence **defeasible even
      from certain premises**). Force is what makes inference the **hinge between
      formal and empirical warrant**.
- **level of abstraction (grain)** — the excision needed to support something may
  vary: a light switch (works, expected to), or Maxwell's equations, or a
  quantum-mechanical account. Floridi's *Level of Abstraction*.
- **directedness** — the *intentional object*: what the record is *of*, **as
  recorded** (Husserl; Peirce's *immediate* object). Not a certified reference.
  The agent holds the object-as-presented; the object-as-it-is is approached
  asymptotically and never possessed (see §4).
- **provenance** — the genealogy: sensory observation → formal mental paths →
  traversal between agents → establishment in broad contexts (society, books).
  *The excision is always part of the support*: provenance/context is
  **constitutive, not metadata** — it cannot be fully stripped.
- **pragmatic adequacy** — fitness for purpose ("expected to work"), relative to a
  purpose and an agent (Peirce/Dewey).

**Entailed, not stipulated:** **completeness** and **fidelity** are *not*
primitives — they follow from **warrant**. Formally-warranted grounds are
internally completable and high-fidelity (the type is recoverable from the
token with little loss — why discrete/formal codes transmit well); empirical
grounds are neither. One fewer thing to assert.

## 3. Composition

**Records are made of Records.** The hierarchy/patchwork is mereological:
formal and empirical grounds, woven together, communicated — a book, an idea
passed between agents. (Mereological transitivity is left *uncommitted* in the
base — see §5.)

## 4. The two excluded limits

Two things the model **points at but never instantiates** — regulative posits,
**never classes**:

- the **world-in-itself** — Peirce's *dynamical object*, the caster of the
  shadow. Approached only through **directedness**, never reached. The
  permanently open gap between the immediate and dynamical object just *is* our
  finitude.
- the **form-in-itself** — the Platonic triangle. Approached only through
  **formal warrant**. (A formally-warranted record is *internally* completable —
  deduction closes it — which is an operation the agent performs, **not** a grasp
  of the form-in-itself.)

To make either a class would re-seat the all-knowing observer. They stay outside.

## 5. The Continuum (the one non-Record)

The **Continuum** is the undivided, continuously interacting ground — the *only*
thing that is **not** a record and not agent-relative; the origin you never get
behind. One distinguished individual, not a class of many. Carriers are
**individuated** from it, and the cut is never clean: *the excision is always
part of the support*, and (the universe interacting continuously) the support is
never causally sealed off from what it was cut from. **No support equals the
whole Continuum ⇒ no total support, no complete [empirical] record.** This is
"we will not become all-knowing," stated as structure rather than regret.

## 6. Settled vs. open

**Settled (encoded in the stub):**
- One class `Record`; agent-relativity (every Record is *for* an Agent).
- Attributes: warrant (formal↔empirical), level of abstraction, directedness,
  provenance, pragmatic adequacy. Fidelity/completeness *derived*, not primitive.
- Composition (Record of Records).
- Continuum as the unique non-Record ground (disjoint from Record).
- The two excluded limits, recorded as commentary, never as classes.
- The formal warrant splits into *objects* (triangle) and *operations*
  (inference); inference carries a *force* (truth-preserving ↔ ampliative). §2, §8.
- Inference modelled by relational form (`hasPremise`, `concludes`) and surfaced
  as a **defined** class `Inference` — not a primitive kind. §8.
- **No metadata:** records directed at records; `metadataOf` is a defined,
  LoA-relative role, never a class. §9.
- **Carrier is a distinct relatum** (`borneBy`), well-founded because it bottoms
  out at the **Agent** via the cogito; the *foundational carrier* is a defined
  class. §11.
- **Stance:** DL-in-form, ecumenical-in-content — the OWL/DL ↔ SKOS schism is
  demoted to the `warrant` attribute, not a choice of framework. §12.

**Open (left uncommitted on purpose):**
- **Composition transitivity** — `partOf`/`composedOf` left non-transitive for
  now (see §6 below); mereological transitivity is a deliberate later decision.
  (Cf. record-harm, which had to *drop* `buildsUpon` transitivity for OWL 2 DL.)
- **Namespace** — born at `https://www.epistemic-ontology.net/record#` rather
  than an `example.org` placeholder, applying the lesson record-harm is still
  paying for (its v3.0 migration). Confirm before external adopters rely on IRIs.

## 7. Relation to neighbours

- **record-harm** models how a Record is *damaged*; it should source its `Record`
  (and `Agent`) from **this** ontology once this stabilises. Its
  *Authenticity*/*Fabrication* become record-web–internal notions (genuine link
  to a *claimed* origin; a false *posit* exposed by incoherence with other
  records) — not correspondence to the noumenon.
- **epistemic-ontology.net** (`eon`) is the intended home; slug `record`.

## 8. Inference, the derivation DAG, and narrative

**Inference *is* a Record** — a formal record whose *form* is a transition over
records. So "an inference composed of inferences and records" introduces no new
compositional primitive: it is a Record `composedOf` other Records, **some of
which bear the inference role**. Base case — premises are empirical or triangle
records; recursive case — premises are the *conclusions* of other inferences.
The result is a **derivation DAG**: given/structural records at the leaves,
inferences at the internal nodes, one standing conclusion.

What sets inference apart from a triangle is not its compositional status
(everything composes) but its **relational form** — it has premises and a
conclusion. So it earns two properties a triangle never uses: `hasPremise`
(Record → Record) and `concludes` (Record → Record).

To keep the no-primitive-kinds discipline (§2), **`Inference` is a *defined*
class, not a primitive one**:

> `Inference ≡ Record ⊓ (∃hasPremise.Record) ⊓ (∃concludes.Record)`

A record *becomes* an inference by having premises — reasoner-recognised, never
stipulated — so a patchwork can have inferential joints without anything being
declared an "Inference kind" up front. Same refusal as not subclassing by
warrant.

**Historical narrative** is the canonical test, because it is a *mixed-warrant
patchwork*: empirical records at the leaves (attested sources), inferences —
*almost all ampliative* — at the joints, and a root narrative `directedToward`
the past (an excluded limit, §4). The model then **predicts the right
epistemics for free**: running on ampliative force over defeasible leaves, a
narrative can never reach triangle-completeness, so its revisability is
*entailed*, not bolted on. This is exactly where `record-harm`'s **Fabrication**
lives — a false posit in the DAG, exposable only by incoherence with the rest of
the web.

## 9. Metadata — there is none

The data/metadata split is **refused**. The excision is always part of the
support (§5), so what is called metadata decomposes with no remainder into
machinery we already have:

- An author, date-stamp, or citation is simply **a record directed at another
  record** (`directedToward` / `hasProvenance` ranging over Records) — a record
  *about* a record, nothing more exotic.
- "Metadata-ness" is **not intrinsic**: it is a **role relative to a chosen level
  of abstraction and purpose**. At a reading LoA a timestamp is background; under
  forensic authentication the *timestamp becomes the focal record* and the
  document its context — the roles swap. So it rides on `atLevelOfAbstraction` +
  `pragmaticAdequacy`, not on a class.

Like `Inference`, metadata is therefore a **defined relational role**
(`metadataOf`), never a primitive class — making it a class would quietly
re-seat the privileged outside vantage (a mild cousin of the apple).

## 10. Future directions (vision — not yet modelled)

Recorded so it does not vanish (late-session sketch, 2026-06-26). **None of this
is built**; it is the horizon the base is being shaped toward. The target is
complex science, where discoveries are built on earlier work and bottom out in
observation.

- **Science as a derivation DAG across time and agents.** A discovery is an
  inference whose premises are earlier conclusions — often *other agents'*, via
  provenance (observation → between agents → social fixation). Already carried by
  `hasPremise`/`concludes`/`composedOf`; "pull the evidence" = traverse premises
  to the empirical leaves. Fluid because it is Record-of-Records throughout.

- **Non-monotonic propagation (the genuinely new mechanism).** When a leaf
  observation changes, the effect should flow up the DAG: *re-level* dependents,
  *propagate uncertainty*, or *open a stub* where support is withdrawn.
  **Architectural rule:** OWL DL is **monotonic** — it cannot retract — so this
  dynamics is a **computational layer *over* the static ontology, never axioms in
  it.** The ontology holds the structure (DAG, warrants, forces); a separate
  engine computes fidelity, forks, and revisions. Keep the two strata distinct.
  Kin to study: truth-maintenance / **assumption-based TMS** (de Kleer —
  justifications, retraction, environments-as-forks) and belief/uncertainty
  propagation (Bayesian networks) over the same graph.

- **Fidelity as a combinatorial quantity (deepens §2).** Fidelity is already
  *entailed by warrant, not primitive*. The extension: it is entailed by the
  **whole sub-DAG** of warrants and forces feeding a record — computed, not a
  scalar stamped per node. **Forks for unknowns** = where ampliative/abductive
  inference admits competing explanations; each fork a candidate sub-DAG, fidelity
  distributed across them. An **open stub** is a first-class hole (a conclusion
  with an unresolved premise — candidate defined classes `OpenQuestion` / `Stub`).
  Refinement = forks collapsing as observations arrive; "discoveries pop out" when
  one fork's fidelity dominates or a stub resolves.

- **Quantum mechanics as the sharpest test — perhaps the truest domain.** Two
  resonances to chase: (1) the *excision / "the cut is part of the support"* maps
  onto the **Heisenberg cut** between system and apparatus; (2) measurement's
  irreducible incompleteness **is** the empirical-branch finitude of §5. A "level
  below to assist the quantum model" = a finer `atLevelOfAbstraction`, exercising
  the re-leveling mechanism. **Caution:** keep the *epistemic fork* (our unknown)
  distinct from *ontic superposition* (the physics) — they meet at
  measurement/decoherence but are not the same; the model must not conflate them.

- **Tie to record-harm.** A revision is *controlled* change; **fabrication** is
  *uncontrolled* false change, exposed by incoherence with the DAG. The
  propagation engine and the harm model are two readings of the same web.

## 11. The Carrier and the cogito (resolving §6)

Why the Carrier question was hard: a **regress**. Every external record is borne
by a carrier *excised from the Continuum*, and the excision is never clean
(carrier ⊂ Continuum, never severed; §5). So what carries the carrier? Either an
infinite regress, or the web floats unanchored.

**Descartes halts it — credit to him.** The **cogito** is the one record whose
carrier is *the act of recording itself*: "I think" is borne by the thinking,
and its tokening entails its own support. The carrier is self-supporting, so the
regress stops — at the **Agent**.

**Resolution:** the Carrier is a **distinct relatum** (`borneBy`: Record →
Carrier), *not* dissolved into Continuum-locus — and it is **well-founded**
because it bottoms out at the Agent. Both old intuitions were partly right:

- for **external** records the carrier really *is* its excised locus/provenance
  (the "dissolve" intuition holds there);
- for the **cogito** the carrier is the **Agent** itself.

So Carrier is one relatum with **two grounding modes**: Continuum-excision (the
many, defeasible) and Agent (the one, self-supporting).

**The fixed point.** The cogito is where the three roles we keep apart *collapse
onto the Agent*: the agent is the *for-whom* (A1), the *carrier* (`borneBy`), and
the *intentional object* (`directedToward`) at once. Indubitable *because* of the
collapse. This gives the system its epistemic shape: a **coherentist web** (§7)
with exactly **one foundationalist anchor**. And it marks an asymmetry with §4 —
the world-in-itself and form-in-itself stay excluded limits, but the
**Agent-in-itself is not excluded**; it is the one thing given to itself.

**The boundary — how much Descartes to credit.** We take the fixed point, not the
substance. The cogito certifies *that* the carrier-agent **exists** (the "I am"),
not *what* it is. Descartes' slide from "I am" to "I am a thinking substance"
(*res cogitans*) is a self-knowledge **apple** — a transparent, complete grasp of
the agent-in-itself. Finitude (§5) must survive even here: the foundational
carrier is a certain anchor of **existence**, not a fully-known object. We halt
the regress with him; we leave the substance dualism on the table.

*Modelled as:* `rec:Carrier` + `rec:borneBy`; `rec:Cogito` a **defined** class
(a Record borne by an Agent — its carrier is an agent, not a Continuum-excision);
`rec:FoundationalCarrier` a **defined** class (a Carrier that is an Agent — the
self-supporting mode). Descartes credited in the term metadata.

## 12. Stance — between the OWL/DL and SKOS/thesaurus camps

A standing schism in knowledge representation: the **OWL/DL** camp (terms are
**classes** with truth-conditions; a **reasoner** classifies and checks
consistency; `owl:Class`/`equivalentClass`/`disjointWith`) versus the
**SKOS/thesaurus** camp (terms are **concepts** related *associatively* by
community convention; `skos:Concept`/`broader`/`related`, deliberately weak, for
indexing and retrieval; SKOS-as-published is OWL Full).

**This implementation is DL-in-form.** Every concrete choice is the DL choice:
defined classes by necessary-and-sufficient conditions, reasoner re-derivation
(`validate.py`), `owl:disjointWith` + a consistency check, dropping transitivity
to stay in OWL 2 DL (in the sibling), and the explicit decision *not* to import
SKOS because it is OWL Full. We say `rdfs:label`, not `skos:prefLabel`.

**But ecumenical-in-content.** The schism is demoted from a *choice of framework*
to an *attribute of a record* — **`warrant`**. A DL hierarchy is a record
warranted **formally** (subsumption, truth-preserving); a SKOS thesaurus is a
record warranted **empirically/given** (community-fixed, ampliative, defeasible —
`skos:broader` is a curatorial edge, not a deductive one). We refuse to make
"ontology vs. thesaurus" a *kind*; it is a *warrant*. A real scientific taxonomy
is **both** — formal at some joints, conventional at others (the patchwork, §2).
So the ontology does not take a side; it **represents the axis** the camps fight
over, using the DL machine to formalise *why* most knowledge is conventional and
never formally complete.

**A third position.** The DL camp's implicit ideal is formal **foundationalism**
(axioms close the world); the SKOS camp is conventional **coherentism** (no
bedrock). Our cogito-anchored web (§11) is **neither** — a coherent web with one
fixed point. This also settles the modelling discipline: because we are DL in
form, the foundational carrier is a *defined class*, not a SKOS-style associative
gesture.

**Where the schism re-enters (the QM roadmap, §10).** Scientific vocabularies —
"spin," "observable," "eigenstate" — *are* community-fixed concepts (SKOS-shaped)
feeding a *formally* structured inference DAG (DL-shaped). `warrant` is the
bridge. And the schism itself is a §10 **fork**: two agent-communities with
different warrant-defaults, an unresolved fork the ontology can represent.

---

*Provenance of this document:* reconstructed verbatim from session transcript
`8adf28a9` after a network failure (ConnectionRefused) killed the original
write mid-sentence — the base had been agreed but never hit disk. Recovered and
recreated 2026-06-26.
