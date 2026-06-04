from src.models.contracts import (
    APISchema
)


class FlaskGenerator:

    @staticmethod
    def generate(
        api_schema: APISchema,
        ui_schema
    ) -> str:

        lines = []

        lines.extend([
            "from flask import Flask, render_template",
            "",
            "app = Flask(__name__)",
            ""
        ])

        for endpoint in api_schema.endpoints:

            route = endpoint.path.replace(
                "{id}",
                "<id>"
            )

            route_suffix = (
                "_by_id"
                if "<id>" in route
                else ""
            )

            function_name = (
                f"{endpoint.method.lower()}_"
                f"{endpoint.entity_name.lower()}"
                f"{route_suffix}"
            )

            lines.extend([
                f"@app.route('{route}', methods=['{endpoint.method}'])",
                f"def {function_name}():",
                "    return {}",
                ""
            ])
        for page in ui_schema.pages:

            route_name = (
                page.name.lower()
            )

            function_name = (
                route_name
            )

            lines.extend([
                f"@app.route('/{route_name}')",
                f"def {function_name}():",
                (
                    f"    return render_template("
                    f"'{route_name}.html'"
                    f")"
                ),
                ""
            ])

        lines.extend([
            "@app.route('/')",
            "def home():",
            "    return render_template('dashboard.html')",
            "",
            "if __name__ == '__main__':",
            "    app.run(debug=True)"
        ])

        return "\n".join(
            lines
        )