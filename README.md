![Version](https://img.shields.io/badge/version-v0.1.0-blue) ![Python](https://img.shields.io/badge/python-3.11+-yellow) ![Platform](https://img.shields.io/badge/platform-Windows-blue) ![License](https://img.shields.io/badge/license-MIT-green)

<img width="130" height="130" alt="logo" src="https://github.com/user-attachments/assets/f05366e1-d7f3-46f4-823d-1ec5c5cae93d" />

# PackSure

> An automated compliance inspection system for packaged commodities under Legal Metrology regulations.

PackSure assists enforcement officials in checking packaged commodities against applicable Legal Metrology requirements. It combines structured product information, regulatory rules, automated validation, and inspection records to make compliance inspection faster, more consistent, explainable, and traceable.

---

# What It Does

PackSure separates product-information handling from regulatory compliance validation:

```
Product Data
    ↓
FastAPI Backend
    ↓
Database
    ↓
Compliance Rule Engine
    ↓
Compliance Result
    ↓
API Response
```

Regulatory requirements are represented as structured, importable rules rather than being hard-coded into the application. A rule engine evaluates product data against these rules and returns explainable PASS / FAIL / REVIEW results.

```
Product Information + Applicable Rule
    ↓
Validator
    ↓
PASS / FAIL / REVIEW
```

The rule importer converts a regulatory dataset (maintained in Excel) into structured database records, rejecting malformed or incomplete entries instead of silently inserting them:

```
Regulatory Rules (Excel)
    ↓
Rule Importer
    ↓
Validation
    ↓
Database
    ↓
Rule Engine
    ↓
Compliance Result
```

---

# Features

## Compliance Management
- Structured regulatory rule storage
- Product and commodity management
- Rule-based compliance engine
- Reusable compliance validators
- Automated compliance evaluation with PASS / FAIL / REVIEW results
- Potential violation identification
- Explainable compliance findings
- Inspection records and history

## Regulatory Data
- Excel-based regulatory rule import
- Rule validation before database insertion
- Structured, versionable, and maintainable rule representation
- Category-specific compliance requirements

## API
REST API built with FastAPI:

```
GET  /rules
GET  /rules/{rule_id}
POST /products
GET  /products/{product_id}
POST /inspections
GET  /inspections/{inspection_id}
```

The API is the integration layer between the compliance engine and any future web or mobile inspection interface.

## Compliance Engine
Reusable validator types currently supported:
- TEXT_EXISTS
- QUANTITY
- CURRENCY
- DATE
- ADDRESS

A compliance finding is designed to be explainable, and can include:
- Rule ID
- Requirement
- Detected value
- Expected condition
- Severity
- Explanation

Additional validator types can be added without rewriting the rule engine.

---

# Architecture

The system is organized into four layers:

1. **Data Layer** — products, regulatory rules, inspections, compliance results, violations
2. **Rule Processing Layer** — Excel rule importer, rule validation, rule transformation
3. **Compliance Layer** — rule engine, reusable validators, compliance result generation
4. **API Layer** — FastAPI, request validation, database interaction, structured API responses

This separation lets each component evolve independently — for example, adding OCR or computer-vision components later without rebuilding the compliance engine.

---

# Design Principles

- **Separation of concerns** — each component has a clearly defined responsibility
- **Data-driven rules** — regulatory requirements exist primarily as structured data, not application code
- **Explainability** — every failed check reports the relevant rule, detected value, expected condition, severity, and explanation
- **Extensibility** — new rules, validators, product categories, and API endpoints can be added without major restructuring
- **Testability** — core compliance logic is testable independently of the API and database

---

# Tech Stack

**Languages:** Python

**Backend:** FastAPI, Uvicorn

**Data & Rule Processing:** Excel, JSON, database persistence, structured regulatory rules, reusable validators, compliance rule engine

---

# Future Improvements

- Package image upload and OCR-based text extraction
- Image preprocessing for scanned/photographed packaging
- Automated product information extraction from package images
- Barcode / GTIN integration for product identification
- Product classification
- A web or mobile interface for inspectors, built on the existing API

The long-term goal is an inspection-assistance pipeline: computer vision → OCR → information extraction → product identification → regulatory rule matching → compliance validation → evidence → reporting. This does not replace regulatory authorities — it reduces repetitive manual work and improves the consistency and explainability of compliance checks.

---

# Contributing

Contributions, ideas, feature requests, and bug reports are welcome. Fork the project, open an issue, or submit a pull request. For larger changes, please discuss the proposed architecture or approach before submitting a PR.

---

# License

This project is licensed under the MIT License.
