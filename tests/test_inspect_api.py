from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_valid_product():

    response = client.post(
        "/inspect",
        json={
            "product_name": "Test Product",
            "brand": "Test Brand",
            "mrp": "₹40",
            "net_quantity": "500 ml",
            "manufacturer": "Test Manufacturer",
            "manufacturer_address": "123 Test Road, Delhi",
            "importer": None,
            "importer_address": None,
            "country_of_origin": "India",
            "customer_care": "9876543210",
            "manufacturing_date": "08/2026",
            "expiry_date": None,
            "raw_text": "Test Product 500 ml MRP ₹40"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "inspection_id" in data
    assert "overall_status" in data
    assert "score" in data
    assert "checks" in data

    print("PASS: valid product")


def test_missing_mrp():

    response = client.post(
        "/inspect",
        json={
            "product_name": "Test Product",
            "brand": "Test Brand",
            "mrp": None,
            "net_quantity": "500 ml",
            "manufacturer": "Test Manufacturer",
            "manufacturer_address": "123 Test Road, Delhi",
            "importer": None,
            "importer_address": None,
            "country_of_origin": "India",
            "customer_care": "9876543210",
            "manufacturing_date": "08/2026",
            "expiry_date": None,
            "raw_text": "Test Product 500 ml"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["overall_status"] == "NON_COMPLIANT"
    assert data["failed_checks"] >= 1

    mrp_check = next(
        check
        for check in data["checks"]
        if check["field"] == "mrp"
    )

    assert mrp_check["status"] == "FAIL"
    assert mrp_check["rule_id"] == "LMPC-003"
    assert mrp_check["severity"] == "CRITICAL"

    print("PASS: missing MRP")


def test_missing_quantity():

    response = client.post(
        "/inspect",
        json={
            "product_name": "Test Product",
            "brand": "Test Brand",
            "mrp": "₹40",
            "net_quantity": None,
            "manufacturer": "Test Manufacturer",
            "manufacturer_address": "123 Test Road, Delhi",
            "importer": None,
            "importer_address": None,
            "country_of_origin": "India",
            "customer_care": "9876543210",
            "manufacturing_date": "08/2026",
            "expiry_date": None,
            "raw_text": "Test Product MRP ₹40"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["overall_status"] == "NON_COMPLIANT"
    assert data["failed_checks"] >= 1

    quantity_check = next(
        check
        for check in data["checks"]
        if check["field"] == "net_quantity"
    )

    assert quantity_check["status"] == "FAIL"
    assert quantity_check["rule_id"] == "LMPC-002"
    assert quantity_check["severity"] == "CRITICAL"

    print("PASS: missing quantity")


def test_invalid_mrp():

    response = client.post(
        "/inspect",
        json={
            "product_name": "Test Product",
            "brand": "Test Brand",
            "mrp": "forty rupees",
            "net_quantity": "500 ml",
            "manufacturer": "Test Manufacturer",
            "manufacturer_address": "123 Test Road, Delhi",
            "importer": None,
            "importer_address": None,
            "country_of_origin": "India",
            "customer_care": "9876543210",
            "manufacturing_date": "08/2026",
            "expiry_date": None,
            "raw_text": "Test Product"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["overall_status"] == "NON_COMPLIANT"
    assert data["failed_checks"] >= 1

    mrp_check = next(
        check
        for check in data["checks"]
        if check["field"] == "mrp"
    )

    assert mrp_check["status"] == "FAIL"
    assert mrp_check["rule_id"] == "LMPC-003"
    assert mrp_check["severity"] == "CRITICAL"

    print("PASS: invalid MRP")


if __name__ == "__main__":
    test_valid_product()
    test_missing_mrp()
    test_missing_quantity()
    test_invalid_mrp()

    print()
    print("====================================")
    print("STEP 14 END-TO-END TESTS PASSED")
    print("====================================")