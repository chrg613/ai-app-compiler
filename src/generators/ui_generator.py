from src.models.contracts import (
    ApplicationIR,
    UISchema,
    PageSchema
)

class UIGenerator:

    @staticmethod
    def generate(
        ir: ApplicationIR
    ) -> UISchema:

        pages = []

        pages.append(
            PageSchema(
                name="Home",
                components=[
                    "Navigation"
                ]
            )
        )

        for entity in ir.entities:

            pages.append(
                PageSchema(
                    name=f"{entity.name}Page",
                    components=[
                        "Table",
                        "CreateForm",
                        "EditForm"
                    ]
                )
            )

        for feature in ir.features:

            pages.append(
                PageSchema(
                    name=(
                        feature.replace(
                            " ",
                            ""
                        ) + "Page"
                    ),
                    components=[
                        "FeatureView"
                    ]
                )
            )

        return UISchema(
            pages=pages
        )