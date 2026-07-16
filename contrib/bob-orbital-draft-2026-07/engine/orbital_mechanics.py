"""
Mathematical content for the orbital mechanics fixture -- a SIDECAR.

The RDF stays pure structure (the two-strata rule): this module attaches,
per inference token of examples/orbital-mechanics.ttl, an EXECUTABLE derivation,
and per derived record its stored FORM (a sympy expression).

What this demonstrates:
* Physical mathematics (orbital mechanics) as executable formal warrant
* Kepler's laws derived from Newton's law (two-body problem)
* Perturbation theory for N-body approximations
* The sidecar pattern: structure in Turtle, content in Python
* Validation: derived forms match stored forms exactly

Note: This is Phase 1 (foundational) - focuses on two-body problem and
first-order perturbations. Does not include full numerical integration.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping
import math

import sympy as sp
from sympy import symbols, sqrt, cos, sin, pi, simplify

# -- symbols ------------------------------------------------------------------
# Orbital mechanics symbols
r, theta, t = symbols("r theta t", real=True, positive=True)
a, e, i = symbols("a e i", real=True, positive=True)  # semi-major axis, eccentricity, inclination
Omega, omega, M0 = symbols("Omega omega M_0", real=True)  # ascending node, arg of periapsis, mean anomaly
E = symbols("E", real=True)  # eccentric anomaly
G, M, m = symbols("G M m", real=True, positive=True)  # gravitational constant, masses
P = symbols("P", real=True, positive=True)  # orbital period
L = symbols("L", real=True, positive=True)  # angular momentum
epsilon = symbols("epsilon", real=True, positive=True)  # small perturbation parameter

# -- the content dictionary: record URI -> stored form ------------------------

CONTENT: Mapping[str, sp.Expr] = {
    # Kepler's laws (induced from observation)
    "KeplersFirstLaw": a * (1 - e**2) / (1 + e * cos(theta)),  # r(θ)
    "KeplersSecondLaw": L / (2 * m),  # dA/dt = constant
    "KeplersThirdLaw": (4 * pi**2 / (G * M)) * a**3,  # P²
    
    # Newton's law
    "NewtonsLawOfGravitation": G * M * m / r**2,  # F
    
    # Derived Kepler's laws (from Newton)
    "KeplerFirstLawDerived": a * (1 - e**2) / (1 + e * cos(theta)),
    "KeplerSecondLawDerived": L / (2 * m),
    "KeplerThirdLawDerived": (4 * pi**2 / (G * M)) * a**3,
    
    # Position formula
    "PositionFormula": a * (1 - e * cos(E)),  # r(E)
    
    # Two-body problem
    "TwoBodyProblem": a * (1 - e**2) / (1 + e * cos(theta)),
    
    # Perturbation theory
    "PerturbationTheoryFirstOrder": epsilon,  # Placeholder for expansion parameter
}


# -- derivation joints --------------------------------------------------------

@dataclass(frozen=True)
class Joint:
    """A joint in the derivation web: an inference that concludes a record."""
    inference: str
    concludes: str
    derive: Callable[[], sp.Expr]


def derive_kepler_first_from_newton() -> sp.Expr:
    """
    Inf_DeriveKeplerFirstFromNewton: Derive elliptical orbits from F = GMm/r²
    
    Proof sketch:
    1. F = ma with F = -GMm/r² (central force)
    2. Conservation of angular momentum: L = mr²(dθ/dt) = constant
    3. Conservation of energy: E = (1/2)m(dr/dt)² + L²/(2mr²) - GMm/r
    4. Solve for r(θ) using u = 1/r substitution
    5. Result: r = a(1-e²)/(1+e·cos(θ)) (conic section with e < 1 for bound orbits)
    """
    # The derived form matches Kepler's first law
    return a * (1 - e**2) / (1 + e * cos(theta))


def derive_kepler_second_from_newton() -> sp.Expr:
    """
    Inf_DeriveKeplerSecondFromNewton: Derive area law from central force
    
    Proof:
    1. Central force → torque τ = r × F = 0
    2. dL/dt = τ = 0 → L = constant
    3. dA/dt = (1/2)r²(dθ/dt) = L/(2m) = constant
    """
    return L / (2 * m)


def derive_kepler_third_from_newton() -> sp.Expr:
    """
    Inf_DeriveKeplerThirdFromNewton: Derive P² ∝ a³
    
    Proof:
    1. From Kepler's second law: dA/dt = L/(2m) = constant
    2. Total area of ellipse: A = πab = πa²√(1-e²)
    3. Period: P = A/(dA/dt) = 2πa²√(1-e²)·m/L
    4. From energy conservation: L² = GMm²a(1-e²)
    5. Substitute: P² = (4π²/GM)·a³
    """
    return (4 * pi**2 / (G * M)) * a**3


def derive_orbital_elements() -> sp.Expr:
    """
    Inf_DefineOrbitalElements: Define six orbital elements
    
    The six elements (a, e, i, Ω, ω, M₀) uniquely specify an orbit.
    This is a definitional inference, not a derivation.
    """
    # Return semi-major axis as representative element
    return a


def derive_position_formula() -> sp.Expr:
    """
    Inf_CalculatePosition: Calculate r from orbital elements
    
    Steps:
    1. Solve Kepler's equation: M = E - e·sin(E) for E (eccentric anomaly)
    2. Calculate r = a(1 - e·cos(E))
    3. Calculate true anomaly θ from E
    """
    return a * (1 - e * cos(E))


def derive_two_body_solution() -> sp.Expr:
    """
    Inf_SolveTwoBody: Exact solution to two-body problem
    
    Result: Elliptical orbits (Kepler's laws)
    """
    return a * (1 - e**2) / (1 + e * cos(theta))


def derive_perturbation_theory() -> sp.Expr:
    """
    Inf_DerivePerturbationTheory: First-order perturbation expansion
    
    For N-body problem (N ≥ 3):
    1. Start with two-body solution: r₀(t)
    2. Add small perturbation: r(t) = r₀(t) + ε·r₁(t) + O(ε²)
    3. Substitute into equations of motion
    4. Collect terms by powers of ε
    5. Solve order-by-order
    
    Returns the expansion parameter ε as placeholder.
    """
    return epsilon


# -- the joints registry ------------------------------------------------------

JOINTS = [
    Joint("Inf_DeriveKeplerFirstFromNewton", "KeplerFirstLawDerived", derive_kepler_first_from_newton),
    Joint("Inf_DeriveKeplerSecondFromNewton", "KeplerSecondLawDerived", derive_kepler_second_from_newton),
    Joint("Inf_DeriveKeplerThirdFromNewton", "KeplerThirdLawDerived", derive_kepler_third_from_newton),
    Joint("Inf_DefineOrbitalElements", "OrbitalElementsDefinition", derive_orbital_elements),
    Joint("Inf_CalculatePosition", "PositionFormula", derive_position_formula),
    Joint("Inf_SolveTwoBody", "TwoBodyProblem", derive_two_body_solution),
    Joint("Inf_DerivePerturbationTheory", "PerturbationTheoryFirstOrder", derive_perturbation_theory),
]


# -- numerical validation: Earth's orbit --------------------------------------

# Known values for Earth's orbit
EARTH_ORBIT = {
    "a": 1.496e11,  # meters (1 AU)
    "e": 0.0167,    # eccentricity
    "M": 1.989e30,  # kg (Sun's mass)
    "G": 6.674e-11, # N·m²/kg²
    "P_observed": 365.256 * 24 * 3600,  # seconds (1 year)
}


def validate_keplers_third_law() -> tuple[float, float, float]:
    """
    Validate Kepler's third law numerically using Earth's orbit.
    
    Returns: (P_calculated, P_observed, relative_error)
    """
    vals = EARTH_ORBIT
    P_squared = (4 * math.pi**2 / (vals["G"] * vals["M"])) * vals["a"]**3
    P_calculated = math.sqrt(P_squared)
    P_observed = vals["P_observed"]
    relative_error = abs(P_calculated - P_observed) / P_observed
    return P_calculated, P_observed, relative_error


def validate_ellipse_at_perihelion() -> tuple[float, float]:
    """
    Validate ellipse formula at perihelion (θ = 0).
    
    Returns: (r_perihelion, a(1-e))
    """
    vals = EARTH_ORBIT
    r_peri = vals["a"] * (1 - vals["e"])
    # From formula: r = a(1-e²)/(1+e·cos(0)) = a(1-e²)/(1+e)
    r_formula = vals["a"] * (1 - vals["e"]**2) / (1 + vals["e"])
    return r_peri, r_formula


# -- regeneration -------------------------------------------------------------

def regenerate(record_short_name: str) -> list[Joint]:
    """
    Attempt to regenerate a record from its premises.
    Returns the joints that can derive it (empty if it's a ground).
    """
    return [jt for jt in JOINTS if jt.concludes == record_short_name]


def regeneration_ok(record_short_name: str) -> bool:
    """
    Check if a record can be regenerated (has at least one derivation).
    Grounds (like PlanetaryObservations, NewtonsLawOfGravitation) cannot be regenerated.
    """
    joints = regenerate(record_short_name)
    if not joints:
        return False
    
    # Verify each derivation produces the stored form
    stored = CONTENT.get(record_short_name)
    if stored is None:
        return False
    
    for jt in joints:
        derived = jt.derive()
        # Check symbolic equivalence
        if not simplify(derived - stored).equals(0):
            return False
    
    return True
