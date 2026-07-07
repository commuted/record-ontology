"""
Orbital mechanics as exercise (§15.1/§15.3): Kepler's laws, RUN.

The kepler-mars fixture's formulations are runnable model descriptions:

    model ellipse a=1.5237 e=0.0934 tol_arcmin=2
    model equant  a=1.5237 e=0.0934 tol_arcmin=2
    obs 0:0.0000 90:100.6414 ...       (mean-anomaly-deg : longitude-deg)

This sidecar parses them off the graph -- no hand registry keyed to record
names; the exercise is derived from the description, like the arith
compiler -- and predicts heliocentric longitudes:

  ellipse -- Kepler's first two laws: solve E - e*sin(E) = M (the area law
             in angle form), then the true anomaly from the eccentric.
  equant  -- the vicarious hypothesis: a circle of radius a centered ae
             from the Sun, uniform angular motion about an equant at 2ae
             (bisected eccentricity). The best of the old astronomy;
             agrees with the ellipse to O(e^2) -- which is exactly 8.96
             arcminutes at the octants for Mars, Kepler's eight minutes.

`exercise_model` compares a model record's predictions against every
observation record currently ASSERTED (adequacy is judged against the
evidence one actually has -- more evidence, stricter exercise), to the
tolerance the formulation itself declares. The geometry alone is
`predicted_longitude`; a model whose adequacy falls is retracted as a
JURISDICTION (§15.2) -- its geometry still runs.

Sidecar: sympy/mpmath stay demo-only; the engine package never imports this.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Optional, Sequence

import mpmath as mp

from .core import Engine, REC, short
from .exercise import ExerciseResult

mp.mp.dps = 30


# ---------------------------------------------------------------------------
# Formulation parsing
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class OrbitModel:
    kind: str            # "ellipse" | "equant"
    a: mp.mpf            # semi-major axis (AU) -- scale-free for longitudes
    e: mp.mpf            # eccentricity
    tol_arcmin: float    # the adequacy the formulation itself claims


def parse_model(formulation: str) -> Optional[OrbitModel]:
    parts = formulation.split()
    if len(parts) < 2 or parts[0] != "model":
        return None
    kv = dict(p.split("=", 1) for p in parts[2:] if "=" in p)
    try:
        return OrbitModel(kind=parts[1], a=mp.mpf(kv["a"]), e=mp.mpf(kv["e"]),
                          tol_arcmin=float(kv["tol_arcmin"]))
    except (KeyError, ValueError):
        return None


def parse_observations(formulation: str) -> Optional[tuple]:
    parts = formulation.split()
    if not parts or parts[0] != "obs":
        return None
    out = []
    for p in parts[1:]:
        m_deg, lon_deg = p.split(":")
        out.append((mp.mpf(m_deg), mp.mpf(lon_deg)))
    return tuple(out)


# ---------------------------------------------------------------------------
# The two geometries
# ---------------------------------------------------------------------------

def _ellipse_longitude(model: OrbitModel, mean_anomaly_deg) -> mp.mpf:
    M = mp.radians(mp.mpf(mean_anomaly_deg))
    e = model.e
    E = mp.findroot(lambda E: E - e * mp.sin(E) - M, M)
    nu = 2 * mp.atan(mp.sqrt((1 + e) / (1 - e)) * mp.tan(E / 2))
    return mp.degrees(mp.atan2(mp.sin(nu), mp.cos(nu))) % 360


def _equant_longitude(model: OrbitModel, mean_anomaly_deg) -> mp.mpf:
    M = mp.radians(mp.mpf(mean_anomaly_deg))
    a, e = model.a, model.e
    # Sun at origin; circle radius a centered (-ae, 0); equant at (-2ae, 0);
    # the planet sits where the uniformly-turning equant ray meets the circle.
    rho = a * e * mp.cos(M) + mp.sqrt(a**2 - (a * e * mp.sin(M))**2)
    px = -2 * a * e + rho * mp.cos(M)
    py = rho * mp.sin(M)
    return mp.degrees(mp.atan2(py, px)) % 360


def predicted_longitude(model: OrbitModel, mean_anomaly_deg) -> mp.mpf:
    fn = {"ellipse": _ellipse_longitude, "equant": _equant_longitude}[model.kind]
    return fn(model, mean_anomaly_deg)


# ---------------------------------------------------------------------------
# Exercise -- the model run against the asserted evidence
# ---------------------------------------------------------------------------

def _formulation_of(engine: Engine, record) -> Optional[str]:
    lit = next(engine.web.graph.objects(record, REC.formulation), None)
    return str(lit) if lit is not None else None


def asserted_observations(engine: Engine, state=None) -> Mapping:
    """Every ASSERTED record whose formulation parses as an observation
    table: record -> ((M_deg, lon_deg), ...)."""
    state = state if state is not None else engine.state()
    out = {}
    for r in sorted(engine.web.grounds, key=str):
        if not state.supported.get(r, False):
            continue
        f = _formulation_of(engine, r)
        if f is None:
            continue
        obs = parse_observations(f)
        if obs:
            out[r] = obs
    return out


def exercise_model(engine: Engine, name, state=None) -> Optional[ExerciseResult]:
    """Run one model record's description against the asserted evidence.
    None if the record's formulation is not a model description."""
    record = engine.resolve(name)
    f = _formulation_of(engine, record)
    if f is None:
        return None
    model = parse_model(f)
    if model is None:
        return None
    worst, worst_at, n = mp.mpf(0), None, 0
    for obs_record, table in asserted_observations(engine, state).items():
        for m_deg, lon_deg in table:
            resid = abs((predicted_longitude(model, m_deg) - lon_deg + 180)
                        % 360 - 180) * 60  # arcminutes
            n += 1
            if resid > worst:
                worst, worst_at = resid, (short(obs_record), float(m_deg))
    if n == 0:
        return ExerciseResult(False, "no observations stand asserted -- "
                                     "adequacy is untestable")
    ok = worst <= model.tol_arcmin
    where = f" (worst at M={worst_at[1]:g} deg in {worst_at[0]})" if worst_at else ""
    return ExerciseResult(
        bool(ok),
        f"{model.kind}: max residual {float(worst):.2f}' over {n} longitudes, "
        f"tolerance {model.tol_arcmin:g}'{where}")


def exercise_and_log_model(engine: Engine, name,
                           note_prefix: str = "") -> Optional[ExerciseResult]:
    """Exercise a model and log the act -- performative provenance, exactly
    as compile.exercise_and_log does for arith descriptions."""
    result = exercise_model(engine, name)
    if result is not None:
        note = (note_prefix + ": " if note_prefix else "") + result.detail
        engine.log_exercise(name, result.passed, note=note)
    return result
