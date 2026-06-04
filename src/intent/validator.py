from src.models.contracts import (
    IntentModel,
    IntentValidationError,
    IntentValidationReport
)


class IntentValidator:

    @staticmethod
    def validate(
        intent: IntentModel
    ) -> IntentValidationReport:

        errors = []

        if not intent.app_name.strip():

            errors.append(
                IntentValidationError(
                    message="Missing app name"
                )
            )

        if len(intent.entities) == 0:

            errors.append(
                IntentValidationError(
                    message="No entities extracted"
                )
            )

        if len(intent.roles) == 0:

            errors.append(
                IntentValidationError(
                    message="No roles extracted"
                )
            )

        if len(intent.features) == 0:

            errors.append(
                IntentValidationError(
                    message="No features extracted"
                )
            )

        return IntentValidationReport(
            status=(
                "PASS"
                if len(errors) == 0
                else "FAIL"
            ),
            errors=errors
        )