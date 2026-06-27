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

**Open (left uncommitted on purpose):**
- **Carrier** — is it a distinct relatum (`Record = form borne by a Carrier`) or
  does it dissolve into the record's *locus/provenance* in the Continuum? Not
  decided.
- **Composition transitivity** — `partOf`/`composedOf` left non-transitive for
  now; mereological transitivity is a deliberate later decision. (Cf.
  record-harm, which had to *drop* `buildsUpon` transitivity to stay OWL 2 DL.)
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

---

*Provenance of this document:* reconstructed verbatim from session transcript
`8adf28a9` after a network failure (ConnectionRefused) killed the original
write mid-sentence — the base had been agreed but never hit disk. Recovered and
recreated 2026-06-26.
