from src.models.contracts import (
    DatabaseSchema,
    APISchema,
    UISchema,
    AuthSchema,
    RuntimeReport
)


class RuntimeSimulator:

    @staticmethod
    def simulate(
        db_schema: DatabaseSchema,
        api_schema: APISchema,
        ui_schema: UISchema,
        auth_schema: AuthSchema
    ) -> RuntimeReport:

        registered_tables = len(
            db_schema.tables
        )

        registered_endpoints = len(
            api_schema.endpoints
        )

        registered_pages = len(
            ui_schema.pages
        )

        status = "PASS"

        # Minimum executable requirements

        if registered_tables == 0:
            status = "FAIL"

        if registered_endpoints == 0:
            status = "FAIL"

        if registered_pages == 0:
            status = "FAIL"

        return RuntimeReport(
            status=status,
            registered_tables=registered_tables,
            registered_endpoints=registered_endpoints,
            registered_pages=registered_pages
        )