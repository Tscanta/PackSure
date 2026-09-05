from schemas.product import ProductInput

from backend.inspection.result import CheckResult

from backend.inspection.validator import (
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


FIELD_VALIDATORS = {

    "product_name": check_product_name,

    "mrp": check_mrp,

    "net_quantity": check_net_quantity,

    "manufacturer": check_manufacturer,

    "manufacturer_address": check_manufacturer_address,

    "importer": check_importer,

    "importer_address": check_importer_address,

    "country_of_origin": check_country_of_origin,

    "customer_care": check_customer_care,

    "customer_care_phone": check_customer_care,

    "date_declaration": check_date,

    "manufacturing_date": check_date,

    "packaging_date": check_date,

    "expiry_date": check_date,

    "best_before": check_date,

    "use_by": check_date,

    "fssai_license_number": check_fssai_license,

    "fssai_license_no": check_fssai_license,

    "lot_number": check_lot_batch,

    "batch_number": check_lot_batch,

    "lot_code": check_lot_batch,

    "lot_batch": check_lot_batch,

    "ingredients": check_ingredients,

    "ingredient_list": check_ingredients,

    "nutrition": check_nutrition,

    "nutrition_facts": check_nutrition,

    "veg_nonveg_symbol": check_veg_nonveg_symbol,

    "food_symbol": check_veg_nonveg_symbol,
}


TYPE_VALIDATORS = {

    "CURRENCY": check_mrp,

    "QUANTITY": check_net_quantity,

    "NUMBER_UNIT": check_net_quantity,

    "ADDRESS": check_manufacturer_address,

    "CONTACT": check_customer_care,

    "PHONE": check_customer_care,

    "DATE": check_date,

    "FSSAI_LICENSE": check_fssai_license,

    "LICENSE_NUMBER": check_fssai_license,

    "LOT": check_lot_batch,

    "BATCH": check_lot_batch,

    "LOT_BATCH": check_lot_batch,

    "INGREDIENTS": check_ingredients,

    "NUTRITION": check_nutrition,

    "VEG_NONVEG": check_veg_nonveg_symbol,

    "FOOD_SYMBOL": check_veg_nonveg_symbol,

    "VISUAL_REVIEW": check_visual_review,

    "FONT_HEIGHT": check_visual_review,

    "LETTER_PROPORTION": check_visual_review,

    "PDP_PLACEMENT": check_visual_review,

    "CLEAR_SPACE": check_visual_review,

    "VISUAL_LEGIBILITY": check_visual_review,
}


def validate_rule(
    product: ProductInput,
    rule: dict
) -> CheckResult:

    rule_id = rule.get("rule_id")

    field = str(
        rule.get("field") or ""
    ).strip().lower()

    validation_type = str(
        rule.get("validation_type") or ""
    ).strip().upper()

    # --------------------------------------------------------
    # FIELD FIRST
    # --------------------------------------------------------

    validator = FIELD_VALIDATORS.get(
        field
    )

    # --------------------------------------------------------
    # VALIDATION TYPE SECOND
    # --------------------------------------------------------

    if validator is None:

        validator = TYPE_VALIDATORS.get(
            validation_type
        )

    # --------------------------------------------------------
    # NO AUTOMATIC CHECK
    # --------------------------------------------------------

    if validator is None:

        result = check_not_automatable(
            product
        )

        return result.model_copy(
            update={
                "field": field or "rule",
                "rule_id": rule_id,
                "severity": rule.get("severity"),
                "mandatory": bool(
                    rule.get("mandatory", False)
                ),
            }
        )

    # --------------------------------------------------------
    # EXECUTE
    # --------------------------------------------------------

    result = validator(
        product
    )

    # --------------------------------------------------------
    # ATTACH RULE METADATA
    # --------------------------------------------------------

    return result.model_copy(
        update={
            "field": field or result.field,
            "rule_id": rule_id or result.rule_id,
            "severity": rule.get("severity"),
            "mandatory": bool(
                rule.get("mandatory", False)
            ),
        }
    )