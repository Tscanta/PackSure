from fastapi import FastAPI, HTTPException

from backend.database.services import (
    list_products,
    find_product,
    add_product,
    list_rules,
    find_rule,
    create_new_inspection,
    get_inspection,
    create_new_violation,
    get_violation,
    list_violations,
)

from backend.inspection.inspector import InspectionEngine
from backend.inspection.persistence import save_inspection_result

from schemas.product import (
    ProductInput,
    ProductCreate,
    ProductResponse,
)

from schemas.rule import RuleResponse

from schemas.inspection import (
    InspectionCreate,
    InspectionResponse,
    InspectionResult,
)

from schemas.violation import (
    ViolationCreate,
    ViolationResponse,
)


app = FastAPI(
    title="Legal Metrology Compliance System",
    description="API for checking packaged commodity compliance.",
    version="1.0.0"
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "Legal Metrology Compliance API is running!"
    }


# ============================================================
# GET ALL PRODUCTS
# ============================================================

@app.get("/products")
def get_products():
    products = list_products()
    return products


# ============================================================
# GET PRODUCT BY ID
# ============================================================

@app.get("/products/{product_id}")
def get_product(product_id: int):

    product = find_product(product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


# ============================================================
# CREATE PRODUCT
# ============================================================

@app.post(
    "/products",
    response_model=ProductResponse
)
def create_new_product(product: ProductCreate):

    try:

        new_product = add_product(
            product_name=product.product_name,
            category=product.category,
            brand=product.brand,
            manufacturer=product.manufacturer
        )

        return new_product

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


# ============================================================
# GET ALL RULES
# ============================================================

@app.get("/rules")
def get_rules():

    rules = list_rules()

    return rules


# ============================================================
# GET RULE BY RULE ID
# ============================================================

@app.get(
    "/rules/{rule_id}",
    response_model=RuleResponse
)
def get_rule(rule_id: str):

    rule = find_rule(rule_id)

    if rule is None:

        raise HTTPException(
            status_code=404,
            detail="Rule not found"
        )

    return rule


# ============================================================
# RUN COMPLIANCE INSPECTION
# ============================================================

@app.post(
    "/inspect",
    response_model=InspectionResult
)
def inspect_product(product: ProductInput):

    try:

        # --------------------------------------------------------
        # 1. CREATE PRODUCT RECORD
        # --------------------------------------------------------

        product_record = add_product(
            product_name=product.product_name or "Unknown Product",
            category="PACKAGED_COMMODITY",
            brand=product.brand,
            manufacturer=product.manufacturer
        )

        # --------------------------------------------------------
        # 2. GET DATABASE PRODUCT ID
        # --------------------------------------------------------

        if isinstance(product_record, dict):

            product_id = product_record["id"]

        else:

            product_id = product_record.id

        # --------------------------------------------------------
        # 3. RUN INSPECTION ENGINE
        # --------------------------------------------------------

        engine = InspectionEngine()

        result = engine.inspect(product)

        # --------------------------------------------------------
        # 4. SAVE INSPECTION + VIOLATIONS
        # --------------------------------------------------------

        save_inspection_result(
            product_id=product_id,
            inspection_result=result
        )

        # --------------------------------------------------------
        # 5. RETURN RESULT
        # --------------------------------------------------------

        return result

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Inspection failed: {str(error)}"
        )


# ============================================================
# CREATE INSPECTION MANUALLY
# ============================================================

@app.post(
    "/inspections",
    response_model=InspectionResponse
)
def create_inspection_endpoint(
    inspection: InspectionCreate
):

    try:

        new_inspection = create_new_inspection(
            product_id=inspection.product_id,
            overall_status=inspection.overall_status,
            confidence=inspection.confidence
        )

        return new_inspection

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


# ============================================================
# GET INSPECTION
# ============================================================

@app.get(
    "/inspections/{inspection_id}",
    response_model=InspectionResponse
)
def get_inspection_endpoint(inspection_id: int):

    inspection = get_inspection(inspection_id)

    if inspection is None:

        raise HTTPException(
            status_code=404,
            detail="Inspection not found"
        )

    return inspection


# ============================================================
# CREATE VIOLATION
# ============================================================

@app.post(
    "/violations",
    response_model=ViolationResponse
)
def create_violation_endpoint(
    violation: ViolationCreate
):

    try:

        new_violation = create_new_violation(
            inspection_id=violation.inspection_id,
            rule_id=violation.rule_id,
            status=violation.status,
            detected_value=violation.detected_value,
            expected_value=violation.expected_value,
            message=violation.message
        )

        return new_violation

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


# ============================================================
# GET VIOLATION
# ============================================================

@app.get(
    "/violations/{violation_id}",
    response_model=ViolationResponse
)
def get_violation_endpoint(violation_id: int):

    violation = get_violation(violation_id)

    if violation is None:

        raise HTTPException(
            status_code=404,
            detail="Violation not found"
        )

    return violation


# ============================================================
# GET VIOLATIONS FOR INSPECTION
# ============================================================

@app.get(
    "/inspections/{inspection_id}/violations"
)
def get_inspection_violations(inspection_id: int):

    inspection = get_inspection(inspection_id)

    if inspection is None:

        raise HTTPException(
            status_code=404,
            detail="Inspection not found"
        )

    return list_violations(inspection_id)