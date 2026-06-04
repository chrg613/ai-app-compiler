from src.models.contracts import (
    DatabaseSchema,
    APISchema,
    UISchema,
    AuthSchema,
    ValidationReport,
    ValidationError
)


class Validator:

    @staticmethod
    def validate(
        db_schema: DatabaseSchema,
        api_schema: APISchema,
        ui_schema: UISchema,
        auth_schema: AuthSchema
    ) -> ValidationReport:

        errors = []
        warnings = []

        # ---------- DB ----------

        if len(db_schema.tables) == 0:
            errors.append(
                ValidationError(
                    type="DatabaseError",
                    message="No database tables generated"
                )
            )

        # ---------- API ----------

        if len(api_schema.endpoints) == 0:
            errors.append(
                ValidationError(
                    type="APIError",
                    message="No API endpoints generated"
                )
            )

        # ---------- UI ----------

        if len(ui_schema.pages) == 0:
            errors.append(
                ValidationError(
                    type="UIError",
                    message="No UI pages generated"
                )
            )

        # ---------- AUTH ----------

        if len(auth_schema.roles) == 0:
            warnings.append(
                "No roles defined"
            )

        status = "PASS"

        if errors:
            status = "FAIL"

        return ValidationReport(
            status=status,
            errors=errors,
            warnings=warnings
        )