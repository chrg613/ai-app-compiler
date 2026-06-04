from src.models.contracts import (
    IntentExtractionResult
)


class IntentExtractor:

    def __init__(
        self,
        provider
    ):

        self.provider = provider

    def extract(
        self,
        prompt: str
    ) -> IntentExtractionResult:

        return (
            self.provider
            .extract_intent(
                prompt
            )
        )