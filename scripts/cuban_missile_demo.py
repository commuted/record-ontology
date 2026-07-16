#!/usr/bin/env python3
"""The Cuban Missile Crisis, computed: the slow ladder (engine/escalation.py).

The Tonkin contrast, act for act — the same machinery, every meaning
inverted by the agents' discipline:

  1. the two ladders side by side — review inhabited vs review outrun,
     consent before the act vs after it;
  2. the maximal rung never taken — the missing edge as RESTRAINT, with
     the internal dissent recorded and consumed rather than omitted;
  3. record selection, classified — the Trollope ploy is fork-selection
     (the skipped letter impugns nothing); Tonkin's was
     defeater-concealment: the engine tells them apart from structure;
  4. evidence displayed, not asserted — premise publicity at consent,
     both fixtures;
  5. rung refusals at two grains — a president and a flotilla commander;
  6. the institutionalized edge — the hotline as standing machinery for
     making two agents' moments comparable.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine import escalation as esc


def main() -> int:
    cuba = esc.load_cuba()
    tonkin = esc.load_tonkin()
    ok = {}

    print("=" * 74)
    print("1. TWO LADDERS  (§13.1, timestamps; Tonkin right, Cuba left)")
    print("=" * 74)
    cl, tl = esc.CUBA_LADDER, esc.TONKIN_LADDER
    rows = [
        ("notice -> rank (review granted)",
         f"{cl.review_time_granted_days():.1f} days",
         f"{tl.review_time_granted_days() * 24:.0f} hours"),
        ("notice -> irrevocable act",
         f"{cl.notice_to_act_days():.1f} days",
         f"{tl.notice_to_act_days():.2f} days"),
        ("consent relative to act",
         f"{cl.consent[1] - cl.act[1]:+.1f} days (BEFORE)",
         f"{tl.consent[1] - tl.act[1]:+.1f} days (after)"),
        ("notice -> resolution/consent",
         f"{esc.CUBA_RESOLUTION_MOMENT - cl.notice[1]:.1f} days",
         f"{tl.notice_to_consent_days():.2f} days"),
    ]
    print(f"  {'':38s} {'CUBA':>22s} {'TONKIN':>14s}")
    for label, c, t in rows:
        print(f"  {label:38s} {c:>22s} {t:>14s}")
    ok["review_inhabited"] = (cl.review_time_granted_days() >= 3.0
                              and tl.review_time_granted_days() < 0.5)
    ok["consent_precedes_act"] = cl.consent[1] < cl.act[1]

    print()
    print("=" * 74)
    print("2. THE MAXIMAL RUNG, NEVER TAKEN  (the missing edge as restraint)")
    print("=" * 74)
    restraint = esc.restraint_edges(cuba, ["AirstrikeOption"])
    for opt, r in restraint.items():
        print(f"  {opt}: act edge exists = {r['act_edge_exists']}; "
              f"impugned from within by {r['impugned_by']}")
    print("  The dissent was CONSUMED by the decision (it sits in")
    print("  Inf_QuarantineDecision's premises) — the impugner of the")
    print("  rejected option entered the premise-set. Tonkin's decision")
    print("  excluded its impugner; this one ate it.")
    dec_premises = cuba.premises_of("Inf_QuarantineDecision")
    ok["restraint_visible"] = (not restraint["AirstrikeOption"]["act_edge_exists"]
                               and "PearlHarborDissent" in dec_premises)

    print()
    print("=" * 74)
    print("3. RECORD SELECTION, CLASSIFIED  (Trollope vs Tonkin, from structure)")
    print("=" * 74)
    trollope = esc.record_selection_report(
        cuba, "Inf_TrollopeReply", ["KhrushchevLetter2"], moment=27.7)
    tonkin_sel = esc.record_selection_report(
        tonkin, "Inf_CongressConsents",
        ["HerrickDoubtCable", "Oplan34ARaids"], moment=esc.CONSENT_MOMENT)
    print(f"  Cuba, Inf_TrollopeReply skips KhrushchevLetter2:")
    for s, v in trollope["skipped"].items():
        print(f"    {s}: {v}")
    print(f"  Tonkin, Inf_CongressConsents skipped:")
    for s, v in tonkin_sel["skipped"].items():
        print(f"    {s}: {v}")
    print("  Same operation — a record skipped — told apart by impugnment")
    print("  structure alone. And the second axis: the Trollope selection was")
    print("  visible to the skipped record's AUTHOR, who retained override;")
    print("  Tonkin's was concealed from the parties it bound.")
    ok["selection_classified"] = (
        "fork-selection" in trollope["skipped"]["KhrushchevLetter2"]
        and "DEFEATER" in tonkin_sel["skipped"]["HerrickDoubtCable"]
    )

    print()
    print("=" * 74)
    print("4. EVIDENCE DISPLAYED, NOT ASSERTED  (premise publicity at consent)")
    print("=" * 74)
    c_frac, c_pub = esc.premise_publicity(cuba, "Inf_OASConsents", esc.CUBA_PUBLIC)
    t_frac, t_pub = esc.premise_publicity(tonkin, "Inf_CongressConsents",
                                          esc.TONKIN_PUBLIC)
    print(f"  Cuba   Inf_OASConsents:     {c_frac:.0%} of premises inspectable {c_pub}")
    print(f"  Tonkin Inf_CongressConsents: {t_frac:.0%} inspectable {t_pub}")
    print("  — and Tonkin's one 'public' premise was an assertion whose")
    print("  underlying records were classified. The photographs were shown;")
    print("  the cables were summarized. Consent's quality tracks the")
    print("  difference.")
    ok["publicity_contrast"] = c_frac > t_frac

    print()
    print("=" * 74)
    print("5. RUNG REFUSALS  (the ladder at every grain)")
    print("=" * 74)
    for t, agent, what in esc.CUBA_REFUSALS:
        print(f"  day {t:.1f}  {agent}: {what}")
    print("  A president declining his own pre-commitment; one officer on a")
    print("  submarine declining an authorization. 'You can only fix your own")
    print("  records' — and on Black Saturday, twice, that was enough.")
    ok["refusals_recorded"] = len(esc.CUBA_REFUSALS) == 2

    print()
    print("=" * 74)
    print("6. THE INSTITUTIONALIZED EDGE")
    print("=" * 74)
    print(f"  HotlineAgreement, day {cuba.extant_at['HotlineAgreement']:.0f}:")
    print("  §13.3 — two agents' moments are incomparable until a")
    print("  communication record creates an edge. The crisis's last lesson")
    print("  was to build the edge machinery BEFORE the next one: the hotline")
    print("  is de-escalation infrastructure, standing.")
    ok["aftermath"] = cuba.extant_at["HotlineAgreement"] > 200

    print()
    print("=" * 74)
    for k, v in ok.items():
        print(f"  [{'OK ' if v else 'FAIL'}] {k}")
    print("=" * 74)
    return 0 if all(ok.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
