import re


def normalize_text(text: str) -> str:
    """
    Clean OCR text while preserving line boundaries.

    Line boundaries are important because product labels
    commonly place declarations on separate lines.
    """

    if not text:
        return ""

    # Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove OCR artifacts
    text = text.replace("|", " ")

    # Clean each line independently
    lines = []

    for line in text.split("\n"):
        line = re.sub(r"\s+", " ", line)
        line = re.sub(r"\s*:\s*", ": ", line)
        line = re.sub(r"\s*,\s*", ", ", line)

        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)