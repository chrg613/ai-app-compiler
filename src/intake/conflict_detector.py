from src.models.contracts import (
    ConflictReport
)
class ConflictDetector:

    CONFLICT_RULES = [

        (
            "no authentication",
            "login",
            "Authentication disabled but login required"
        ),

        (
            "no authentication",
            "sign in",
            "Authentication disabled but sign-in required"
        ),

        (
            "no users",
            "user management",
            "Users disabled but user management requested"
        ),

        (
            "single tenant",
            "isolated databases",
            "Single tenant conflicts with isolated customer databases"
        )

    ]

    @staticmethod
    def detect(
        prompt: str
    ):

        prompt_lower = prompt.lower()

        issues = []

        score = 0.0

        for (
            left,
            right,
            message
        ) in (
            ConflictDetector
            .CONFLICT_RULES
        ):

            if (
                left in prompt_lower
                and
                right in prompt_lower
            ):

                issues.append(
                    message
                )

                score += 0.4

        score = min(
            score,
            1.0
        )

        return ConflictReport(
            conflict_score=score,
            issues=issues
        )