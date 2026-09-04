import re
from datetime import datetime

from schemas.product import ProductInput
from schemas.inspection import CheckResult


# ============================================================
# PRODUCT NAME
# Rule: TEST001
# Validation type: TEXT_EXISTS
# ============================================================

def check_product_name(product: ProductInput) -> CheckResult:
    """
    Check whether the product name is present.
    """

    if (
        product.product_name is None
        or product.product_name.strip() == ""
    ):
        return CheckResult(
            field="product_name",
            status="FAIL",
            message="Product name is missing",
            rule_id="TEST001"
        )

    return CheckResult(
        field="product_name",
        status="PASS",
        message="Product name is present",
        rule_id="TEST001"
    )


# ============================================================
# MRP
# Rule: LMPC-003
# Validation type: CURRENCY
# ============================================================

def check_mrp(product: ProductInput) -> CheckResult:
    """
    Validate the Maximum Retail Price declaration.
    """

    if (
        product.mrp is None
        or product.mrp.strip() == ""
    ):
        return CheckResult(
            field="mrp",
            status="FAIL",
            message="Maximum Retail Price declaration is missing",
            rule_id="LMPC-003"
        )

    mrp = product.mrp.strip()

    # Accepted examples:
    # ₹50
    # ₹50.99
    # Rs 50
    # Rs. 50
    # INR 50
    # 50

    pattern = r"^(?:₹|Rs\.?|INR)?\s*\d+(?:\.\d{1,2})?$"

    if not re.match(pattern, mrp, re.IGNORECASE):
        return CheckResult(
            field="mrp",
            status="FAIL",
            message="MRP format is invalid",
            rule_id="LMPC-003"
        )

    return CheckResult(
        field="mrp",
        status="PASS",
        message="MRP declaration is present and has a valid currency format",
        rule_id="LMPC-003"
    )


# ============================================================
# NET QUANTITY
# Rule: LMPC-002
# Validation type: QUANTITY
# ============================================================

def check_net_quantity(product: ProductInput) -> CheckResult:
    """
    Validate the net quantity declaration.
    """

    if (
        product.net_quantity is None
        or product.net_quantity.strip() == ""
    ):
        return CheckResult(
            field="net_quantity",
            status="FAIL",
            message="Net quantity declaration is missing",
            rule_id="LMPC-002"
        )

    quantity = product.net_quantity.strip()

    pattern = (
        r"^\d+(?:\.\d+)?\s*"
        r"(mg|g|kg|ml|l|"
        r"milligram|milligrams|"
        r"gram|grams|"
        r"kilogram|kilograms|"
        r"millilitre|millilitres|"
        r"milliliter|milliliters|"
        r"litre|litres|"
        r"liter|liters)$"
    )

    if not re.match(pattern, quantity, re.IGNORECASE):
        return CheckResult(
            field="net_quantity",
            status="FAIL",
            message="Net quantity format is invalid",
            rule_id="LMPC-002"
        )

    return CheckResult(
        field="net_quantity",
        status="PASS",
        message="Net quantity has a valid number and unit",
        rule_id="LMPC-002"
    )


# ============================================================
# MANUFACTURER ADDRESS
# Rule: LMPC-001
# Validation type: ADDRESS
# ============================================================

def check_manufacturer_address(product: ProductInput) -> CheckResult:
    """
    Perform a basic validation of the manufacturer's address.
    """

    if (
        product.manufacturer_address is None
        or product.manufacturer_address.strip() == ""
    ):
        return CheckResult(
            field="manufacturer_address",
            status="FAIL",
            message="Manufacturer address is missing",
            rule_id="LMPC-001"
        )

    address = product.manufacturer_address.strip()

    # Basic sanity checks.
    if len(address) < 10:
        return CheckResult(
            field="manufacturer_address",
            status="FAIL",
            message="Manufacturer address appears incomplete",
            rule_id="LMPC-001"
        )

    # An address should normally contain either
    # a number or a comma separating address components.
    if not re.search(r"\d|,", address):
        return CheckResult(
            field="manufacturer_address",
            status="FAIL",
            message="Manufacturer address appears incomplete",
            rule_id="LMPC-001"
        )

    return CheckResult(
        field="manufacturer_address",
        status="PASS",
        message="Manufacturer address is present and appears sufficiently detailed",
        rule_id="LMPC-001"
    )


# ============================================================
# MANUFACTURER NAME
# ============================================================

def check_manufacturer(product: ProductInput) -> CheckResult:
    """
    Check whether the manufacturer's name is present.
    """

    if (
        product.manufacturer is None
        or product.manufacturer.strip() == ""
    ):
        return CheckResult(
            field="manufacturer",
            status="FAIL",
            message="Manufacturer name is missing",
            rule_id=None
        )

    return CheckResult(
        field="manufacturer",
        status="PASS",
        message="Manufacturer name is present",
        rule_id=None
    )


# ============================================================
# IMPORTER
# ============================================================

def check_importer(product: ProductInput) -> CheckResult:
    """
    Check importer information.

    Importer information is only relevant when the product
    is imported. Until the rule-applicability system is built,
    absence of importer information produces a warning rather
    than an automatic failure.
    """

    if (
        product.importer is None
        or product.importer.strip() == ""
    ):
        return CheckResult(
            field="importer",
            status="WARNING",
            message="Importer information could not be identified; applicability requires review",
            rule_id=None
        )

    return CheckResult(
        field="importer",
        status="PASS",
        message="Importer information is present",
        rule_id=None
    )


# ============================================================
# IMPORTER ADDRESS
# ============================================================

def check_importer_address(product: ProductInput) -> CheckResult:
    """
    Check importer address when importer information exists.
    """

    if (
        product.importer is not None
        and product.importer.strip() != ""
    ):

        if (
            product.importer_address is None
            or product.importer_address.strip() == ""
        ):
            return CheckResult(
                field="importer_address",
                status="FAIL",
                message="Importer address is missing",
                rule_id=None
            )

        address = product.importer_address.strip()

        if len(address) < 10:
            return CheckResult(
                field="importer_address",
                status="FAIL",
                message="Importer address appears incomplete",
                rule_id=None
            )

    return CheckResult(
        field="importer_address",
        status="PASS",
        message="Importer address requirement satisfied",
        rule_id=None
    )


# ============================================================
# COUNTRY OF ORIGIN
# ============================================================

def check_country_of_origin(product: ProductInput) -> CheckResult:
    """
    Check whether country of origin is present.
    """

    if (
        product.country_of_origin is None
        or product.country_of_origin.strip() == ""
    ):
        return CheckResult(
            field="country_of_origin",
            status="FAIL",
            message="Country of origin declaration is missing",
            rule_id=None
        )

    return CheckResult(
        field="country_of_origin",
        status="PASS",
        message="Country of origin declaration is present",
        rule_id=None
    )


# ============================================================
# CUSTOMER CARE / PHONE
# Rule: LMPC-004
# Validation type: PHONE
# ============================================================

def check_customer_care(product: ProductInput) -> CheckResult:
    """
    Validate consumer-care contact information.
    """

    if (
        product.customer_care is None
        or product.customer_care.strip() == ""
    ):
        return CheckResult(
            field="customer_care",
            status="FAIL",
            message="Consumer-care contact information is missing",
            rule_id="LMPC-004"
        )

    phone = product.customer_care.strip()

    # Remove common separators.
    normalized_phone = re.sub(
        r"[\s\-().]",
        "",
        phone
    )

    # Basic Indian mobile number validation.
    # Examples:
    # 9876543210
    # +919876543210

    if not re.fullmatch(
        r"(?:\+91)?[6-9]\d{9}",
        normalized_phone
    ):
        return CheckResult(
            field="customer_care",
            status="FAIL",
            message="Consumer-care phone number format is invalid",
            rule_id="LMPC-004"
        )

    return CheckResult(
        field="customer_care",
        status="PASS",
        message="Consumer-care phone number has a valid format",
        rule_id="LMPC-004"
    )


# ============================================================
# DATE DECLARATION
# Rule: LMPC-005
# Validation type: DATE
# ============================================================

def check_date(product: ProductInput) -> CheckResult:
    """
    Validate manufacturing or expiry date declarations.
    """

    dates = [
        product.manufacturing_date,
        product.expiry_date
    ]

    dates = [
        value.strip()
        for value in dates
        if value is not None and value.strip() != ""
    ]

    if not dates:
        return CheckResult(
            field="date_declaration",
            status="FAIL",
            message="Date declaration is missing",
            rule_id="LMPC-005"
        )

    accepted_formats = [
        "%d/%m/%Y",
        "%m/%Y",
        "%d-%m-%Y",
        "%m-%Y",
        "%d/%m/%y",
        "%d-%m-%y",
    ]

    for date_value in dates:

        valid = False

        for date_format in accepted_formats:

            try:
                datetime.strptime(
                    date_value,
                    date_format
                )

                valid = True
                break

            except ValueError:
                continue

        if not valid:
            return CheckResult(
                field="date_declaration",
                status="FAIL",
                message=f"Invalid date format: {date_value}",
                rule_id="LMPC-005"
            )

    return CheckResult(
        field="date_declaration",
        status="PASS",
        message="Date declaration has a recognized format",
        rule_id="LMPC-005"
    )