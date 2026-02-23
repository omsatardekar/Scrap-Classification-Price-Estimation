from difflib import get_close_matches

from .base_prices import BASE_PRICES
from .modifiers import (
    confidence_factor,
    weight_slab_factor,
    impurity_penalty,
    market_factor,
)

# --------------------------------
# MATERIAL NORMALIZATION LAYER
# --------------------------------

MATERIAL_ALIAS = {
    # steel variants
    "stainless steel": "stainless_steel",
    "ss steel": "stainless_steel",
    "metal alloy": "stainless_steel",
    "alloy steel": "stainless_steel",
    "steel alloy": "stainless_steel",

    # iron / mild steel
    "mild steel": "iron",
    "ms steel": "iron",

    # aluminium variants
    "aluminium": "aluminum",
    "alu": "aluminum",

    # e-waste naming
    "e-waste": "ewaste",
    "electronic waste": "ewaste",
}

DEFAULT_PRICE_PER_KG = 20


def normalize_material(material: str) -> str:
    material = material.lower().strip()

    if material in BASE_PRICES:
        return material

    if material in MATERIAL_ALIAS:
        return MATERIAL_ALIAS[material]

    # fuzzy match (handles small typos / variations)
    match = get_close_matches(
        material,
        BASE_PRICES.keys(),
        n=1,
        cutoff=0.6
    )
    if match:
        return match[0]

    return "unknown"


# --------------------------------
# MAIN PRICE ESTIMATION ENGINE
# --------------------------------

def estimate_price(material: str, weight: float, confidence: float):
    original_material = material
    normalized_material = normalize_material(material)

    # base price
    base_price = BASE_PRICES.get(
        normalized_material,
        DEFAULT_PRICE_PER_KG
    )

    base_amount = base_price * weight

    # modifiers
    conf_factor = confidence_factor(confidence)
    slab_factor = weight_slab_factor(weight)
    impurity_factor = impurity_penalty(normalized_material)
    market = market_factor()

    final_price = (
        base_amount
        * conf_factor
        * slab_factor
        * impurity_factor
        * market
    )

    breakdown = [
        {
            "label": "Material Type",
            "value": normalized_material.replace("_", " ").title(),
            "amount": f"₹ {base_price}/kg",
        },
        {
            "label": "AI Prediction",
            "value": original_material,
            "amount": "Normalized intelligently",
        },
        {
            "label": "Base Amount",
            "value": f"{weight} kg × ₹ {base_price}",
            "amount": round(base_amount, 2),
        },
        {
            "label": "Confidence Adjustment",
            "value": f"{int((conf_factor - 1) * 100)}%",
            "amount": round(base_amount * (conf_factor - 1), 2),
        },
        {
            "label": "Weight Slab Adjustment",
            "value": f"{int((slab_factor - 1) * 100)}%",
            "amount": round(base_amount * (slab_factor - 1), 2),
        },
        {
            "label": "Impurity Penalty",
            "value": f"{int((impurity_factor - 1) * 100)}%",
            "amount": round(base_amount * (impurity_factor - 1), 2),
        },
        {
            "label": "Market Adjustment",
            "value": f"{int((market - 1) * 100)}%",
            "amount": round(base_amount * (market - 1), 2),
        },
    ]

    return {
        "estimated_price": round(final_price, 2),
        "breakdown": breakdown,
    }
