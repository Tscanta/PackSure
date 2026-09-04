from schemas.product import ProductInput
from backend.inspection.inspector import InspectionEngine


engine = InspectionEngine()


# ==========================================
# TEST 1 — GOOD PRODUCT
# ==========================================

good_product = ProductInput(
    product_name="Test Biscuit",
    brand="Test Brand",
    mrp="₹50",
    net_quantity="500 g",
    manufacturer="ABC Foods Pvt Ltd",
    manufacturer_address="Hyderabad, Telangana, India",
    importer="",
    importer_address="",
    country_of_origin="India",
    customer_care="1800-123-4567"
)

result = engine.inspect(good_product)

print("=" * 60)
print("TEST 1 — GOOD PRODUCT")
print("=" * 60)
print(result.model_dump_json(indent=2))


# ==========================================
# TEST 2 — BAD PRODUCT
# ==========================================

bad_product = ProductInput(
    product_name="Bad Product",
    brand="Bad Brand",
    mrp=None,
    net_quantity="banana",
    manufacturer=None,
    manufacturer_address=None,
    country_of_origin=None,
    customer_care=None
)

result = engine.inspect(bad_product)

print()
print("=" * 60)
print("TEST 2 — BAD PRODUCT")
print("=" * 60)
print(result.model_dump_json(indent=2))