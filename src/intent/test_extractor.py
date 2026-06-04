import os

from src.intent.extractor import (
    IntentExtractor
)

from src.llm.providers.openrouter_provider import (
    OpenRouterProvider
)


provider = OpenRouterProvider(
    api_key=os.getenv(
        "OPENROUTER_API_KEY"
    )
)

extractor = IntentExtractor(
    provider
)

result = (
    extractor.extract(
        """
Create an app with a list of jobs; each job has linked materials (name, quantity, optional cost) or a checklist. Include a form to add or edit jobs and a way to add materials per job. Add a header and "Add job" button. Works for job-based material tracking.
        """
    )
)

print(
    result.model_dump_json(
        indent=2
    )
)