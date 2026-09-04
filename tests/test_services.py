from backend.database.services import list_products
from backend.database.services import find_product
from backend.database.services import add_product


print("\n===== ALL PRODUCTS =====")

products = list_products()

for product in products:
    print(product)


print("\n===== FIND PRODUCT =====")

product = find_product(1)

print(product)


print("\n===== CREATE PRODUCT =====")

new_product = add_product(
    product_name="XYZ Shampoo",
    category="Personal Care",
    brand="XYZ",
    manufacturer="XYZ Consumer Products Pvt Ltd"
)

print(new_product)