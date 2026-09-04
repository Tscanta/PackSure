from schemas.product import Product, ProductInput

def to_product_input(product: Product) -> ProductInput:
    return ProductInput(
        product_name=product.product_name,
        mrp=str(product.mrp) if product.mrp is not None else None,
        net_quantity=product.net_quantity,
        manufacturer=product.manufacturer,
        manufacturer_address=product.manufacturer_address,
        importer=product.importer,
        country_of_origin=product.country_of_origin,
        customer_care=product.customer_care,
        manufacturing_date=product.manufacturing_date,
        raw_text=product.raw_text,
    )