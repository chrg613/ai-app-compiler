from src.models.contracts import (
    Assumption,
    AssumptionReport
)


class AssumptionEngine:

    @staticmethod
    def generate(
        prompt: str
    ) -> AssumptionReport:

        assumptions = []

        prompt_lower = prompt.lower()

        if (
            "login" not in prompt_lower
            and
            "auth" not in prompt_lower
        ):

            assumptions.append(
                Assumption(
                    reason=(
                        "Authentication "
                        "not specified"
                    ),
                    assumption=(
                        "Email-password "
                        "authentication"
                    )
                )
            )

        if (
            "role" not in prompt_lower
        ):

            assumptions.append(
                Assumption(
                    reason=(
                        "Roles not specified"
                    ),
                    assumption=(
                        "Admin and User roles"
                    )
                )
            )

        return AssumptionReport(
            assumptions=assumptions
        )