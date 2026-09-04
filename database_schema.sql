-- ============================================================
-- PACKSHO DATABASE SCHEMA
-- ============================================================

-- ============================================================
-- PRODUCTS
-- ============================================================

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,

    product_name VARCHAR(255) NOT NULL,

    category VARCHAR(100),

    brand VARCHAR(255),

    manufacturer VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- RULES
-- ============================================================

CREATE TABLE IF NOT EXISTS rules (
    id SERIAL PRIMARY KEY,

    rule_id VARCHAR(100) NOT NULL UNIQUE,

    category VARCHAR(100) NOT NULL,

    requirement TEXT NOT NULL,

    description TEXT,

    mandatory BOOLEAN NOT NULL DEFAULT TRUE,

    validation_type VARCHAR(100),

    severity VARCHAR(20),

    source TEXT,

    effective_date DATE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- INSPECTIONS
-- ============================================================

CREATE TABLE IF NOT EXISTS inspections (
    id SERIAL PRIMARY KEY,

    product_id INTEGER NOT NULL,

    inspection_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    overall_status VARCHAR(30) NOT NULL,

    confidence NUMERIC(5,2),

    CONSTRAINT fk_inspection_product
        FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE CASCADE,

    CONSTRAINT check_inspection_status
        CHECK (
            overall_status IN (
                'COMPLIANT',
                'NON_COMPLIANT',
                'REVIEW_REQUIRED'
            )
        )
);


-- ============================================================
-- VIOLATIONS
-- ============================================================

CREATE TABLE IF NOT EXISTS violations (
    id SERIAL PRIMARY KEY,

    inspection_id INTEGER NOT NULL,

    rule_id INTEGER NOT NULL,

    status VARCHAR(20) NOT NULL,

    detected_value TEXT,

    expected_value TEXT,

    message TEXT,

    CONSTRAINT fk_violation_inspection
        FOREIGN KEY (inspection_id)
        REFERENCES inspections(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_violation_rule
        FOREIGN KEY (rule_id)
        REFERENCES rules(id)
        ON DELETE CASCADE
);


-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_rules_rule_id
    ON rules(rule_id);

CREATE INDEX IF NOT EXISTS idx_rules_category
    ON rules(category);

CREATE INDEX IF NOT EXISTS idx_inspections_product_id
    ON inspections(product_id);

CREATE INDEX IF NOT EXISTS idx_violations_inspection_id
    ON violations(inspection_id);

CREATE INDEX IF NOT EXISTS idx_violations_rule_id
    ON violations(rule_id);