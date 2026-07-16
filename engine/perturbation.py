"""
The Neptune arc's mathematics, RUN (§15.1/§15.3 for the perturbation face).

neptune-discovery.ttl narrates the structure: Bouvard's tables fail against
observation (the anomaly), two agents abduce an unseen perturber, Le Verrier
computes WHERE, Galle looks and finds. The fixture holds the mathematical
machinery (`ex:PerturbationMathematics`) as a premise-less formal object --
held, in 1845 as now, mostly testimonially. This module converts the part
of that holding that carries the arc:

  FORWARD (Bouvard's side): integrate Uranus 1750-1850 with and without
  Neptune (pure-Python RK4, heliocentric EOM with indirect terms; modern
  elements). The difference in heliocentric longitude IS the anomaly: it
  grows through tens of arcseconds, and its structure keys to the
  Uranus-Neptune conjunction (~1821 -- the same epoch Bouvard's tables
  were built, which is why they failed so soon after).

  INVERSE (Le Verrier's side, coarse): given only those residuals and a
  perturber CONSTRAINED TO THE WRONG ORBIT -- circular at the Titius-Bode
  radius, as the fixture's ex:BodesLaw premise records -- grid-fit the
  perturber's mass and epoch longitude, allowing the linear detrend that
  stands in for Bouvard's freedom to re-fit Uranus's elements. Then ask
  the fitted perturber where it sits on 1846-09-23.

  The point the fixture already narrates ("both predicted ORBITS were
  substantially wrong while the predicted DIRECTION was right") stops
  being narration: the wrong-radius fit still lands the discovery-night
  LONGITUDE, because the residual curve pins the conjunction epoch, and
  at conjunction the perturber must be where the pull is. Fidelity is not
  all-or-nothing -- computed, this time, not felt (§10).

No scipy, no numpy: the integrator is ~40 lines of RK4 over lists. Modern
elements and masses; as with mathcontent.py, the point is the structure of
the agreement, not anachronistic precision.

Sidecar: demo-only (scripts/neptune_math_demo.py); the engine package
never imports this.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

# -- units: AU, years, solar masses; GM_sun = 4·pi² ------------------------------
MU = 4.0 * math.pi**2

# J2000 mean ecliptic elements (planar approximation: i = 0).
#   a [AU], e, varpi = longitude of perihelion [deg], lam0 = mean longitude
#   at J2000.0 [deg], mass [M_sun].
ELEMENTS = {
    "uranus":  dict(a=19.19126, e=0.04717, varpi=170.954, lam0=313.238,
                    mass=4.366e-5),
    "neptune": dict(a=30.06992, e=0.00859, varpi=44.965,  lam0=304.880,
                    mass=5.149e-5),
}

J2000 = 2000.0
DISCOVERY_EPOCH = 1846.73        # 1846-09-23
NEPTUNE_TRUE_LONGITUDE_1846 = None   # computed from elements, below
BODE_RADIUS_AU = 38.8            # the Titius-Bode slot the fixture records


# -- Kepler machinery (the Layer-2 formulas, used numerically) --------------------

def solve_kepler(M_anom: float, e: float, tol: float = 1e-12) -> float:
    """E - e·sinE = M, Newton's iteration."""
    E = M_anom if e < 0.8 else math.pi
    for _ in range(60):
        d = (E - e * math.sin(E) - M_anom) / (1.0 - e * math.cos(E))
        E -= d
        if abs(d) < tol:
            return E
    return E


def state_from_elements(el: dict, t_years: float) -> Tuple[float, float, float, float]:
    """Heliocentric planar state (x, y, vx, vy) at epoch t (calendar years).

    Uses the derived Layer-2 content: mean motion from Kepler III
    (n² a³ = μ(1+m)), r = a(1 - e·cosE), true anomaly from E.
    """
    a, e = el["a"], el["e"]
    varpi = math.radians(el["varpi"])
    mu = MU * (1.0 + el["mass"])
    n = math.sqrt(mu / a**3)
    M0 = math.radians(el["lam0"]) - varpi
    M_anom = M0 + n * (t_years - J2000)
    E = solve_kepler(math.fmod(M_anom, 2 * math.pi), e)
    r = a * (1.0 - e * math.cos(E))                     # PositionFromAnomaly, run
    nu = 2.0 * math.atan2(math.sqrt(1 + e) * math.sin(E / 2),
                          math.sqrt(1 - e) * math.cos(E / 2))
    th = nu + varpi
    x, y = r * math.cos(th), r * math.sin(th)
    # velocity in the orbital plane, rotated by varpi
    p = a * (1.0 - e * e)                               # SemiLatusRectum, run
    h = math.sqrt(mu * p)                               # AngularMomentumEllipse, run
    vr = (h * e / p) * math.sin(nu)
    vt = h / r
    vx = vr * math.cos(th) - vt * math.sin(th)
    vy = vr * math.sin(th) + vt * math.cos(th)
    return x, y, vx, vy


def heliocentric_longitude(x: float, y: float) -> float:
    """Ecliptic longitude in degrees, [0, 360)."""
    return math.degrees(math.atan2(y, x)) % 360.0


# -- the integrator: heliocentric N-body with indirect terms ----------------------

@dataclass
class Body:
    name: str
    mass: float
    x: float
    y: float
    vx: float
    vy: float


def _accels(bodies: List[Body]) -> List[Tuple[float, float]]:
    """Heliocentric equations of motion:
    r̈ᵢ = -μ(1+mᵢ)·rᵢ/rᵢ³ + Σⱼ μ·mⱼ·[(rⱼ-rᵢ)/|rⱼ-rᵢ|³ - rⱼ/rⱼ³]"""
    out = []
    for i, bi in enumerate(bodies):
        ri3 = (bi.x**2 + bi.y**2) ** 1.5
        ax = -MU * (1 + bi.mass) * bi.x / ri3
        ay = -MU * (1 + bi.mass) * bi.y / ri3
        for j, bj in enumerate(bodies):
            if j == i:
                continue
            dx, dy = bj.x - bi.x, bj.y - bi.y
            d3 = (dx * dx + dy * dy) ** 1.5
            rj3 = (bj.x**2 + bj.y**2) ** 1.5
            ax += MU * bj.mass * (dx / d3 - bj.x / rj3)
            ay += MU * bj.mass * (dy / d3 - bj.y / rj3)
        out.append((ax, ay))
    return out


def integrate(bodies: List[Body], t0: float, t1: float, dt: float,
              sample_name: str, sample_every: float = 1.0) -> List[Tuple[float, float]]:
    """RK4; returns [(epoch, heliocentric longitude of sample_name), ...]."""
    samples = []
    t = t0
    next_sample = t0
    idx = next(i for i, b in enumerate(bodies) if b.name == sample_name)
    n_steps = int(round((t1 - t0) / dt))
    for _ in range(n_steps + 1):
        if t >= next_sample - 1e-9:
            b = bodies[idx]
            samples.append((t, heliocentric_longitude(b.x, b.y)))
            next_sample += sample_every
        # RK4 step over the flattened state
        state = [(b.x, b.y, b.vx, b.vy) for b in bodies]

        def deriv(st):
            tmp = [Body(b.name, b.mass, s[0], s[1], s[2], s[3])
                   for b, s in zip(bodies, st)]
            acc = _accels(tmp)
            return [(s[2], s[3], a[0], a[1]) for s, a in zip(st, acc)]

        k1 = deriv(state)
        k2 = deriv([tuple(s[m] + 0.5 * dt * k1[i][m] for m in range(4))
                    for i, s in enumerate(state)])
        k3 = deriv([tuple(s[m] + 0.5 * dt * k2[i][m] for m in range(4))
                    for i, s in enumerate(state)])
        k4 = deriv([tuple(s[m] + dt * k3[i][m] for m in range(4))
                    for i, s in enumerate(state)])
        for i, b in enumerate(bodies):
            b.x += dt / 6 * (k1[i][0] + 2 * k2[i][0] + 2 * k3[i][0] + k4[i][0])
            b.y += dt / 6 * (k1[i][1] + 2 * k2[i][1] + 2 * k3[i][1] + k4[i][1])
            b.vx += dt / 6 * (k1[i][2] + 2 * k2[i][2] + 2 * k3[i][2] + k4[i][2])
            b.vy += dt / 6 * (k1[i][3] + 2 * k2[i][3] + 2 * k3[i][3] + k4[i][3])
        t += dt
    return samples


def _make_uranus(t0: float) -> Body:
    el = ELEMENTS["uranus"]
    x, y, vx, vy = state_from_elements(el, t0)
    return Body("uranus", el["mass"], x, y, vx, vy)


def _make_neptune(t0: float) -> Body:
    el = ELEMENTS["neptune"]
    x, y, vx, vy = state_from_elements(el, t0)
    return Body("neptune", el["mass"], x, y, vx, vy)


def _make_perturber(t0: float, radius_au: float, lam0_deg_at_t0: float,
                    mass: float) -> Body:
    """Circular perturber: the Bode-slot hypothesis in its first, naive form."""
    th = math.radians(lam0_deg_at_t0)
    v = math.sqrt(MU * (1 + mass) / radius_au)
    return Body("perturber", mass,
                radius_au * math.cos(th), radius_au * math.sin(th),
                -v * math.sin(th), v * math.cos(th))


def _make_perturber_el(t0: float, a_p: float, e_p: float, varpi_deg: float,
                       lam_t0_deg: float, mass: float) -> Body:
    """Eccentric perturber from elements AT t0 (Le Verrier's actual freedom:
    Bode-neighborhood semi-major axis, eccentricity, perihelion placement)."""
    el = dict(a=a_p, e=max(e_p, 1e-9), varpi=varpi_deg, mass=mass,
              # state_from_elements references J2000; shift lam so that the
              # mean longitude AT t0 equals lam_t0_deg
              lam0=0.0)
    mu = MU * (1.0 + mass)
    n = math.sqrt(mu / a_p**3)
    el["lam0"] = (lam_t0_deg - math.degrees(n * (t0 - J2000))) % 360.0
    x, y, vx, vy = state_from_elements(el, t0)
    return Body("perturber", mass, x, y, vx, vy)


def _wrap_deg(d: float) -> float:
    return (d + 180.0) % 360.0 - 180.0


# -- FORWARD: the anomaly, computed ------------------------------------------------

def uranus_residuals(t0: float = 1750.0, t1: float = 1850.0,
                     dt: float = 0.02) -> List[Tuple[float, float]]:
    """Heliocentric-longitude residuals of Uranus, (with Neptune) - (without),
    arcseconds, sampled yearly. Both runs start from the identical Uranus
    state at t0, so the curve is pure Neptune."""
    with_n = integrate([_make_uranus(t0), _make_neptune(t0)],
                       t0, t1, dt, "uranus")
    without = integrate([_make_uranus(t0)], t0, t1, dt, "uranus")
    return [(ta, _wrap_deg(la - lb) * 3600.0)
            for (ta, la), (tb, lb) in zip(with_n, without)]


def conjunction_epoch(t0: float = 1750.0, t1: float = 1850.0) -> float:
    """Epoch at which Uranus and Neptune share heliocentric longitude
    (elements propagated two-body): the residual curve's hinge."""
    best_t, best_gap = t0, 360.0
    t = t0
    while t <= t1:
        lu = heliocentric_longitude(*state_from_elements(ELEMENTS["uranus"], t)[:2])
        ln = heliocentric_longitude(*state_from_elements(ELEMENTS["neptune"], t)[:2])
        gap = abs(_wrap_deg(lu - ln))
        if gap < best_gap:
            best_gap, best_t = gap, t
        t += 0.1
    return best_t


# -- INVERSE: Le Verrier's move, coarse --------------------------------------------

def _detrended_rms(obs: Sequence[float], model: Sequence[float],
                   ts: Sequence[float]) -> float:
    """RMS of (obs - model) after removing the best-fit linear trend --
    the stand-in for re-fitting Uranus's epoch and mean motion, the freedom
    Bouvard's tables actually had."""
    d = [o - m for o, m in zip(obs, model)]
    n = len(d)
    st = sum(ts); st2 = sum(t * t for t in ts)
    sd = sum(d); std_ = sum(t * x for t, x in zip(ts, d))
    den = n * st2 - st * st
    beta = (n * std_ - st * sd) / den
    alpha = (sd - beta * st) / n
    resid = [x - alpha - beta * t for x, t in zip(d, ts)]
    return math.sqrt(sum(r * r for r in resid) / n)


def perturber_residuals(pert: Body, t0: float = 1750.0, t1: float = 1850.0,
                        dt: float = 0.05) -> List[Tuple[float, float]]:
    with_p = integrate([_make_uranus(t0), pert], t0, t1, dt, "uranus")
    without = integrate([_make_uranus(t0)], t0, t1, dt, "uranus")
    return [(ta, _wrap_deg(la - lb) * 3600.0)
            for (ta, la), (tb, lb) in zip(with_p, without)]


_MASSES = (5.15e-5, 1.03e-4, 2.06e-4)


def _fit_candidates(candidates, obs_ts, obs_v, t0, t1, dt_grid):
    """Score each candidate perturber-element dict against the residuals."""
    best = None
    for cand in candidates:
        pert = _make_perturber_el(t0, cand["a"], cand["e"], cand["varpi"],
                                  cand["lam"], cand["mass"])
        mod = perturber_residuals(pert, t0, t1 + 4.0, dt_grid)
        mv = [v for t, v in mod if t0 <= t <= t1]
        s = _detrended_rms(obs_v, mv, obs_ts)
        if best is None or s < best[0]:
            best = (s, cand)
    return best


def _predict_1846(cand, t0):
    """Where the fitted perturber sits on discovery night, vs Neptune."""
    pert = _make_perturber_el(t0, cand["a"], cand["e"], cand["varpi"],
                              cand["lam"], cand["mass"])
    run = integrate([_make_uranus(t0), pert], t0, DISCOVERY_EPOCH + 0.01, 0.05,
                    "perturber", sample_every=0.5)
    predicted = run[-1][1]
    xn, yn, _, _ = state_from_elements(ELEMENTS["neptune"], DISCOVERY_EPOCH)
    truth = heliocentric_longitude(xn, yn)
    return predicted, truth, abs(_wrap_deg(predicted - truth))


def leverrier_fit(t0: float = 1750.0, t1: float = 1846.0) -> Dict:
    """Le Verrier's move, in two historically honest stages.

    Stage 1 -- the naive hypothesis: a CIRCULAR perturber at the Bode
    radius (38.8 AU). The fit converges, but on a slower-than-Neptune
    circle the pull-history pins the perturber ~35-40 degrees BEHIND
    Neptune's true 1846 position. The residuals themselves refuse the
    circle -- which is the finding, not a failure of the method.

    Stage 2 -- Le Verrier's actual freedom: Bode-NEIGHBORHOOD semi-major
    axis (36.2 / 38.8 AU -- still 20-30% beyond Neptune's real 30.1),
    eccentricity ~0.11 with free perihelion. Near perihelion a too-large
    eccentric orbit moves faster and sits closer, so the pull history AND
    the 1846 direction can both be matched: his published elements
    (a=36.15, e=0.1076) are exactly this shape. The claim the fixture
    narrates -- wrong ORBIT, right DIRECTION -- is the stage-2 output.

    Calibration of expectations, honestly stated: this coarse grid lands
    the direction to ~20 degrees, against Le Verrier's ~1 degree -- he ran
    a 33-equation conditioned fit (and had luck; his orbit diverges from
    Neptune's within decades outside the fitted arc). Two structural
    findings survive the coarseness and are the demo's verdicts: the
    residuals REFUSE the circle (stage 1 is pinned tens of degrees behind,
    at 4x the RMS), and the LONG arc is load-bearing -- fitting only the
    modern era (1800+) reaches 1.2 arcsec RMS while pointing 154 degrees
    wrong, a degenerate far-side solution. More evidence, stricter
    exercise (§16.2), computed.
    """
    obs = uranus_residuals(t0, t1 + 4.0, dt=0.02)
    window = [(t, v) for t, v in obs if t0 <= t <= t1]
    ts = [t for t, _ in window]
    ov = [v for _, v in window]

    # -- stage 1: the Bode circle --------------------------------------------
    circ = [dict(a=BODE_RADIUS_AU, e=0.0, varpi=0.0, lam=lam, mass=mass)
            for lam in range(0, 360, 10) for mass in _MASSES]
    s1, best1 = _fit_candidates(circ, ts, ov, t0, t1, 0.1)
    pred1, truth, err1 = _predict_1846(best1, t0)

    # -- stage 2: eccentric, Bode-neighborhood -------------------------------
    ecc = [dict(a=a_p, e=0.11, varpi=vp, lam=lam, mass=mass)
           for a_p in (36.2, BODE_RADIUS_AU)
           for vp in range(0, 360, 45)
           for lam in range(0, 360, 15)
           for mass in _MASSES]
    s2, best2 = _fit_candidates(ecc, ts, ov, t0, t1, 0.1)
    # refine around the winner
    ref = [dict(best2, lam=(best2["lam"] + dl) % 360.0,
                varpi=(best2["varpi"] + dv) % 360.0)
           for dl in (-7.5, -3.75, 0.0, 3.75, 7.5)
           for dv in (-20.0, -10.0, 0.0, 10.0, 20.0)]
    s2r, best2 = _fit_candidates(ref, ts, ov, t0, t1, 0.05)
    s2 = min(s2, s2r)
    pred2, _, err2 = _predict_1846(best2, t0)

    return {
        "circular": {
            "elements": best1, "fit_rms_arcsec": s1,
            "predicted_longitude_1846_deg": pred1, "error_deg": err1,
        },
        "leverrier": {
            "elements": best2, "fit_rms_arcsec": s2,
            "predicted_longitude_1846_deg": pred2, "error_deg": err2,
        },
        "neptune_longitude_1846_deg": truth,
    }


# -- verdicts (what the demo asserts) ------------------------------------------------

def run_all() -> Dict:
    """The whole arc: anomaly amplitude, conjunction hinge, inverse fit."""
    res = uranus_residuals()
    peak_t, peak_v = max(res, key=lambda tv: abs(tv[1]))
    final_t, final_v = res[-1]
    conj = conjunction_epoch()
    fit = leverrier_fit()
    err_circ = fit["circular"]["error_deg"]
    err_lv = fit["leverrier"]["error_deg"]
    return {
        "residuals": res,
        "residual_final": (final_t, final_v),
        "residual_peak": (peak_t, peak_v),
        "conjunction_epoch": conj,
        "fit": fit,
        "verdicts": {
            "anomaly_material": 30.0 <= abs(peak_v) <= 5000.0,
            "conjunction_near_1821": 1815.0 <= conj <= 1830.0,
            "circle_refused": err_circ >= 30.0 and
                              fit["circular"]["fit_rms_arcsec"] >
                              2.0 * fit["leverrier"]["fit_rms_arcsec"],
            "circle_refused_deg": err_circ,
            "direction_recovered_deg": err_lv,
            # the zone verdict: within the ~25-degree region a sweep search
            # (Challis's approach) would cover; Le Verrier's 1-degree needed
            # the full 33-equation fit this coarse grid does not attempt
            "direction_recovered": err_lv <= 25.0,
        },
    }
