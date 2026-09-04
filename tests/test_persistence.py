from schemas.product import ProductInput

from backend.database.queries import (
    create_product,
    get_inspection_by_id,
    get_violations_by_inspection,
)

from backend.inspection.inspector import InspectionEngine
from backend.inspection.persistence import save_inspection_result


def main():

    # ------------------------------------------------------------
    # 1. CREATE TEST PRODUCT
    # ------------------------------------------------------------

    product_id = create_product(
        product_name="Test Coca Cola",
        category="PACKAGED_COMMODITY",
        brand="Coca Cola",
        manufacturer="Test Manufacturer"
    )

    print("Created product:", product_id)

    # ------------------------------------------------------------
    # 2. CREATE PRODUCT INPUT
    # ------------------------------------------------------------

    product = ProductInput(
        product_name="Test Coca Cola",
        brand="Coca Cola",
        mrp=None,
        net_quantity="500 ml",
        manufacturer="Test Manufacturer",
        manufacturer_address="123 Test Road, Delhi",
        customer_care="9876543210",
        manufacturing_date="08/2026"
    )

    # ------------------------------------------------------------
    # 3. RUN INSPECTION
    # ------------------------------------------------------------

    engine = InspectionEngine()

    result = engine.inspect(product)

    print()
    print("Inspection result:")
    print("Status:", result.overall_status)
    print("Score:", result.score)
    print("Total checks:", result.total_checks)
    print("Passed:", result.passed_checks)
    print("Failed:", result.failed_checks)
    print("Warnings:", result.warning_checks)

    # ------------------------------------------------------------
    # 4. SAVE INSPECTION
    # ------------------------------------------------------------

    db_inspection_id = save_inspection_result(
        product_id=product_id,
        inspection_result=result
    )

    print()
    print("Database inspection ID:", db_inspection_id)

    # ------------------------------------------------------------
    # 5. READ INSPECTION BACK
    # ------------------------------------------------------------

    inspection = get_inspection_by_id(
        db_inspection_id
    )

    print()
    print("Saved inspection:")
    print(inspection)

    # ------------------------------------------------------------
    # 6. READ VIOLATIONS BACK
    # ------------------------------------------------------------

    violations = get_violations_by_inspection(
        db_inspection_id
    )

    print()
    print("Saved violations:")
    print(violations)


if __name__ == "__main__":
    main()