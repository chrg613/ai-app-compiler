from src.models.contracts import (
    ValidationReport,
    RepairReport
)


class RepairEngine:

    @staticmethod
    def repair(
        validation_report: ValidationReport
    ) -> list[RepairReport]:

        repairs = []

        for error in validation_report.errors:

            if error.type == "DatabaseError":

                repairs.append(
                    RepairReport(
                        repair_action="RegenerateDatabaseSchema",
                        target="Database",
                        details=error.message
                    )
                )

            elif error.type == "APIError":

                repairs.append(
                    RepairReport(
                        repair_action="RegenerateAPISchema",
                        target="API",
                        details=error.message
                    )
                )

            elif error.type == "UIError":

                repairs.append(
                    RepairReport(
                        repair_action="RegenerateUISchema",
                        target="UI",
                        details=error.message
                    )
                )

        return repairs