from src.models.contracts import (
    DatabaseSchema
)


class SQLGenerator:

    @staticmethod
    def generate(
        schema: DatabaseSchema
    ) -> str:

        statements = []

        for table in schema.tables:

            columns = []

            for column in table.columns:

                sql_type = "TEXT"

                if column.type == "uuid":
                    sql_type = "UUID"

                columns.append(
                    f"{column.name} {sql_type}"
                )

            statement = (
                f"CREATE TABLE {table.name} (\n"
                + ",\n".join(columns)
                + "\n);\n"
            )

            statements.append(
                statement
            )

        return "\n".join(
            statements
        )