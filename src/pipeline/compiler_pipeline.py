from src.intake.risk_analyzer import (
    RiskAnalyzer
)

from src.assumptions.assumption_engine import (
    AssumptionEngine
)

from src.intent.repair import (
    IntentRepair
)

from src.intent.extractor import (
    IntentExtractor
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

from src.repair.repair_engine import (
    RepairEngine
)

from src.runtime.simulator import (
    RuntimeSimulator
)

from src.diagnostics.diagnostics_engine import (
    DiagnosticsEngine
)

from src.intent.validator import (
    IntentValidator
)
from src.codegen.exporter import (
    Exporter
)

class CompilerPipeline:

    def __init__(
        self,
        intent_extractor
    ):

        self.intent_extractor = (
            intent_extractor
        )

    def compile(
        self,
        prompt: str
    ):

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

        extraction_result = (
            self.intent_extractor.extract(
                prompt
            )
        )

        intent = (
            extraction_result.intent
        )
        
        intent_validation = (
            IntentValidator.validate(
                intent
            )
        )

        if intent_validation.status == "FAIL":

            intent = (
                IntentRepair.repair(
                    intent,
                    intent_validation
                )
            )

            intent_validation = (
                IntentValidator.validate(
                    intent
                )
            )
        

        ir = (
            IRBuilder.build(
                intent
            )
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
        export_result = Exporter.export(
            ir.app_name,
            db_schema,
            api_schema,
            ui_schema
        )
        return {
            "intent": intent,
            "ir": ir,
            "database": db_schema,
            "api": api_schema,
            "ui": ui_schema,
            "auth": auth_schema,
            "diagnostics": diagnostics,
            "project_dir": export_result.get('project_dir') if export_result else None
        }
