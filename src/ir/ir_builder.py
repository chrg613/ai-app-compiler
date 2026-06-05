import re
import logging

from src.models.contracts import (
    IntentModel,
    ApplicationIR,
    EntityIR,
    AttributeIR,
    IntegrationIR
)

logger = logging.getLogger(__name__)


class IRBuilder:
    """
    Builds the Application Intermediate Representation from intent.
    The IR is the single source of truth for all downstream generators.
    """

    @staticmethod
    def build(intent: IntentModel) -> ApplicationIR:
        """
        Transform IntentModel (with EntityModel objects containing full attributes)
        into ApplicationIR (with EntityIR objects ready for code generation).
        """

        entities = []
        
        # Handle the new EntityModel structure from LLM
        for entity_model in intent.entities:
            attributes = []
            
            # Transform EntityModel attributes to AttributeIR
            if entity_model.attributes:
                for attr in entity_model.attributes:
                    attributes.append(
                        AttributeIR(
                            name=IRBuilder.to_snake_case(attr.name),
                            type=attr.type,
                            nullable=attr.nullable,
                            is_primary=attr.is_primary,
                            description=attr.description
                        )
                    )
            else:
                # Fallback: add default id field if none provided
                attributes.append(
                    AttributeIR(
                        name="id",
                        type="uuid",
                        is_primary=True,
                        description="Unique identifier"
                    )
                )

            entities.append(
                EntityIR(
                    name=IRBuilder.to_snake_case(entity_model.name),
                    description=entity_model.description,
                    attributes=attributes
                )
            )

        # Transform integrations
        integrations = []
        for integration_name in intent.integrations:
            integrations.append(
                IntegrationIR(
                    name=integration_name,
                    config={}  # Config can be populated by specific generators
                )
            )

        return ApplicationIR(
            app_name=intent.app_name,
            description=intent.description,
            entities=entities,
            roles=intent.roles,
            features=intent.features,
            integrations=integrations,
            assumptions=[]  # Will be populated by assumption engine
        )

    @staticmethod
    def to_snake_case(name: str) -> str:
        """
        Convert CamelCase or PascalCase to snake_case.
        Example: UserProfile -> user_profile, ContactInfo -> contact_info
        """
        # Insert underscore before uppercase letters that follow lowercase
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        # Insert underscore before uppercase letters that follow lowercase or digits
        s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
        # Replace spaces and hyphens with underscores
        s3 = re.sub(r'[\s\-]+', '_', s2)
        # Convert to lowercase and remove multiple underscores
        s4 = s3.lower()
        s4 = re.sub(r'_+', '_', s4)
        return s4.strip('_')
