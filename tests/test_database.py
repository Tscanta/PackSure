from database.queries import get_all_products


products = get_all_products()

for product in products:
    print(product)