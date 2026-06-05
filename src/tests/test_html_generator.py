from src.models.contracts import (
    UISchema,
    PageSchema
)

from src.codegen.html_generator import (
    HTMLGenerator
)

schema = UISchema(
    pages=[
        PageSchema(
            name="PatientPage",
            components=[
                "Table",
                "CreateForm"
            ]
        )
    ]
)

pages = (
    HTMLGenerator.generate(
        schema
    )
)

for (
    filename,
    content
) in pages.items():

    print(filename)

    print(content)