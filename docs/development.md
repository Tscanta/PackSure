# PackSho — Phase 1 Development Guide

## 1. Objective

Phase 1 establishes the technical foundation for the PackSho compliance system.

The development team works in parallel with the research team.

```text
Research Team
    ↓
Legal/compliance dataset

Coding Team
    ↓
Backend + database + rule engine

Integration
    ↓
Complete Phase 1 system
```

---

## 2. Team Division

### Developer 1 — Backend

Responsibilities:

1. Project setup
2. FastAPI setup
3. Database setup
4. Database models
5. API endpoints
6. Product endpoints
7. Inspection endpoints
8. Database/API integration
9. Final integration

### Developer 2 — Rule/Data

Responsibilities:

1. Rule-data format
2. Excel importer
3. Rule-data validation
4. Data transformation
5. Validators
6. Rule engine
7. Compliance result generation
8. Rule-engine tests

### Research Team

Responsibilities:

1. Find authoritative legal sources.
2. Identify mandatory requirements.
3. Identify conditional requirements.
4. Identify exceptions.
5. Categorize requirements.
6. Prepare the Excel rule dataset.
7. Provide source references.

---

## 3. Development Environment

Recommended stack:

```text
Python
FastAPI
Uvicorn
PostgreSQL
Pandas
OpenPyXL
Pydantic
Pytest
Git
GitHub
```

---

## 4. Initial Setup

Create the project:

```bash
mkdir legal-metrology-system
cd legal-metrology-system
```

Create virtual environment:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
venv\Scriptsctivate
```

Install dependencies:

```bash
pip install fastapi uvicorn pandas openpyxl sqlalchemy psycopg2-binary pytest
```

Save dependencies:

```bash
pip freeze > requirements.txt
```

---

## 5. Project Structure

Recommended structure:

```text
legal-metrology-system/
│
├── backend/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── rules.py
│   │   ├── products.py
│   │   └── inspections.py
│   │
│   ├── models/
│   │   ├── rule.py
│   │   ├── product.py
│   │   └── inspection.py
│   │
│   ├── services/
│   │   ├── rule_service.py
│   │   ├── compliance_service.py
│   │   └── inspection_service.py
│   │
│   ├── validators/
│   │   ├── text_validator.py
│   │   ├── quantity_validator.py
│   │   ├── currency_validator.py
│   │   └── date_validator.py
│   │
│   └── database/
│       ├── connection.py
│       ├── models.py
│       └── setup.py
│
├── data/
│   ├── compliance_rules.xlsx
│   └── sample_products.xlsx
│
├── tests/
│
├── docs/
│   ├── architecture.md
│   ├── database.md
│   ├── api.md
│   └── development.md
│
├── requirements.txt
└── README.md
```

---

## 6. Parallel Development Plan

### Developer 1

```text
Project setup
    ↓
Database
    ↓
Database models
    ↓
FastAPI
    ↓
API routes
    ↓
Database integration
```

### Developer 2

```text
Mock rules
    ↓
Excel reader
    ↓
Excel validation
    ↓
Rule importer
    ↓
Validators
    ↓
Rule engine
```

Both developers use the agreed data schema.

---

## 7. Use Mock Data

Do not wait for the research team to finish.

Developer 2 can initially use temporary rules:

```text
TEST001
Product name must exist

TEST002
Net quantity must exist

TEST003
MRP must exist
```

These are development rules only.

They must be clearly separated from authoritative legal rules.

---

## 8. Git Workflow

Each developer should work on a separate branch.

Example:

```text
main
│
├── feature/backend
│
└── feature/rule-engine
```

Developer 1:

```bash
git checkout -b feature/backend
```

Developer 2:

```bash
git checkout -b feature/rule-engine
```

Commit frequently with meaningful messages.

Examples:

```text
Add database connection
Create rule model
Add rules API
Implement Excel importer
Add text validator
Implement compliance engine
Add inspection tests
```

---

## 9. Integration Rules

Before merging:

- Pull the latest `main`.
- Resolve conflicts locally.
- Run all tests.
- Confirm the agreed schema has not changed unexpectedly.
- Test the API.
- Test rule import.
- Test the rule engine.

Integration should happen only after each independent component works.

---

## 10. End-to-End Test

Use a simple test product:

```json
{
  "product_name": "ABC Biscuits",
  "net_quantity": "100 g",
  "mrp": "₹20",
  "manufacturer": "ABC Foods",
  "address": "Hyderabad"
}
```

Run the inspection.

Expected conceptual flow:

```text
POST /inspections
       ↓
Load product
       ↓
Load rules
       ↓
Rule Engine
       ↓
Validators
       ↓
Results
       ↓
PASS / FAIL / REVIEW
```

---

## 11. Negative Testing

The system must also be tested with incomplete data.

Example:

```json
{
  "product_name": "ABC Biscuits",
  "net_quantity": "100 g",
  "mrp": "₹20",
  "manufacturer": "ABC Foods",
  "address": null
}
```

Expected:

```text
Manufacturer address rule
        ↓
FAIL
```

The system should explain the failure rather than simply returning `false`.

---

## 12. Important Engineering Rule

Do not hard-code the legal requirements into the application unless there is a deliberate reason to do so.

Prefer:

```text
Rule Dataset
     ↓
Database
     ↓
Rule Engine
```

over:

```text
Python source code
     ↓
500 hard-coded legal conditions
```

The first approach allows the legal dataset to evolve without rewriting the entire application.

---

## 13. Phase 1 Definition of Done

### Backend

- [ ] Application starts
- [ ] Database connects
- [ ] Models work
- [ ] API routes work
- [ ] Product data can be stored
- [ ] Inspection can be created

### Rule/Data

- [ ] Excel can be read
- [ ] Required columns are validated
- [ ] Invalid rows are rejected
- [ ] Rules can be imported
- [ ] Validators work
- [ ] Rule engine produces results

### Integration

- [ ] Database and rule engine communicate
- [ ] API can trigger an inspection
- [ ] Results are stored
- [ ] Violations are returned
- [ ] Tests pass

### Documentation

- [ ] Architecture documented
- [ ] Database documented
- [ ] API documented
- [ ] Development process documented

---

## 14. Phase 1 Final Architecture

The completed Phase 1 system should conceptually operate as:

```text
              RESEARCH DATA
                    │
                    ↓
            compliance_rules.xlsx
                    │
                    ↓
              RULE IMPORTER
                    │
                    ↓
                DATABASE
                    │
          ┌─────────┴─────────┐
          ↓                   ↓
       PRODUCTS             RULES
          │                   │
          └─────────┬─────────┘
                    ↓
               RULE ENGINE
                    │
                    ↓
             COMPLIANCE RESULT
                    │
          ┌─────────┴─────────┐
          ↓                   ↓
        PASS                 FAIL
                              │
                              ↓
                         VIOLATION
                         + EXPLANATION
```

This foundation is intentionally designed so that the next phase can replace manually entered product fields with OCR/AI-extracted fields without rebuilding the compliance system from scratch.
