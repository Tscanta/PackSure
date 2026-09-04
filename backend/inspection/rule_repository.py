from backend.database.queries import get_all_rules


def get_compliance_rules():
    """
    Fetch all compliance rules from the database.
    """

    rows = get_all_rules()

    rules = []

    for row in rows:
        rule = {
            "id": row[0],
            "rule_id": row[1],
            "category": row[2],
            "requirement": row[3],
            "description": row[4],
            "mandatory": row[5],
            "validation_type": row[6],
            "severity": row[7],
            "source": row[8],
            "effective_date": row[9],
            "created_at": row[10],
        }

        rules.append(rule)

    return rules