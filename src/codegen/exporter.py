from src.codegen.sql_generator import (
    SQLGenerator
)

from src.codegen.flask_generator import (
    FlaskGenerator
)

from src.codegen.file_writer import (
    FileWriter
)
from src.codegen.requirements_generator import (
    RequirementsGenerator
)

from src.codegen.readme_generator import (
    ReadmeGenerator
)
from src.codegen.html_generator import(
        HTMLGenerator
)
class Exporter:

    @staticmethod
    def export(
        app_name,
        db_schema,
        api_schema,
        ui_schema
    ):

        sql = (
            SQLGenerator.generate(
                db_schema
            )
        )

        flask_code = (
            FlaskGenerator.generate(
                api_schema,
                ui_schema
            )
        )

        requirements = (
            RequirementsGenerator.generate()
        )

        readme = (
            ReadmeGenerator.generate(
                app_name
            )
        )

        html_pages = (
            HTMLGenerator.generate(
                ui_schema
            )
        )

        FileWriter.write(
            "generated",
            "schema.sql",
            sql
        )

        FileWriter.write(
            "generated",
            "app.py",
            flask_code
        )

        FileWriter.write(
            "generated",
            "requirements.txt",
            requirements
        )

        FileWriter.write(
            "generated",
            "README.md",
            readme
        )
        for (
            filename,
            content
        ) in html_pages.items():

            FileWriter.write(
                "generated/templates",
                filename,
                content
            )