from src.models.contracts import (
    IntentModel,
    ApplicationIR,
    EntityIR,
    AttributeIR
)


class IRBuilder:

    @staticmethod
    def build(intent: IntentModel) -> ApplicationIR:

        entities = []

        for entity_name in intent.entities:

            entities.append(
                EntityIR(
                    name=entity_name,
                    attributes=[
                        AttributeIR(
                            name="id",
                            type="uuid"
                        )
                    ]
                )
            )

        return ApplicationIR(
            app_name=intent.app_name,
            entities=entities,
            roles=intent.roles,
            features=intent.features
        )