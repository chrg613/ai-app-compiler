from src.models.contracts import (
    IntentModel,
    IntentValidationReport
)


class IntentRepair:

    @staticmethod
    def repair(
        intent: IntentModel,
        report: IntentValidationReport
    ) -> IntentModel:

        repaired = intent.model_copy()

        messages = [
            e.message
            for e in report.errors
        ]

        if "No entities extracted" in messages:

            repaired.entities = [
                "DefaultEntity"
            ]

        if "No roles extracted" in messages:

            repaired.roles = [
                "Admin"
            ]

        if "No features extracted" in messages:

            repaired.features = [
                "Management"
            ]

        if not repaired.app_name:

            repaired.app_name = (
                "GeneratedApplication"
            )

        return repaired