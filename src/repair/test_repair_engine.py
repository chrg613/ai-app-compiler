from src.models.contracts import (
    ValidationReport,
    ValidationError
)

from src.repair.repair_engine import (
    RepairEngine
)

report = ValidationReport(
    status="FAIL",

    errors=[
        ValidationError(
            type="APIError",
            message="No API endpoints generated"
        )
    ],

    warnings=[]
)

repairs = RepairEngine.repair(
    report
)

for repair in repairs:
    print(
        repair.model_dump_json(
            indent=2
        )
    )