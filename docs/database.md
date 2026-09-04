# PackSho — Phase 1 Database Documentation

## 1. Purpose

The database stores the structured information required by the PackSho compliance system.

The database must separate:

- Legal/compliance rules
- Products
- Inspections
- Compliance results
- Violations

This prevents legal rules from being mixed with individual inspection records.

---

## 2. Core Entities

```text
RULE
 │
 │ applied during
 ↓
INSPECTION
 │
 ├── produces → COMPLIANCE RESULT
 │
 └── produces → VIOLATION

PRODUCT
 │
 └── inspected through → INSPECTION
```

---

## 3. Rules Table

The `rules` table stores the machine-readable compliance requirements supplied by the research team.

Suggested fields:

| Field | Type | Description |
|---|---|---|
| id | Integer | Internal primary key |
| rule_id | String | Unique legal/rule identifier |
| category | String | Rule category |
| requirement | Text | Short description of requirement |
| description | Text | Detailed explanation |
| mandatory | Boolean | Whether the declaration/check is mandatory |
| validation_type | String | Validator used by the rule engine |
| severity | String | Severity of failure |
| source | Text | Legal source/reference |
| effective_date | Date | Date from which the rule applies |
| active | Boolean | Whether the rule is currently active |

Example:

```text
rule_id: LM001
category: Product
requirement: Product name must be declared
mandatory: true
validation_type: TEXT_EXISTS
severity: HIGH
```

---

## 4. Products Table

The `products` table stores product information submitted for inspection.

Suggested fields:

| Field | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| product_name | String | Product name |
| category | String | Product category |
| brand | String | Brand name |
| manufacturer | String | Manufacturer/packer |
| address | Text | Manufacturer/packer address |
| net_quantity | String | Declared net quantity |
| mrp | String/Numeric | Declared MRP |
| created_at | DateTime | Creation timestamp |

The exact schema can be expanded when OCR is introduced.

---

## 5. Inspections Table

An inspection represents one compliance-checking event.

Suggested fields:

| Field | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| product_id | Integer | Product being inspected |
| inspection_date | DateTime | Time of inspection |
| overall_status | String | Overall compliance status |

Possible statuses:

```text
COMPLIANT
NON_COMPLIANT
REVIEW
```

`REVIEW` is useful when the system cannot make a reliable determination.

---

## 6. Compliance Results Table

This table stores the result of applying an individual rule during an inspection.

Suggested fields:

| Field | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| inspection_id | Integer | Related inspection |
| rule_id | Integer/String | Rule evaluated |
| status | String | PASS/FAIL/REVIEW |
| detected_value | Text | Value found in product data |
| expected_value | Text | Expected condition |
| confidence | Float | Optional confidence score |
| message | Text | Explanation |

Example:

```text
Rule: LM004
Status: FAIL
Detected value: NULL
Expected value: Manufacturer address
Message: Manufacturer address is missing.
```

---

## 7. Violations Table

A violation records a failed compliance requirement.

Suggested fields:

| Field | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| inspection_id | Integer | Related inspection |
| rule_id | Integer/String | Violated rule |
| severity | String | Violation severity |
| description | Text | Explanation |
| recommendation | Text | Suggested corrective action |

This allows a single inspection to contain multiple violations.

---

## 8. Relationships

```text
PRODUCT
   │
   │ 1:N
   ↓
INSPECTION
   │
   ├──────────────┐
   │              │
   │ 1:N          │ 1:N
   ↓              ↓
COMPLIANCE      VIOLATION
RESULT
   │
   │ references
   ↓
 RULE
```

A product can have many inspections.

An inspection can evaluate many rules.

An inspection can produce many violations.

---

## 9. Database Rules

### Rule IDs must be unique

Two different records should not use the same `rule_id`.

### Required fields must not be empty

At minimum:

```text
rule_id
category
requirement
mandatory
validation_type
severity
```

### Foreign keys must be valid

An inspection cannot reference a product that does not exist.

A compliance result cannot reference an invalid inspection.

### Do not store legal rules only in source code

The database should remain the source used by the runtime rule engine.

---

## 10. Example End-to-End Record

### Product

```text
Product:
ABC Biscuits

Quantity:
100 g

MRP:
₹20

Manufacturer:
ABC Foods

Address:
NULL
```

### Inspection

```text
Inspection ID:
101

Product ID:
20

Overall Status:
NON_COMPLIANT
```

### Result

```text
Rule:
LM004

Status:
FAIL

Detected:
NULL

Expected:
Manufacturer address
```

### Violation

```text
Severity:
HIGH

Description:
Manufacturer address is missing.
```

---

## 11. Future Database Extensions

Later phases may add:

- Image records
- OCR text
- OCR confidence
- Extracted fields
- Product batches
- QR/barcode information
- User accounts
- Inspection locations
- Audit history
- Rule versions
- AI review records

These should be added without breaking the Phase 1 structure.
