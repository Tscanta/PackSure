![Version](https://img.shields.io/badge/version-v0.1.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-yellow)
![Platform](https://img.shields.io/badge/platform-Windows-blue)
![License](https://img.shields.io/badge/license-MIT-green)

<img width="130" height="130" alt="logo" src="https://github.com/user-attachments/assets/f05366e1-d7f3-46f4-823d-1ec5c5cae93d" />

# 📦 PackSure

> An automated compliance inspection system for packaged commodities under Legal Metrology regulations.

PackSure is a software system designed to assist enforcement officials in checking packaged commodities against applicable Legal Metrology requirements.


The system combines structured product information, regulatory rules, automated validation, and inspection records to make compliance inspection faster, more consistent, explainable, and traceable.

---

# Version: v0.1.0

PackSure is currently under active development.

The current implementation focuses on establishing the core compliance infrastructure, including the backend API, database models, regulatory rule storage, rule importing, reusable validators, and the compliance rule engine.

Future phases will extend this foundation with package-image analysis, OCR, product information extraction, and intelligent inspection workflows.

---

# Features

## Compliance Management

- Structured regulatory rule storage
- Product and commodity management
- Rule-based compliance engine
- Reusable compliance validators
- Automated compliance evaluation
- PASS / FAIL / REVIEW results
- Potential violation identification
- Explainable compliance findings
- Inspection records and history

## Regulatory Data

- Excel-based regulatory rule import
- Rule validation before database insertion
- Structured rule representation
- Category-specific compliance requirements
- Versionable and maintainable regulatory data

## API

- REST API built with FastAPI
- Product management endpoints
- Regulatory rule endpoints
- Inspection endpoints
- Structured API responses

## Intelligent Inspection

Planned / integration features:

- Package image upload
- OCR-based text extraction
- Image preprocessing
- Product information extraction
- Barcode / GTIN integration
- Product classification
- Automated package analysis

---

# How It Works

PackSure separates product-information extraction from regulatory compliance validation.

The current core workflow is:

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

The future inspection workflow extends this into:

Product Image
↓
OCR / Computer Vision
↓
Extracted Product Fields
↓
Product Identification
↓
Applicable Regulatory Rules
↓
Compliance Rule Engine
↓
Compliance Report

This architecture allows future OCR and AI components to plug into the existing compliance infrastructure without rebuilding the core compliance engine.

---

# Compliance Engine

PackSure uses a structured, data-driven rule engine to evaluate packaged commodities against applicable regulatory requirements.

Instead of embedding every legal requirement directly into application code, regulatory requirements are represented as structured rules that can be imported, stored, validated, and executed by the compliance engine.

Product Information
+
Applicable Rule
↓
Validator
↓
PASS / FAIL / REVIEW

The current validation framework supports reusable validators such as:

- TEXT_EXISTS
- QUANTITY
- CURRENCY
- DATE
- ADDRESS

Additional validator types can be introduced without rewriting the entire rule engine.

A compliance finding is designed to be explainable and can include:

- Rule ID
- Requirement
- Detected value
- Expected condition
- Severity
- Explanation

---

# How the Rule Pipeline Works

Regulatory Rules
↓
Excel Dataset
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

The rule importer converts the research team's regulatory dataset into structured database records.

Malformed or incomplete rule records are rejected instead of being silently inserted.


# 🛠 Tech Stack

## Languages

- Python

## Backend

- FastAPI
- Uvicorn

## Data & Rule Processing

- Excel
- JSON
- Database persistence
- Structured regulatory rules
- Reusable validators
- Compliance rule engine

## Planned Technologies

- OCR
- Computer Vision
- Barcode / GTIN processing
- Product classification
- Web / mobile inspection interface

---

# API

PackSure provides a REST API that allows applications to interact with products, regulatory rules, and inspections.

Example endpoints:

GET /rules
GET /rules/{rule_id}

POST /products
GET /products/{product_id}

POST /inspections
GET /inspections/{inspection_id}

The API acts as the integration layer between the compliance engine and future web or mobile inspection interfaces.

---

# Architecture

The system follows a modular architecture built around four core layers:

1. Data Layer
   - Products
   - Regulatory rules
   - Inspections
   - Compliance results
   - Violations

2. Rule Processing Layer
   - Excel rule importer
   - Rule validation
   - Rule transformation

3. Compliance Layer
   - Rule engine
   - Reusable validators
   - Compliance result generation

4. API Layer
   - FastAPI
   - Request validation
   - Database interaction
   - Structured API responses

This separation of concerns allows individual components to evolve independently.

---

# Design Principles

### Separation of Concerns

Each component has a clearly defined responsibility.

### Data-Driven Rules

Regulatory requirements should primarily exist as structured data rather than being buried inside application code.

### Explainability

Every failed check should provide the relevant rule, detected value, expected condition, severity, and explanation wherever available.

### Extensibility

The architecture is designed to allow new rules, validators, product categories, API endpoints, and AI/OCR components to be added without major restructuring.

### Testability

Core compliance logic should be independently testable from the API and database.

---

# VISION

PackSure aims to become a digital compliance inspection platform that helps enforcement officials inspect packaged commodities faster, more consistently, and with better traceability.

The long-term vision is to combine:

Computer Vision
→ OCR
→ Information Extraction
→ Product Identification
→ Regulatory Rules
→ Compliance Validation
→ Evidence
→ Reporting

The goal is not to replace regulatory authorities, but to provide them with an intelligent inspection-assistance system that reduces repetitive manual work and improves the consistency and explainability of compliance checks.

---

# CONTRIBUTING

Contributions, ideas, feature requests, and bug reports are welcome.

Feel free to fork the project, open an issue, or submit a pull request.

For larger changes, please discuss the proposed architecture or implementation approach before submitting a pull request.

---

# 📄 LICENSE

This project is licensed under the MIT License.
