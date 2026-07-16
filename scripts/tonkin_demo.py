#!/usr/bin/env python3
"""The Gulf of Tonkin, computed: consent by omission (engine/escalation.py).

Five acts over examples/tonkin-consent.ttl, everything as-of-moment (no
hindsight: the 2005 study appears only in act 5, as the oracle):

  1. the omission, measured -- the impugning records extant at each
     decision that its premise-set excluded;
  2. corroboration contrast -- Aug 2's engagement vs Aug 4's, as numbers;
  3. velocity -- the irrevocability ladder with timestamps: the review
     rung was REACHED (Herrick filed it) and then climbed over;
  4. the counterfactual -- the consent inference with its omitted
     premises restored: what Congress would have had to weigh openly;
  5. the oracle -- the record outlasting the fabrication by 41 years,
     confirming what the as-of-moment web already impugned.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine import escalation as esc


def main() -> int:
    web = esc.load_tonkin()
    ok = {}

    print("=" * 74)
    print("1. THE OMISSION, MEASURED  (records extant, impugning, and absent)")
    print("=" * 74)
    for inf, moment, label in [
        ("Inf_RetaliationDecision", esc.DECISION_MOMENT, "strike order, ~Aug 4 23:36 DC"),
        ("Inf_CongressConsents", esc.CONSENT_MOMENT, "resolution vote, Aug 7"),
    ]:
        omitted = web.omitted_impugners(inf, moment)
        print(f"\n  {inf}  ({label})")
        print(f"    premises: {web.premises_of(inf)}")
        for premise, imps in omitted.items():
            for i in imps:
                print(f"    OMITTED: {i}  (extant day {web.extant_at[i]:.2f}, "
                      f"impugns {premise})")
    dec_omitted = web.omitted_impugners("Inf_RetaliationDecision", esc.DECISION_MOMENT)
    con_omitted = web.omitted_impugners("Inf_CongressConsents", esc.CONSENT_MOMENT)
    ok["omission_visible"] = (
        "HerrickDoubtCable" in sum(dec_omitted.values(), [])
        and "HerrickDoubtCable" in sum(con_omitted.values(), [])
    )

    print()
    print("=" * 74)
    print("2. CORROBORATION CONTRAST  (impugners extant, as of the vote)")
    print("=" * 74)
    contrast = web.corroboration_contrast(
        ["Aug2Engagement", "Aug4AttackReport"], esc.CONSENT_MOMENT)
    for r, n in contrast.items():
        print(f"  {r:20s} impugners: {n}")
    print("  The well-held and the weakly-held record, side by side — the")
    print("  resolution's case load-bore on the weaker one.")
    ok["contrast"] = (contrast["Aug2Engagement"] == 0
                      and contrast["Aug4AttackReport"] >= 2)

    print()
    print("=" * 74)
    print("3. VELOCITY  (the irrevocability ladder, §13.1, with timestamps)")
    print("=" * 74)
    lad = esc.TONKIN_LADDER
    for rung, name, t in lad.rungs():
        print(f"  {rung:8s} day {t:5.2f}  {name}")
    review = lad.review_time_granted_days()
    print(f"\n  notice → irrevocable act: {lad.notice_to_act_days():.2f} days")
    print(f"  notice → consent:         {lad.notice_to_consent_days():.2f} days")
    print(f"  review time granted:      {review * 24:.1f} hours — against a cable")
    print(f"  that said 'suggest complete evaluation before any further action'")
    print(f"  (contrast: Cuban Missile Crisis, notice → resolution "
          f"{esc.CUBAN_MISSILE_NOTICE_TO_RESOLUTION_DAYS:.0f} days,")
    print(f"   and the maximal rung never taken)")
    ok["ladder_outrun"] = review < 0.5 and lad.notice_to_consent_days() < 4.0

    print()
    print("=" * 74)
    print("4. THE COUNTERFACTUAL  (the premise-set, restored)")
    print("=" * 74)
    cf = esc.counterfactual_restoration(web, "Inf_CongressConsents",
                                        esc.CONSENT_MOMENT)
    print(f"  as presented: {cf['original_premises']}")
    print(f"  as restored:  {cf['restored_premises']}")
    for premise, imps in cf["conflicts_made_visible"].items():
        print(f"  now visible:  {premise}  vs  {imps}")
    print("  The curated set contained zero impugners of its key premise;")
    print("  the extant web contained them. Consent's warrant is bounded by")
    print("  its premise-set — which is why the premise-set was the target.")
    ok["counterfactual"] = bool(cf["conflicts_made_visible"])

    print()
    print("=" * 74)
    print("5. THE ORACLE  (2005: the record outlasts the fabrication)")
    print("=" * 74)
    years = (web.extant_at["HanyokStudy"] - esc.CONSENT_MOMENT) / 365.25
    print(f"  HanyokStudy enters the web {years:.1f} years after the vote,")
    print(f"  impugning: {sorted(t for t in esc.TONKIN_IMPUGNS['HanyokStudy'])}")
    print(f"  It CONFIRMS what act 1 computed from records extant in 1964 —")
    print(f"  the oracle in the Beltrami sense, not the conviction. Both")
    print(f"  halves of the lesson: the record wins, and forty-one years is")
    print(f"  what waiting for the oracle costs. The as-of-moment discipline")
    print(f"  is the cheap version; teach the wide part to run act 1.")
    ok["oracle_late"] = years > 40

    print()
    print("=" * 74)
    for k, v in ok.items():
        print(f"  [{'OK ' if v else 'FAIL'}] {k}")
    print("=" * 74)
    return 0 if all(ok.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
