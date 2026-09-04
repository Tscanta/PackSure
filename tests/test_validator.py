from backend.inspection.validator import (
    check_mrp,
    check_net_quantity,
    check_manufacturer,
    check_manufacturer_address,
    check_importer,
    check_importer_address,
    check_country_of_origin,
    check_customer_care
)   

from backend.inspection.validator import (
    check_mrp,
    check_net_quantity,
    check_manufacturer,
    check_manufacturer_address
)

from schemas.product import ProductInput
from backend.inspection.validator import (
    check_mrp,
    check_net_quantity
)


# -------------------------
# MRP TEST
# -------------------------

product = ProductInput(
    product_name="Test Product",
    mrp="₹50"
)

result = check_mrp(product)

print("MRP TEST")
print(result)
print()


# -------------------------
# QUANTITY TESTS
# -------------------------

test_quantities = [
    "500 g",
    "1 kg",
    "250 ml",
    "2 L",
    None,
    "",
    "banana"
]

for quantity in test_quantities:

    product = ProductInput(
        product_name="Test Product",
        net_quantity=quantity
    )

    result = check_net_quantity(product)

    print(f"QUANTITY: {quantity}")
    print(result)
    print()

# -------------------------
# MANUFACTURER TESTS
# -------------------------

print("MANUFACTURER TESTS")

product = ProductInput(
    product_name="Test Product",
    manufacturer="ABC Foods Pvt Ltd",
    manufacturer_address="Hyderabad, Telangana, India"
)

print(check_manufacturer(product))
print(check_manufacturer_address(product))
print()


# Missing manufacturer
product = ProductInput(
    product_name="Test Product",
    manufacturer=None,
    manufacturer_address="Hyderabad, Telangana, India"
)

print("MISSING MANUFACTURER")
print(check_manufacturer(product))
print()


# Missing address
product = ProductInput(
    product_name="Test Product",
    manufacturer="ABC Foods Pvt Ltd",
    manufacturer_address=None
)

print("MISSING MANUFACTURER ADDRESS")
print(check_manufacturer_address(product))
print()

# -------------------------
# IMPORTER TESTS
# -------------------------

print("IMPORTER TESTS")

product = ProductInput(
    product_name="Imported Product",
    importer="XYZ Imports Pvt Ltd",
    importer_address="Mumbai, Maharashtra, India"
)

print(check_importer(product))
print(check_importer_address(product))
print()


# Missing importer address
product = ProductInput(
    product_name="Imported Product",
    importer="XYZ Imports Pvt Ltd",
    importer_address=None
)

print("MISSING IMPORTER ADDRESS")
print(check_importer_address(product))
print()


# -------------------------
# COUNTRY OF ORIGIN
# -------------------------

print("COUNTRY OF ORIGIN")

product = ProductInput(
    product_name="Test Product",
    country_of_origin="India"
)

print(check_country_of_origin(product))
print()


product = ProductInput(
    product_name="Test Product",
    country_of_origin=None
)

print("MISSING COUNTRY OF ORIGIN")
print(check_country_of_origin(product))
print()


# -------------------------
# CUSTOMER CARE
# -------------------------

print("CUSTOMER CARE")

product = ProductInput(
    product_name="Test Product",
    customer_care="1800-123-4567"
)

print(check_customer_care(product))
print()


product = ProductInput(
    product_name="Test Product",
    customer_care=None
)

print("MISSING CUSTOMER CARE")
print(check_customer_care(product))
print()