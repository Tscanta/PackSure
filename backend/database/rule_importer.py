import json
from datetime import date

from backend.database.connection import get_connection


# ============================================================
# IMPORT RULES FROM JSON
# ============================================================

def import_rules_from_json(file_path):

    # --------------------------------------------------------
    # READ JSON FILE
    # --------------------------------------------------------

    with open(file_path, "r", encoding="utf-8") as file:
        rules = json.load(file)

    connection = get_connection()

    imported_count = 0
    skipped_count = 0

    try:

        with connection.cursor() as cursor:

            for rule in rules:

                # ------------------------------------------------
                # GET DATA FROM JSON
                # ------------------------------------------------

                rule_id = rule["rule_id"]
                category = rule["category"]
                requirement = rule["requirement"]
                description = rule.get("description")
                mandatory = rule["mandatory"]
                validation_type = rule["validation_type"]
                severity = rule["severity"]
                source = rule.get("source")
                effective_date = rule.get("effective_date")

                # ------------------------------------------------
                # CONVERT DATE
                # ------------------------------------------------

                if effective_date:
                    effective_date = date.fromisoformat(
                        effective_date
                    )

                # ------------------------------------------------
                # INSERT RULE
                # ------------------------------------------------

                cursor.execute("""
                    INSERT INTO rules
                    (
                        rule_id,
                        category,
                        requirement,
                        description,
                        mandatory,
                        validation_type,
                        severity,
                        source,
                        effective_date
                    )
                    VALUES
                    (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    ON CONFLICT (rule_id)
                    DO UPDATE SET
                        category = EXCLUDED.category,
                        requirement = EXCLUDED.requirement,
                        description = EXCLUDED.description,
                        mandatory = EXCLUDED.mandatory,
                        validation_type = EXCLUDED.validation_type,
                        severity = EXCLUDED.severity,
                        source = EXCLUDED.source,
                        effective_date = EXCLUDED.effective_date;
                """, (
                    rule_id,
                    category,
                    requirement,
                    description,
                    mandatory,
                    validation_type,
                    severity,
                    source,
                    effective_date
                ))

                imported_count += 1

        connection.commit()

        return {
            "imported": imported_count,
            "skipped": skipped_count
        }

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()