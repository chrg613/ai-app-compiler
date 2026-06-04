from src.models.contracts import IntentModel
from src.ir.ir_builder import IRBuilder
from src.generators.ui_generator import UIGenerator


intent = IntentModel(
    app_name="Drone Maintenance System",
    entities=[
        "Drone",
        "Technician"
    ],
    roles=["Admin"],
    features=["Scheduling"]
)

ir = IRBuilder.build(intent)

ui_schema = UIGenerator.generate(ir)

print(
    ui_schema.model_dump_json(
        indent=2
    )
)