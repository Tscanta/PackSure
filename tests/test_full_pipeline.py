from extraction.normalizer import normalize_text
from extraction.parser import extract_product_data
from extraction.adapter import to_product_input
from backend.inspection.inspector import InspectionEngine


def test_full_extraction_to_inspection():

    raw_text = """
    TEST BISCUIT
    MRP ₹50
    Net Quantity 100 g
    Manufactured by Test Foods Pvt Ltd
    123 Industrial Area, Hyderabad
    Customer Care 9876543210
    Country of Origin India
    MFD 08/2026
    BEST BEFORE 12 MONTHS FROM MANUFACTURE
    """

    # Coder 2 pipeline
    normalized_text = normalize_text(raw_text)
    extracted_product = extract_product_data(normalized_text)

    # Coder 2 → Coder 1 bridge
    product_input = to_product_input(extracted_product)

    # Coder 1 compliance engine
    result = InspectionEngine().inspect(product_input)

    print("\n===== FULL PIPELINE =====")
    print("Product:", product_input.product_name)
    print("MRP:", product_input.mrp)
    print("Quantity:", product_input.net_quantity)
    print("Manufacturer:", product_input.manufacturer)
    print("Status:", result.overall_status)
    print("Score:", result.score)

    for check in result.checks:
        print(
            f"{check.field}: "
            f"{check.status} "
            f"[{check.rule_id}]"
        )

    assert extracted_product is not None
    assert product_input is not None
    assert result is not None
    assert len(result.checks) > 0