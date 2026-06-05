from src.models.contracts import IntentModel

from src.ir.ir_builder import IRBuilder

from src.generators.db_generator import DatabaseGenerator
from src.generators.api_generator import APIGenerator
from src.generators.ui_generator import UIGenerator
from src.generators.auth_generator import AuthGenerator

from src.runtime.simulator import RuntimeSimulator


intent = IntentModel(
    app_name="Drone Maintenance",

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

db_schema = DatabaseGenerator.generate(ir)

api_schema = APIGenerator.generate(ir)

ui_schema = UIGenerator.generate(ir)

auth_schema = AuthGenerator.generate(ir)

runtime_report = RuntimeSimulator.simulate(
    db_schema,
    api_schema,
    ui_schema,
    auth_schema
)

print(
    runtime_report.model_dump_json(
        indent=2
    )
)