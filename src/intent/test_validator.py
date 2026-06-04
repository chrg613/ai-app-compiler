from src.models.contracts import (
    IntentModel
)

from src.intent.validator import (
    IntentValidator
)

intent = IntentModel(
    app_name="",
    entities=[],
    roles=[],
    features=[]
)

report = (
    IntentValidator.validate(
        intent
    )
)

print(
    report.model_dump_json(
        indent=2
    )
)