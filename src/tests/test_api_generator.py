from src.models.contracts import IntentModel
from src.ir.ir_builder import IRBuilder
from src.generators.api_generator import APIGenerator


intent = IntentModel(
    app_name="Drone Maintenance System",

    entities=[
        "Drone",
        "Technician"
    ],

    roles=[
        "Admin"
    ],

    features=[
        "Scheduling"
    ]
)

ir = IRBuilder.build(intent)

api_schema = APIGenerator.generate(ir)

print(
    api_schema.model_dump_json(
        indent=2
    )
)