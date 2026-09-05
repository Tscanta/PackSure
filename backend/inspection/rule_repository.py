from backend.database.queries import get_all_rules
from backend.models.rule import Rule


def _row_value(row, index, key, default=None):
    if isinstance(row, dict):
        return row.get(key, default)
    try:
        return row[index]
    except (IndexError, TypeError):
        return default


def get_compliance_rules(product=None) -> list[Rule]:
    """
    Fetch all compliance rules from the database.
    """

    rows = get_all_rules()

    rules = []

    for row in rows:
        # Stable DB queries return the original 11 columns; mappings can also
        # carry structured field/operator/value data for generic validation.
        rules.append(Rule(
            id=_row_value(row, 0, "id"), rule_id=_row_value(row, 1, "rule_id"),
            category=_row_value(row, 2, "category"), requirement=_row_value(row, 3, "requirement"),
            description=_row_value(row, 4, "description"), mandatory=bool(_row_value(row, 5, "mandatory", True)),
            validation_type=_row_value(row, 6, "validation_type"), severity=_row_value(row, 7, "severity"),
            source=_row_value(row, 8, "source"), effective_date=_row_value(row, 9, "effective_date"),
            legal_reference=_row_value(row, 11, "legal_reference"), applicability=_row_value(row, 12, "applicability"),
            exceptions=_row_value(row, 13, "exceptions"), field=_row_value(row, 14, "field"),
            operator=_row_value(row, 15, "operator"), value=_row_value(row, 16, "value"),
        ))

    return rules
