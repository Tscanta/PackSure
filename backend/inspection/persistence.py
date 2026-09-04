from backend.database.queries import (
    create_inspection,
    create_violation,
    get_rule_by_id,
)


def save_inspection_result(
    product_id: int,
    inspection_result
):
    """
    Save an InspectionResult and its failed checks
    into PostgreSQL.

    Returns the database inspection ID.
    """

    # ------------------------------------------------------------
    # SAVE INSPECTION
    # ------------------------------------------------------------

    inspection_id = create_inspection(
        product_id=product_id,
        overall_status=inspection_result.overall_status,
        confidence=inspection_result.score / 100
    )

    # ------------------------------------------------------------
    # SAVE VIOLATIONS
    # ------------------------------------------------------------

    for check in inspection_result.checks:

        # Only failed checks are violations.
        if check.status != "FAIL":
            continue

        # Find the corresponding database rule.
        rule = get_rule_by_id(check.rule_id)

        if rule is None:
            continue

        # Database rule primary key.
        rule_db_id = rule[0]

        create_violation(
            inspection_id=inspection_id,
            rule_id=rule_db_id,
            status=check.status,
            detected_value=None,
            expected_value=None,
            message=check.message
        )

    return inspection_id