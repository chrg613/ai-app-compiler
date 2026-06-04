from src.assumptions.assumption_engine import (
    AssumptionEngine
)

report = (
    AssumptionEngine.generate(
        "Build a CRM"
    )
)

print(
    report.model_dump_json(
        indent=2
    )
)