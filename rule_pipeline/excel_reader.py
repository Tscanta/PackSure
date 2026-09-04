import pandas as pd

from rule_model import Rule


def read_rules_from_excel(file_path):
    df = pd.read_excel(file_path)

    return df


def convert_to_rules(df):

    rules = []

    for _, row in df.iterrows():

        rule = Rule(
            rule_id=str(row["rule_id"]).strip(),

            category=str(row["category"]).strip(),

            requirement=str(row["requirement"]).strip(),

            description=str(row["description"]).strip(),

            mandatory=(
                str(row["mandatory"])
                .strip()
                .upper() == "YES"
            ),

            validation_type=(
                str(row["validation_type"])
                .strip()
                .upper()
            ),

            severity=(
                str(row["severity"])
                .strip()
                .upper()
            ),

            source=str(row["source"]).strip(),

            effective_date=pd.to_datetime(
                row["effective_date"]
            ).date()
        )

        rules.append(rule)

    return rules