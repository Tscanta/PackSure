# PackSho — Phase 1 Architecture

## 1. Purpose

This document describes the basic software architecture of the PackSho Legal Metrology packaged-commodity compliance system.

Phase 1 focuses on building the foundation that will later receive product information extracted from packaging images.

The Phase 1 flow is:

```text
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

The research team independently prepares the legal/compliance rules in an Excel dataset. The coding team provides the software infrastructure required to import, store, retrieve, and execute those rules.

---

## 2. Phase 1 Scope

### Included

- Backend project structure
- FastAPI application
- Database structure
- Compliance-rule storage
- Excel rule-data import
- Rule validation
- Basic rule engine
- Product data model
- Inspection data model
- Compliance result generation
- Unit testing
- API documentation

### Not included yet

- OCR
- Computer vision
- Automatic package-image analysis
- Advanced AI interpretation
- Production mobile application
- Production deployment
- Hardware-based authenticity verification

These can be added in later phases.

---

## 3. High-Level Architecture

```text
                    ┌───────────────────┐
                    │   Research Team   │
                    │ Legal Rules Excel │
                    └─────────┬─────────┘
                              │
                              ↓
                    ┌───────────────────┐
                    │   Rule Importer   │
                    └─────────┬─────────┘
                              │
                              ↓
                    ┌───────────────────┐
                    │     Database      │
                    │                   │
                    │ Rules             │
                    │ Products          │
                    │ Inspections       │
                    │ Violations        │
                    └─────────┬─────────┘
                              │
                              ↓
                    ┌───────────────────┐
                    │    Rule Engine    │
                    └─────────┬─────────┘
                              │
                              ↓
                    ┌───────────────────┐
                    │ Compliance Result │
                    └─────────┬─────────┘
                              │
                              ↓
                    ┌───────────────────┐
                    │    FastAPI API    │
                    └───────────────────┘
```

---

## 4. Main Components

### 4.1 FastAPI Backend

The backend exposes API endpoints that allow other parts of the application to interact with the compliance system.

Responsibilities:

- Receive requests
- Validate request data
- Call application services
- Read/write database data
- Return structured responses

---

### 4.2 Database

The database is the persistent storage layer.

It stores:

- Compliance rules
- Product information
- Inspection records
- Compliance results
- Violations

The database should remain independent from the API and rule-engine implementation.

---

### 4.3 Rule Importer

The importer converts the research team's Excel spreadsheet into database records.

```text
Excel
 ↓
Read
 ↓
Validate
 ↓
Transform
 ↓
Insert/Update Database
```

The importer must reject malformed or incomplete rule records instead of silently inserting invalid data.

---

### 4.4 Rule Engine

The rule engine determines whether a product satisfies applicable compliance requirements.

Conceptually:

```text
Product + Rule
      ↓
Validator
      ↓
PASS / FAIL / REVIEW
```

The engine should use reusable validators rather than hard-coding hundreds of unrelated conditions.

---

### 4.5 Validators

Validators perform specific types of checks.

Examples:

- `TEXT_EXISTS`
- `QUANTITY`
- `CURRENCY`
- `DATE`
- `ADDRESS`

New validator types can be added without rewriting the entire rule engine.

---

## 5. Data Flow

### Current Phase 1 flow

```text
Research Excel
      ↓
Rule Importer
      ↓
Database
      ↓
Product submitted through API
      ↓
Rule Engine
      ↓
Compliance Results
      ↓
API response
```

### Future flow

```text
Product Image
      ↓
OCR / Computer Vision
      ↓
Extracted Product Fields
      ↓
Phase 1 Compliance Engine
      ↓
Compliance Report
```

This separation allows future OCR/AI components to plug into the existing compliance infrastructure.

---

## 6. Design Principles

### Separation of concerns

Each component should have one clear responsibility.

### Data-driven rules

Legal requirements should primarily live in structured data rather than being buried inside source code.

### Explainability

A failed check should identify:

- Rule ID
- Requirement
- Detected value
- Expected condition
- Severity
- Explanation

### Extensibility

The architecture should allow new:

- Rules
- Validators
- Product categories
- API endpoints
- AI/OCR components

without major restructuring.

### Testability

Core compliance logic must be testable independently from the API and database.

---

## 7. Team Responsibilities

### Backend Developer

- Project setup
- Database
- Database models
- FastAPI application
- API endpoints
- Database/API integration
- Final integration

### Rule/Data Developer

- Excel importer
- Rule-data validation
- Validation functions
- Rule engine
- Compliance result generation

### Research Team

- Identify applicable legal requirements
- Interpret requirements
- Identify exceptions
- Prepare structured rule dataset
- Provide authoritative sources

---

## 8. Integration Contract

The research team and coding team must agree on a stable rule schema.

Minimum fields:

```text
rule_id
category
requirement
mandatory
validation_type
severity
source
```

Changes to this schema should be communicated to both coding tracks before implementation.

---

## 9. Phase 1 Completion Criteria

Phase 1 is considered technically complete when:

- The backend starts successfully.
- Database tables are created.
- Rules can be imported.
- Invalid rule data is detected.
- Rules can be retrieved through the API.
- A product can be submitted.
- The rule engine can evaluate applicable rules.
- Compliance results are generated.
- Violations are explainable.
- Automated tests pass.
- Documentation is available.
