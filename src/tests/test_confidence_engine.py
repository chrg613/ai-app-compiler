from src.models.contracts import (
    RiskReport,
    ValidationReport,
    RuntimeReport
)

from src.diagnostics.confidence_engine import (
    ConfidenceEngine
)

risk_report = RiskReport(
    ambiguity_score=0.2,
    conflict_score=0.0,
    completeness_score=0.8,
    issues=[]
)

validation_report = ValidationReport(
    status="PASS",
    errors=[],
    warnings=[]
)

runtime_report = RuntimeReport(
    status="PASS"
)

confidence = (
    ConfidenceEngine.calculate(
        risk_report,
        validation_report,
        runtime_report,
        assumption_count=2,
        repair_count=0
    )
)

print(confidence)