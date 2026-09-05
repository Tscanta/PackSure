"""
PackSho Inspection Validators

This module contains the technical validation functions used by
the PackSho compliance inspection system.

IMPORTANT:
- Legal requirements are stored in the rule dataset / Supabase.
- This module contains HOW a detected product value is checked.
- It does not hard-code the complete legal rule database.
"""

import re
from typing import Any

from backend.inspection.result import CheckResult


# ============================================================
# GENERIC HELPERS
# ============================================================

def _get_value(product: Any, *field_names: str) -> Any:
    """Return the first non-empty value found on a product object/dict."""

    for field_name in field_names:

        if isinstance(product, dict):
            value = product.get(field_name)
        else:
            value = getattr(product, field_name, None)

        if value is not None and str(value).strip() != "":
            return value

    return None


def _text(value: Any) -> str:
    """Convert a value to clean text."""

    if value is None:
        return ""

    return str(value).strip()


def _result(
    field: str,
    status: str,
    message: str,
    *,
    rule_id: str | None = None,
    severity: str | None = None,
    mandatory: bool = False,
    detected_value: Any = None,
    expected_value: Any = None,
    confidence: float | None = None,
    evidence: str | None = None,
) -> CheckResult:

    return CheckResult(
        field=field,
        status=status,
        message=message,
        rule_id=rule_id,
        severity=severity,
        mandatory=mandatory,
        detected_value=None if detected_value is None else str(detected_value),
        expected_value=None if expected_value is None else str(expected_value),
        confidence=confidence,
        evidence=evidence,
    )


# ============================================================
# PRODUCT NAME
# ============================================================

def check_product_name(product: Any) -> CheckResult:

    value = _get_value(product, "product_name")

    if not value:
        return _result(
            "product_name",
            "FAIL",
            "Product name is missing.",
            severity="HIGH",
            mandatory=True,
        )

    return _result(
        "product_name",
        "PASS",
        "Product name is present.",
        severity="HIGH",
        mandatory=True,
        detected_value=value,
    )


# ============================================================
# MRP
# ============================================================

def check_mrp(product: Any) -> CheckResult:

    value = _get_value(product, "mrp")

    if value is None:
        return _result(
            "mrp",
            "FAIL",
            "MRP is missing.",
            severity="HIGH",
            mandatory=True,
        )

    text = _text(value)

    if not re.search(r"\d", text):
        return _result(
            "mrp",
            "FAIL",
            "MRP does not contain a recognizable numeric value.",
            severity="HIGH",
            mandatory=True,
            detected_value=text,
        )

    return _result(
        "mrp",
        "PASS",
        "MRP is present.",
        severity="HIGH",
        mandatory=True,
        detected_value=text,
    )


# ============================================================
# NET QUANTITY
# ============================================================

def check_net_quantity(product: Any) -> CheckResult:

    value = _get_value(
        product,
        "net_quantity",
        "package_size",
    )

    if value is None:
        return _result(
            "net_quantity",
            "FAIL",
            "Net quantity is missing.",
            severity="HIGH",
            mandatory=True,
        )

    text = _text(value)

    if not re.search(r"\d", text):
        return _result(
            "net_quantity",
            "FAIL",
            "Net quantity does not contain a recognizable numeric value.",
            severity="HIGH",
            mandatory=True,
            detected_value=text,
        )

    return _result(
        "net_quantity",
        "PASS",
        "Net quantity is present.",
        severity="HIGH",
        mandatory=True,
        detected_value=text,
    )


# ============================================================
# MANUFACTURER
# ============================================================

def check_manufacturer(product: Any) -> CheckResult:

    value = _get_value(
        product,
        "manufacturer",
        "brand_owner",
    )

    if not value:
        return _result(
            "manufacturer",
            "FAIL",
            "Manufacturer or brand-owner information is missing.",
            severity="HIGH",
            mandatory=True,
        )

    return _result(
        "manufacturer",
        "PASS",
        "Manufacturer/brand-owner information is present.",
        severity="HIGH",
        mandatory=True,
        detected_value=value,
    )


# ============================================================
# MANUFACTURER ADDRESS
# ============================================================

def check_manufacturer_address(product: Any) -> CheckResult:

    value = _get_value(
        product,
        "manufacturer_address",
        "brand_owner_address",
        "address",
    )

    if not value:
        return _result(
            "manufacturer_address",
            "FAIL",
            "Manufacturer/brand-owner address is missing.",
            severity="HIGH",
            mandatory=True,
        )

    return _result(
        "manufacturer_address",
        "PASS",
        "Manufacturer/brand-owner address is present.",
        severity="HIGH",
        mandatory=True,
        detected_value=value,
    )


# ============================================================
# IMPORTER
# ============================================================

def check_importer(product: Any) -> CheckResult:

    is_imported = _get_value(product, "is_imported")
    importer = _get_value(product, "importer")

    if is_imported in (False, "False", "false", 0):
        return _result(
            "importer",
            "NOT_APPLICABLE",
            "Importer information is not applicable to a non-imported product.",
            mandatory=False,
        )

    if not importer:
        return _result(
            "importer",
            "REVIEW",
            "Importer information could not be confirmed from the extracted data.",
            severity="HIGH",
            mandatory=True,
        )

    return _result(
        "importer",
        "PASS",
        "Importer information is present.",
        severity="HIGH",
        mandatory=True,
        detected_value=importer,
    )


# ============================================================
# IMPORTER ADDRESS
# ============================================================

def check_importer_address(product: Any) -> CheckResult:

    is_imported = _get_value(product, "is_imported")

    if is_imported in (False, "False", "false", 0):
        return _result(
            "importer_address",
            "NOT_APPLICABLE",
            "Importer address is not applicable to a non-imported product.",
        )

    value = _get_value(
        product,
        "importer_address",
    )

    if not value:
        return _result(
            "importer_address",
            "REVIEW",
            "Importer address could not be confirmed from the extracted data.",
            severity="HIGH",
            mandatory=True,
        )

    return _result(
        "importer_address",
        "PASS",
        "Importer address is present.",
        severity="HIGH",
        mandatory=True,
        detected_value=value,
    )


# ============================================================
# COUNTRY OF ORIGIN
# ============================================================

def check_country_of_origin(product: Any) -> CheckResult:

    is_imported = _get_value(product, "is_imported")
    value = _get_value(product, "country_of_origin")

    if is_imported in (False, "False", "false", 0):
        return _result(
            "country_of_origin",
            "NOT_APPLICABLE",
            "Country-of-origin declaration is not being evaluated as an imported-product requirement.",
        )

    if not value:
        return _result(
            "country_of_origin",
            "FAIL",
            "Country of origin is missing for an imported product.",
            severity="HIGH",
            mandatory=True,
        )

    return _result(
        "country_of_origin",
        "PASS",
        "Country of origin is present.",
        severity="HIGH",
        mandatory=True,
        detected_value=value,
    )


# ============================================================
# CUSTOMER CARE
# ============================================================

def check_customer_care(product: Any) -> CheckResult:

    value = _get_value(
        product,
        "customer_care",
        "customer_care_phone",
        "customer_care_email",
        "customer_care_address",
    )

    if not value:
        return _result(
            "customer_care",
            "FAIL",
            "Consumer/customer-care information is missing.",
            severity="MEDIUM",
            mandatory=True,
        )

    return _result(
        "customer_care",
        "PASS",
        "Customer-care information is present.",
        severity="MEDIUM",
        mandatory=True,
        detected_value=value,
    )


# ============================================================
# DATE
# ============================================================

def check_date(product: Any) -> CheckResult:

    fields = [
        "manufacturing_date",
        "packaging_date",
        "expiry_date",
        "best_before",
        "use_by",
    ]

    found = []

    for field in fields:
        value = _get_value(product, field)

        if value:
            found.append(f"{field}: {value}")

    if not found:
        return _result(
            "date",
            "REVIEW",
            "No recognizable date marking was extracted from the product.",
            severity="HIGH",
            mandatory=True,
        )

    return _result(
        "date",
        "PASS",
        "At least one product date marking was detected.",
        severity="HIGH",
        mandatory=True,
        detected_value="; ".join(found),
    )


# ============================================================
# FSSAI LICENSE
# ============================================================

def check_fssai_license(product: Any) -> CheckResult:

    value = _get_value(
        product,
        "fssai_license_number",
        "fssai_license_no",
        "fssai_registration_number",
    )

    if not value:

        return _result(
            "fssai_license_number",
            "FAIL",
            "FSSAI license/registration number is missing.",
            severity="HIGH",
            mandatory=True,
        )

    text = _text(value)

    digits = "".join(ch for ch in text if ch.isdigit())

    if len(digits) != 14:

        return _result(
            "fssai_license_number",
            "FAIL",
            "FSSAI license/registration number should contain 14 digits.",
            severity="HIGH",
            mandatory=True,
            detected_value=text,
            expected_value="14-digit FSSAI number",
        )

    return _result(
        "fssai_license_number",
        "PASS",
        "FSSAI license/registration number is present and has 14 digits.",
        severity="HIGH",
        mandatory=True,
        detected_value=text,
        expected_value="14-digit FSSAI number",
    )


# ============================================================
# LOT / BATCH
# ============================================================

def check_lot_batch(product: Any) -> CheckResult:

    value = _get_value(
        product,
        "lot_number",
        "batch_number",
        "lot_code",
    )

    if not value:
        return _result(
            "lot_batch",
            "FAIL",
            "Lot/batch identification is missing.",
            severity="MEDIUM",
            mandatory=True,
        )

    return _result(
        "lot_batch",
        "PASS",
        "Lot/batch identification is present.",
        severity="MEDIUM",
        mandatory=True,
        detected_value=value,
    )


# ============================================================
# INGREDIENTS
# ============================================================

def check_ingredients(product: Any) -> CheckResult:

    value = _get_value(
        product,
        "ingredients",
        "ingredient_list",
    )

    if not value:
        return _result(
            "ingredients",
            "FAIL",
            "Ingredient information is missing.",
            severity="HIGH",
            mandatory=True,
        )

    return _result(
        "ingredients",
        "PASS",
        "Ingredient information is present.",
        severity="HIGH",
        mandatory=True,
        detected_value=value,
    )


# ============================================================
# NUTRITION
# ============================================================

def check_nutrition(product: Any) -> CheckResult:

    value = _get_value(
        product,
        "nutrition",
        "nutrition_facts",
    )

    nutrition_fields = [
        "energy",
        "protein",
        "carbohydrate",
        "total_sugars",
        "added_sugars",
        "total_fat",
        "saturated_fat",
        "trans_fat",
        "cholesterol",
        "sodium",
        "dietary_fibre",
    ]

    detected = []

    if value:
        detected.append(str(value))

    for field in nutrition_fields:
        field_value = _get_value(product, field)

        if field_value is not None:
            detected.append(f"{field}: {field_value}")

    if not detected:
        return _result(
            "nutrition",
            "FAIL",
            "Nutrition information was not detected.",
            severity="HIGH",
            mandatory=True,
        )

    return _result(
        "nutrition",
        "PASS",
        "Nutrition information is present in the extracted product data.",
        severity="HIGH",
        mandatory=True,
        detected_value="; ".join(detected),
    )


# ============================================================
# VEGETARIAN / NON-VEGETARIAN SYMBOL
# ============================================================

def check_veg_nonveg_symbol(product: Any) -> CheckResult:

    value = _get_value(
        product,
        "veg_nonveg_symbol",
        "food_symbol",
        "vegetarian",
        "non_vegetarian",
    )

    if value is None:
        return _result(
            "veg_nonveg_symbol",
            "REVIEW",
            "Vegetarian/non-vegetarian declaration could not be confirmed automatically.",
            severity="HIGH",
            mandatory=True,
        )

    return _result(
        "veg_nonveg_symbol",
        "PASS",
        "Vegetarian/non-vegetarian declaration information was detected.",
        severity="HIGH",
        mandatory=True,
        detected_value=value,
    )


# ============================================================
# VISUAL REVIEW
# ============================================================

def check_visual_review(product: Any) -> CheckResult:

    return _result(
        "visual_review",
        "REVIEW",
        "This requirement requires visual/image inspection and cannot be reliably confirmed from structured text alone.",
        severity="MEDIUM",
        mandatory=True,
    )


# ============================================================
# NOT AUTOMATABLE
# ============================================================

def check_not_automatable(product: Any) -> CheckResult:

    return _result(
        "manual_review",
        "REVIEW",
        "This requirement requires additional context, calculation, physical inspection, or manual verification.",
        severity="MEDIUM",
        mandatory=True,
    )


# ============================================================
# PUBLIC EXPORTS
# ============================================================

__all__ = [
    "check_product_name",
    "check_mrp",
    "check_net_quantity",
    "check_manufacturer",
    "check_manufacturer_address",
    "check_importer",
    "check_importer_address",
    "check_country_of_origin",
    "check_customer_care",
    "check_date",
    "check_fssai_license",
    "check_lot_batch",
    "check_ingredients",
    "check_nutrition",
    "check_veg_nonveg_symbol",
    "check_visual_review",
    "check_not_automatable",
]