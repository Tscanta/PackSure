import re
from numbers import Number
from typing import Any

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


# Structured operators are intentionally small and deterministic.  Legacy
# validation_type rules above remain supported for the imported rule dataset.
SUPPORTED_OPERATORS = {"REQUIRED", "EQUALS", "IN", "REGEX", "MIN", "MAX", "CONTAINS"}


def _read(rule: Any, name: str, default=None):
    return rule.get(name, default) if isinstance(rule, dict) else getattr(rule, name, default)


def _product_value(product: Any, field: str):
    return product.get(field) if isinstance(product, dict) else getattr(product, field, None)


def _empty(value: Any) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def _number(value: Any) -> float | None:
    if isinstance(value, Number) and not isinstance(value, bool):
        return float(value)
    if isinstance(value, str):
        match = re.search(r"[-+]?\d+(?:\.\d+)?", value.replace(",", ""))
        if match:
            try:
                return float(match.group())
            except ValueError:
                return None
    return None


def evaluate_rule(product: Any, rule: Any) -> CheckResult:
    """Evaluate a stored structured rule, falling back to legacy validators."""
    operator = str(_read(rule, "operator") or _read(rule, "validation_type") or "").strip().upper()
    field = str(_read(rule, "field") or "").strip()
    if operator not in SUPPORTED_OPERATORS or not field:
        # The existing database does not yet store field/operator constraints.
        # Its validation_type remains a deterministic technical mapping.
        return validate_rule(product, rule)

    applicability = _read(rule, "applicability")
    if isinstance(applicability, dict):
        for applicability_field, expected in applicability.items():
            allowed = expected if isinstance(expected, (list, tuple, set)) else [expected]
            if _product_value(product, applicability_field) not in allowed:
                return CheckResult(field=field, status="NOT_APPLICABLE", message="Rule does not apply to this product.", rule_id=_read(rule, "rule_id"), severity=_read(rule, "severity"), mandatory=bool(_read(rule, "mandatory", False)), database_rule_id=_read(rule, "id"))

    actual = _product_value(product, field)
    expected = _read(rule, "value", _read(rule, "expected_value"))
    passed, error = False, None
    if operator == "REQUIRED":
        passed, expected = not _empty(actual), expected if expected is not None else "a non-empty value"
    elif _empty(actual):
        error = "Product field is missing."
    elif operator == "EQUALS":
        passed = str(actual).strip().casefold() == str(expected).strip().casefold()
    elif operator == "IN":
        allowed = expected if isinstance(expected, (list, tuple, set)) else [expected]
        passed = any(str(actual).strip().casefold() == str(item).strip().casefold() for item in allowed)
    elif operator == "REGEX":
        try:
            passed = re.search(str(expected), str(actual)) is not None
        except re.error:
            error = "Stored rule has an invalid regular expression."
    elif operator in {"MIN", "MAX"}:
        actual_number, expected_number = _number(actual), _number(expected)
        if actual_number is None or expected_number is None:
            error = "A numeric value is required for this rule."
        else:
            passed = actual_number >= expected_number if operator == "MIN" else actual_number <= expected_number
    elif operator == "CONTAINS":
        values = actual if isinstance(actual, (list, tuple, set)) else [actual]
        passed = any(str(expected).casefold() in str(item).casefold() for item in values)

    return CheckResult(field=field, status="PASS" if passed else "FAIL", message="Rule satisfied." if passed else (error or "Value does not satisfy the stored rule condition."), rule_id=_read(rule, "rule_id"), severity=_read(rule, "severity"), mandatory=bool(_read(rule, "mandatory", False)), detected_value=None if actual is None else str(actual), expected_value=None if expected is None else str(expected), database_rule_id=_read(rule, "id"))
