"""
Pavement Design Calculator
---------------------------
A small Python tool that estimates flexible pavement layer thicknesses
(surface, base, sub-base) using a simplified version of the
AASHTO 1993 empirical method.

Inputs:
    - ESAL   : Equivalent Single Axle Load (design traffic, in millions)
    - CBR    : California Bearing Ratio of the subgrade soil (%)
    - SN_target : target Structural Number (can be computed or given)

Outputs:
    - Required Structural Number (SN)
    - Suggested thickness for each layer (cm)
    - A chart showing how layer thickness changes with traffic load
"""

import math


# --- Layer coefficients (typical values, AASHTO) ---
A1 = 0.44  # surface course (asphalt concrete) coefficient per cm
A2 = 0.14  # base course (granular) coefficient per cm
A3 = 0.11  # sub-base course coefficient per cm


def subgrade_resilient_modulus(cbr):
    """Estimate subgrade resilient modulus (MPa) from CBR (simplified)."""
    return 10.3 * cbr  # common approximation: MR(MPa) ~ 10.3 * CBR


def required_structural_number(esal_millions, cbr, reliability=0.90):
    """
    Very simplified structural number estimate.
    This is NOT the full AASHTO nomograph equation, but a compact
    approximation useful for teaching / portfolio purposes:
    SN grows with log(traffic) and shrinks with stronger subgrade (CBR).
    """
    mr = subgrade_resilient_modulus(cbr)
    reliability_factor = 1 + (reliability - 0.75) * 0.8  # mild adjustment
    sn = 1.5 * math.log10(esal_millions * 1e6) / math.log10(mr) * reliability_factor
    return max(sn, 1.0)


def layer_thicknesses(sn):
    """
    Split the required Structural Number (SN) into three layers
    using typical proportion rules: 35% surface, 35% base, 30% sub-base.
    Returns thickness in cm for each layer.
    """
    sn_surface = 0.35 * sn
    sn_base = 0.35 * sn
    sn_subbase = 0.30 * sn

    t_surface = sn_surface / A1
    t_base = sn_base / A2
    t_subbase = sn_subbase / A3

    return {
        "surface_cm": round(t_surface, 1),
        "base_cm": round(t_base, 1),
        "subbase_cm": round(t_subbase, 1),
        "total_cm": round(t_surface + t_base + t_subbase, 1),
    }


def design_pavement(esal_millions, cbr, reliability=0.90):
    sn = required_structural_number(esal_millions, cbr, reliability)
    layers = layer_thicknesses(sn)
    return {
        "ESAL_millions": esal_millions,
        "CBR": cbr,
        "SN": round(sn, 2),
        **layers,
    }


if __name__ == "__main__":
    # Example run
    result = design_pavement(esal_millions=5, cbr=6, reliability=0.90)
    print("Pavement Design Result")
    print("-----------------------")
    for k, v in result.items():
        print(f"{k:15s}: {v}")
