# PackSho — Phase 1 API Documentation

## 1. Purpose

The API provides the interface between the frontend and the PackSho backend.

Technology:

- Python
- FastAPI
- Uvicorn

The API is responsible for receiving requests, validating data, calling services, and returning structured responses.

---

## 2. Base URL

Development:

```text
http://127.0.0.1:8000
```

FastAPI automatically provides interactive API documentation at:

```text
/docs
```

---

## 3. Health Check

### `GET /`

Checks whether the backend is running.

Example response:

```json
{
  "message": "Legal Metrology Compliance System"
}
```

---

## 4. Rules

### `GET /rules`

Returns all active compliance rules.

Example response:

```json
[
  {
    "rule_id": "LM001",
    "category": "Product",
    "requirement": "Product name must be declared",
    "mandatory": true,
    "validation_type": "TEXT_EXISTS",
    "severity": "HIGH"
  }
]
```

---

### `GET /rules/{rule_id}`

Returns one rule.

Example:

```text
GET /rules/LM001
```

Possible responses:

- `200` — Rule found
- `404` — Rule not found

---

## 5. Products

### `POST /products`

Creates a product record.

Example request:

```json
{
  "product_name": "ABC Biscuits",
  "category": "Food",
  "brand": "ABC",
  "manufacturer": "ABC Foods",
  "address": "Hyderabad",
  "net_quantity": "100 g",
  "mrp": "₹20"
}
```

The backend validates the request before storing it.

---

### `GET /products/{product_id}`

Returns one stored product.

Possible responses:

- `200` — Product found
- `404` — Product not found

---

## 6. Inspections

### `POST /inspections`

Creates a compliance inspection.

Conceptual request:

```json
{
  "product_id": 20
}
```

The backend:

```text
Product
   ↓
Retrieve applicable rules
   ↓
Rule Engine
   ↓
Evaluate rules
   ↓
Store results
   ↓
Return overall result
```

Example response:

```json
{
  "inspection_id": 101,
  "status": "NON_COMPLIANT",
  "violations": [
    {
      "rule_id": "LM004",
      "severity": "HIGH",
      "message": "Manufacturer address is missing."
    }
  ]
}
```

---

### `GET /inspections/{inspection_id}`

Returns a previous inspection and its results.

Example:

```json
{
  "inspection_id": 101,
  "product_id": 20,
  "status": "NON_COMPLIANT",
  "results": [
    {
      "rule_id": "LM001",
      "status": "PASS"
    },
    {
      "rule_id": "LM004",
      "status": "FAIL"
    }
  ]
}
```

---

## 7. HTTP Status Codes

Use standard HTTP status codes.

| Code | Meaning |
|---|---|
| 200 | Successful request |
| 201 | Resource created |
| 400 | Invalid request |
| 404 | Resource not found |
| 422 | Validation error |
| 500 | Unexpected server error |

---

## 8. API Design Rules

### Keep business logic out of route functions

Bad:

```python
@app.post("/inspections")
def inspect():
    # hundreds of lines of compliance logic
```

Better:

```python
@app.post("/inspections")
def inspect():
    return inspection_service.inspect_product(...)
```

The route should coordinate the request, not contain the entire application.

---

## 9. Suggested Backend Structure

```text
backend/
│
├── main.py
│
├── api/
│   ├── rules.py
│   ├── products.py
│   └── inspections.py
│
├── models/
│   ├── rule.py
│   ├── product.py
│   └── inspection.py
│
├── services/
│   ├── rule_service.py
│   ├── product_service.py
│   └── inspection_service.py
│
└── database/
    ├── connection.py
    └── models.py
```

---

## 10. Future API Extensions

Later phases can add endpoints for:

```text
POST /images
POST /ocr
GET /ocr/{id}
POST /compliance/analyze
GET /reports/{id}
POST /products/{id}/images
```

These should consume the existing compliance infrastructure rather than duplicate it.
