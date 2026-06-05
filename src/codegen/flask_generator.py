import logging
from typing import List

from src.models.contracts import APISchema, UISchema

logger = logging.getLogger(__name__)


class FlaskGenerator:
    """
    Generates production-ready Flask application code.
    Creates actual CRUD logic, validation, and error handling.
    """

    @staticmethod
    def generate(api_schema: APISchema, ui_schema: UISchema) -> str:
        """Generate complete Flask application with CRUD endpoints"""
        lines: List[str] = []

        # Add imports and app setup
        lines.extend(FlaskGenerator._generate_imports())
        lines.extend(FlaskGenerator._generate_app_setup())

        # Generate API endpoints
        for endpoint in api_schema.endpoints:
            endpoint_code = FlaskGenerator._generate_endpoint(endpoint)
            lines.extend(endpoint_code)

        # Generate UI routes
        for page in ui_schema.pages:
            page_code = FlaskGenerator._generate_page_route(page)
            lines.extend(page_code)

        # Add main block
        lines.extend(FlaskGenerator._generate_main())

        logger.info(f"[FlaskGen] Generated {len(api_schema.endpoints)} API endpoints")
        return "\n".join(lines)

    @staticmethod
    def _generate_imports() -> List[str]:
        """Generate import statements"""
        return [
            "import logging",
            "import os",
            "from flask import Flask, render_template, request, jsonify",
            "from flask_cors import CORS",
            "from datetime import datetime",
            "import json",
            "",
            "logger = logging.getLogger(__name__)",
        ]

    @staticmethod
    def _generate_app_setup() -> List[str]:
        """Generate Flask app setup"""
        return [
            "",
            "# Application Setup",
            "app = Flask(__name__)",
            "CORS(app)",
            "",
            "# Configuration",
            "app.config['JSON_SORT_KEYS'] = False",
            "app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False') == 'True'",
            "",
            "# In-memory database (replace with real DB)",
            "DATABASE = {}",
            "",
        ]

    @staticmethod
    def _generate_endpoint(endpoint) -> List[str]:
        """Generate a single API endpoint with real logic"""
        lines: List[str] = []
        route = endpoint.path.replace("{id}", "<id>")
        function_name = FlaskGenerator._sanitize_function_name(
            f"{endpoint.method.lower()}_{endpoint.entity_name.lower()}_"
            f"{'by_id' if '<id>' in route else 'list'}"
        )

        method_upper = endpoint.method.upper()

        lines.extend([
            "",
            f"@app.route('{route}', methods=['{method_upper}'])",
            f"def {function_name}(id=None):",
            f"    \"\"\"",
            f"    {endpoint.description}",
            f"    \"\"\"",
            "    try:",
        ])

        # Generate method-specific logic
        if endpoint.method == "GET":
            if "<id>" in route:
                # GET by ID
                lines.extend([
                    f"        entity_name = '{endpoint.entity_name.lower()}'",
                    f"        if id not in DATABASE.get(entity_name, {{}}):",
                    f"            return jsonify({{'error': '{endpoint.entity_name} not found'}}), 404",
                    f"        return jsonify(DATABASE[entity_name][id]), 200",
                ])
            else:
                # GET list
                lines.extend([
                    f"        entity_name = '{endpoint.entity_name.lower()}'",
                    f"        limit = request.args.get('limit', 10, type=int)",
                    f"        offset = request.args.get('offset', 0, type=int)",
                    f"        items = list(DATABASE.get(entity_name, {{}}).values())",
                    f"        paginated = items[offset:offset + limit]",
                    f"        return jsonify({{'items': paginated, 'total': len(items)}}), 200",
                ])
        elif endpoint.method == "POST":
            lines.extend([
                f"        entity_name = '{endpoint.entity_name.lower()}'",
                f"        data = request.get_json() or {{}}",
                f"        if not data:",
                f"            return jsonify({{'error': 'Request body required'}}), 400",
                f"        if entity_name not in DATABASE:",
                f"            DATABASE[entity_name] = {{}}",
                f"        item_id = str(len(DATABASE[entity_name]) + 1)",
                f"        data['id'] = item_id",
                f"        data['created_at'] = datetime.now().isoformat()",
                f"        DATABASE[entity_name][item_id] = data",
                f"        return jsonify(data), 201",
            ])
        elif endpoint.method == "PUT":
            lines.extend([
                f"        entity_name = '{endpoint.entity_name.lower()}'",
                f"        data = request.get_json() or {{}}",
                f"        if id not in DATABASE.get(entity_name, {{}}):",
                f"            return jsonify({{'error': '{endpoint.entity_name} not found'}}), 404",
                f"        DATABASE[entity_name][id].update(data)",
                f"        DATABASE[entity_name][id]['updated_at'] = datetime.now().isoformat()",
                f"        return jsonify(DATABASE[entity_name][id]), 200",
            ])
        elif endpoint.method == "DELETE":
            lines.extend([
                f"        entity_name = '{endpoint.entity_name.lower()}'",
                f"        if id not in DATABASE.get(entity_name, {{}}):",
                f"            return jsonify({{'error': '{endpoint.entity_name} not found'}}), 404",
                f"        deleted = DATABASE[entity_name].pop(id)",
                f"        return jsonify({{'message': '{endpoint.entity_name} deleted', 'id': id}}), 200",
            ])

        # Add error handling
        lines.extend([
            "    except Exception as e:",
            "        logger.error(f'Error in {}: {{e}}'.format(__name__))",
            "        return jsonify({'error': str(e)}), 500",
        ])

        return lines

    @staticmethod
    def _generate_page_route(page) -> List[str]:
        """Generate a UI page route"""
        lines: List[str] = []
        route = page.route or f"/{page.name.lower()}"
        function_name = FlaskGenerator._sanitize_function_name(page.name.lower())

        auth_check = "    # TODO: Add auth check if required" if page.requires_auth else ""

        lines.extend([
            "",
            f"@app.route('{route}')",
            f"def {function_name}():",
            f"    \"\"\"Render {page.name} page\"\"\"",
            auth_check,
            f"    try:",
            f"        return render_template('{function_name}.html'), 200",
            f"    except Exception as e:",
            f"        logger.error(f'Error rendering {page.name}: {{e}}')",
            f"        return jsonify({{'error': 'Page not found'}}), 500",
        ])

        return lines

    @staticmethod
    def _generate_main() -> List[str]:
        """Generate main block - DO NOT add home or health routes (framework provides these)"""
        return [
            "",
            "if __name__ == '__main__':",
            "    port = int(os.getenv('PORT', 5000))",
            "    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])",
        ]

    @staticmethod
    def _sanitize_function_name(name: str) -> str:
        """Sanitize name to valid Python function name"""
        name = name.replace("-", "_").replace(" ", "_").lower()
        if name[0].isdigit():
            name = f"_{name}"
        return name
