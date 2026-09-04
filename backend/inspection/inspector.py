from uuid import uuid4

from schemas.product import ProductInput
from schemas.inspection import CheckResult, InspectionResult

from backend.inspection.rule_repository import get_compliance_rules
from backend.inspection.validator_registry import VALIDATOR_REGISTRY


class InspectionEngine:

    def inspect(self, product: ProductInput) -> InspectionResult:

        # ------------------------------------------------------------
        # LOAD RULES FROM DATABASE
        # ------------------------------------------------------------

        rules = get_compliance_rules()

        checks: list[CheckResult] = []

        # ------------------------------------------------------------
        # RUN VALIDATORS
        # ------------------------------------------------------------

        for rule in rules:

            validation_type = rule["validation_type"]

            validator = VALIDATOR_REGISTRY.get(
                validation_type
            )

            # --------------------------------------------------------
            # NO VALIDATOR FOUND
            # --------------------------------------------------------

            if validator is None:

                checks.append(
                    CheckResult(
                        field=rule["category"],
                        status="WARNING",
                        message=(
                            "No validator implemented for "
                            f"validation type: {validation_type}"
                        ),
                        rule_id=rule["rule_id"],
                        severity=rule["severity"],
                        mandatory=rule["mandatory"]
                    )
                )

                continue

            # --------------------------------------------------------
            # RUN VALIDATOR
            # --------------------------------------------------------

            result = validator(product)

            # --------------------------------------------------------
            # ADD DATABASE RULE INFORMATION
            # --------------------------------------------------------

            result.rule_id = rule["rule_id"]
            result.severity = rule["severity"]
            result.mandatory = rule["mandatory"]

            checks.append(result)

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
            if check.status == "WARNING"
        )

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

            checks=checks
        )