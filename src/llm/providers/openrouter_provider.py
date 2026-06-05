import json
import logging

from openai import OpenAI

from src.models.contracts import (
    IntentModel,
    EntityModel,
    AttributeModel,
    IntentExtractionResult
)

from src.llm.providers.base_provider import (
    BaseLLMProvider
)

logger = logging.getLogger(__name__)


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
        """
        Enhanced intent extraction with structured attribute discovery.
        The LLM now returns detailed entity definitions instead of just names.
        """

        system_prompt = """You are an AI application compiler. Your role is to analyze application requirements and produce a complete, structured specification.

CRITICAL: Return ONLY valid JSON. No markdown, no explanations, just pure JSON.

You must extract:
1. App name - the primary name for the application
2. Description - what the app does
3. Entities - database models/resources with their attributes
4. Roles - user types or access levels
5. Features - main application capabilities
6. Integrations - external services needed (e.g., Stripe, SendGrid)

For each entity, identify:
- name: CamelCase entity name (e.g., "User", "Product", "Order")
- description: What this entity represents
- attributes: List of fields with:
  - name: lowercase_with_underscores
  - type: uuid|text|integer|boolean|timestamp|float|date|json|array
  - nullable: true/false
  - is_primary: true only for id fields
  - description: brief explanation

JSON Schema:
{
  "app_name": "string - application name",
  "description": "string - detailed description of what the app does",
  "entities": [
    {
      "name": "string - CamelCase",
      "description": "what this entity represents",
      "attributes": [
        {
          "name": "string - snake_case",
          "type": "uuid|text|integer|boolean|timestamp|float|date|json|array",
          "nullable": boolean,
          "is_primary": boolean,
          "description": "field description"
        }
      ]
    }
  ],
  "roles": ["admin", "user", "moderator"],
  "features": ["string - feature names"],
  "integrations": ["Stripe", "SendGrid", "Twilio"]
}

RULES:
- Every entity must have at least an id field (type: uuid, is_primary: true)
- If the prompt doesn't specify roles, default to ["admin", "user"]
- If payment is mentioned, include Stripe in integrations
- If emails are mentioned, include SendGrid or similar
- Be thorough with attributes - don't leave entities empty
- Attribute types MUST be one of: uuid|text|integer|boolean|timestamp|float|date|json|array
"""

        response = (
            self.client.chat.completions.create(
                model="deepseek/deepseek-chat-v3-0324",
                temperature=0.1,
                max_tokens=4096,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": f"Build the following application specification based on these requirements:\n\n{prompt}"
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

        # Clean markdown formatting if present
        if raw.startswith("```json"):
            raw = raw.replace("```json", "", 1)
        if raw.startswith("```"):
            raw = raw.replace("```", "", 1)
        if raw.endswith("```"):
            raw = raw[:-3]

        raw = raw.strip()

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            logger.error(f"[v0] Failed to parse LLM JSON response: {e}")
            logger.error(f"[v0] Raw response: {raw[:500]}")
            raise ValueError(f"Invalid JSON from LLM: {str(e)}")

        # Transform LLM output to IntentModel with EntityModel objects
        entities = []
        if "entities" in data and data["entities"]:
            for entity_data in data["entities"]:
                attributes = []
                if "attributes" in entity_data:
                    for attr_data in entity_data["attributes"]:
                        attributes.append(
                            AttributeModel(
                                name=attr_data.get("name", "field"),
                                type=attr_data.get("type", "text"),
                                nullable=attr_data.get("nullable", False),
                                is_primary=attr_data.get("is_primary", False),
                                description=attr_data.get("description", "")
                            )
                        )
                
                # Ensure every entity has at least an id field
                if not any(attr.is_primary for attr in attributes):
                    attributes.insert(0, AttributeModel(
                        name="id",
                        type="uuid",
                        nullable=False,
                        is_primary=True,
                        description="Unique identifier"
                    ))
                
                entities.append(
                    EntityModel(
                        name=entity_data.get("name", "Entity"),
                        description=entity_data.get("description", ""),
                        attributes=attributes
                    )
                )

        intent = IntentModel(
            app_name=data.get("app_name", "Application"),
            description=data.get("description", ""),
            entities=entities,
            roles=data.get("roles", ["admin", "user"]),
            features=data.get("features", []),
            integrations=data.get("integrations", [])
        )

        confidence = self._calculate_confidence(intent, raw)

        return IntentExtractionResult(
            intent=intent,
            confidence=confidence,
            raw_response=raw
        )

    def _calculate_confidence(self, intent: IntentModel, raw_response: str) -> float:
        """Calculate confidence score based on completeness of extracted data"""
        score = 0.5
        
        if intent.app_name and len(intent.app_name) > 0:
            score += 0.1
        if intent.description and len(intent.description) > 0:
            score += 0.1
        if len(intent.entities) > 0:
            score += 0.1
            # Bonus for entities with full attributes
            full_entities = sum(1 for e in intent.entities if len(e.attributes) > 1)
            score += min(0.1, full_entities * 0.05)
        if len(intent.roles) > 0:
            score += 0.1
        if len(intent.features) > 0:
            score += 0.1
        
        return min(0.99, score)
