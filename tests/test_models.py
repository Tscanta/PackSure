from backend.database.models import Product

product = Product(
    id=1,
    product_name="ABC Biscuits",
    category="Food",
    brand="ABC",
    manufacturer="ABC Foods Pvt Ltd"
)

print(product)