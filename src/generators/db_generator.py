import re
import logging

from src.models.contracts import (
    ApplicationIR,
    DatabaseSchema,
    TableSchema,
    ColumnSchema
)

logger = logging.getLogger(__name__)


class DatabaseGenerator:
    """
    Generates database schema from Application IR.
    Ensures proper type mapping and deterministic naming conventions.
    """

    # Type mapping from intent types to SQL types
    TYPE_MAPPING = {
        "uuid": "UUID",
        "text": "TEXT",
        "integer": "INTEGER",
        "boolean": "BOOLEAN",
        "timestamp": "TIMESTAMP",
        "float": "NUMERIC",
        "date": "DATE",
        "json": "JSONB",
        "array": "TEXT[]",
    }

    @staticmethod
    def generate(
        ir: ApplicationIR
    ) -> DatabaseSchema:
        """Generate complete database schema from IR"""

        tables = []

        for entity in ir.entities:
            columns = []

            for attribute in entity.attributes:
                sql_type = DatabaseGenerator.TYPE_MAPPING.get(
                    attribute.type.lower(),
                    "TEXT"
                )

                columns.append(
                    ColumnSchema(
                        name=DatabaseGenerator.to_snake_case(attribute.name),
                        type=sql_type,
                        nullable=attribute.nullable,
                        is_primary=attribute.is_primary,
                        description=attribute.description
                    )
                )

            tables.append(
                TableSchema(
                    name=DatabaseGenerator.to_snake_case(entity.name),
                    description=entity.description,
                    columns=columns
                )
            )

        return DatabaseSchema(tables=tables)

    @staticmethod
    def to_snake_case(name: str) -> str:
        """
        Convert CamelCase/PascalCase to snake_case.
        Regex approach ensures consistent results.
        """
        # Insert underscore before uppercase letters that follow lowercase
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name.replace(" ", ""))
        # Insert underscore before uppercase letters that follow lowercase or digits
        s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
        # Replace hyphens with underscores
        s3 = re.sub(r'-', '_', s2)
        # Convert to lowercase
        s4 = s3.lower()
        # Remove multiple consecutive underscores
        s4 = re.sub(r'_+', '_', s4)
        return s4.strip('_')
