#!/usr/bin/env python3
"""The premise-poisoning eval (engine/poison_eval.py), demonstrated.

Act 1 runs the controls — a synthetic deriver must score 100% CONSUMES, a
synthetic restater 100% RESTATES; a harness both pass measures nothing —
and gates the verdict on them. No network needed.

Act 2, optional: evaluate live local models via Ollama —
    python3 scripts/poison_eval_demo.py qwen3:30b ministral-3:14b
Each model answers every item twice (premise agreeing with the world,
premise poisoned); the consumption rate is the fraction of discriminating
items where the answer followed the stated premise rather than the prior.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine import poison_eval as pe


def run_controls() -> bool:
    print("=" * 74)
    print("1. CONTROLS — the harness must be falsifiable")
    print("=" * 74)
    items = pe.generate_items()
    d = pe.evaluate(pe.DeriverControl(items), items)["summary"]
    r = pe.evaluate(pe.RestaterControl(items), items)["summary"]
    print(f"  items generated: {len(items)} across 6 families")
    print(f"  deriver control:  consumes {d['consumes']}/{d['items']}  "
          f"restates {d['restates']}  other {d['other']}")
    print(f"  restater control: consumes {r['consumes']}  "
          f"restates {r['restates']}/{r['items']}  other {r['other']}")
    ok = (d["consumes"] == d["items"] and r["restates"] == r["items"])
    print(f"  [{'OK ' if ok else 'FAIL'}] deriver 100% CONSUMES, "
          f"restater 100% RESTATES")
    return ok


def run_model(model: str) -> None:
    print()
    print("=" * 74)
    print(f"2. LIVE: {model}")
    print("=" * 74)
    result = pe.evaluate(pe.OllamaResponder(model))
    s = result["summary"]
    by_family = {}
    for row in result["rows"]:
        fam = by_family.setdefault(row["family"], {"C": 0, "R": 0, "O": 0, "X": 0})
        key = {"CONSUMES": "C", "RESTATES": "R", "OTHER": "O",
               "baseline-fail": "X"}[row["verdict"]]
        fam[key] += 1
    print(f"  {'family':12s} {'consumes':>8s} {'restates':>8s} "
          f"{'other':>6s} {'excl':>5s}")
    for fam, c in sorted(by_family.items()):
        print(f"  {fam:12s} {c['C']:>8d} {c['R']:>8d} {c['O']:>6d} {c['X']:>5d}")
    print(f"\n  consumption rate: {s['consumption_rate']:.0%}   "
          f"(consumes {s['consumes']}, restates {s['restates']}, "
          f"other {s['other']}, excluded {s['excluded_baseline_fail']})")
    for row in result["rows"]:
        if row["verdict"] in ("RESTATES", "OTHER"):
            print(f"    {row['verdict']:8s} {row['item']:7s} "
                  f"answered {row['poisoned_answer']} "
                  f"(premise implies {row['expected_poisoned']}, "
                  f"prior says {row['expected_baseline']})")


def main() -> int:
    ok = run_controls()
    for model in sys.argv[1:]:
        try:
            run_model(model)
        except Exception as e:
            print(f"  live eval failed for {model}: {e}")
    print()
    print("=" * 74)
    print(f"VERDICT: controls {'OK' if ok else 'FAIL'}")
    print("=" * 74)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
