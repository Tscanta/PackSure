import re

from schemas.product import Product


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(value: str) -> str:
    """Clean and normalize OCR-extracted text."""

    if not value:
        return ""

    # Common OCR artifacts
    value = value.replace("|", " ")
    value = value.replace("@", " ")

    # Normalize whitespace
    value = " ".join(value.split())

    # Remove unwanted punctuation at the ends
    return value.strip(" ,.-|")


# ============================================================
# ADDRESS CLEANING
# ============================================================

def clean_address(value: str) -> str:
    """Clean an extracted postal address."""

    if not value:
        return ""

    value = value.replace("|", " ")
    value = value.replace("@", " ")

    # Remove licence information accidentally captured
    value = re.split(
        r"\bLIC\.?\s*NO\.?",
        value,
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0]

    value = clean_text(value)

    return value


# ============================================================
# PRODUCT EXTRACTION
# ============================================================

def extract_product_data(text: str) -> Product:
    """
    Extract structured product information from OCR text.

    Pipeline:
        OCR text
            ↓
        MRP
        Quantity
        Category
        Product name
        Ingredients
        Allergens
        Best before
        Manufacturer
        Manufacturer address
        Importer / marketer
        Country of origin
        FSSAI licence
        Customer care
        Manufacturing date
            ↓
        Product
    """

    if not text:
        return Product(raw_text=text)

    product = Product(raw_text=text)

    # ========================================================
    # MRP
    # ========================================================

    mrp_match = re.search(
        r"(?:MRP|M\.R\.P\.?)"
        r".{0,50}?"
        r"(?:₹|Rs\.?|INR)?"
        r"\s*"
        r"(\d+(?:\.\d+)?)",
        text,
        re.IGNORECASE | re.DOTALL,
    )

    if mrp_match:
        try:
            product.mrp = float(mrp_match.group(1))
        except ValueError:
            pass

    # ========================================================
    # NET QUANTITY
    # ========================================================

    quantity_match = re.search(
        r"(?:NET\s*(?:QTY|QUANTITY)|NET\s*WT\.?)"
        r"\s*[:\-]?\s*"
        r"([\d.]+\s*(?:kg|g|mg|l|ml))",
        text,
        re.IGNORECASE,
    )

    if quantity_match:
        product.net_quantity = (
            quantity_match.group(1)
            .replace(" ", "")
        )

    # ========================================================
    # PRODUCT CATEGORY
    # ========================================================

    category_match = re.search(
        r"PRODUCT\s+CATEGORY\s*[:\-]?\s*"
        r"(.*?)(?=\.\s*INGREDIENTS\b|\n|$)",
        text,
        re.IGNORECASE | re.DOTALL,
    )

    if category_match:
        category = clean_text(category_match.group(1))

        if category:
            product.product_category = category

    # ========================================================
    # PRODUCT NAME / FLAVOUR
    # ========================================================

    flavour_match = re.search(
        r"\b([A-Za-z][A-Za-z\s\-]{2,})\s+FLAVOUR\b",
        text,
        re.IGNORECASE,
    )

    if flavour_match:

        flavour = clean_text(
            flavour_match.group(1)
        )

        # Avoid meaningless OCR captures
        if flavour.upper() not in {
            "PRODUCT",
            "NATURAL",
            "ARTIFICIAL",
            "NATURE IDENTICAL",
        }:
            product.product_name = (
                flavour.title() + " Flavour"
            )

    # ========================================================
    # PRODUCT NAME FALLBACK
    # ========================================================

    if not product.product_name:

        lines = [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]

        stop_keywords = [
            "MRP",
            "NET QUANTITY",
            "NET QTY",
            "NET WT",
            "PRODUCT CATEGORY",
            "INGREDIENTS",
            "MANUFACTURED",
            "MANUFACTURER",
            "MFD",
            "BEST BEFORE",
        ]

        for line in lines:

            upper_line = line.upper()

            # Stop once declarations begin
            if any(
                keyword in upper_line
                for keyword in stop_keywords
            ):
                break

            # Ignore obvious OCR garbage
            if re.fullmatch(
                r"[\d\s\-:/.,]+",
                line,
            ):
                continue

            if len(line) >= 3:

                cleaned = clean_text(line)

                if cleaned:
                    product.product_name = cleaned
                    break

    # ========================================================
    # INGREDIENTS
    # ========================================================

    ingredients_match = re.search(
        r"INGREDIENTS\s*:\s*(.*?)"
        r"(?=\bBEST\s+BEFORE\b|"
        r"\n\s*MFD\b|"
        r"\n\s*FOR\s+MFD\b|"
        r"$)",
        text,
        re.IGNORECASE | re.DOTALL,
    )

    if ingredients_match:

        ingredients = ingredients_match.group(1)

        # Remove allergen statements from ingredient field
        ingredients = re.sub(
            r"\[?\s*CONTAINS\s*"
            r"(?:SOY|MILK|WHEAT|EGG|PEANUT|"
            r"NUTS|ALMOND|GLUTEN)\s*\]?",
            "",
            ingredients,
            flags=re.IGNORECASE,
        )

        # Remove OCR artefacts
        ingredients = re.sub(
            r"\s+\d+\s*[A-Z]\s*$",
            "",
            ingredients,
            flags=re.IGNORECASE,
        )

        ingredients = re.sub(
            r"\s+\d+\s*$",
            "",
            ingredients,
        )

        ingredients = clean_text(ingredients)

        if ingredients:
            product.ingredients = ingredients

    # ========================================================
    # ALLERGENS
    # ========================================================

    allergen_text = []

    allergen_pattern = (
        r"\bCONTAINS\s*[:\-]?\s*"
        r"(SOY|MILK|WHEAT|EGG|PEANUT|"
        r"NUTS|ALMOND|GLUTEN)\b"
    )

    contains_matches = re.findall(
        allergen_pattern,
        text,
        re.IGNORECASE,
    )

    for match in contains_matches:
        allergen_text.append(match.upper())

    # OCR joined forms:
    # CONTAINSSOY
    # CONTAINSMILK
    # CONTAINSWHEAT

    joined_matches = re.findall(
        r"\bCONTAINS\s*"
        r"(SOY|MILK|WHEAT|EGG|PEANUT|"
        r"NUTS|ALMOND|GLUTEN)\b",
        text,
        re.IGNORECASE,
    )

    for match in joined_matches:
        allergen_text.append(match.upper())

    if allergen_text:

        cleaned_allergens = list(
            dict.fromkeys(allergen_text)
        )

        product.allergens = ", ".join(
            cleaned_allergens
        )

    # ========================================================
    # BEST BEFORE
    # ========================================================

    best_before_match = re.search(
        r"BEST\s+BEFORE\s+"
        r"(.*?)(?=\.\s*(?:WHEN|FROM|STORED)|"
        r"\n|$)",
        text,
        re.IGNORECASE | re.DOTALL,
    )

    if best_before_match:

        best_before = clean_text(
            best_before_match.group(1)
        )

        if best_before:
            product.best_before = best_before

    # ========================================================
    # BEST BEFORE FALLBACK
    # ========================================================

    if not product.best_before:

        best_before_match = re.search(
            r"BEST\s+BEFORE\s+"
            r"(.*?FROM\s+MANUFACTURE)",
            text,
            re.IGNORECASE | re.DOTALL,
        )

        if best_before_match:

            best_before = clean_text(
                best_before_match.group(1)
            )

            if best_before:
                product.best_before = best_before

    # ========================================================
    # MANUFACTURER
    # ========================================================

    manufacturer_match = re.search(
        r"(?:MFD\.?\s*BY|"
        r"MANUFACTURED\s*BY|"
        r"MANUFACTURER)"
        r"\s*[:\-]?\s*"
        r"(.*?)"
        r"(?=,\s*(?:AT\s*)?[A-Z][A-Z\s\-]*"
        r"(?:ROAD|ROAD,|NAGAR|AREA|INDUSTRIAL|"
        r"ESTATE|PARK)\b|"
        r",\s*[A-Z][A-Z\s]+\s*-\s*\d{6}|"
        r"\bLIC\.?\s*NO\b|"
        r"\n|$)",
        text,
        re.IGNORECASE | re.DOTALL,
    )

    if manufacturer_match:

        manufacturer = clean_text(
            manufacturer_match.group(1)
        )

        # Remove accidental trailing comma
        manufacturer = manufacturer.rstrip(",")

        if manufacturer:
            product.manufacturer = manufacturer

    # ========================================================
    # MANUFACTURER ADDRESS
    # ========================================================

    manufacturer_block_match = re.search(
        r"(?:MFD\.?\s*BY|"
        r"MANUFACTURED\s*BY|"
        r"MANUFACTURER)"
        r"\s*[:\-]?\s*"
        r"(?P<manufacturer>[^,\n]+)"
        r",\s*"
        r"(?P<address>.*?)(?="
        r"\bLIC\.?\s*NO\b|"
        r"\n\s*(?:MARKETED|IMPORTED|"
        r"DISTRIBUTED|FOR\s+CONSUMER|"
        r"FOR\s+CUSTOMER|FOR\s+MFD)\b|"
        r"$)",
        text,
        re.IGNORECASE | re.DOTALL,
    )

    if manufacturer_block_match:

        address = manufacturer_block_match.group(
            "address"
        )

        # Clean licence number and OCR noise
        address = clean_address(address)

        if address:
            product.manufacturer_address = address

    # ========================================================
    # MANUFACTURER ADDRESS FALLBACK
    # ========================================================

    if not product.manufacturer_address:

        address_match = re.search(
            r"(?:MFD\.?\s*BY|"
            r"MANUFACTURED\s*BY|"
            r"MANUFACTURER)"
            r"[^\n]*\n"
            r"([^\n]+)",
            text,
            re.IGNORECASE,
        )

        if address_match:

            address = clean_address(
                address_match.group(1)
            )

            if address:
                product.manufacturer_address = address

    # ========================================================
    # IMPORTER / MARKETER / DISTRIBUTOR
    # ========================================================

    importer_match = re.search(
        r"(?:IMPORTED\s*BY|"
        r"IMPORTER|"
        r"MARKETED\s*(?:AND\s*)?"
        r"DISTRIBUTED\s*BY)"
        r"\s*[:\-]?\s*"
        r"(?P<name>.*?)"
        r"(?=\n|"
        r"\bLIC\.?\s*NO\b|"
        r"$)",
        text,
        re.IGNORECASE | re.DOTALL,
    )

    if importer_match:

        importer = clean_text(
            importer_match.group("name")
        )

        # Remove address accidentally captured
        importer = re.split(
            r",\s*\d+[A-Z0-9\-]*\s*,",
            importer,
            maxsplit=1,
            flags=re.IGNORECASE,
        )[0]

        importer = clean_text(importer)

        if importer:
            product.importer = importer

    # ========================================================
    # COUNTRY OF ORIGIN
    # ========================================================

    origin_match = re.search(
        r"(?:COUNTRY\s*OF\s*ORIGIN|"
        r"MADE\s*IN)"
        r"\s*[:\-]?\s*"
        r"([A-Za-z]+(?:\s+[A-Za-z]+)*?)"
        r"(?=\s+(?:CUSTOMER|CONSUMER|"
        r"MRP|NET|MANUFACTURER|"
        r"IMPORTER|INGREDIENTS)\b|"
        r"[.,\n]|$)",
        text,
        re.IGNORECASE,
    )

    if origin_match:

        origin = clean_text(
            origin_match.group(1)
        )

        if origin:
            product.country_of_origin = origin

    # ========================================================
    # FSSAI / LICENCE NUMBERS
    # ========================================================

    fssai_matches = re.findall(
        r"LIC\.?\s*NO\.?\s*[:\-]?\s*"
        r"(\d{10,15})",
        text,
        re.IGNORECASE,
    )

    if fssai_matches:

        unique_numbers = list(
            dict.fromkeys(fssai_matches)
        )

        product.fssai_license = ", ".join(
            unique_numbers
        )

    # ========================================================
    # CUSTOMER CARE
    # ========================================================

    # First look specifically for CALL AT.
    phone_match = re.search(
        r"(?:CALL\s*AT)"
        r"\s*[:\-]?\s*"
        r"(\+?\d[\d\s\-().]{8,}\d)",
        text,
        re.IGNORECASE,
    )

    # Fallback to customer service / contact declarations.
    if not phone_match:

        phone_match = re.search(
            r"(?:CUSTOMER\s*CARE|"
            r"CUSTOMER\s*SERVICE|"
            r"CONSUMER\s*QUERIES|"
            r"CONTACT)"
            r"\s*[:\-]?\s*"
            r"(\+?\d[\d\s\-().]{8,}\d)",
            text,
            re.IGNORECASE,
        )

    if phone_match:

        phone = phone_match.group(1)

        # Keep only digits and optional +
        phone = re.sub(
            r"[^\d+]",
            "",
            phone,
        )

        if phone:
            product.customer_care = phone

    # ========================================================
    # MANUFACTURING DATE
    # ========================================================

    manufacturing_date_match = re.search(
        r"(?:MFD|MFG|"
        r"MANUFACTURED\s*DATE|"
        r"MANUFACTURING\s*DATE)"
        r"\s*[:\-]?\s*"
        r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|"
        r"\d{1,2}[/-]\d{2,4})",
        text,
        re.IGNORECASE,
    )

    if manufacturing_date_match:

        product.manufacturing_date = (
            manufacturing_date_match.group(1)
        )

    # ========================================================
    # RETURN
    # ========================================================

    return product