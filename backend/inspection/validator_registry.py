"""
Validator registry.

Maps validation_type values from the rule dataset
to technical validation functions.

IMPORTANT:
The registry defines HOW a rule can be checked.

The legal requirement itself comes from the rule dataset.
"""

from backend.inspection.rule import (
    check_product_name,
    check_mrp,
    check_net_quantity,
    check_manufacturer,
    check_manufacturer_address,
    check_importer,
    check_importer_address,
    check_country_of_origin,
    check_customer_care,
    check_date,
    check_fssai_license,
    check_lot_batch,
    check_ingredients,
    check_nutrition,
    check_veg_nonveg_symbol,
    check_visual_review,
    check_not_automatable,
)


# ============================================================
# AUTOMATED VALIDATORS
# ============================================================

VALIDATOR_REGISTRY = {

    # --------------------------------------------------------
    # LEGAL METROLOGY
    # --------------------------------------------------------

    "TEXT_EXISTS": check_product_name,

    "CURRENCY": check_mrp,

    "QUANTITY": check_net_quantity,

    "ADDRESS": check_manufacturer_address,

    "PHONE": check_customer_care,

    "CONTACT": check_customer_care,

    "DATE": check_date,

    "NUMBER_UNIT": check_net_quantity,

    # --------------------------------------------------------
    # FSSAI
    # --------------------------------------------------------

    "FSSAI_LICENSE": check_fssai_license,

    "LICENSE_NUMBER": check_fssai_license,

    "LOT": check_lot_batch,

    "BATCH": check_lot_batch,

    "LOT_BATCH": check_lot_batch,

    "INGREDIENTS": check_ingredients,

    "NUTRITION": check_nutrition,

    "VEG_NONVEG": check_veg_nonveg_symbol,

    "FOOD_SYMBOL": check_veg_nonveg_symbol,

    # --------------------------------------------------------
    # GENERIC TEXT
    # --------------------------------------------------------

    "MANUFACTURER": check_manufacturer,

    "IMPORTER": check_importer,

    "COUNTRY_OF_ORIGIN": check_country_of_origin,

    # --------------------------------------------------------
    # VISUAL
    # --------------------------------------------------------

    "FONT_HEIGHT": check_visual_review,

    "LETTER_PROPORTION": check_visual_review,

    "PDP_PLACEMENT": check_visual_review,

    "CLEAR_SPACE": check_visual_review,

    "VISUAL_LEGIBILITY": check_visual_review,

    "VISUAL_REVIEW": check_visual_review,

    # --------------------------------------------------------
    # CONTEXTUAL / NOT AUTOMATABLE
    # --------------------------------------------------------

    "APPLICABILITY": check_not_automatable,

    "STANDARD_PACK_SIZE": check_not_automatable,

    "SPECIAL_CATEGORY": check_not_automatable,

    "SPECIAL_UNIT": check_not_automatable,

    "QUALIFIER_APPLICABILITY": check_not_automatable,

    "DECLARATION_SET": check_not_automatable,

    "PHYSICAL_QUANTITY": check_not_automatable,

    "PHYSICAL_TEST": check_not_automatable,

    "LOT_TEST": check_not_automatable,

    "MPE_CALCULATION": check_not_automatable,

    "SAMPLE_SIZE": check_not_automatable,

    "PRICE_COMPARISON": check_not_automatable,

    "FORBIDDEN_WORDS": check_not_automatable,

    "LANGUAGE": check_not_automatable,

}


# ============================================================
# REGISTRY HELPERS
# ============================================================

def get_validator(validation_type: str):
    """
    Return the validator for a given validation type.

    Returns None when the validation type is not supported.
    """

    if not validation_type:
        return None

    return VALIDATOR_REGISTRY.get(
        validation_type.upper().strip()
    )


def is_supported(validation_type: str) -> bool:
    """
    Check whether a validation type is supported.
    """

    return get_validator(validation_type) is not None