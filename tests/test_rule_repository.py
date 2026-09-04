from backend.inspection.rule_repository import get_compliance_rules


rules = get_compliance_rules()

print(f"Total rules: {len(rules)}")

for rule in rules:
    print()
    print("Rule ID:", rule["rule_id"])
    print("Category:", rule["category"])
    print("Requirement:", rule["requirement"])
    print("Mandatory:", rule["mandatory"])
    print("Validation:", rule["validation_type"])
    print("Severity:", rule["severity"])