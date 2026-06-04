from src.models.contracts import (
    RiskReport,
    ValidationReport,
    RuntimeReport
)


class ConfidenceEngine:

    @staticmethod
    def calculate(
        risk_report: RiskReport,
        validation_report: ValidationReport,
        runtime_report: RuntimeReport,
        assumption_count: int,
        repair_count: int
    ) -> float:

        confidence = 1.0

        # Risk penalties

        confidence -= (
            risk_report.ambiguity_score
            * 0.30
        )

        confidence -= (
            risk_report.conflict_score
            * 0.40
        )

        # Validation penalties

        confidence -= (
            len(validation_report.errors)
            * 0.15
        )

        confidence -= (
            len(validation_report.warnings)
            * 0.05
        )

        # Assumption penalties

        confidence -= (
            assumption_count
            * 0.03
        )

        # Repair penalties

        confidence -= (
            repair_count
            * 0.07
        )

        # Runtime penalty

        if runtime_report.status == "FAIL":

            confidence -= 0.30

        confidence = max(
            confidence,
            0.0
        )

        confidence = min(
            confidence,
            1.0
        )

        return round(
            confidence,
            2
        )