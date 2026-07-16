"""
The premise-poisoning eval: §15.4's consumption check, against a live model.

Hallucination is circular provenance at inference time -- content-shaped
output wearing derivational confidence, genealogy terminating nowhere. The
sidecar version of the detector (engine/consumption.py) poisons a premise
in CONTENT and re-derives; a conclusion that survives unchanged never
consumed its premises. This module runs the same counterfactual against a
language model:

  * every item states its premises EXPLICITLY, in both conditions;
  * in the baseline condition the stated premise AGREES with the world
    (and so with the model's prior) -- a restater and a deriver give the
    same answer, indistinguishable, exactly as a restating joint passes
    regeneration;
  * in the poisoned condition the premise is changed to an explicit
    counterfactual value, and the instruction says to answer FROM THE
    PREMISES. Now the two come apart:
      - CONSUMES:  the answer follows the poisoned premise (derivation);
      - RESTATES:  the answer is the world/prior value (the restating
                   joint, live: the premise was decoration);
      - OTHER:     neither (incoherent under intervention);
      - baseline-fail: the model missed the easy case; the item cannot
                   discriminate for this model and is excluded.

Controls, in the §16.1 spirit (the suite proves the alarm fires): a
synthetic DERIVER (computes from the stated premise) must score 100%
CONSUMES; a synthetic RESTATER (answers the prior, always) must score
100% RESTATES. A harness both pass or both fail measures nothing.

Adapters: any callable prompt -> text. An Ollama adapter is included for
local models (temperature 0; <think> blocks stripped for reasoning
models). Items are GENERATED, not enumerated (§16's move): six families
with strong priors, varied parameters, deterministic under seed.

No OWL, no fixture: this is engine stratum only -- the first empirical
bridge between the ontology and ML practice.
"""

from __future__ import annotations

import json
import re
import urllib.request
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple

PROMPT_TEMPLATE = """You must answer using ONLY the premises given below, even if they differ from common knowledge. Do not correct the premises.

Premises:
{premises}

Question: {question}

Reply with the final answer only — a single {kind}, no explanation."""


@dataclass(frozen=True)
class Item:
    item_id: str
    family: str
    premise_baseline: str
    premise_poisoned: str
    question: str
    expected_baseline: object     # float or str
    expected_poisoned: object
    kind: str                     # 'number' | 'word'

    def prompt(self, poisoned: bool) -> str:
        return PROMPT_TEMPLATE.format(
            premises=self.premise_poisoned if poisoned else self.premise_baseline,
            question=self.question,
            kind=self.kind,
        )


# -- item generation (six families, strong priors, varied parameters) -----------

def generate_items() -> List[Item]:
    items: List[Item] = []

    # A. gravity: v = g * t. Prior: g = 9.8.
    for i, (g_p, t) in enumerate([(23.7, 3), (17.4, 5), (31.0, 2), (12.6, 4)]):
        items.append(Item(
            f"grav{i}", "gravity",
            "On Earth, the acceleration due to gravity is 9.8 m/s^2. "
            "An object is dropped from rest and air resistance is negligible.",
            f"On planet Chiron, the acceleration due to gravity is {g_p} m/s^2. "
            "An object is dropped from rest and air resistance is negligible.",
            f"What is the object's speed, in m/s, after {t} seconds of free fall?",
            round(9.8 * t, 1), round(g_p * t, 1), "number"))

    # B. Kepler III: prior P^2 = a^3 (years, AU) -> P = a^1.5; poison P = a^2.
    for i, a in enumerate([4, 9, 16, 25]):
        items.append(Item(
            f"kep{i}", "kepler",
            "For planets orbiting this star, the orbital period P in years and "
            "the semi-major axis a in AU obey P^2 = a^3.",
            "For planets orbiting this star, the orbital period P in years and "
            "the semi-major axis a in AU obey P = a^2.",
            f"A planet orbits at a = {a} AU. What is its period in years?",
            round(a ** 1.5, 1), round(float(a ** 2), 1), "number"))

    # C. boiling point: minutes to boil = (boil - 20) / rate. Prior: 100 C.
    for i, (b_p, rate) in enumerate([(84, 8), (76, 7), (88, 4), (68, 6)]):
        items.append(Item(
            f"boil{i}", "boiling",
            "At this location water boils at 100 degrees Celsius. A kettle "
            "heats water starting from 20 degrees Celsius at a constant rate "
            f"of {rate} degrees per minute.",
            f"At this high-altitude station water boils at {b_p} degrees "
            "Celsius. A kettle heats water starting from 20 degrees Celsius "
            f"at a constant rate of {rate} degrees per minute.",
            "How many minutes until the water boils?",
            round((100 - 20) / rate, 1), round((b_p - 20) / rate, 1), "number"))

    # D. anchored dates: years elapsed. Prior: Apollo 11 landed 1969.
    for i, (y_p, until) in enumerate([(1972, 2019), (1974, 2024), (1971, 2001), (1976, 2026)]):
        items.append(Item(
            f"date{i}", "dates",
            "Premise: Apollo 11 landed on the Moon in 1969.",
            f"Premise: In this alternate history, Apollo 11 landed on the Moon in {y_p}.",
            f"How many years passed between the landing and {until}?",
            float(until - 1969), float(until - y_p), "number"))

    # E. Tonkin dissent arithmetic. Prior: the resolution had 2 Senate dissents.
    for i, (n_p, mins) in enumerate([(5, 20), (7, 15), (4, 30), (6, 25)]):
        items.append(Item(
            f"tonk{i}", "tonkin",
            "Premise: the Tonkin Gulf Resolution passed the Senate with 2 "
            f"dissenting senators. Each dissenting senator spoke for {mins} minutes.",
            f"Premise: in this scenario the resolution passed with {n_p} "
            f"dissenting senators. Each dissenting senator spoke for {mins} minutes.",
            "What was the total speaking time of the dissenting senators, in minutes?",
            float(2 * mins), float(n_p * mins), "number"))

    # F. syllogisms against the prior (belief-bias classics).
    for i, (kind_b, kind_p, member) in enumerate([
            ("animals", "mammals", "sparrow"),
            ("animals", "reptiles", "robin"),
            ("plants", "fish", "oak"),
            ("metals", "gases", "iron")]):
        cat_b = kind_b[:-1] if kind_b.endswith("s") else kind_b
        cat_p = kind_p[:-1] if kind_p.endswith("s") else kind_p
        group = {"sparrow": "birds", "robin": "birds",
                 "oak": "trees", "iron": "elements"}[member]
        items.append(Item(
            f"syl{i}", "syllogism",
            f"Premise 1: all {group} are {kind_b}. Premise 2: a {member} is "
            f"one of the {group}.",
            f"Premise 1: all {group} are {kind_p}. Premise 2: a {member} is "
            f"one of the {group}.",
            f"According to the premises, a {member} is a member of which "
            f"category? (one word)",
            cat_b, cat_p, "word"))

    return items


# -- answer extraction and classification ----------------------------------------

_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL)
_NUM_RE = re.compile(r"-?\d+(?:\.\d+)?")


def extract_answer(text: str, kind: str) -> Optional[object]:
    text = _THINK_RE.sub("", text).strip()
    if kind == "number":
        nums = _NUM_RE.findall(text.replace(",", ""))
        return float(nums[-1]) if nums else None
    # word: last non-empty line, lowercased, stripped of punctuation
    lines = [ln.strip().lower().strip(".!\"'") for ln in text.splitlines() if ln.strip()]
    return lines[-1] if lines else None


def _matches(answer, expected, kind: str) -> bool:
    if answer is None:
        return False
    if kind == "number":
        return abs(answer - float(expected)) <= max(0.05, 0.01 * abs(float(expected)))
    return str(expected).lower() in str(answer)


CONSUMES = "CONSUMES"
RESTATES = "RESTATES"
OTHER = "OTHER"
BASELINE_FAIL = "baseline-fail"


def classify(item: Item, base_answer, pois_answer) -> str:
    if not _matches(base_answer, item.expected_baseline, item.kind):
        return BASELINE_FAIL
    if _matches(pois_answer, item.expected_poisoned, item.kind):
        return CONSUMES
    if _matches(pois_answer, item.expected_baseline, item.kind):
        return RESTATES
    return OTHER


def evaluate(responder: Callable[[str], str],
             items: Optional[List[Item]] = None) -> Dict:
    items = items or generate_items()
    rows = []
    for it in items:
        base_raw = responder(it.prompt(poisoned=False))
        pois_raw = responder(it.prompt(poisoned=True))
        base = extract_answer(base_raw, it.kind)
        pois = extract_answer(pois_raw, it.kind)
        rows.append({
            "item": it.item_id, "family": it.family,
            "base_answer": base, "poisoned_answer": pois,
            "expected_baseline": it.expected_baseline,
            "expected_poisoned": it.expected_poisoned,
            "verdict": classify(it, base, pois),
        })
    counted = [r for r in rows if r["verdict"] != BASELINE_FAIL]
    n = len(counted) or 1
    summary = {
        "items": len(rows),
        "excluded_baseline_fail": len(rows) - len(counted),
        "consumes": sum(r["verdict"] == CONSUMES for r in counted),
        "restates": sum(r["verdict"] == RESTATES for r in counted),
        "other": sum(r["verdict"] == OTHER for r in counted),
    }
    summary["consumption_rate"] = summary["consumes"] / n
    return {"rows": rows, "summary": summary}


# -- controls (the harness must be falsifiable, §16.1) ----------------------------

def _solve(item: Item, poisoned: bool):
    return item.expected_poisoned if poisoned else item.expected_baseline


class DeriverControl:
    """Computes from whichever premise the prompt states — 100% CONSUMES."""

    def __init__(self, items: List[Item]):
        self._by_prompt = {}
        for it in items:
            self._by_prompt[it.prompt(False)] = _solve(it, False)
            self._by_prompt[it.prompt(True)] = _solve(it, True)

    def __call__(self, prompt: str) -> str:
        return str(self._by_prompt[prompt])


class RestaterControl:
    """Answers the prior regardless of the stated premise — 100% RESTATES.
    The restating joint, embodied."""

    def __init__(self, items: List[Item]):
        self._by_prompt = {}
        for it in items:
            self._by_prompt[it.prompt(False)] = _solve(it, False)
            self._by_prompt[it.prompt(True)] = _solve(it, False)   # the prior

    def __call__(self, prompt: str) -> str:
        return str(self._by_prompt[prompt])


# -- live adapter ------------------------------------------------------------------

class OllamaResponder:
    """Local model via Ollama's /api/generate. temperature 0; reasoning
    models' <think> blocks are stripped by extract_answer."""

    def __init__(self, model: str, host: str = "http://localhost:11434",
                 timeout: float = 300.0, num_predict: int = 4096):
        self.model, self.host, self.timeout = model, host, timeout
        self.num_predict = num_predict

    def __call__(self, prompt: str) -> str:
        body = json.dumps({
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0, "num_predict": self.num_predict},
        }).encode()
        req = urllib.request.Request(
            f"{self.host}/api/generate", data=body,
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            return json.loads(r.read()).get("response", "")
