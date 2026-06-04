from src.models.contracts import (
    UISchema
)


class HTMLGenerator:

    @staticmethod
    def generate(
        ui_schema: UISchema
    ):

        pages = {}

        for page in ui_schema.pages:

            html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{page.name}</title>
</head>
<body>

<h1>{page.name}</h1>

"""

            for component in page.components:

                html += (
                    f"<div>{component}</div>\n"
                )

            html += """
</body>
</html>
"""

            pages[
                f"{page.name.lower()}.html"
            ] = html

        return pages