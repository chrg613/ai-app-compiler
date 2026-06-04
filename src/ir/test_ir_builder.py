from src.models.contracts import IntentModel
from src.ir.ir_builder import IRBuilder


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
        "Scheduling",
        "Maintenance Tracking"
    ]
)

ir = IRBuilder.build(intent)

print(
    ir.model_dump_json(
        indent=2
    )
)