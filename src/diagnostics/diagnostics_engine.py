from src.models.contracts import (
    DiagnosticsReport,
    ValidationReport,
    RuntimeReport,
    RiskReport,
    AssumptionReport,
    RepairReport
)

from src.diagnostics.confidence_engine import (
    ConfidenceEngine
)


class DiagnosticsEngine:

    @staticmethod
    def generate(
        risk_report: RiskReport,
        assumption_report: AssumptionReport,
        validation_report: ValidationReport,
        runtime_report: RuntimeReport,
        repairs: list[RepairReport]
    ) -> DiagnosticsReport:

        confidence = (
            ConfidenceEngine.calculate(
                risk_report=risk_report,
                validation_report=validation_report,
                runtime_report=runtime_report,
                assumption_count=len(
                    assumption_report.assumptions
                ),
                repair_count=len(
                    repairs
                )
            )
        )

        return DiagnosticsReport(
            warnings=validation_report.warnings,

            assumptions=[
                a.assumption
                for a in assumption_report.assumptions
            ],

            repairs=[
                r.repair_action
                for r in repairs
            ],

            confidence=confidence,

            rules_version="1.0",

            template_version="1.0"
        )