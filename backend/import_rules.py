from backend.database.rule_importer import (
    import_rules_from_json
)


file_path = "data/rules.json"


result = import_rules_from_json(file_path)


print("\n===== RULE IMPORT RESULT =====")

print(f"Rules imported: {result['imported']}")
print(f"Rules skipped: {result['skipped']}")