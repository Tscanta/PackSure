import re

from schemas.product import Nutrition


def clean_nutrition_text(text: str) -> str:
    """
    Clean OCR text specifically for nutrition extraction.
    """

    text = text.replace("|", " ")
    text = text.replace("@", " ")

    # Common OCR corrections
    text = text.replace("m9", "mg")
    text = text.replace("g9", "g")

    # Remove excessive whitespace
    text = " ".join(text.split())

    return text.strip()


def extract_number(value: str):
    """
    Extract the first numeric value from a string.

    Examples:
    10g      -> 10
    1.5g     -> 1.5
    <1g      -> 1
    120mg    -> 120
    """

    if not value:
        return None

    match = re.search(
        r"(\d+(?:\.\d+)?)",
        value
    )

    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return None

    return None


def extract_nutrition_value(
    text: str,
    patterns: list[str]
):
    """
    Try multiple regex patterns and return
    the first numeric value found.
    """

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            groups = match.groups()

            for group in groups:

                if group and re.search(
                    r"\d",
                    group
                ):

                    value = extract_number(
                        group
                    )

                    if value is not None:
                        return value

    return None

def extract_nutrition_data(text: str) -> Nutrition:
    """
    Extract nutrition information from OCR text.
    """

    text = clean_nutrition_text(text)

    nutrition = Nutrition()

    # =========================================================
    # SERVING SIZE
    # =========================================================

    serving_match = re.search(
        r"SERVING\s+SIZE\s*"
        r"[:\-]?\s*"
        r"(.{1,50}?)"
        r"(?=\s+(?:SERVINGS?|CALORIES|TOTAL|$))",
        text,
        re.IGNORECASE
    )

    if serving_match:

        serving_size = (
            serving_match.group(1)
            .strip()
        )

        if serving_size:
            nutrition.serving_size = serving_size

    # =========================================================
    # CALORIES
    # =========================================================

    nutrition.calories = extract_nutrition_value(
        text,
        [
            r"\bCALORIES\s*[:\-]?\s*(\d+(?:\.\d+)?)",
            r"\bCALORIES\s+(\d+(?:\.\d+)?)",
        ]
    )

    # =========================================================
    # TOTAL FAT
    # =========================================================

    nutrition.total_fat = extract_nutrition_value(
        text,
        [
            r"\bTOTAL\s+FAT\s*[:\-]?\s*"
            r"(<\s*)?(\d+(?:\.\d+)?)"
        ]
    )

    # =========================================================
    # SATURATED FAT
    # =========================================================

    nutrition.saturated_fat = extract_nutrition_value(
        text,
        [
            r"\bSATURATED\s+FAT\s*[:\-]?\s*"
            r"(<\s*)?(\d+(?:\.\d+)?)"
        ]
    )

    # =========================================================
    # TRANS FAT
    # =========================================================

    nutrition.trans_fat = extract_nutrition_value(
        text,
        [
            r"\bTRANS\s+FAT\s*[:\-]?\s*"
            r"(<\s*)?(\d+(?:\.\d+)?)"
        ]
    )

    # =========================================================
    # CHOLESTEROL
    # =========================================================

    nutrition.cholesterol = extract_nutrition_value(
        text,
        [
            r"\bCHOLESTEROL\s*[:\-]?\s*"
            r"(\d+(?:\.\d+)?)"
        ]
    )

    # =========================================================
    # SODIUM
    # =========================================================

    nutrition.sodium = extract_nutrition_value(
        text,
        [
            r"\bSODIUM\s*[:\-]?\s*"
            r"(\d+(?:\.\d+)?)"
        ]
    )

    # =========================================================
    # POTASSIUM
    # =========================================================

    nutrition.potassium = extract_nutrition_value(
        text,
        [
            r"\bPOTASSIUM\s*[:\-]?\s*"
            r"(\d+(?:\.\d+)?)"
        ]
    )

    # =========================================================
    # TOTAL CARBOHYDRATE
    # =========================================================

    nutrition.total_carbohydrate = extract_nutrition_value(
        text,
        [
            r"\bTOTAL\s+CARBOHYDRATE\s*[:\-]?\s*"
            r"(\d+(?:\.\d+)?)",
            r"\bTOTAL\s+CARBOHYDRATES\s*[:\-]?\s*"
            r"(\d+(?:\.\d+)?)",
        ]
    )

    # =========================================================
    # DIETARY FIBER
    # =========================================================

    nutrition.dietary_fiber = extract_nutrition_value(
        text,
        [
            r"\bDIETARY\s+FIBER\s*[:\-]?\s*"
            r"(\d+(?:\.\d+)?)",
            r"\bFIBER\s*[:\-]?\s*"
            r"(\d+(?:\.\d+)?)",
        ]
    )

    # =========================================================
    # SUGARS
    # =========================================================

    nutrition.sugars = extract_nutrition_value(
        text,
        [
            r"\bSUGARS?\s*[:\-]?\s*"
            r"(<\s*)?(\d+(?:\.\d+)?)"
        ]
    )

    # =========================================================
    # PROTEIN
    # =========================================================

    nutrition.protein = extract_nutrition_value(
        text,
        [
            r"\bPROTEIN\s*[:\-]?\s*"
            r"(\d+(?:\.\d+)?)"
        ]
    )

    # =========================================================
    # VITAMIN A
    # =========================================================

    nutrition.vitamin_a = extract_nutrition_value(
        text,
        [
            r"\bVITAMIN\s*A\s*"
            r"(\d+(?:\.\d+)?)"
        ]
    )

    # =========================================================
    # VITAMIN C
    # =========================================================

    nutrition.vitamin_c = extract_nutrition_value(
        text,
        [
            r"\bVITAMIN\s*C\s*"
            r"(\d+(?:\.\d+)?)"
        ]
    )

    # =========================================================
    # VITAMIN D
    # =========================================================

    nutrition.vitamin_d = extract_nutrition_value(
        text,
        [
            r"\bVITAMIN\s*D\s*"
            r"(\d+(?:\.\d+)?)"
        ]
    )

    # =========================================================
    # CALCIUM
    # =========================================================

    nutrition.calcium = extract_nutrition_value(
        text,
        [
            r"\bCALCIUM\s*"
            r"(\d+(?:\.\d+)?)"
        ]
    )

    # =========================================================
    # IRON
    # =========================================================

    nutrition.iron = extract_nutrition_value(
        text,
        [
            r"\bIRON\s*"
            r"(\d+(?:\.\d+)?)"
        ]
    )

    # =========================================================
    # MAGNESIUM
    # =========================================================

    nutrition.magnesium = extract_nutrition_value(
        text,
        [
            r"\bMAGNESIUM\s*"
            r"(\d+(?:\.\d+)?)"
        ]
    )

    # =========================================================
    # PHOSPHORUS
    # =========================================================

    nutrition.phosphorus = extract_nutrition_value(
        text,
        [
            r"\bPHOSPHORUS\s*"
            r"(\d+(?:\.\d+)?)"
        ]
    )

    # =========================================================
    # NIACIN
    # =========================================================

    nutrition.niacin = extract_nutrition_value(
        text,
        [
            r"\bNIACIN\s*"
            r"(\d+(?:\.\d+)?)"
        ]
    )

    # =========================================================
    # VITAMIN B6
    # =========================================================

    nutrition.vitamin_b6 = extract_nutrition_value(
        text,
        [
            r"\bVITAMIN\s*B6\s*"
            r"(\d+(?:\.\d+)?)",
            r"\bVITAMIN\s*B\s*6\s*"
            r"(\d+(?:\.\d+)?)",
        ]
    )

    return nutrition