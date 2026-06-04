from src.generators.api_generator import (
    APIGenerator
)

from src.ir.ir_builder import (
    IRBuilder
)

from src.models.contracts import (
    IntentModel
)

from src.codegen.flask_generator import (
    FlaskGenerator
)
from src.generators.ui_generator import (
    UIGenerator
)

intent = IntentModel(
    app_name="Hospital",

    entities=[
        "Patient",
        "Doctor"
    ],

    roles=[
        "Admin"
    ],

    features=[
        "Scheduling"
    ]
)

ir = (
    IRBuilder.build(
        intent
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
code = (
    FlaskGenerator.generate(
        api_schema,
        ui_schema
    )
)
print(code)