from src.models.contracts import (
    IntentModel
)


class SchemaGuard:

    @staticmethod
    def validate_intent(
        data: dict
    ) -> bool:

        try:

            IntentModel(
                **data
            )

            return True

        except Exception:

            return False