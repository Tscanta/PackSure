import re

from schemas.product import ProductInput
from schemas.inspection import CheckResult


# ============================================================
# PRODUCT NAME
# ============================================================

def check_product_name(product: ProductInput) -> CheckResult:

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
# ============================================================

def check_mrp(product: ProductInput) -> CheckResult:

    if product.mrp is None or product.mrp.strip() == "":
        return CheckResult(
            field="mrp",
            status="FAIL",
            message="MRP is missing",
            rule_id="LMPC-003"
        )

    mrp = product.mrp.strip()

    normalized_mrp = re.sub(
        r"[₹RsINR\s]",
        "",
        mrp,
        flags=re.IGNORECASE
    )

    if not re.fullmatch(
        r"\d+(?:\.\d+)?",
        normalized_mrp
    ):
        return CheckResult(
            field="mrp",
            status="FAIL",
            message="MRP format is invalid",
            rule_id="LMPC-003"
        )

    return CheckResult(
        field="mrp",
        status="PASS",
        message="MRP is present and has a valid numeric format",
        rule_id="LMPC-003"
    )


# ============================================================
# NET QUANTITY
# ============================================================

def check_net_quantity(product: ProductInput) -> CheckResult:

    if (
        product.net_quantity is None
        or product.net_quantity.strip() == ""
    ):
        return CheckResult(
            field="net_quantity",
            status="FAIL",
            message="Net quantity is missing",
            rule_id="LMPC-002"
        )

    quantity = product.net_quantity.strip()

    if not re.fullmatch(
        r"\d+(?:\.\d+)?\s*(?:mg|g|kg|ml|l)",
        quantity,
        re.IGNORECASE
    ):
        return CheckResult(
            field="net_quantity",
            status="FAIL",
            message="Net quantity format is invalid",
            rule_id="LMPC-002"
        )

    return CheckResult(
        field="net_quantity",
        status="PASS",
        message="Net quantity is present and has a valid format",
        rule_id="LMPC-002"
    )


# ============================================================
# MANUFACTURER
# ============================================================

def check_manufacturer(product: ProductInput) -> CheckResult:

    if (
        product.manufacturer is None
        or product.manufacturer.strip() == ""
    ):
        return CheckResult(
            field="manufacturer",
            status="FAIL",
            message="Manufacturer name is missing",
            rule_id="LMPC-MANUFACTURER"
        )

    return CheckResult(
        field="manufacturer",
        status="PASS",
        message="Manufacturer name is present",
        rule_id="LMPC-MANUFACTURER"
    )


# ============================================================
# MANUFACTURER ADDRESS
# ============================================================

def check_manufacturer_address(
    product: ProductInput
) -> CheckResult:

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

    if len(address) < 10:
        return CheckResult(
            field="manufacturer_address",
            status="FAIL",
            message="Manufacturer address appears incomplete",
            rule_id="LMPC-001"
        )

    if not re.search(r"\d|,", address):
        return CheckResult(
            field="manufacturer_address",
            status="FAIL",
            message="Manufacturer address format appears invalid",
            rule_id="LMPC-001"
        )

    return CheckResult(
        field="manufacturer_address",
        status="PASS",
        message="Manufacturer address is present",
        rule_id="LMPC-001"
    )


# ============================================================
# IMPORTER
# ============================================================

def check_importer(product: ProductInput) -> CheckResult:

    if (
        product.importer is None
        or product.importer.strip() == ""
    ):
        return CheckResult(
            field="importer",
            status="FAIL",
            message="Importer or marketer information is missing",
            rule_id="LMPC-IMPORTER"
        )

    return CheckResult(
        field="importer",
        status="PASS",
        message="Importer or marketer information is present",
        rule_id="LMPC-IMPORTER"
    )


# ============================================================
# IMPORTER ADDRESS
# ============================================================

def check_importer_address(
    product: ProductInput
) -> CheckResult:

    if (
        product.importer_address is None
        or product.importer_address.strip() == ""
    ):
        return CheckResult(
            field="importer_address",
            status="FAIL",
            message="Importer address is missing",
            rule_id="LMPC-IMPORTER-ADDRESS"
        )

    address = product.importer_address.strip()

    if len(address) < 10:
        return CheckResult(
            field="importer_address",
            status="FAIL",
            message="Importer address appears incomplete",
            rule_id="LMPC-IMPORTER-ADDRESS"
        )

    if not re.search(r"\d|,", address):
        return CheckResult(
            field="importer_address",
            status="FAIL",
            message="Importer address format appears invalid",
            rule_id="LMPC-IMPORTER-ADDRESS"
        )

    return CheckResult(
        field="importer_address",
        status="PASS",
        message="Importer address is present",
        rule_id="LMPC-IMPORTER-ADDRESS"
    )


# ============================================================
# COUNTRY OF ORIGIN
# ============================================================

def check_country_of_origin(
    product: ProductInput
) -> CheckResult:

    if (
        product.country_of_origin is None
        or product.country_of_origin.strip() == ""
    ):
        return CheckResult(
            field="country_of_origin",
            status="FAIL",
            message="Country of origin is missing",
            rule_id="LMPC-COUNTRY"
        )

    return CheckResult(
        field="country_of_origin",
        status="PASS",
        message="Country of origin is present",
        rule_id="LMPC-COUNTRY"
    )


# ============================================================
# CUSTOMER CARE
# ============================================================

def check_customer_care(
    product: ProductInput
) -> CheckResult:
    """
    Accepts Indian mobile and 1800 toll-free numbers.
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

    normalized_phone = re.sub(
        r"[\s\-().]",
        "",
        phone
    )

    mobile_pattern = r"(?:\+91)?[6-9]\d{9}"

    toll_free_pattern = r"1800\d{7}"

    if not (
        re.fullmatch(
            mobile_pattern,
            normalized_phone
        )
        or
        re.fullmatch(
            toll_free_pattern,
            normalized_phone
        )
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
        message="Consumer-care contact has a recognized Indian phone format",
        rule_id="LMPC-004"
    )


# ============================================================
# DATE
# ============================================================

def check_date(product: ProductInput) -> CheckResult:

    date_value = None

    if (
        product.manufacturing_date
        and product.manufacturing_date.strip()
    ):
        date_value = product.manufacturing_date.strip()

    elif (
        product.expiry_date
        and product.expiry_date.strip()
    ):
        date_value = product.expiry_date.strip()

    if not date_value:
        return CheckResult(
            field="date_declaration",
            status="FAIL",
            message="Manufacturing or expiry date is missing",
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

    from datetime import datetime

    for date_format in accepted_formats:

        try:
            datetime.strptime(
                date_value,
                date_format
            )

            return CheckResult(
                field="date_declaration",
                status="PASS",
                message="Date declaration has a recognized format",
                rule_id="LMPC-005"
            )

        except ValueError:
            continue

    return CheckResult(
        field="date_declaration",
        status="FAIL",
        message="Date declaration format is invalid",
        rule_id="LMPC-005"
    )