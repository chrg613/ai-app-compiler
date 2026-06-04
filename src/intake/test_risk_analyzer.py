from src.intake.risk_analyzer import (
    RiskAnalyzer
)

report = (
    RiskAnalyzer.analyze(
        """
        Build a CRM.

        No authentication.

        Admins must login.
        """
    )
)

print(
    report.model_dump_json(
        indent=2
    )
)

report = (
    RiskAnalyzer.analyze(
        "Build a system"
    )
)

print(
    report.model_dump_json(
        indent=2
    )
)