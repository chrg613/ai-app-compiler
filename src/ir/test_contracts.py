from src.models.contracts import *

crm = ApplicationIR(
    app_name="CRM",
    entities=[
        EntityIR(
            name="User",
            attributes=[
                AttributeIR(
                    name="name",
                    type="string"
                ),
                AttributeIR(
                    name="email",
                    type="string"
                )
            ]
        )
    ],
    roles=[
        "Admin",
        "User"
    ],
    features=[
        "Authentication"
    ]
)

print(
    crm.model_dump_json(
        indent=2
    )
)