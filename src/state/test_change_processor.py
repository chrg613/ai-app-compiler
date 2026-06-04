from src.models.contracts import (
    ApplicationIR
)

from src.state.change_request import (
    ChangeRequest
)

from src.state.change_processor import (
    ChangeProcessor
)

ir = ApplicationIR(
    app_name="CRM",

    features=[
        "Authentication"
    ]
)

change = ChangeRequest(
    action="ADD",
    target="feature",
    value="Payments"
)

updated_ir = (
    ChangeProcessor.apply(
        ir,
        change
    )
)

print(
    updated_ir.model_dump_json(
        indent=2
    )
)