from src.models.contracts import (
    RiskReport
)
from src.intake.conflict_detector import (
    ConflictDetector
)

class RiskAnalyzer:

    VAGUE_TERMS = {
        "system",
        "platform",
        "tool",
        "app",
        "software"
    }

    @staticmethod
    def analyze(
        prompt: str
    ) -> RiskReport:

        prompt_lower = prompt.lower()

        issues = []

        ambiguity = 0.0

        conflict_report = (
        ConflictDetector.detect(
            prompt
        )
)

        conflict = conflict_report.conflict_score

        completeness = 1.0

        for term in (
            RiskAnalyzer
            .VAGUE_TERMS
        ):

            if term in prompt_lower:

                ambiguity += 0.2

                issues.append(
                    f"Vague term detected: {term}"
                )

        if len(prompt.split()) < 5:

            completeness -= 0.3

            issues.append(
                "Prompt may be underspecified"
            )

        ambiguity = min(
            ambiguity,
            1.0
        )

        completeness = max(
            completeness,
            0.0
        )
        
        issues.extend(
            conflict_report.issues
        )
        
        return RiskReport(
            ambiguity_score=ambiguity,
            conflict_score=conflict,
            completeness_score=completeness,
            issues=issues
        )