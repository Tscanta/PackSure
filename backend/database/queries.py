from backend.database.connection import get_connection


# ============================================================
# PRODUCTS
# ============================================================

def get_all_products():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    product_name,
                    category,
                    brand,
                    manufacturer,
                    created_at
                FROM products
                ORDER BY id;
            """)

            products = cursor.fetchall()

            return products

    finally:
        connection.close()


def get_product_by_id(product_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    product_name,
                    category,
                    brand,
                    manufacturer,
                    created_at
                FROM products
                WHERE id = %s;
            """, (product_id,))

            product = cursor.fetchone()

            return product

    finally:
        connection.close()


def create_product(
    product_name,
    category,
    brand,
    manufacturer
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO products
                (
                    product_name,
                    category,
                    brand,
                    manufacturer
                )
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """, (
                product_name,
                category,
                brand,
                manufacturer
            ))

            product_id = cursor.fetchone()[0]

            connection.commit()

            return product_id

    finally:
        connection.close()


# ============================================================
# RULES
# ============================================================

def get_all_rules():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    rule_id,
                    category,
                    requirement,
                    description,
                    mandatory,
                    validation_type,
                    severity,
                    source,
                    effective_date,
                    created_at
                FROM rules
                ORDER BY id;
            """)

            rules = cursor.fetchall()

            return rules

    finally:
        connection.close()


def get_rule_by_id(rule_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    rule_id,
                    category,
                    requirement,
                    description,
                    mandatory,
                    validation_type,
                    severity,
                    source,
                    effective_date,
                    created_at
                FROM rules
                WHERE rule_id = %s;
            """, (rule_id,))

            rule = cursor.fetchone()

            return rule

    finally:
        connection.close()


# ============================================================
# INSPECTIONS
# ============================================================

def create_inspection(
    product_id,
    overall_status,
    confidence
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO inspections
                (
                    product_id,
                    overall_status,
                    confidence
                )
                VALUES (%s, %s, %s)
                RETURNING id;
            """, (
                product_id,
                overall_status,
                confidence
            ))

            inspection_id = cursor.fetchone()[0]

            connection.commit()

            return inspection_id

    finally:
        connection.close()


def get_inspection_by_id(inspection_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    product_id,
                    inspection_date,
                    overall_status,
                    confidence
                FROM inspections
                WHERE id = %s;
            """, (inspection_id,))

            inspection = cursor.fetchone()

            return inspection

    finally:
        connection.close()


# ============================================================
# VIOLATIONS
# ============================================================

def create_violation(
    inspection_id,
    rule_id,
    status,
    detected_value,
    expected_value,
    message
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO violations
                (
                    inspection_id,
                    rule_id,
                    status,
                    detected_value,
                    expected_value,
                    message
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (
                inspection_id,
                rule_id,
                status,
                detected_value,
                expected_value,
                message
            ))

            violation_id = cursor.fetchone()[0]

            connection.commit()

            return violation_id

    finally:
        connection.close()


def get_violation_by_id(violation_id):
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

            violation = cursor.fetchone()

            return violation

    finally:
        connection.close()


def get_violations_by_inspection(inspection_id):
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
                WHERE inspection_id = %s
                ORDER BY id;
            """, (inspection_id,))

            violations = cursor.fetchall()

            return violations

    finally:
        connection.close()