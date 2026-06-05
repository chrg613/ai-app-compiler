import os

from src.intent.extractor import (
    IntentExtractor
)

from src.llm.providers.openrouter_provider import (
    OpenRouterProvider
)

from src.pipeline.compiler_pipeline import (
    CompilerPipeline
)


provider = OpenRouterProvider(
    api_key=os.getenv(
        "OPENROUTER_API_KEY"
    )
)

extractor = (
    IntentExtractor(
        provider
    )
)

pipeline = (
    CompilerPipeline(
        extractor
    )
)

result = (
    pipeline.compile(
        """
Build a hospital management system.

Doctors manage patients.

Receptionists schedule appointments.

Admins manage billing.
        """
    )
)

print("\n===== INTENT =====")
print(
    result["intent"]
    .model_dump_json(indent=2)
)

print("\n===== DIAGNOSTICS =====")
print(
    result["diagnostics"]
    .model_dump_json(indent=2)
)