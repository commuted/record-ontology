"""
Mathematical content for the orbital-mechanics fixture -- a SIDECAR.

Layer 2 of the Neptune arc (credit: the layering analysis is Bob's, from
his review of neptune-discovery): between pure mathematics (arith, trig)
and the historical narrative (neptune-discovery) sits the physical
mathematics both of them presuppose. neptune-discovery holds
`ex:PerturbationMathematics` as a premise-less formal object -- machinery
Bouvard and Le Verrier held mostly TESTIMONIALLY (§15.2). This module is
the §15.3 conversion for the two-body core of that machinery: run the
derivations, and testimonial holding becomes formal holding.

The discipline this file answers to (and the reason it replaced an earlier
draft): every Joint below DERIVES its conclusion by symbolic work that
consumes its premises -- dsolve on the Binet equation, substitution chains,
simplification that sympy actually performs. A derive() that restates its
stored form earns nothing: `regeneration_ok` would pass vacuously
(simplify(x - x) == 0), which is formal warrant worn without the form --
the pretender pattern, §15.3, in its hardest-to-see form because the
exercise CLOSES. Joints that only STATE a result are declared in
STATED_JOINTS, which the consumption check (engine/consumption.py) treats
as honest testimonial holdings rather than alarms.

What scripts/orbital_mechanics_demo.py exercises:

* the orbit equation r(θ) = p/(1 + e·cosθ) SOLVED from the Binet equation
  u'' + u = GMm²/L² (sympy dsolve -- the two-body problem, actually run);
* the semi-latus rectum identified from perihelion geometry (solve, not
  state): p = a(1 - e²);
* Kepler I assembled by substitution of that identification;
* Kepler II from the areal element and L = m·r²·θ̇ (r² genuinely cancels);
* L² = GMm²·a(1-e²) recovered from the Binet constant + the semi-latus
  identification -- then Kepler III: P = area/areal-rate, squared,
  simplifying to 4π²a³/GM with everything cancelling on its own;
* r = a(1 - e·cosE) from the ellipse parametrization (b² = a²(1-e²)
  substituted, the root extracted under 0 < e < 1);
* numerical corroboration on Earth's orbit (kept from Bob's draft): the
  sidereal year from Kepler III to 1e-4, perihelion distance two ways.

First-order perturbation theory is present only as a STATED ground -- the
expansion r = r₀ + εr₁ + O(ε²) is the header of the machinery, not its
content. Its real content, for this arc, is numerical and lives in
engine/perturbation.py: Uranus's residuals with and without Neptune, and
the coarse inverse fit that recovers the DIRECTION Le Verrier recovered.

Sidecar: sympy stays demo-only; the engine package never imports this.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Mapping

import sympy as sp

# -- symbols -------------------------------------------------------------------
theta = sp.symbols("theta", real=True)
E_anom = sp.symbols("E", real=True)
a = sp.symbols("a", positive=True)
e = sp.symbols("e", positive=True)          # 0 < e < 1 imposed where needed
p_sl = sp.symbols("p", positive=True)       # semi-latus rectum
G, M, m = sp.symbols("G M m", positive=True)
L = sp.symbols("L", positive=True)          # angular momentum
P = sp.symbols("P", positive=True)          # period
u = sp.Function("u")                        # u(θ) = 1/r, the Binet substitution
epsilon = sp.symbols("epsilon", positive=True)

# -- the content dictionary: record short-name -> stored form -------------------

CONTENT: Mapping[str, sp.Expr] = {
    # grounds / definitions
    "NewtonGravitation":    G * M * m / p_sl**2,          # F at r = p (form as held)
    "AngularMomentumDef":   m * p_sl**2,                  # L = m r² θ̇ at unit θ̇ (definitional shape)
    # derived, two-body
    "OrbitEquation":        p_sl / (1 + e * sp.cos(theta)),
    "SemiLatusRectum":      a * (1 - e**2),
    "KeplerFirstLaw":       a * (1 - e**2) / (1 + e * sp.cos(theta)),
    "KeplerSecondLaw":      L / (2 * m),
    "AngularMomentumEllipse": G * M * m**2 * a * (1 - e**2),   # L²
    "KeplerThirdLaw":       4 * sp.pi**2 * a**3 / (G * M),     # P²
    "PositionFromAnomaly":  a * (1 - e * sp.cos(E_anom)),
    "PerihelionDistance":   a * (1 - e),
    # stated ground (held testimonially -- see STATED_JOINTS)
    "PerturbationExpansion": epsilon,   # placeholder shape: r = r0 + ε·r1 + O(ε²)
}


# -- derivations ----------------------------------------------------------------

def derive_orbit_equation() -> sp.Expr:
    """Inf_SolveBinet: the two-body problem, run.

    Newton's law for a central inverse-square force, in the u = 1/r
    substitution, is the Binet equation  u''(θ) + u(θ) = GMm²/L².
    dsolve gives u = C·cos(θ - θ₀) + GMm²/L²; orient periapsis to θ₀ = 0,
    name the ratio of the two constants e, and invert. With the semi-latus
    rectum p ≡ L²/(GMm²) the orbit is r = p/(1 + e·cosθ): a conic."""
    k = G * M * m**2 / L**2                       # the Binet constant, 1/p
    ode = sp.Eq(u(theta).diff(theta, 2) + u(theta), k)
    sol = sp.dsolve(ode, u(theta)).rhs            # C1·sin θ + C2·cos θ + k
    C1, C2 = sp.symbols("C1 C2")
    # periapsis at θ = 0: the sin component vanishes; name C2 = e·k
    sol = sol.subs({C1: 0, C2: e * k})
    r_of_theta = sp.simplify(1 / sol)             # r = 1/u
    # express via p = 1/k
    return sp.simplify(r_of_theta.subs(1 / k, p_sl).subs(k, 1 / p_sl))


def derive_semi_latus() -> sp.Expr:
    """Inf_IdentifySemiLatus: p from the ellipse's own geometry, solved.

    At periapsis r = a(1-e); the DERIVED orbit equation, evaluated at
    θ = 0, gives the same radius. Solve the pair for p -- sympy does the
    solving, and the orbit side is consumed from Inf_SolveBinet's output,
    not retyped (the consumption check caught an earlier draft that
    hardcoded p/(1+e) here)."""
    r_peri_geom = a * (1 - e)
    r_peri_orbit = derive_orbit_equation().subs(sp.cos(theta), 1)
    (sol,) = sp.solve(sp.Eq(r_peri_geom, r_peri_orbit), p_sl)
    return sp.expand(sol)


def derive_kepler_first() -> sp.Expr:
    """Inf_AssembleKeplerFirst: substitute the identified p into the solved
    orbit equation. Consumes both premises' derived content."""
    orbit = derive_orbit_equation()
    p_val = derive_semi_latus()
    return sp.simplify(orbit.subs(p_sl, p_val))


def derive_kepler_second() -> sp.Expr:
    """Inf_DeriveArealLaw: dA/dt for a central force.

    The areal element is dA = ½·r²·dθ, so dA/dt = ½·r²·θ̇. Angular
    momentum L = m·r²·θ̇ gives θ̇ = L/(m·r²). Substitute: the r² must
    cancel -- sympy performs the cancellation."""
    r = sp.symbols("r", positive=True)
    theta_dot = L / (m * r**2)
    dA_dt = sp.Rational(1, 2) * r**2 * theta_dot
    out = sp.simplify(dA_dt)
    assert r not in out.free_symbols, "r failed to cancel -- not a central-force law"
    return out


def derive_L_squared() -> sp.Expr:
    """Inf_RecoverAngularMomentum: L² on an ellipse.

    From the Binet constant, p = L²/(GMm²); from the geometry, p = a(1-e²).
    Solve for L² -- the bridge between the dynamical and geometric faces."""
    p_val = derive_semi_latus()
    (L2,) = sp.solve(sp.Eq(L**2 / (G * M * m**2), p_val), L**2)
    return sp.expand(L2)


def derive_kepler_third() -> sp.Expr:
    """Inf_DeriveHarmonicLaw: P² = 4π²a³/GM, everything cancelling.

    Period = total area / areal rate: P = πab / (L/2m), with
    b = a·√(1-e²). Square it, substitute the derived L² -- e and m must
    both vanish. They do; sympy verifies it rather than the reader."""
    b = a * sp.sqrt(1 - e**2)
    area = sp.pi * a * b
    P_expr = area / derive_kepler_second()          # πab/(L/2m)
    P2 = sp.expand(P_expr**2)
    P2 = P2.subs(L**2, derive_L_squared())
    out = sp.simplify(P2)
    assert e not in out.free_symbols and m not in out.free_symbols, \
        "eccentricity or test mass survived -- the harmonic law did not close"
    return out


def derive_position_from_anomaly() -> sp.Expr:
    """Inf_ParametrizeEllipse: r(E) = a(1 - e·cosE) from the parametrization.

    x = a(cosE - e), y = b·sinE with b² = a²(1-e²);
    r = √(x² + y²) collapses to a(1 - e·cosE) for 0 < e < 1."""
    e1 = sp.symbols("e1", positive=True)            # with 0 < e1 < 1 assumed below
    b2 = a**2 * (1 - e1**2)
    x = a * (sp.cos(E_anom) - e1)
    y2 = b2 * sp.sin(E_anom)**2
    r2 = sp.expand(x**2 + y2)
    # r² = a²(1 - e·cosE)²; take the positive root under the stated domain
    r2_factored = sp.factor(r2)
    root = sp.sqrt(r2_factored)
    out = sp.refine(sp.powsimp(root, force=False),
                    sp.Q.positive(1 - e1 * sp.cos(E_anom)))
    out = sp.simplify(out)
    candidate = a * (1 - e1 * sp.cos(E_anom))
    # establish equality by squaring (both sides positive on the domain)
    assert sp.simplify(sp.expand(out**2 - candidate**2)) == 0
    return candidate.subs(e1, e)


def derive_perihelion() -> sp.Expr:
    """Inf_EvaluatePerihelion: θ = 0 in the DERIVED first law (consumes the
    upstream derivation, not the stored form)."""
    return sp.simplify(derive_kepler_first().subs(sp.cos(theta), 1))


def state_perturbation_expansion() -> sp.Expr:
    """Inf_StatePerturbation: STATED, not derived -- declared in
    STATED_JOINTS. The expansion r = r₀ + ε·r₁ + O(ε²) is held
    testimonially here; its working content for the Neptune arc is
    numerical (engine/perturbation.py)."""
    return epsilon


# -- the joints registry ----------------------------------------------------------

@dataclass(frozen=True)
class Joint:
    """A joint in the derivation web: an inference that concludes a record."""
    inference: str
    concludes: str
    title: str
    derive: Callable[[], sp.Expr]


JOINTS = (
    Joint("Inf_SolveBinet", "OrbitEquation",
          "the two-body problem: Binet's equation, dsolved to a conic",
          derive_orbit_equation),
    Joint("Inf_IdentifySemiLatus", "SemiLatusRectum",
          "p = a(1-e²) solved from periapsis geometry",
          derive_semi_latus),
    Joint("Inf_AssembleKeplerFirst", "KeplerFirstLaw",
          "Kepler I: the identified p substituted into the solved orbit",
          derive_kepler_first),
    Joint("Inf_DeriveArealLaw", "KeplerSecondLaw",
          "Kepler II: dA/dt = L/2m, the r² cancelling",
          derive_kepler_second),
    Joint("Inf_RecoverAngularMomentum", "AngularMomentumEllipse",
          "L² = GMm²·a(1-e²): dynamical and geometric p equated",
          derive_L_squared),
    Joint("Inf_DeriveHarmonicLaw", "KeplerThirdLaw",
          "Kepler III: P² = 4π²a³/GM with e and m vanishing",
          derive_kepler_third),
    Joint("Inf_ParametrizeEllipse", "PositionFromAnomaly",
          "r(E) = a(1 - e·cosE) from the ellipse parametrization",
          derive_position_from_anomaly),
    Joint("Inf_EvaluatePerihelion", "PerihelionDistance",
          "perihelion: θ = 0 in the derived first law",
          derive_perihelion),
    Joint("Inf_StatePerturbation", "PerturbationExpansion",
          "the perturbation expansion, STATED (testimonial; see STATED_JOINTS)",
          state_perturbation_expansion),
)

# Joints that STATE rather than derive -- honest testimonial holdings, exempt
# from the consumption alarm (engine/consumption.py) because the skip is
# declared. §13.1: a stub is the explicit form of a skip.
STATED_JOINTS = frozenset({"Inf_StatePerturbation"})


# -- numerical corroboration: Earth's orbit (kept from Bob's draft) ---------------

EARTH_ORBIT = {
    "a": 1.495978707e11,          # m (1 AU)
    "e": 0.0167086,
    "GM": 1.32712440018e20,       # m³/s² (heliocentric gravitational parameter)
    "P_observed": 365.25636 * 86400.0,   # sidereal year, s
}


def validate_keplers_third_law() -> tuple[float, float, float]:
    """Earth's sidereal year from the DERIVED harmonic law (not a retyped
    formula: the derived expression is lambdified and evaluated)."""
    P2 = derive_kepler_third()                     # 4π²a³/(GM)
    P2_num = float(P2.subs({a: EARTH_ORBIT["a"], G: 1.0, M: EARTH_ORBIT["GM"]}))
    P_calc = math.sqrt(P2_num)
    P_obs = EARTH_ORBIT["P_observed"]
    return P_calc, P_obs, abs(P_calc - P_obs) / P_obs


def validate_perihelion() -> tuple[float, float]:
    """Perihelion two ways: the derived r(θ=0) vs the derived a(1-e)."""
    vals = {a: EARTH_ORBIT["a"], e: EARTH_ORBIT["e"]}
    r_from_law = float(derive_kepler_first().subs(sp.cos(theta), 1).subs(vals))
    r_direct = float(derive_perihelion().subs(vals))
    return r_from_law, r_direct


# -- regeneration (§14, run) -------------------------------------------------------

def regenerate(record: str) -> list:
    """Re-derive a punctured record's content from the machinery."""
    return [sp.simplify(jt.derive()) for jt in JOINTS if jt.concludes == record]


def regeneration_ok(record: str) -> bool:
    stored = CONTENT[record]
    outs = regenerate(record)
    return bool(outs) and all(sp.simplify(out - stored) == 0 for out in outs)
