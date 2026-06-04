from src.models.contracts import (
    DatabaseSchema,
    TableSchema,
    ColumnSchema
)

from src.codegen.sql_generator import (
    SQLGenerator
)

schema = DatabaseSchema(
    tables=[
        TableSchema(
            name="patient",
            columns=[
                ColumnSchema(
                    name="id",
                    type="uuid"
                ),
                ColumnSchema(
                    name="name",
                    type="string"
                )
            ]
        )
    ]
)

sql = (
    SQLGenerator.generate(
        schema
    )
)

print(sql)