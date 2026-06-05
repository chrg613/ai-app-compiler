import logging
import os
from datetime import datetime

from src.codegen.sql_generator import SQLGenerator
from src.codegen.flask_generator import FlaskGenerator
from src.codegen.file_writer import FileWriter
from src.codegen.requirements_generator import RequirementsGenerator
from src.codegen.readme_generator import ReadmeGenerator
from src.codegen.html_generator import HTMLGenerator
from src.codegen.css_generator import CSSGenerator
from src.codegen.js_generator import JSGenerator

logger = logging.getLogger(__name__)


class Exporter:
    """
    Exports generated application to filesystem.
    Creates complete project structure with all necessary files.
    """

    @staticmethod
    def export(app_name, db_schema, api_schema, ui_schema):
        """
        Export compilation result to filesystem.
        Creates a complete application directory structure.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_dir = f"generated/{app_name}_{timestamp}"

        logger.info(f"[Exporter] Starting export to {project_dir}")

        # Create project structure
        os.makedirs(project_dir, exist_ok=True)
        os.makedirs(f"{project_dir}/templates", exist_ok=True)
        os.makedirs(f"{project_dir}/static/css", exist_ok=True)
        os.makedirs(f"{project_dir}/static/js", exist_ok=True)

        # Generate all files
        try:
            # Database schema
            sql = SQLGenerator.generate(db_schema)
            sql_indexes = SQLGenerator.generate_indexes(db_schema)
            FileWriter.write(project_dir, "schema.sql", sql)
            if sql_indexes:
                FileWriter.write(project_dir, "indexes.sql", sql_indexes)
            logger.info("[Exporter] Generated database schema")

            # Flask application
            flask_code = FlaskGenerator.generate(api_schema, ui_schema)
            FileWriter.write(project_dir, "app.py", flask_code)
            logger.info("[Exporter] Generated Flask application")

            # Requirements
            requirements = RequirementsGenerator.generate()
            FileWriter.write(project_dir, "requirements.txt", requirements)
            logger.info("[Exporter] Generated requirements.txt")

            # README
            readme = ReadmeGenerator.generate(app_name)
            FileWriter.write(project_dir, "README.md", readme)
            logger.info("[Exporter] Generated README.md")

            # HTML pages
            html_pages = HTMLGenerator.generate(ui_schema)
            for filename, content in html_pages.items():
                FileWriter.write(f"{project_dir}/templates", filename, content)
            logger.info(f"[Exporter] Generated {len(html_pages)} HTML pages")

            # CSS stylesheet
            css = CSSGenerator.generate()
            FileWriter.write(f"{project_dir}/static/css", "style.css", css)
            logger.info("[Exporter] Generated style.css")

            # JavaScript utilities
            js = JSGenerator.generate()
            FileWriter.write(f"{project_dir}/static/js", "app.js", js)
            logger.info("[Exporter] Generated app.js")

            # Environment template
            env_template = Exporter._generate_env_template()
            FileWriter.write(project_dir, ".env.example", env_template)
            logger.info("[Exporter] Generated .env.example")

            # Docker configuration
            docker_config = Exporter._generate_dockerfile(app_name)
            FileWriter.write(project_dir, "Dockerfile", docker_config)
            logger.info("[Exporter] Generated Dockerfile")

            # Docker Compose
            docker_compose = Exporter._generate_docker_compose(app_name)
            FileWriter.write(project_dir, "docker-compose.yml", docker_compose)
            logger.info("[Exporter] Generated docker-compose.yml")

            # Package.json
            package_json = Exporter._generate_package_json(app_name)
            FileWriter.write(project_dir, "package.json", package_json)
            logger.info("[Exporter] Generated package.json")

            # Export manifest
            manifest = Exporter._generate_manifest(app_name)
            FileWriter.write(project_dir, "PROJECT.json", manifest)
            logger.info("[Exporter] Generated PROJECT.json")

            logger.info(f"[Exporter] Export completed successfully to {project_dir}")

            return {
                'status': 'success',
                'project_dir': project_dir,
                'files_created': 10 + len(html_pages),
                'schemas': {
                    'database': 'schema.sql',
                    'api': 'app.py',
                    'ui': 'templates/*',
                    'styling': 'static/css/style.css',
                    'scripts': 'static/js/app.js'
                }
            }

        except Exception as e:
            logger.error(f"[Exporter] Export failed: {e}")
            raise

    @staticmethod
    def _generate_env_template() -> str:
        """Generate .env.example template"""
        return """# Environment Configuration
# Copy this to .env and fill in your values

# Application
APP_ENV=development
APP_DEBUG=True

# API Configuration
API_HOST=0.0.0.0
API_PORT=5000

# Logging
LOG_LEVEL=INFO

# Database (optional)
DATABASE_URL=

# Security
SECRET_KEY=change_me_in_production
"""

    @staticmethod
    def _generate_dockerfile(app_name: str) -> str:
        """Generate Dockerfile for containerization"""
        return f"""FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "app.py"]
"""

    @staticmethod
    def _generate_docker_compose(app_name: str) -> str:
        """Generate docker-compose.yml"""
        return f"""version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
      - APP_DEBUG=True
    volumes:
      - .:/app
    command: python app.py
"""

    @staticmethod
    def _generate_package_json(app_name: str) -> str:
        """Generate package.json"""
        import json
        package = {
            "name": app_name.lower().replace(" ", "-"),
            "version": "1.0.0",
            "description": f"{app_name} - Generated by AI Application Compiler",
            "scripts": {
                "start": "python app.py",
                "dev": "python app.py",
                "docker:up": "docker-compose up -d",
                "docker:down": "docker-compose down"
            },
            "keywords": ["generated", "ai-compiler"],
            "license": "MIT"
        }
        return json.dumps(package, indent=2)

    @staticmethod
    def _generate_manifest(app_name: str) -> str:
        """Generate PROJECT.json manifest"""
        import json
        manifest = {
            "name": app_name,
            "version": "1.0.0",
            "generated_at": datetime.now().isoformat(),
            "generator": "AI Application Compiler v2.1",
            "structure": {
                "app.py": "Flask application",
                "schema.sql": "Database schema",
                "templates": "HTML templates",
                "requirements.txt": "Python dependencies"
            }
        }
        return json.dumps(manifest, indent=2)