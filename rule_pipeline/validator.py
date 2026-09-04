REQUIRED_COLUMNS = [
    "rule_id",
    "category",
    "requirement",
    "description",
    "mandatory",
    "validation_type",
    "severity",
    "source",
    "effective_date"
]


VALID_MANDATORY_VALUES = {
    "YES",
    "NO"
}


VALID_VALIDATION_TYPES = {
    "TEXT_EXISTS",
    "QUANTITY",
    "CURRENCY",
    "DATE",
    "ADDRESS",
    "PHONE",
    "EMAIL"
}


VALID_SEVERITIES = {
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL"
}


def validate_columns(df):

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )


def validate_required_values(df):

    required_fields = [
        "rule_id",
        "category",
        "requirement",
        "mandatory",
        "validation_type",
        "severity",
        "source",
        "effective_date"
    ]

    for field in required_fields:

        empty_rows = df[
            df[field].isna()
            |
            (df[field].astype(str).str.strip() == "")
        ]

        if not empty_rows.empty:
            raise ValueError(
                f"Empty values found in column: {field}"
            )


def validate_mandatory_values(df):

    values = (
        df["mandatory"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    invalid_values = values[
        ~values.isin(VALID_MANDATORY_VALUES)
    ]

    if not invalid_values.empty:
        raise ValueError(
            f"Invalid mandatory values: "
            f"{invalid_values.tolist()}"
        )


def validate_validation_types(df):

    values = (
        df["validation_type"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    invalid_values = values[
        ~values.isin(VALID_VALIDATION_TYPES)
    ]

    if not invalid_values.empty:
        raise ValueError(
            f"Invalid validation types: "
            f"{invalid_values.tolist()}"
        )


def validate_severity(df):

    values = (
        df["severity"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    invalid_values = values[
        ~values.isin(VALID_SEVERITIES)
    ]

    if not invalid_values.empty:
        raise ValueError(
            f"Invalid severity values: "
            f"{invalid_values.tolist()}"
        )


def validate_rule_ids(df):

    duplicates = df[
        df["rule_id"].duplicated()
    ]["rule_id"].tolist()

    if duplicates:
        raise ValueError(
            f"Duplicate rule IDs found: {duplicates}"
        )


def validate_rules(df):

    validate_columns(df)

    validate_required_values(df)

    validate_mandatory_values(df)

    validate_validation_types(df)

    validate_severity(df)

    validate_rule_ids(df)

    return True