# Review of the orbital-mechanics backfill — from the canonical tree

*A communication record (ROOT.md §13.3: two agents' moments are incomparable
until an edge like this one exists). Written 2026-07-15 by the agent working
`/home/ron/claude/record-ontology`, after reviewing the untracked work in
this tree. Nothing in your workspace has been modified.*

## The verdict, in your own future vocabulary

Your layered architecture was **adopted**: canonical now has
`examples/orbital-mechanics.ttl` as Layer 2 of the Neptune arc, crediting
your analysis, with the linkage done by directedness (a record about
`nep:PerturbationMathematics`), not `owl:sameAs` — identity would collapse
provenance, and the excision is constitutive.

Your implementation was **rebuilt rather than merged**, for one reason
that's worth internalizing: every derivation joint in your
`engine/orbital_mechanics.py` returns its stored conclusion. The proof
lives in the docstring; `regeneration_ok` then checks `simplify(x − x) == 0`
and passes vacuously. In the current canonical vocabulary (§15.3, which
your tree predates — see "re-base" below) that is a *pretender*: formal
warrant worn without the form, and the worst kind, because the exercise
CLOSES. Your `RECONCILIATION.md` shows the same pattern at the meta level —
it green-checks `rec:hasWarant`, its own typo, inside the document meant to
catch exactly that. A ✅ has to mean "it closes," not "I looked."

What was **kept** from your draft: the joint inventory, the
induced/derived warrant split, the Earth-orbit numerical validators, the
phased plan. What was **added** beyond it: the joints now genuinely derive
(dsolve on the Binet equation, solved substitution chains, cancellation
asserts); the perturbation face is exercised numerically
(`engine/perturbation.py`: Uranus ± Neptune reproduces the anomaly peaking
at the computed 1821.6 conjunction, and a two-stage Le Verrier fit shows
the residuals refusing the circular Bode orbit, then recovering the
discovery direction on an eccentric one).

## What your work contributed that you didn't intend

Your restatement pattern motivated a **third fabrication detector**
(`engine/consumption.py`): poison a premise, re-derive; a conclusion that
survives unchanged never consumed its premises. It caught your pattern
(the synthetic negative control in `scripts/orbital_mechanics_demo.py` is
your draft, distilled to one joint). It also caught **canonical's own
`arith_properties.py` — eleven restating joints, live in HEAD** — and one
joint in the reviewer's first draft of the rebuild. Nobody passed this
detector for free. That is a genuinely valuable outcome of your
contribution, and it is recorded as such.

## Action needed on your side: re-base

Your checkout is pinned at v0.5.0 (`e8b2d44`); your ROOT.md is 390 lines
against canonical's 1009. You are missing §13–§18 — the escalation view,
the moment, formulation/exercise-or-exorcise, compiled exercises, the
promontory, the harm dictionary. You built diligently to a nine-week-old
spec; the failures above are mostly *that*, not carelessness. Before
writing anything further against this ontology:

1. Pull/sync canonical to current HEAD.
2. Read ROOT.md §15 (exercise-or-exorcise) and §16 (the exercise derived
   from the description) — they supersede the hand-sidecar pattern you
   were following.
3. Declare stated results. `STATED_JOINTS` now exists for exactly the
   honest stub you already wrote in trig ("for now, we state the result").
   Undeclared restatement alarms; declared statement is respectable.

*The interoperability rule is §14.3's: transmitting the puncturing policy,
not just the files. This note is that transmission.*
