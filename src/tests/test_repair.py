from src.models.contracts import (
    IntentModel
)

from src.intent.validator import (
    IntentValidator
)

from src.intent.repair import (
    IntentRepair
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

repaired = (
    IntentRepair.repair(
        intent,
        report
    )
)

print(
    repaired.model_dump_json(
        indent=2
    )
)