from backend.database.models import Product, Rule, Inspection
from backend.database.models import Product, Rule
from backend.database.models import Product, Rule, Inspection
from backend.database.queries import (
    get_all_products,
    get_product_by_id,
    create_product,
    get_all_rules,
    get_rule_by_id
)

from backend.database.models import (
    Product,
    Rule,
    Inspection,
    Violation
)


# ============================================================
# PRODUCT SERVICES
# ============================================================

def list_products():
    """
    Get all products from the database.
    """

    rows = get_all_products()

    products = []

    for row in rows:
        product = Product(
            id=row[0],
            product_name=row[1],
            category=row[2],
            brand=row[3],
            manufacturer=row[4],
            created_at=row[5]
        )

        products.append(product)

    return products


def find_product(product_id):
    """
    Find one product by its ID.
    """

    row = get_product_by_id(product_id)

    if row is None:
        return None

    return Product(
        id=row[0],
        product_name=row[1],
        category=row[2],
        brand=row[3],
        manufacturer=row[4],
        created_at=row[5]
    )


def add_product(
    product_name,
    category=None,
    brand=None,
    manufacturer=None
):
    """
    Create a new product.
    """

    # Basic validation
    if not product_name or not product_name.strip():
        raise ValueError("Product name is required.")

    product_id = create_product(
        product_name.strip(),
        category,
        brand,
        manufacturer
    )

    return find_product(product_id)


# ============================================================
# RULE SERVICES
# ============================================================

def list_rules():
    """
    Get all compliance rules.
    """

    rows = get_all_rules()

    rules = []

    for row in rows:
        rule = Rule(
            id=row[0],
            rule_id=row[1],
            category=row[2],
            requirement=row[3],
            description=row[4],
            mandatory=row[5],
            validation_type=row[6],
            severity=row[7],
            source=row[8],
            effective_date=row[9],
            created_at=row[10]
        )

        rules.append(rule)

    return rules


def find_rule(rule_id):
    """
    Find a compliance rule using its rule ID.
    """

    row = get_rule_by_id(rule_id)

    if row is None:
        return None

    return Rule(
        id=row[0],
        rule_id=row[1],
        category=row[2],
        requirement=row[3],
        description=row[4],
        mandatory=row[5],
        validation_type=row[6],
        severity=row[7],
        source=row[8],
        effective_date=row[9],
        created_at=row[10]
    )


# ============================================================
# INSPECTION SERVICES
# ============================================================

def create_new_inspection(
    product_id,
    overall_status,
    confidence
):
    """
    Create an inspection for a product.
    """

    # Make sure the product exists
    product = find_product(product_id)

    if product is None:
        raise ValueError("Product not found.")

    # Validate status
    if overall_status not in ["COMPLIANT", "NON_COMPLIANT"]:
        raise ValueError(
            "Overall status must be COMPLIANT or NON_COMPLIANT."
        )

    # Validate confidence
    if confidence is not None and not 0 <= confidence <= 100:
        raise ValueError(
            "Confidence must be between 0 and 100."
        )

    from backend.database.queries import create_inspection

    inspection_id = create_inspection(
        product_id,
        overall_status,
        confidence
    )

    return get_inspection(inspection_id)


def get_inspection(inspection_id):
    """
    Get an inspection by ID.
    """

    from backend.database.queries import get_inspection_by_id

    row = get_inspection_by_id(inspection_id)

    if row is None:
        return None

    return Inspection(
        id=row[0],
        product_id=row[1],
        inspection_date=row[2],
        overall_status=row[3],
        confidence=row[4]
    )

# ============================================================
# VIOLATION SERVICES
# ============================================================

def create_new_violation(
    inspection_id,
    rule_id,
    status,
    detected_value=None,
    expected_value=None,
    message=None
):
    """
    Create a violation for an inspection.
    """

    from backend.database.queries import (
        create_violation,
        get_inspection_by_id,
        get_rule_by_id
    )

    # Check inspection exists
    inspection = get_inspection_by_id(inspection_id)

    if inspection is None:
        raise ValueError("Inspection not found.")

    # Check rule exists
    rule = get_rule_by_id(rule_id)

    if rule is None:
        raise ValueError("Rule not found.")

    # Validate status
    if status not in ["PASS", "FAIL"]:
        raise ValueError(
            "Violation status must be PASS or FAIL."
        )

    violation_id = create_violation(
        inspection_id,
        rule_id,
        status,
        detected_value,
        expected_value,
        message
    )

    return get_violation(violation_id)


def get_violation(violation_id):
    """
    Get one violation by ID.
    """

    from backend.database.connection import get_connection

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT
                    id,
                    inspection_id,
                    rule_id,
                    status,
                    detected_value,
                    expected_value,
                    message
                FROM violations
                WHERE id = %s;
            """, (violation_id,))

            row = cursor.fetchone()

            if row is None:
                return None

            return Violation(
                id=row[0],
                inspection_id=row[1],
                rule_id=row[2],
                status=row[3],
                detected_value=row[4],
                expected_value=row[5],
                message=row[6]
            )

    finally:
        connection.close()


def list_violations(inspection_id):
    """
    Get all violations belonging to an inspection.
    """

    from backend.database.queries import (
        get_violations_by_inspection
    )

    rows = get_violations_by_inspection(inspection_id)

    violations = []

    for row in rows:

        violation = Violation(
            id=row[0],
            inspection_id=row[1],
            rule_id=row[2],
            status=row[3],
            detected_value=row[4],
            expected_value=row[5],
            message=row[6]
        )

        violations.append(violation)

    return violations