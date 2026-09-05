from io import BytesIO
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

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
from extraction.adapter import to_product_input
from extraction.normalizer import normalize_text
from extraction.ocr import extract_text_from_image
from extraction.parser import extract_product_data

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development only: do not combine with auth.
    allow_methods=["*"],
    allow_headers=["*"],
)


def _run_inspection(product: ProductInput):
    """Persist a product, run the deterministic engine, and save failures."""
    product_record = add_product(
        product_name=product.product_name or "Unknown Product",
        category=product.product_category or "PACKAGED_COMMODITY",
        brand=product.brand,
        manufacturer=product.manufacturer,
    )
    product_id = product_record["id"] if isinstance(product_record, dict) else product_record.id
    result = InspectionEngine().inspect(product)
    save_inspection_result(product_id=product_id, inspection_result=result)
    return result


async def _extract_uploaded_product(file: UploadFile):
    """Read an uploaded image in memory and return OCR plus parsed data."""
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=415, detail="Upload a PNG, JPEG, or other image file.")
    image_data = await file.read()
    if not image_data:
        raise HTTPException(status_code=422, detail="The uploaded image is empty.")
    if len(image_data) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Image must be 10 MB or smaller.")
    try:
        raw_text = extract_text_from_image(BytesIO(image_data))
    except Exception as error:
        raise HTTPException(status_code=422, detail=f"OCR could not read the image: {error}") from error
    normalized_text = normalize_text(raw_text)
    return raw_text, normalized_text, extract_product_data(normalized_text)


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

        return _run_inspection(product)

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


@app.post("/extract")
async def extract_package_data(file: UploadFile = File(...)):
    """OCR a package image and return raw text plus parsed declarations."""
    raw_text, normalized_text, extracted_product = await _extract_uploaded_product(file)
    return {
        "raw_text": raw_text,
        "normalized_text": normalized_text,
        "product": extracted_product.model_dump(mode="json"),
    }


@app.post("/inspect/image", response_model=InspectionResult)
async def inspect_package_image(
    file: UploadFile = File(...),
    product_name: str | None = Form(None),
    manufacturer: str | None = Form(None),
    net_quantity: str | None = Form(None),
    mrp: str | None = Form(None),
    product_category: str | None = Form(None),
    batch_number: str | None = Form(None),
    manufacturing_date: str | None = Form(None),
):
    """OCR a package image, merge supplied values, and inspect it."""
    raw_text, _normalized_text, extracted_product = await _extract_uploaded_product(file)
    product = to_product_input(extracted_product)
    manual_values = {
        "product_name": product_name, "manufacturer": manufacturer,
        "net_quantity": net_quantity, "mrp": mrp,
        "product_category": product_category, "batch_number": batch_number,
        "manufacturing_date": manufacturing_date,
    }
    product = product.model_copy(update={key: value for key, value in manual_values.items() if value})
    try:
        result = _run_inspection(product)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Inspection failed: {error}") from error
    payload = result.model_dump()
    payload["ocr_text"] = raw_text
    payload["extracted_product"] = extracted_product.model_dump(mode="json")
    return payload


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


_frontend_dir = Path(__file__).resolve().parents[1] / "PackSure Frontend"
if _frontend_dir.is_dir():
    app.mount("/app", StaticFiles(directory=_frontend_dir, html=True), name="packsure-frontend")
