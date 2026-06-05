from src.models.contracts import (
    IntentModel
)

from src.ir.ir_builder import (
    IRBuilder
)

from src.generators.db_generator import (
    DatabaseGenerator
)

from src.generators.api_generator import (
    APIGenerator
)

from src.generators.ui_generator import (
    UIGenerator
)

from src.generators.auth_generator import (
    AuthGenerator
)

from src.validation.validator import (
    Validator
)

from src.runtime.simulator import (
    RuntimeSimulator
)

from src.intake.risk_analyzer import (
    RiskAnalyzer
)

from src.assumptions.assumption_engine import (
    AssumptionEngine
)

from src.repair.repair_engine import (
    RepairEngine
)

from src.diagnostics.diagnostics_engine import (
    DiagnosticsEngine
)


prompt = "Build a CRM"


risk_report = (
    RiskAnalyzer.analyze(
        prompt
    )
)

assumption_report = (
    AssumptionEngine.generate(
        prompt
    )
)


intent = IntentModel(
    app_name="CRM",

    entities=[
        "User",
        "Contact"
    ],

    roles=[
        "Admin"
    ],

    features=[
        "Authentication"
    ]
)


ir = IRBuilder.build(
    intent
)

db_schema = (
    DatabaseGenerator.generate(
        ir
    )
)

api_schema = (
    APIGenerator.generate(
        ir
    )
)

ui_schema = (
    UIGenerator.generate(
        ir
    )
)

auth_schema = (
    AuthGenerator.generate(
        ir
    )
)

validation_report = (
    Validator.validate(
        db_schema,
        api_schema,
        ui_schema,
        auth_schema
    )
)

repairs = (
    RepairEngine.repair(
        validation_report
    )
)

runtime_report = (
    RuntimeSimulator.simulate(
        db_schema,
        api_schema,
        ui_schema,
        auth_schema
    )
)

diagnostics = (
    DiagnosticsEngine.generate(
        risk_report,
        assumption_report,
        validation_report,
        runtime_report,
        repairs
    )
)

print(
    diagnostics.model_dump_json(
        indent=2
    )
)