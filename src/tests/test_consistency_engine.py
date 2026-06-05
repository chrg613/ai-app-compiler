from src.models.contracts import IntentModel
from src.ir.ir_builder import IRBuilder
from src.generators.db_generator import DatabaseGenerator
from src.generators.api_generator import APIGenerator
from src.consistency.consistency_engine import ConsistencyEngine


intent = IntentModel(
    app_name="Drone Maintenance",

    entities=[
        "Drone",
        "Technician"
    ],

    roles=["Admin"],

    features=[]
)

ir = IRBuilder.build(intent)

db_schema = DatabaseGenerator.generate(ir)

api_schema = APIGenerator.generate(ir)

errors = (
    ConsistencyEngine
    .check_api_db_consistency(
        db_schema,
        api_schema
    )
)

print(errors)