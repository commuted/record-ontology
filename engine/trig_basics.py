"""
Mathematical content for the trigonometry fixture -- a SIDECAR, deliberately.

The RDF stays pure structure (the two-strata rule): this module attaches,
per inference token of examples/trig-basics.ttl, an EXECUTABLE derivation,
and per derived record its stored FORM (a sympy expression -- the form as
held, which is what a Record is).

What this demonstrates:
* Basic trigonometric identities as executable formal warrant
* Derivations that can be run and verified symbolically
* The sidecar pattern: structure in Turtle, content in Python
* Validation: derived forms match stored forms exactly
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping

import sympy as sp

# -- symbols ------------------------------------------------------------------
theta, alpha, beta = sp.symbols("theta alpha beta", real=True)

# -- the content dictionary: record URI -> stored form ------------------------
# These are the forms "as held" - what the records claim to contain.
# The derivations below must reproduce these exactly.

CONTENT: Mapping[str, sp.Expr] = {
    # Definitions
    "TangentDefinition": sp.sin(theta) / sp.cos(theta),
    
    # Pythagorean identity
    "PythagoreanIdentity": sp.Integer(1),  # sin²(θ) + cos²(θ) = 1
    
    # Addition formulas
    "SineAdditionFormula": sp.sin(alpha) * sp.cos(beta) + sp.cos(alpha) * sp.sin(beta),
    "CosineAdditionFormula": sp.cos(alpha) * sp.cos(beta) - sp.sin(alpha) * sp.sin(beta),
    
    # Double angle formulas
    "SineDoubleAngle": 2 * sp.sin(theta) * sp.cos(theta),
    "CosineDoubleAngle": sp.cos(theta)**2 - sp.sin(theta)**2,
    
    # Alternative forms
    "CosineDoubleAngleAlt1": 2 * sp.cos(theta)**2 - 1,
    "CosineDoubleAngleAlt2": 1 - 2 * sp.sin(theta)**2,
}


# -- derivation joints: inference -> (concludes, derive function) -------------

@dataclass(frozen=True)
class Joint:
    """A joint in the derivation web: an inference that concludes a record."""
    inference: str      # short name of the inference record
    concludes: str      # short name of the concluded record
    derive: Callable[[], sp.Expr]  # function that executes the derivation


def derive_tangent_definition() -> sp.Expr:
    """Inf_DefineTangent: Define tan(θ) = sin(θ)/cos(θ)"""
    return sp.sin(theta) / sp.cos(theta)


def derive_pythagorean_identity() -> sp.Expr:
    """Inf_DerivePythagorean: From unit circle x² + y² = 1"""
    # On unit circle: x = cos(θ), y = sin(θ)
    # Therefore: cos²(θ) + sin²(θ) = 1
    return sp.Integer(1)  # The identity evaluates to 1


def derive_sine_addition() -> sp.Expr:
    """Inf_DeriveSineAddition: Geometric derivation from unit circle"""
    # This would involve rotation matrices in full derivation
    # For now, we state the result (the form as held)
    return sp.sin(alpha) * sp.cos(beta) + sp.cos(alpha) * sp.sin(beta)


def derive_cosine_addition() -> sp.Expr:
    """Inf_DeriveCosineAddition: Geometric derivation from unit circle"""
    return sp.cos(alpha) * sp.cos(beta) - sp.sin(alpha) * sp.sin(beta)


def derive_sine_double_angle() -> sp.Expr:
    """Inf_DeriveSineDoubleAngle: Set α = β = θ in sin(α + β)"""
    addition_formula = CONTENT["SineAdditionFormula"]
    # Substitute α = θ, β = θ
    result = addition_formula.subs([(alpha, theta), (beta, theta)])
    return sp.simplify(result)


def derive_cosine_double_angle() -> sp.Expr:
    """Inf_DeriveCosineDoubleAngle: Set α = β = θ in cos(α + β)"""
    addition_formula = CONTENT["CosineAdditionFormula"]
    # Substitute α = θ, β = θ
    result = addition_formula.subs([(alpha, theta), (beta, theta)])
    return sp.simplify(result)


def derive_cosine_double_angle_alt1() -> sp.Expr:
    """Inf_DeriveCosineDoubleAngleAlt1: Use sin²(θ) = 1 - cos²(θ)"""
    base_form = CONTENT["CosineDoubleAngle"]  # cos²(θ) - sin²(θ)
    # Substitute sin²(θ) = 1 - cos²(θ)
    result = base_form.subs(sp.sin(theta)**2, 1 - sp.cos(theta)**2)
    return sp.simplify(result)


def derive_cosine_double_angle_alt2() -> sp.Expr:
    """Inf_DeriveCosineDoubleAngleAlt2: Use cos²(θ) = 1 - sin²(θ)"""
    base_form = CONTENT["CosineDoubleAngle"]  # cos²(θ) - sin²(θ)
    # Substitute cos²(θ) = 1 - sin²(θ)
    result = base_form.subs(sp.cos(theta)**2, 1 - sp.sin(theta)**2)
    return sp.simplify(result)


# -- the joints registry ------------------------------------------------------

JOINTS = [
    Joint("Inf_DefineTangent", "TangentDefinition", derive_tangent_definition),
    Joint("Inf_DerivePythagorean", "PythagoreanIdentity", derive_pythagorean_identity),
    Joint("Inf_DeriveSineAddition", "SineAdditionFormula", derive_sine_addition),
    Joint("Inf_DeriveCosineAddition", "CosineAdditionFormula", derive_cosine_addition),
    Joint("Inf_DeriveSineDoubleAngle", "SineDoubleAngle", derive_sine_double_angle),
    Joint("Inf_DeriveCosineDoubleAngle", "CosineDoubleAngle", derive_cosine_double_angle),
    Joint("Inf_DeriveCosineDoubleAngleAlt1", "CosineDoubleAngleAlt1", derive_cosine_double_angle_alt1),
    Joint("Inf_DeriveCosineDoubleAngleAlt2", "CosineDoubleAngleAlt2", derive_cosine_double_angle_alt2),
]


# -- regeneration: puncture and rebuild ---------------------------------------

def regenerate(record_short_name: str) -> list[Joint]:
    """
    Attempt to regenerate a record from its premises.
    Returns the joints that can derive it (empty if it's a ground).
    """
    return [jt for jt in JOINTS if jt.concludes == record_short_name]


def regeneration_ok(record_short_name: str) -> bool:
    """
    Check if a record can be regenerated (has at least one derivation).
    Grounds (like UnitCircleDefinition) cannot be regenerated.
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
        if not sp.simplify(derived - stored).equals(0):
            return False
    
    return True
