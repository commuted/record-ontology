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

- **warrant** — *formal · empirical/given · self-verifying*. How the agent
  **holds/justifies** the record. Demoting warrant from kind to attribute is the
  same move as not eating the apple, completed — it describes how the record is
  *warranted*, not a relation to a thing-in-itself. **Three values, one per
  limit** (the strongest reason it is a triad, not a pair — see the table below):
    - **formal** — true *in virtue of form* (internal, deductive — the triangle
      verifies itself); **agent-independent**, type-level; reaches toward the
      *form-in-itself* (excluded, §4). Internally completable. Two faces: *formal
      objects* (the **triangle** — a self-standing structure) and *formal
      operations* (**inference** — a transition over records); the object/morphism
      (term/rule, formula/derivation) duality, plausibly *exhaustive* of formal
      content (§8). Inference also carries a **force**: *truth-preserving*
      (deductive — passes a triangle's completeness through) or *ampliative*
      (abductive/inductive — adds content, hence **defeasible even from certain
      premises**). Force is the hinge between formal and empirical warrant.
    - **empirical / given** — true *by givenness* (through the senses or an
      instrument; defeasible, never closed); agent-relative; reaches toward the
      *world-in-itself* (excluded, §4).
    - **self-verifying / performative** — true *in virtue of the act of recording*
      (Hintikka: the cogito as performance, not inference); **agent-dependent**,
      first-person, token-level; reaches toward the **Agent-in-itself**, the one
      limit that is **not** excluded but given to itself (§11). Indubitable but
      **punctual**: it certifies *existence, not nature* — high fidelity, **zero
      amplification** (you cannot deduce a domain from "I am"). This is the
      warrant of the cogito; it is a **peer of formal, not a species of it** —
      formal is agent-independent and extensible, self-verifying is
      agent-dependent and barren.

  | warrant | reaches toward | the limit's status |
  |---|---|---|
  | formal | form-in-itself | excluded (§4) |
  | empirical/given | world-in-itself | excluded (§4) |
  | self-verifying | **Agent-in-itself** | **not excluded** — given to itself (§11) |
- **level of abstraction (grain)** — the excision needed to support something may
  vary: a light switch (works, expected to), or Maxwell's equations, or a
  quantum-mechanical account. Floridi's *Level of Abstraction*.
- **directedness** — the *intentional object*: what the record is *of*, **as
  recorded** (Husserl; Peirce's *immediate* object). Not a certified reference.
  The agent holds the object-as-presented; the object-as-it-is is approached
  asymptotically and never possessed (see §4).
- **provenance** — the genealogy (*whence*): sensory observation → formal mental
  paths → traversal between agents → establishment in broad contexts (society,
  books). *The excision is always part of the support*: provenance/context is
  **constitutive, not metadata** — it cannot be fully stripped.
- **locus** — *where/when* the form is borne, **agent-relative** (as
  experienced/individuated), never a certified position in space-time-in-itself.
  Provenance (*whence*) + locus (*where/when*) are what the **carrier dissolves
  into** — there is no `Carrier` class (§11).
- **pragmatic adequacy** — fitness for purpose ("expected to work"), relative to a
  purpose and an agent (Peirce/Dewey).

**Entailed, not stipulated:** **completeness** and **fidelity** are *not*
primitives — they follow from **warrant**. Formally-warranted grounds are
internally completable and high-fidelity (the type is recoverable from the
token with little loss — why discrete/formal codes transmit well); empirical
grounds are neither; self-verifying grounds are maximally certain but
non-extensible (high fidelity, zero amplification). One fewer thing to assert.

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
behind. One distinguished individual, not a class of many. A record's support (its
locus) is **individuated** from it, and the cut is never clean: *the excision is always
part of the support*, and (the universe interacting continuously) the support is
never causally sealed off from what it was cut from. **No support equals the
whole Continuum ⇒ no total support, no complete [empirical] record.** This is
"we will not become all-knowing," stated as structure rather than regret.

## 6. Settled vs. open

**Settled (encoded in the stub):**
- One class `Record`; agent-relativity (every Record is *for* an Agent).
- Attributes: warrant (formal · empirical · self-verifying — one per limit),
  level of abstraction, directedness, provenance, locus, pragmatic adequacy.
  Fidelity/completeness *derived*, not primitive.
- Composition (Record of Records).
- Continuum as the unique non-Record ground (disjoint from Record).
- The two excluded limits, recorded as commentary, never as classes.
- The formal warrant splits into *objects* (triangle) and *operations*
  (inference); inference carries a *force* (truth-preserving ↔ ampliative). §2, §8.
- **Warrant is a triad, one value per limit:** formal (form-in-itself),
  empirical (world-in-itself), self-verifying/performative (Agent-in-itself —
  the cogito's warrant; a peer of formal, not a species). §2, §11.
- Inference modelled by relational form (`hasPremise`, `concludes`) and surfaced
  as a **defined** class `Inference` — not a primitive kind. §8.
- **No metadata:** records directed at records; `metadataOf` is a defined,
  LoA-relative role, never a class. §9.
- **Carrier dissolves** into `hasProvenance` + `hasLocus` (no `Carrier` class).
  The cogito's foundation lives in the **self-verifying warrant** + reflexive
  provenance — a *pattern*, not a class; the regress halts in the warrant. §11.
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

## 10. Scope and future directions

**Indicated scope — the epistemic structure, not the domains.** This is a
*domain-neutral* ontology of **warranted record-structure**: how agents warrant,
compose, ground, and revise records — the connective grammar of knowledge, not
the things known. It applies wherever agents build knowledge from evidence:
scientific discovery above all (the motivating case), but equally history (§8),
scholarship, law, intelligence analysis. It is **not a domain ontology** — it
models neither electrons nor organisms nor battles, only the *records* of them
and how they are held. (The same refusal as directedness: we never name a record
by the world-object it is "of"; §2.) Domain ontologies and vocabularies — SKOS
thesauri, scientific term-sets — **plug in** through `warrant` (§12); they are
*attached, never absorbed*.

**The rest of this section is unbuilt vision** (sketched 2026-06-26), recorded so
it does not vanish — the horizon the base is being shaped toward, where
discoveries are built on earlier work and bottom out in observation:

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

- **Tie to record-harm.** A revision is *controlled* change; **fabrication** is
  *uncontrolled* false change, exposed by incoherence with the DAG. The
  propagation engine and the harm model are two readings of the same web.

## 11. The carrier dissolved, and the cogito as self-verifying foundation (resolving §6)

Why the carrier question was hard: a **regress**. Every external record is borne
by a support *excised from the Continuum*, and the excision is never clean
(support ⊂ Continuum, never severed; §5). So what carries the carrier? Either an
infinite regress, or the web floats unanchored.

**Resolution — dissolution, not a new class.** The carrier is *not* a distinct
relatum. It **dissolves into two attributes already in hand**: `hasProvenance`
(the genealogy — *whence* the form was individuated from the Continuum) and
`hasLocus` (*where/when* it is borne, agent-relative — never a certified position
in space-time-in-itself). This honours the founding creed (§1–§2): **one class,
attributes not kinds**. Reintroducing a `Carrier` class to hold the support
would have bought the regress-halt at the cost of the ontology's own discipline.
(An earlier draft *did* make Carrier a relatum, `borneBy`, grounded at the Agent;
we reversed it — see "why the reversal" below.)

**Where, then, does the regress halt? In the warrant, not in a thing.** The
**cogito** is the record whose warrant is **self-verifying** (§2's third value):
"I think" is true in virtue of the *act* of recording it, and its **provenance is
that very act**. Its support is not a substrate it *has* but the thinking it *is*
— which is more faithful to Descartes than positing a carrier-substance. So the
regress stops not at an entity but at a **warrant** (self-verification) backed by
a **reflexive provenance** (the act that is its own genealogy). Credit Descartes
for the cogito; **Hintikka** for the warrant (performance, not inference).

**The fixed point.** The cogito is where the roles we keep apart *coincide on the
Agent*: the *for-whom* (A1) and the *intentional object* (`directedToward`) are
both the agent, and the *provenance* is the agent's own act. Indubitable
*because* of the collapse. This gives the system its epistemic shape: a
**coherentist web** (§7) with exactly **one foundationalist anchor** — placed now
in the self-verifying warrant, not a class. And it keeps the asymmetry with §4:
the world-in-itself and form-in-itself stay excluded limits, but the
**Agent-in-itself is not excluded** — it is the one thing given to itself, and
the self-verifying warrant is exactly the warrant that reaches it.

**The boundary — how much Descartes to credit.** The fixed point, not the
substance. The cogito certifies *that* the agent **exists** (the "I am"), not
*what* it is. Descartes' slide from "I am" to "I am a thinking substance"
(*res cogitans*) is a self-knowledge **apple** — a complete grasp of the
agent-in-itself. Finitude (§5) survives even here: a certain anchor of
**existence**, not a fully-known object.

**Why the reversal** (from the earlier distinct-relatum resolution): two reasons,
both decisive. (1) **Discipline** — a `Carrier` class violates "attributes not
kinds"; dissolution into provenance + locus keeps the one-class ontology intact.
(2) **Over-capture** — a *defined* `Cogito` class (Record borne by an Agent with
self-verifying warrant) wrongly swept up *every* performative: a **promise** is
agent-borne and self-verifying yet is not the cogito (the normative/aesthetic
stress test surfaced this). Demoting the cogito from a **class** to a **pattern**
— self-verifying warrant + reflexive provenance + directedness at one's own
existence — dissolves the over-capture too: performatives share the *warrant*
without being mistaken for *the* cogito.

*Modelled as:* `rec:hasLocus` (new) alongside `rec:hasProvenance`; **no**
`Carrier`/`Cogito`/`FoundationalCarrier` classes and **no** `borneBy`. The cogito
is recognised by its pattern (self-verifying warrant, reflexive provenance,
self-directedness), not by a class membership a reasoner derives.

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
fixed point, anchored in the self-verifying *warrant* rather than a SKOS-style
associative gesture.

**Where the schism re-enters (the scope of §10).** A discipline's vocabulary —
its named concepts and categories — *is* community-fixed (SKOS-shaped), yet it
feeds a *formally* structured inference DAG (DL-shaped). `warrant` is the bridge:
the term is warranted by convention, the inference by form. And the schism itself
is a §10 **fork**: two agent-communities with different warrant-defaults, an
unresolved fork the ontology can represent.

---

*Provenance of this document:* reconstructed verbatim from session transcript
`8adf28a9` after a network failure (ConnectionRefused) killed the original
write mid-sentence — the base had been agreed but never hit disk. Recovered and
recreated 2026-06-26.
