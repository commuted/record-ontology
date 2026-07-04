# Brainstorm: Capability Depth for record-ontology

*2026-07-03 · Product-trio ideation (PM / Designer / Engineer) · objective: turn the
ROOT.md §10 horizon — science-as-DAG, non-monotonic fidelity propagation,
forks/stubs — into concrete, buildable capability.*

*Refreshed later the same day, after the Neptune exemplar landed (`edd9021`) and
ROOT.md gained §13 (escalations / formation / the moment) and §14 (the
knowledge-automaton): statuses and framings updated in place; the revision log
was promoted out of the deferred pile.*

## Framing

- **Product:** record-ontology v0.5.0 — one class `Record`, warrant triad,
  inference as defined class, carrier dissolved, validated OWL 2 DL stub.
- **Objective:** capability depth. The static base is settled; the differentiating
  capability (the "genuinely new mechanism," §10) is unbuilt.
- **Segment:** agents building knowledge from evidence — initially Ron + future
  adopters in scholarship, intelligence analysis, and AI-agent epistemics.
- **Desired outcomes:** a working propagation/fork layer over the static ontology;
  a demonstration that "discoveries pop out" when a fork dominates or a stub
  resolves; the DAG capability observable, not just described.
- **Standing architectural rule (constrains everything below):** OWL DL is
  monotonic — all dynamics live in a **computational layer over** the ontology,
  never as axioms in it.

---

## Ideas by perspective

### Product Manager (business value, strategy, customer impact)

| # | Idea | One-liner |
|---|------|-----------|
| PM-1 | **Flagship discovery exemplar** | Reconstruct one real scientific discovery (e.g. Neptune's prediction from Uranus's orbital residuals, or the ozone hole) as a full derivation DAG — empirical leaves, ampliative joints, one standing conclusion. |
| PM-2 | **Evidence-audit report** | Given any record, emit a human-readable audit: its sub-DAG, warrant mix, weakest links, open stubs — the "pull the evidence" traversal productized. |
| PM-3 | **record-harm integration: fabrication as concealed escalation** | First applied use of the propagation engine — fabrication *is* a concealed escalation (a trade-off made but never surfaced, §13.1), *exposed* by DAG incoherence; evaluation runs on the as-of-moment sub-DAG + was-the-trade-off-recorded. Start from §13, not this row. |
| PM-4 | **Revision-event contract spec** | A small published format (append-only log of leaf assertions/retractions) defining the interface between the static ontology and *any* dynamics engine — lets third parties build engines. |
| PM-5 | **AI-agent epistemic hygiene** | Position records-with-warrant-provenance as the citation/justification structure for LLM-agent outputs — a claim an agent makes is a conclusion whose premises must trace to leaves. |

### Product Designer (experience, usability, delight)

| # | Idea | One-liner |
|---|------|-----------|
| D-1 | **Interactive DAG explorer** | Click a conclusion, watch evidence flow up from the leaves; warrant rendered as color (formal / empirical / self-verifying), force as edge style. |
| D-2 | **"What if this observation fell?" scrubber** | Toggle a leaf off and watch re-leveling propagate live — the non-monotonic dynamics made *tangible*, the demo that explains the whole project in ten seconds. |
| D-3 | **Fork comparison view** | Competing abductive explanations as parallel sub-DAGs with fidelity distributed across them; watch one collapse as observations arrive. |
| D-4 | **Stub inbox** | Open stubs surfaced as a first-class worklist — each hole phrased as "what observation would resolve this?"; refinement becomes a to-do list. |
| D-5 | **Authoring notation** | A compact text notation (YAML-ish) that compiles to Turtle, so building a DAG doesn't require hand-writing RDF — lowers the cost of every other idea. |

### Software Engineer (technical leverage, data, scale)

| # | Idea | One-liner |
|---|------|-----------|
| E-1 | **ATMS-style propagation engine prototype** | Python over rdflib: justification graph, retraction, environments-as-forks, label propagation (de Kleer) — *the* new mechanism, kept strictly outside the ontology. |
| E-2 | **Fidelity calculus** | Define the combinatorial function: warrant + force per edge → a computed fidelity (interval or distribution) per node over the whole feeding sub-DAG; map to Bayesian belief propagation; property-based tests. |
| E-3 | **`OpenQuestion`/`Stub` as defined classes** | The static half of stubs, in OWL now: a conclusion with an unresolved premise, reasoner-recognized (like `Inference`), never a primitive kind; extend `validate.py`. |
| E-4 | **SPARQL traversal library** | Canned queries on existing structure: evidence-pull to empirical leaves, warrant-mix summary, incoherence candidates — data leverage with zero new mechanism. |
| E-5 | **Replayable revision log** | Append-only event stream of assert/retract on leaves; replay = time-travel through a discovery's history. *Promoted (see top-5 addendum):* §13.3 makes the log the **carrier of moments** (log position = moment; as-of-moment views), and §14 makes replay the automaton's **regeneration** mechanism — no longer a test-harness byproduct. |

---

## Top 5 (prioritized)

Criteria: alignment with the capability-depth objective · impact on the horizon ·
feasibility/effort · differentiation.

### 1. Flagship discovery exemplar (PM-1) — ✅ DONE
**Built as `examples/neptune-discovery.ttl`, committed `edd9021`, validator
green.** Both assumptions validated: the existing vocabulary sufficed with no
new primitives, and the DAG landed eyeball-sized (~22 records, 6 inferences,
6 agents). Bonuses beyond the sketch: fork B is self-undermining (contests
`LawOfGravitation`, a premise of its own evidence — a combinatorial-fidelity
test case), Bode's law rides along as the false-but-used assumption, and the
letter to Galle is the cross-agent ordering edge §13.3 now cares about. The
Airy/Challis inaction story makes it the §13 escalation test case too.

### 2. ATMS-style propagation engine prototype (E-1)
**What:** A separate Python package (`engine/`, MIT like the other scripts) that
loads the ontology + an example DAG via rdflib and implements: justification
tracking, leaf retraction, dependent re-leveling, environments-as-forks.
**Why:** this *is* the capability-depth objective — §10 calls it "the genuinely
new mechanism." Kin literature is already identified (de Kleer's ATMS); the
architectural rule (layer over, not axioms in) is settled, so no design blockage.
**Assumptions to validate:** the two-strata split is workable in practice (the
engine can treat the OWL file as read-only structure); ATMS environments map
cleanly onto §10 forks; performance is a non-issue at exemplar scale.

### 3. `OpenQuestion`/`Stub` defined classes (E-3)
**What:** OWL-side stubs: `Stub ≡ Record ⊓ ∃hasPremise.(unresolved)` — exact
modelling to be worked out (likely a marker on the *premise slot*, since OWL has
no negation-as-failure); plus `validate.py` entailment tests and a
`minimal-stub.ttl`.
**Why:** the one horizon piece that lives in the *static* stratum, so it's cheap,
keeps the defined-not-primitive discipline, and gives the engine a vocabulary for
holes it opens. Natural v0.6.0 ontology increment.
**Assumptions to validate:** "unresolved premise" is expressible in OWL 2 DL
without closed-world tricks — if not, the honest answer may be that stub-ness is
*engine-computed*, not reasoner-derived, which is itself a finding worth recording
in ROOT.md.
**§13 update:** stubs acquired an ethical role — a stub is the *explicit form of
a skip* (§13.1, "the ethical hinge"), so the modelling should carry the skip's
**reason** ("deferred, for objective Y, at this moment"), not just the hole.

### 4. Fidelity calculus (E-2)
**What:** A written spec + implementation in the engine: how warrant and force
per edge combine over a sub-DAG into computed fidelity; forks split it,
truth-preserving edges pass it through, ampliative edges attenuate it,
self-verifying leaves are certain-but-barren (fidelity 1, amplification 0 — §2
already dictates this boundary condition).
**Why:** it operationalizes "fidelity is entailed by the whole sub-DAG" and is
the thing that makes fork-collapse *quantitative* — without it, "one fork's
fidelity dominates" has no meaning. §2's entailments act as fixed test cases.
**Assumptions to validate:** a simple algebra (intervals or discrete grades)
suffices before reaching for full Bayesian networks; fidelity composition is
actually associative/order-independent over the DAG (property-test this).
**§13/§14 update:** the calculus gained a second consumer — §14's puncturing map
makes it double as a **rate–distortion theory** (what may be dropped and
regenerated is entailed by warrant), and §13.3 implies fidelity must be
computable **as-of-moment**, which couples its design to the revision log below.

### 5. "What-if" DAG explorer (D-1 + D-2 merged)
**What:** A single self-contained HTML visualization of the exemplar DAG —
warrant as color, force as edge style, click a leaf to retract it and watch the
engine's re-leveling propagate; a fork panel showing fidelity shift.
**Why:** the dynamics are the product, and dynamics you can't *see* are hard to
validate, debug, or show anyone. This is also the cheapest credibility artifact
for future adopters — the ten-second explanation of the whole project.
**Assumptions to validate:** the engine can expose propagation as a step-by-step
trace (design the engine's output with this consumer in mind); one exemplar DAG
fits legibly on one screen.

### Addendum (post §13–§14): the revision log joins the top tier

**+ Replayable revision log (E-5, promoted).** Originally deferred as a
test-harness byproduct — that rationale is dead. §13.3 makes the append-only
log the **carrier of moments** (log position = moment; as-of-moment views are
what retrospective evaluation and clock-free anachronism detection run on), and
§14 makes replay the knowledge-automaton's **regeneration** mechanism. Design it
as a first-class contract *with* the engine (idea 2), not inside it — it is the
interface between the static ontology and every dynamics consumer.
**Assumptions to validate:** an append-only assert/retract event format covers
everything §13.3 needs (communication edges between agents included); log
position alone suffices as the moment (no hybrid clock needed at exemplar
scale).

### Sequencing note

1 (✅ done) → 2 form the first milestone (fixture + mechanism, exactly the
resumption plan already on record) — with the revision log designed alongside 2
as its interface, not after it. 3 can proceed in parallel (static stratum,
independent). 4 lands inside the engine once retraction works, now with
as-of-moment indexing in scope. 5 last — it consumes the engine's trace output.

**Deliberately deferred:** fabrication-as-concealed-escalation (PM-3) — high
strategic value but depends on a working engine *and* record-harm stabilizing
on this ontology's `Record`; start any pickup from ROOT.md §13.1, which
superseded the original "false posit exposed by incoherence" framing. The
authoring notation (D-5) becomes worth it only if DAGs beyond the exemplar get
built by hand.
