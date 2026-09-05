"""Offline coverage for the database-backed rule evaluator's operators."""

from backend.inspection.field_validator import evaluate_rule
from schemas.product import ProductInput


def test_supported_operators_and_not_applicable_rule():
    product = ProductInput(
        product_name="Tea",
        mrp="50",
        ingredients="tea, sugar",
        product_type="food",
    )
    cases = [
        ({"field": "product_name", "operator": "REQUIRED"}, "PASS"),
        ({"field": "product_name", "operator": "EQUALS", "value": "Tea"}, "PASS"),
        ({"field": "product_type", "operator": "IN", "value": ["food"]}, "PASS"),
        ({"field": "mrp", "operator": "REGEX", "value": r"^\d+$"}, "PASS"),
        ({"field": "mrp", "operator": "MIN", "value": 40}, "PASS"),
        ({"field": "mrp", "operator": "MAX", "value": 60}, "PASS"),
        ({"field": "ingredients", "operator": "CONTAINS", "value": "sugar"}, "PASS"),
        ({"field": "mrp", "operator": "MIN", "value": 60}, "FAIL"),
        ({"field": "importer", "operator": "REQUIRED", "applicability": {"is_imported": True}}, "NOT_APPLICABLE"),
    ]

    for rule, expected_status in cases:
        assert evaluate_rule(product, rule).status == expected_status


def test_malformed_values_fail_without_raising():
    product = ProductInput(mrp="not a number")
    result = evaluate_rule(product, {"field": "mrp", "operator": "MIN", "value": "bad"})
    assert result.status == "FAIL"

    result = evaluate_rule(product, {"field": "mrp", "operator": "REGEX", "value": "["})
    assert result.status == "FAIL"
