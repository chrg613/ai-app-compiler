import json

from openai import OpenAI

from src.models.contracts import (
    IntentModel,
    IntentExtractionResult
)

from src.llm.providers.base_provider import (
    BaseLLMProvider
)


class OpenRouterProvider(
    BaseLLMProvider
):

    def __init__(
        self,
        api_key: str
    ):
        if not api_key:
            raise ValueError(
                "OPENROUTER_API_KEY not found"
            )
    
        self.client = OpenAI(
            api_key=api_key.strip(),
            base_url="https://openrouter.ai/api/v1"
        )

    def extract_intent(
        self,
        prompt: str
    ) -> IntentExtractionResult:

        system_prompt = """
You are an application compiler.

Return ONLY valid JSON.

Schema:

{
    "app_name": string,
    "entities": [string],
    "roles": [string],
    "features": [string]
}
"""

        response = (
            self.client.chat.completions.create(
                model="deepseek/deepseek-chat-v3-0324",

                temperature=0,

                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
        )

        raw = (
            response
            .choices[0]
            .message
            .content
        )

        raw = raw.strip()

        if raw.startswith("```json"):
            raw = raw.replace("```json", "", 1)

        if raw.endswith("```"):
            raw = raw[:-3]

        raw = raw.strip()

        data = json.loads(raw)

        intent = IntentModel(
            **data
        )

        return IntentExtractionResult(
            intent=intent,
            confidence=1.0,
            raw_response=raw
        )