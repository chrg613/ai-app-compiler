from src.models.contracts import IntentModel
from src.ir.ir_builder import IRBuilder
from src.generators.db_generator import DatabaseGenerator


intent = IntentModel(
    app_name="Drone Maintenance System",

    entities=[
        "Drone",
        "Technician",
        "MaintenanceRecord"
    ],

    roles=[
        "Admin",
        "Technician"
    ],

    features=[
        "Scheduling"
    ]
)

ir = IRBuilder.build(intent)

db_schema = DatabaseGenerator.generate(ir)

print(
    db_schema.model_dump_json(
        indent=2
    )
)