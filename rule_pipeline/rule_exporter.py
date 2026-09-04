import json


def rules_to_dict(rules):

    return [
        rule.model_dump(mode="json")
        for rule in rules
    ]


def save_rules_to_json(rules, file_path):

    data = rules_to_dict(rules)

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )