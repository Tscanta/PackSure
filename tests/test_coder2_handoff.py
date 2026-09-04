from schemas.product import ProductInput

from backend.inspection.inspector import InspectionEngine


def main():

    # Simulated output from Coder 2
    product = ProductInput(
        product_name="Test Biscuit",
        brand="Test Brand",
        mrp="₹50",
        net_quantity="100 g",
        manufacturer="Test Foods Pvt Ltd",
        manufacturer_address="123 Industrial Area, Hyderabad",
        importer=None,
        importer_address=None,
        country_of_origin="India",
        customer_care="9876543210",
        manufacturing_date="08/2026",
        expiry_date="08/2027",
        raw_text=(
            "Test Biscuit "
            "100 g "
            "MRP ₹50 "
            "Manufactured 08/2026 "
            "Expiry 08/2027"
        )
    )

    # Your engine receives Coder 2's output
    engine = InspectionEngine()

    result = engine.inspect(product)

    print("Product:", product.product_name)
    print("Inspection:", result.inspection_id)
    print("Status:", result.overall_status)
    print("Score:", result.score)

    print()
    print("Checks:")

    for check in result.checks:

        print(
            f"{check.field}: "
            f"{check.status} "
            f"[{check.rule_id}] "
            f"{check.severity}"
        )


if __name__ == "__main__":
    main()