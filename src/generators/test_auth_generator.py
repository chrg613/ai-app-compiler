from src.models.contracts import IntentModel
from src.ir.ir_builder import IRBuilder
from src.generators.auth_generator import AuthGenerator


intent = IntentModel(
    app_name="Drone Maintenance System",
    entities=["Drone"],
    roles=["Admin", "Technician"],
    features=[]
)

ir = IRBuilder.build(intent)

auth_schema = AuthGenerator.generate(ir)

print(
    auth_schema.model_dump_json(
        indent=2
    )
)