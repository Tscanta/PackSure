from uuid import uuid4

from schemas.product import ProductInput
from backend.inspection.result import CheckResult, InspectionResult

from backend.inspection.rule_repository import get_compliance_rules
from backend.inspection.field_validator import evaluate_rule
from backend.models.violation import Violation


class InspectionEngine:

    def inspect(self, product: ProductInput) -> InspectionResult:

        # ------------------------------------------------------------
        # LOAD RULES FROM DATABASE
        # ------------------------------------------------------------

        rules = get_compliance_rules(product)

        checks: list[CheckResult] = []

        # ------------------------------------------------------------
        # RUN VALIDATORS
        # ------------------------------------------------------------

        for rule in rules:

            checks.append(evaluate_rule(product, rule))

        # ------------------------------------------------------------
        # COUNT RESULTS
        # ------------------------------------------------------------

        total_checks = len(checks)

        passed_checks = sum(
            1
            for check in checks
            if check.status == "PASS"
        )

        failed_checks = sum(
            1
            for check in checks
            if check.status == "FAIL"
        )

        warning_checks = sum(
            1
            for check in checks
            if check.status in {"WARNING", "REVIEW"}
        )

        violations = [
            Violation(
                field=check.field,
                rule_id=check.rule_id or "",
                message=check.message,
                expected_value=check.expected_value,
                actual_value=check.detected_value,
                severity=check.severity,
                database_rule_id=check.database_rule_id,
            )
            for check in checks
            if check.status == "FAIL"
        ]

        # ------------------------------------------------------------
        # SEVERITY-WEIGHTED SCORE
        #
        # CRITICAL = 4
        # HIGH     = 3
        # MEDIUM   = 2
        # LOW      = 1
        # ------------------------------------------------------------

        severity_weights = {
            "CRITICAL": 4,
            "HIGH": 3,
            "MEDIUM": 2,
            "LOW": 1,
        }

        total_weight = 0
        failed_weight = 0

        for check in checks:

            severity = check.severity or "LOW"

            weight = severity_weights.get(
                severity.upper(),
                1
            )

            total_weight += weight

            if check.status == "FAIL":
                failed_weight += weight

        # ------------------------------------------------------------
        # CALCULATE SCORE
        # ------------------------------------------------------------

        if total_weight > 0:

            score = (
                1 - (failed_weight / total_weight)
            ) * 100

        else:

            score = 0

        # ------------------------------------------------------------
        # DETERMINE OVERALL STATUS
        # ------------------------------------------------------------

        critical_failure = any(
            check.status == "FAIL"
            and check.severity == "CRITICAL"
            for check in checks
        )

        mandatory_failure = any(
            check.status == "FAIL"
            and check.mandatory is True
            for check in checks
        )

        if critical_failure:

            overall_status = "NON_COMPLIANT"

        elif mandatory_failure:

            overall_status = "NON_COMPLIANT"

        elif warning_checks > 0:

            overall_status = "REVIEW_REQUIRED"

        else:

            overall_status = "COMPLIANT"

        # ------------------------------------------------------------
        # CREATE INSPECTION RESULT
        # ------------------------------------------------------------

        return InspectionResult(

            inspection_id=(
                f"INS-{uuid4().hex[:8].upper()}"
            ),

            overall_status=overall_status,

            score=round(score, 2),

            total_checks=total_checks,

            passed_checks=passed_checks,

            failed_checks=failed_checks,

            warning_checks=warning_checks,

            checks=checks,

            violations=violations
        )
