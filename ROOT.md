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
- **Formulation** — `rec:formulation`, the form as held: the first datatype
  property (§15). Opaque to the reasoner by design (DL stays decidable); for
  formally-warranted records it should suffice to *exercise* them. Exercise
  and exorcism are engine events, never OWL vocabulary — warrant is earned by
  exercise, withdrawn by exorcism, at a moment. §15.

**Open (left uncommitted on purpose):**
- **Composition transitivity** — `partOf`/`composedOf` left non-transitive for
  now (see §6 below); mereological transitivity is a deliberate later decision.
  (Cf. record-harm, which had to *drop* `buildsUpon` transitivity for OWL 2 DL.)
- **Namespace** — born at `https://www.epistemic-ontology.net/record#` rather
  than an `example.org` placeholder, applying the lesson record-harm is still
  paying for (its v3.0 migration). Confirm before external adopters rely on IRIs.
- **Objectives and the escalation pattern** (§13) — objectives must become
  first-class (today latent in `pragmaticAdequacy`); escalation as a *defined*
  relational pattern over them. No vocabulary committed yet.
- **The moment** (§13) — order-derived time (happened-before over
  `hasPremise`/provenance). Deliberately *not* axiomatized in OWL (would force
  the transitivity question); engine-materialized, carried by the revision log.

## 7. Relation to neighbours

- **record-harm** models how a Record is *damaged*; it should source its `Record`
  (and `Agent`) from **this** ontology once this stabilises. Its
  *Authenticity*/*Fabrication* become record-web–internal notions (genuine link
  to a *claimed* origin; a false *posit* exposed by incoherence with other
  records) — not correspondence to the noumenon.
- **arith** (`ontology/arith.ttl`, slug `arith`) — the **arithmetic
  companion** (§15): the formal *object* face laid out in full, representative
  scope (four operations in a definitional hierarchy bottoming at the Peano
  ground; expressions as formal Records — `arith:Expression ⊑ rec:Record`,
  operands ⊑ `composedOf`). Attached never absorbed (§12's pattern applied to
  mathematics itself); the reasoner checks shape, the engine computes value.
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

## 13. The escalation view, formation, and the moment (unbuilt, recorded 2026-07-03)

**Horizon, like §10** — recorded so it does not vanish; nothing here is in the
Turtle. Three linked ideas that join at the root.

**13.1 The escalation view — replacing punitive calculus.** An **escalation** is
a *surfaced trade-off between objectives*, and every decision process is a
resolution of such trade-offs; escalations are **between objectives, always**.
Like inference (§8), an escalation is set apart by its **relational form** —
objectives in tension, plus a resolution — so it will be a *defined* pattern,
never a primitive kind. This forces **objectives to become first-class**
(currently latent in `pragmaticAdequacy`, range deferred).

- **Why it replaces punitive calculus.** Punitive calculus judges an agent
  against what they *should have known* — a counterfactual, fully-informed
  standpoint. That is the *sicut-deus* apple applied to time: **hindsight is
  the god's-eye view along the temporal axis**. The replacement criterion is
  web-internal: judge by (a) the sub-DAG **as it stood at the agent's moment**
  (13.3), and (b) whether the escalation was **explicit** — recorded — never by
  whether the resolution turned out right. The blame boundary moves from "was
  it wrong?" (correspondence — unavailable) to "was the trade-off recorded?"
  (available). Same move as record-harm's Fabrication becoming
  incoherence-with-the-web: **fabrication is a concealed escalation** — a
  trade-off made but never surfaced, exposed later by incoherence (§7, §10).
- **Skipped data is normal.** Deliberately skipping data is §5 restated as
  decision practice: the excision is constitutive; no total support; finite
  agents *must* winnow. The honesty condition: the skip should itself become a
  record ("X deferred, for objective Y, at this moment") — and that is exactly
  the §10 stub machinery. **A stub is the explicit form of a skip**; the same
  gap left unrecorded is where negligence and fabrication live. Stubs are not
  just epistemic bookkeeping — they are the ethical hinge.
- **Errors are entailed, not primitive.** An error is *a node whose support was
  later withdrawn* — precisely what the propagation engine computes.
  Error-identification falls out of non-monotonic re-leveling, time-indexed and
  relational; no punitive stamp needed. One fewer thing to assert (again).
- **Actions are maximal escalations.** The record web is non-monotonic, but
  **time is monotonic**: the engine can retract a belief; nothing retracts an
  action. Escalations therefore order by **irrevocability** — noticing a
  tension < recording it < ranking it < acting on it — with action at the top
  because it spends the one non-retractable resource. Adopted (*scoped*)
  objectives sit there too: adopting an objective governs all downstream
  winnowing. This is why a decision layer is needed at all, given a retraction
  engine: **retraction reaches records, never the world.**
- **The winnowing regress and its halt.** Not every escalation can be recorded
  (recording costs; total explicitness is another god-like demand), so
  escalations are themselves winnowed and ranked — and that ranking is an
  escalation. The regress halts by **level of abstraction**, as metadata's did
  (§9): record the winnowing *policy*, not every application. Significance is
  combinatorial like fidelity (§10): computed over the web, never stamped per
  node.

**13.2 Agent-centricity — formation, not verdict.** Escalation records feed
back into the agent: the accumulated, winnowed history of one's own escalations
becomes the **prior for future winnowing**. So the purpose of recording
trade-offs is finally stated — not adjudication but **formation**. This is
virtue-shaped rather than court-shaped, and it completes the Bonhoeffer lineage
of §0: refusing the judge's standpoint was never amoral — it relocates good and
bad from *verdicts on* the agent to *formation of* the agent.

- **The Agent gains interior structure, but only as records.** Character — the
  standing residue of escalation history — is a **self-directed, empirically
  warranted, defeasible** record. The §11 boundary survives: the cogito
  certifies *existence, not nature*; finitude applies reflexively; **no agent
  completes its own file**. This keeps agent-centricity from becoming a
  self-knowledge apple.
- **The back door to guard.** Punitive calculus will try to re-enter as a
  *scalar* — a reputation score or reward signal stamped per agent. Refused for
  the same reason fidelity is never stamped per node: agent quality is
  **entailed by the whole web** (which escalations were explicit, how their
  sub-DAGs fared). Escalation records inform future decisions **as premises,
  never as a number**. A reputation scalar is punitive calculus with better
  marketing.
- **Person or AI alike** (§1's A1): formation-by-recorded-escalations is the
  defensible shape of AI self-improvement — post-hoc review of explicit
  trade-offs feeding policy, evaluated as-of-the-moment, no god's-eye reward.

**13.3 The moment — time from order; the clock as overlay.** `hasLocus` already
refuses "a certified position in space-time-in-itself" (§2) — which means
**clock time was always apple-adjacent**. What the agent actually has is
*order*: this-was-built-on-that. The derivation DAG already induces it —
`hasPremise` and provenance edges are a *happened-before* relation (credit
**Lamport**, arrived at here from the epistemology side). A **moment** is a
position in that order. It is therefore **entailed by structure the web already
has, not a new primitive** — one fewer thing to assert; the same move as
fidelity, error, and inference.

- **A partial order, and that is a feature.** Across agents there is no global
  clock: two agents' concurrent moments are genuinely *incomparable* until a
  communication record creates an edge (the letter to Galle, in the Neptune
  exemplar). A **priority dispute** — Adams v. Le Verrier is the canonical case
  — demands a *total* order the record web honestly supplies only partially:
  punitive calculus applied to time.
- **Retrospection is as-of-moment, not as-of-timestamp.** The temporal place of
  an error or escalation (13.1) is the sub-DAG **reachable at that point in the
  order**. Anachronism becomes *structurally detectable without any clock* — a
  premise edge from a record that sits later in the order — a purely
  web-internal test, exactly what the founding rule permits.
- **Clock time re-enters as content.** A date is a record *about* a record
  (`metadataOf` — the Atticus dating in the narrative example is already this):
  an empirically warranted, defeasible claim tying a moment to a calendar.
  Dating documents *is* reconciling order with clock. The clock is a derived
  overlay — important when coordinating across webs or with the world's
  periodic processes — while the moment is load-bearing.
- **Strata discipline (§10's rule, applied to time).** Order stays **out of the
  OWL stratum** — axiomatizing it would demand the transitivity §6 deliberately
  defers. The engine materializes moments; the append-only revision log is
  their carrier (log position = moment; as-of views index by it); a retraction
  is a **new moment appended, never a rewrite of old ones** — "a record to
  amend rather than a thread to remember," applied to time itself.

**13.4 Where they join.** The cogito is **punctual** (§2): it certifies
existence *at the act*, token-level — so **the cogito is a moment**, and
nothing more. The agent's continuity across moments — the very character that
escalation history forms (13.2) — is an **empirical composition of punctual
self-verifying anchors**: certain of existence at each token, only defeasibly
stitched into a persisting self (the *res cogitans* refused again, now along
the temporal axis). Formation is what composition-across-moments looks like
from the inside.

## 14. The first escalation is the cut, and the knowledge-automaton (unbuilt, recorded 2026-07-03)

**Horizon, like §10 and §13** — recorded so it does not vanish; nothing here is
in the Turtle, and (unlike §13) nothing here even asks for vocabulary: this is
the engine/asset layer imagined at full size.

**14.1 The first escalation is the cut (§5 ⋈ §13).** The excision that
individuates a support from the Continuum is itself an escalation — the primal
one, made before any objective is explicit. What to excise and what to leave
*is* a trade-off; §5 already says the cut is never clean and the excision is
always part of the support. So winnowing is not something agents *add* to
records — **records begin in it**: every record's existence already embodies an
escalation, and provenance is the escalation trail read backward. This grounds
§13 retroactively — the escalation view was never a layer *on top of* the
ontology; it was present in the first act the ontology describes.

**14.2 The knowledge-automaton.** Imagine an agent's groomed record web operated
as a *generative* store — a **knowledge-automaton** that grows by the §13 loop
(escalations surfaced, recorded, ranked; formation as the prior for future
winnowing), expanding in **size and accuracy together**. Then the payoff the
base has been quietly preparing:

- **Growth in accuracy creates compressibility.** *Subsumption* is the DL word
  for the growth of internal redundancy: as grooming strengthens the general
  records, ever more of the web's interior becomes *derivable* from them —
  and what is derivable need not be stored.
- **The puncturing map is entailed by warrant (§2 pays off).** §2 already holds
  that formally-warranted grounds are high-fidelity because "the type is
  recoverable from the token with little loss — why discrete/formal codes
  transmit well." Read as compression: the **formally-warranted interior may be
  punctured** — deduction regenerates it on demand. **Empirical leaves cannot
  be regenerated** (no total support, §5) and must be kept. **Ampliative
  regions regenerate only defeasibly**: a punctured abduction may regenerate a
  *different fork* — drift. (The analogy is punctured convolutional codes under
  Viterbi decoding: drop exactly the bits the trellis's redundancy lets the
  decoder reconstruct. Here the trellis is the derivation structure, the
  puncturing matrix is the winnowing policy, and decoding is re-derivation.)
- **So the minimal asset is the non-derivable residue:** the empirical leaves +
  **the escalation records themselves** — fork resolutions, explicit skips, the
  winnowing policy — + pointers to the formal machinery. The "details kept for
  reconstruction" are precisely the **escalation trail**: everything
  deductively downstream of a decision regenerates, but the decision itself
  never does. Cut down after subsumption, the automaton becomes a small,
  dependable asset that regenerates specific knowledge on demand.
- **Regeneration is replay.** The §13.3 moment machinery already provides the
  mechanism: re-derivation from the punctured core *in order* (the revision
  log), "pull the evidence" run forward. And the fidelity calculus (§10)
  doubles as a **rate–distortion theory of knowledge**: a web's compression
  ratio is its warrant profile — formal-heavy webs punct to almost nothing;
  ampliative-heavy webs must keep their decisions or accept drift.

**14.3 Divergence between agents — §12 generalized, not a bug.** Importance is
objective-relative (§13.1), so two agents' automata puncture *differently*:
what one drops as derivable-noise another keeps as load-bearing. This is the
OWL/SKOS schism (§12) generalized from communities to agents — different
winnowing priors, an unresolved fork the ontology can represent.
Interoperability is therefore not agreement but **transmitting the puncturing
policy along with the core** — the excision is part of the support, stated for
compression. (A teaching aside: a **textbook is a punctured web** — axioms,
kept worked details, and exercises that make the student *regenerate the
interior*. Education is puncturing tuned so the decoder strengthens by
decoding.)

**14.4 Birthing, and the guard (§13.2 applied).** How does such an automaton
stay on track? Seed it with a known base web — *birth it* with curated
knowledge — then let lived escalations shape its importance-prior: formation
**becoming its choices**, the §13.2 loop run at full scale, for a person or an
AI alike. The guard matters more here than anywhere: an automaton that grooms
its own store is judge and party at once, and **concealed grooming is
self-fabrication** (§13.1) — a trade-off made against one's own web and not
recorded. The explicitness discipline is what keeps the asset auditable: the
escalation trail it must keep for *reconstruction* is the same trail that keeps
it *honest*. Compression and integrity turn out to be one requirement.

## 15. The form, fattened: formulation, provenance of the formal, exercise-or-exorcise (decided 2026-07-03)

Unlike §13–§14 this section **settles vocabulary**: `rec:formulation` enters
the stub (v0.6.0), the ontology's first datatype property. The rest is
engine-side discipline, prototyped.

**15.1 Formulation — the missing first component.** §1 defines a Record as *a
form, in a carrier, for an agent, at a level of abstraction* — and until now
every record in the fixtures carried **no form**: labels (prose glosses) and
structure (premises, warrants), but E_n and the triangle's description lived
nowhere in the graph. The ontology of forms-in-carriers contained no forms.
`rec:formulation` closes the gap: **the form as held, serialized** — a literal
carrying the record's own content (a formula, a constraint list, a text, a
data table — it is *not* math-specific; the Atticus letter's formulation is
its text). This passes the founding rule: it is the *token serialization of
what this agent holds*, not the form-in-itself (§1's refused `Form` class
stays refused; §4's limit stays excluded — the triangle has content here, but
no birthday, 15.2).

Two disciplines ride with it:

- **The reasoner never evaluates a formulation.** OWL 2 DL is decidable
  *because* it excludes nearly all mathematics; a formulation is opaque
  content to the classifier. Execution belongs to the engine — the §10
  architectural rule striking a second time, symmetrically: *dynamics live
  over the statics because DL is monotonic; computation lives over the
  statics because DL is decidable.* One rule, two corollaries: the ontology
  holds structure, engines perform operations (which §2 already located:
  internal completability "is an operation the agent performs").
- **For a formally-warranted record, the formulation must suffice to
  exercise it** (15.3): a description — the triangle's three sides, its
  angles, their relationships — not a picture. A formal record whose
  formulation cannot be run is held testimonially, whatever its warrant
  claims.

**15.2 Provenance of the formal — the coupling spectrum.** Formal warrant is
agent-independent and type-level (§2); provenance is agent-relative and
constitutive (§2, §5). No contradiction: they answer different questions —
warrant is *how is it justified?*, provenance is *whence did it come?* (Kant:
knowledge that *begins with* experience need not *arise out of* it; the
rationalist/empiricist quarrel was each collapsing one into the other). Ask
how tightly warrant couples to provenance and the triad completes itself, one
value per limit again:

| warrant | coupling | consequence |
|---|---|---|
| formal | **decoupled** — warrant survives total provenance loss | anonymous theorems are fine |
| empirical | **constituted** — lose the chain of custody, lose the warrant | anonymous data is worthless |
| self-verifying | **coincident** — the act is both genealogy and justification (§11) | an anonymous cogito is impossible |

Corollaries, several already living in the fixtures:

- Decoupling is *why* "the type is recoverable from the token" (§2), why
  formal codes transmit well, and why §14's puncturing works. Restated: **you
  may drop whatever is provenance-decoupled; you must keep whatever is
  provenance-constituted** — the minimal asset (leaves + escalation trail) is
  exactly the provenance-constituted residue.
- **Most mathematics-as-held is testimonially warranted.** §2's "internally
  complet*able*" is a capacity, rarely exercised; theorems are mostly held on
  traversal-between-agents (provenance). Running the derivation converts
  testimonial holding into formal holding — which is what the executable
  mathematics does.
- **Provenance and warrant can diverge under a standing conclusion**: the
  fine-structure formula's provenance forever runs through Sommerfeld's
  ellipses; its warrant now runs through spin. The environment swap is this
  divergence, computed.
- **Formal records are retracted as jurisdictions, never as forms**: 1926
  retracted the *postulates*; the phase-integral mathematics survives (as
  WKB). Same shape as Bohr's 1913 escalation — suspend the law's
  jurisdiction, not the law.
- A formal genealogy bottoms out in **an act of derivation by some agent** —
  never in the form. The form-in-itself stays an excluded limit (§4), so
  formal provenance approaches it exactly as directedness approaches the
  world-in-itself: asymptotically. **The triangle has no birthday**; only
  graspings of it do. (Epistemically constructivist, metaphysically silent.)

**15.3 Exercise-or-exorcise — warrant earned, not stipulated.** The validator
has always refused stipulated inference-hood: strip `a rec:Inference`, demand
the reasoner re-derive it. The same discipline now extends to formal warrant:
`hasWarrant rec:Formal` is a **claim**, and *exercising* the formulation —
running its description, checking it closes — is what confirms it. The
lifecycle:

> claim (assert formal) → **exercise** (run the description) →
> confirmed (warrant earned) *or* **exorcised** (warrant withdrawn)

with the common third state *before* the fork: never exercised = testimonially
held (15.2). What exorcism expels is a **pretender** — formal warrant worn
without the form — not the record: Kempe's 1879 "proof" of the four-color
theorem stood eleven years until Heawood exercised it; the paper remains a
real, historically important record (a record *about* it — §9 — keeps the
history), but its formal warrant is withdrawn, **at a moment** (1890). As-of
1885, trusting Kempe was justified — hindsight-blame stays the temporal apple
(§13). A repaired proof is a *new* record, not a restoration.

Two failure modes, now cleanly split (the fixtures bracket them):

- **jurisdictional** (Sommerfeld): the mathematics *passes* exercise — valid
  then, valid now — but its empirical premises fell. Retract the premises;
  the form is untouched.
- **formal** (Kempe): the description itself does not close. Exorcise the
  warrant; downstream support cascades away (the four-color theorem reverts
  to an *explanandum* until Appel–Haken — whose own exercise, fittingly,
  required a new machine).

This hands record-harm its second detector: **empirical fabrication** is
exposed by incoherence *with the web* (a concealed escalation, §13);
**formal fabrication** — the pseudo-proof — by incoherence *with itself*,
failing its own exercise. One fabrication concept, two detectors, one per
excluded limit.

*Modelled as:* `rec:formulation` (datatype property, v0.6.0) in the stub;
**no** OWL vocabulary for exercise or exorcism — like fork collapse, they are
**engine events over static structure** (`engine/exercise.py`,
`Engine.exorcise`; an exorcised ground keeps its place in the graph and the
log but can no longer transmit support). **Exercise acts are themselves
logged, at a moment — performative provenance**: a formal genealogy bottoms
out in acts of derivation (15.2), and the log entry is such an act's own
record — it attests itself (the performative face) while what it confirms is
formal (the content); two warrants, stacked. The earned warrant thereby *has*
a genealogy ("exercised at m, passed"), and the lifecycle carries a standing
per record: unexercised → confirmed / failed → exorcised. Full structural
descriptions — "the whole thing: sides, and all, coming together" — live in
the **arithmetic companion** (`ontology/arith.ttl`, §7): expressions as
formal Records composed of Records, exercised by a *compiler*
(`engine/compile.py`) rather than a hand registry — the exercise derived
from the description, not written beside it.

## 16. The engine grows its own discipline: generated suites, the observation planner, and the cycle run on Mars (prototyped 2026-07-07)

Engine-side throughout, like §15's second half: **nothing here enters the
Turtle** — three mechanisms, each a payoff of an earlier section, each
demonstrated green rather than asserted.

**16.1 Generated suites (§15's move, generalized).** The compiler derived an
exercise from a description; the same rule derives a SUITE from a web. Each
discipline implies a family of checks and the loaded web supplies the
instances: replay determinism and calculus agreement at every moment
(§13.3), label sufficiency and minimality environment-by-environment (§10),
Level ⇔ grade agreement, category-error refusal for every derived record
(§14), exercise-closure for every runnable description (§15.3). Nothing is
written per fixture (`engine/testgen.py`; 590 cases from the merged
exemplars at first run). The payoff is the **pretender alarm**: a record
whose exercise fails while it stands unexorcised is formal warrant worn
without the form — and the generated suite found BOTH planted 2=1 records
and, once the octants arrived, the vicarious hypothesis, with no test naming
any of them. §15.3's fabrication detectors, run as a regression suite the
web writes for itself.

**16.2 The observation planner (§13's escalations, prospective).** A stub or
explanandum is a hole with a shape: its label says which minimal
environments would carry it, the state says what each still lacks, and the
deficit sorts by warrant — *observe* (empirical: only the world supplies
it), *derive* (formal: an agent can), *secure* (the rest). "Observe X to
resolve Y", computed (`engine/meta.py`). For forks, corroboration runs
FORWARD: an unasserted empirical ground that would corroborate exactly one
rival under the §10 temporal rule DISCRIMINATES — experiment design as a
query over the DAG. The oracles: as of 1845 the planner's one decisive
observation is Galle's; as of 1600 it is the octants — the engine designs
the experiment history ran, before it runs. And when an explanandum has NO
theoretical environment at all, the planner says so: **no plan completes;
only a new abduction can** — absence of a route is the discovery signal,
stated. (Compression as the driver, guarded: a candidate record's worth as
discovery is the interior it would make derivable — compression progress —
but the gain is weighed BY an objective (§13.1), never installed as one, or
the automaton grooms toward triviality.)

**16.3 The puncture report (§14.2, computed) and the cycle run on Mars.**
The §14.2 partition as a function: constituted leaves and formal pointers
KEPT, the derivable interior PUNCTURED, the non-seed log — the escalation
trail — never punctured (§14.4: recipe and audit are one list). The
interior splits **lossless** (a live amp-free environment: deduction alone
replays it) vs **decision-pinned** (every live environment crosses an
ampliative joint: replay needs the trail). §14.2's "the compression ratio
is the warrant profile" lands in that split, measured: Neptune's ampliative
resolution grows only the pinned share — such a web compresses only because
its decisions are kept — while on Mars the octants grow the interior and
the deprecation shrinks the pinned share. Grooming is recompression, as a
number moving the right way (`examples/kepler-mars.ttl`,
`scripts/kepler_demo.py`; the fixture's models are RUN, not narrated —
`engine/orbits.py` executes the formulations, and the equant model misses
the octant longitudes by 8.96′ against Tycho's 2′: the eight minutes,
recomputed).

**16.4 Deprecation, disentangled.** The cycle forces a distinction the
vocabulary already carried but no fixture had exercised — three ways a
record leaves the working web, none of them deletion:

| operation | what it is | trigger | the form |
|---|---|---|---|
| **puncture** | storage decision | derivable given the kept trail | untouched; regenerates |
| **exorcise** | warrant withdrawn | formal fabrication: the description does not close (§15.3) | was never there |
| **deprecate** | jurisdiction suspended | adequacy fell; the description still runs (§15.2, Sommerfeld's pattern) | untouched; retracted as ground |

The vicarious hypothesis is the type case of the third: its geometry passes
exercise in 1609 and today; its empirical adequacy died at the octants; it
is RETRACTED at a moment, its claim and ephemeris cascade away, its standing
stays "failed" (never "exorcised"), and *Astronomia Nova* — the record about
it — survives untouched (§9). Each operation is an escalation in the log;
compression supplies the deprecation detector (in no minimal description,
never exercised, unsupported) and the trail keeps the tombstone.

*Modelled as:* `engine/testgen.py`, `engine/meta.py`, `engine/orbits.py`
(sidecars where sympy/mpmath enter; `meta.py` is engine-proper) +
`examples/kepler-mars.ttl` and three demos (`testgen_demo`, `meta_demo`,
`kepler_demo`). No OWL vocabulary: suites, plans and reports are views over
the statics and the log, recomputable at any moment — which is what lets
them be generated rather than maintained.

---

*Provenance of this document:* reconstructed verbatim from session transcript
`8adf28a9` after a network failure (ConnectionRefused) killed the original
write mid-sentence — the base had been agreed but never hit disk. Recovered and
recreated 2026-06-26.
