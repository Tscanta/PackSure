from extraction.ocr import extract_text_from_image
from extraction.normalizer import normalize_text
from extraction.parser import extract_product_data
from extraction.adapter import to_product_input
from backend.inspection.inspector import InspectionEngine


def test_real_image_pipeline():

    # =========================================================
    # 1. OCR
    # =========================================================

    raw_text = extract_text_from_image(
        "assets/test_product.png"
    )

    assert raw_text

    # =========================================================
    # 2. NORMALIZE
    # =========================================================

    normalized_text = normalize_text(raw_text)

    assert normalized_text

    # =========================================================
    # 3. PARSE
    # =========================================================

    extracted_product = extract_product_data(
        normalized_text
    )

    assert extracted_product is not None

    # =========================================================
    # 4. ADAPT TO INSPECTION MODEL
    # =========================================================

    product_input = to_product_input(
        extracted_product
    )

    # =========================================================
    # 5. COMPLIANCE INSPECTION
    # =========================================================

    result = InspectionEngine().inspect(
        product_input
    )

    # =========================================================
    # DEBUG OUTPUT
    # =========================================================

    print("\n===== REAL IMAGE PIPELINE =====")

    print("\n--- OCR ---")
    print(raw_text)

    print("\n--- EXTRACTED PRODUCT ---")
    print(extracted_product)

    print("\n--- INSPECTION INPUT ---")
    print(product_input)

    print("\n--- COMPLIANCE ---")
    print("Status:", result.overall_status)
    print("Score:", result.score)

    for check in result.checks:
        print(
            f"{check.field}: "
            f"{check.status} "
            f"[{check.rule_id}]"
        )

    assert result is not None
    assert len(result.checks) > 0