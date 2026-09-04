from schemas.product import Product
from extraction.adapter import to_product_input


def test_product_adapter():

    extracted = Product(
        product_name="Test Biscuit",
        mrp=50.0,
        net_quantity="100 g",
        manufacturer="Test Foods Pvt Ltd",
        manufacturer_address="123 Industrial Area",
        importer=None,
        country_of_origin="India",
        customer_care="9876543210",
        raw_text="Test Biscuit MRP ₹50 100 g"
    )

    result = to_product_input(extracted)

    assert result.product_name == "Test Biscuit"
    assert result.mrp == "50.0"
    assert result.net_quantity == "100 g"
    assert result.manufacturer == "Test Foods Pvt Ltd"
    assert result.country_of_origin == "India"