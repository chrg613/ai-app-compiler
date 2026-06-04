from src.models.contracts import (
    ApplicationIR,
    DatabaseSchema,
    TableSchema,
    ColumnSchema
)


class DatabaseGenerator:

    @staticmethod
    def generate(
        ir: ApplicationIR
    ) -> DatabaseSchema:

        tables = []

        for entity in ir.entities:

            columns = []

            for attribute in entity.attributes:

                columns.append(
                    ColumnSchema(
                        name=attribute.name,
                        type=attribute.type
                    )
                )

            tables.append(
                TableSchema(
                    name=entity.name.lower(),
                    columns=columns
                )
            )

        return DatabaseSchema(
            tables=tables
        )
    
# TODO:
# Convert CamelCase -> snake_case
# Example:
# MaintenanceRecord -> maintenance_record