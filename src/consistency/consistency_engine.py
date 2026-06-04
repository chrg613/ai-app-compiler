from src.models.contracts import (
    DatabaseSchema,
    APISchema,
    ValidationError
)


class ConsistencyEngine:

    @staticmethod
    def check_api_db_consistency(
        db_schema: DatabaseSchema,
        api_schema: APISchema
    ):

        errors = []

        table_names = {
            table.name.lower()
            for table in db_schema.tables
        }

        for endpoint in api_schema.endpoints:

            entity_table = endpoint.entity_name.lower()

            if entity_table not in table_names:

                errors.append(
                    ValidationError(
                        type="ConsistencyError",
                        message=(
                            f"Endpoint references "
                            f"missing table: {entity_table}"
                        )
                    )
                )

        return errors