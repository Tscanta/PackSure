![Version](https://img.shields.io/badge/version-v0.1.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-yellow)
![Platform](https://img.shields.io/badge/platform-Windows-blue)
![License](https://img.shields.io/badge/license-MIT-green)

<img width="130" height="130" alt="logo" src="https://github.com/user-attachments/assets/f05366e1-d7f3-46f4-823d-1ec5c5cae93d" />

# PackSure

> An automated compliance inspection and evidence management system for packaged commodities under Legal Metrology regulations.

PackSure is a digital inspection platform designed to assist enforcement officials and compliance teams in checking packaged commodities against applicable Legal Metrology requirements.

The system combines package image analysis, OCR, structured product information, regulatory rules, automated validation, inspection records, evidence, and reporting into a single workflow.

PackSure is designed to make compliance inspection faster, more consistent, explainable, and traceable while keeping regulatory requirements separate from application logic.

---

# Overview

PackSure allows an inspector to inspect packaged commodities by providing product information or uploading an image of a package.

The system can extract information from package images using OCR, convert the extracted information into structured product data, identify applicable compliance requirements, and evaluate the product using a rule-based compliance engine.

The resulting inspection can contain:

- Compliance status
- Detected product information
- Regulatory findings
- Potential violations
- Applicable rules
- Detected values
- Expected conditions
- Severity
- Explanations
- Inspection records
- Supporting evidence

The system also provides a web interface for viewing inspections, products, evidence, reports, analytics, and regulatory rules.

---

# Core Features

## Automated Package Inspection

PackSure supports inspection from package images.

The image inspection workflow performs:

1. Image upload
2. Image validation
3. OCR text extraction
4. Text normalization
5. Product information extraction
6. Product data construction
7. Regulatory rule evaluation
8. Compliance result generation
9. Inspection persistence

This allows inspectors to move from a physical package image to a structured compliance assessment without manually entering every field.

---

## OCR and Product Information Extraction

PackSure integrates OCR-based text extraction to process information printed on product packaging.

Extracted text can be processed to identify structured product information such as:

- Product name
- Manufacturer details
- Net quantity
- Maximum Retail Price
- Dates
- Addresses
- Other package declarations

The extraction layer is kept separate from the compliance engine so that OCR and information-extraction methods can be improved without changing the core regulatory validation system.

---

# Compliance Rule Engine

PackSure uses a structured, data-driven rule engine to evaluate products against regulatory requirements.

Regulatory requirements are represented as structured rules rather than being hard-coded throughout the application.

The general evaluation process is:

```text
Product Data
     |
     v
Applicable Regulatory Rules
     |
     v
Validator
     |
     v
Compliance Evaluation
     |
     v
PASS / FAIL / REVIEW
