import logging
from typing import List

from src.models.contracts import DatabaseSchema

logger = logging.getLogger(__name__)


class SQLGenerator:
    """
    Generates SQL DDL statements from database schema.
    Supports comprehensive type mapping and constraint generation.
    """

    # Complete type mapping for all supported field types
    TYPE_MAPPING = {
        "uuid": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
        "text": "TEXT NOT NULL",
        "integer": "INTEGER NOT NULL",
        "boolean": "BOOLEAN NOT NULL DEFAULT false",
        "timestamp": "TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP",
        "float": "NUMERIC(10,2) NOT NULL",
        "date": "DATE NOT NULL",
        "json": "JSONB",
        "array": "TEXT[] DEFAULT ARRAY[]::TEXT[]",
    }

    @staticmethod
    def generate(schema: DatabaseSchema) -> str:
        """Generate complete SQL DDL from database schema"""
        statements: List[str] = []

        for table in schema.tables:
            columns: List[str] = []

            for column in table.columns:
                # Get SQL type from mapping, default to TEXT
                base_type = SQLGenerator.TYPE_MAPPING.get(
                    column.type.lower(),
                    "TEXT"
                )

                # Build column definition
                col_def = f"  {column.name} {base_type}"

                # Add NULL constraint if nullable
                if column.nullable and "PRIMARY KEY" not in base_type:
                    col_def = col_def.replace("NOT NULL", "")
                    col_def = col_def.replace("  ", "  ").strip()
                    col_def = f"  {column.name} {base_type}".replace(
                        "NOT NULL", ""
                    ).strip()

                # Add description as comment if present
                if column.description:
                    col_def += f"  -- {column.description}"

                columns.append(col_def)

            # Build complete CREATE TABLE statement
            table_comment = f"-- {table.description}\n" if table.description else ""
            statement = (
                f"{table_comment}"
                f"CREATE TABLE IF NOT EXISTS {table.name} (\n"
                + ",\n".join(columns)
                + "\n);\n"
            )

            statements.append(statement)

        logger.info(f"[SQLGen] Generated {len(statements)} table definitions")
        return "\n".join(statements)

    @staticmethod
    def generate_indexes(schema: DatabaseSchema) -> str:
        """Generate index statements for performance optimization"""
        statements: List[str] = []

        for table in schema.tables:
            for column in table.columns:
                # Create indexes for common filter columns
                if column.type in ["uuid", "integer", "boolean"]:
                    idx_name = f"idx_{table.name}_{column.name}"
                    idx_stmt = f"CREATE INDEX IF NOT EXISTS {idx_name} ON {table.name}({column.name});"
                    statements.append(idx_stmt)

        return "\n".join(statements) if statements else ""

    @staticmethod
    def generate_migrations(
        old_schema: DatabaseSchema,
        new_schema: DatabaseSchema
    ) -> str:
        """Generate migration statements for schema changes"""
        # This is a simplified migration generator
        # In production, use Alembic or similar
        statements: List[str] = []

        old_tables = {t.name for t in old_schema.tables}
        new_tables = {t.name for t in new_schema.tables}

        # Add new tables
        for table in new_schema.tables:
            if table.name not in old_tables:
                statements.append(SQLGenerator.generate_for_table(table))

        return "\n".join(statements) if statements else ""

    @staticmethod
    def generate_for_table(table) -> str:
        """Helper to generate CREATE TABLE for a single table"""
        columns: List[str] = []

        for column in table.columns:
            base_type = SQLGenerator.TYPE_MAPPING.get(
                column.type.lower(),
                "TEXT"
            )
            col_def = f"  {column.name} {base_type}"
            if column.description:
                col_def += f"  -- {column.description}"
            columns.append(col_def)

        return (
            f"CREATE TABLE IF NOT EXISTS {table.name} (\n"
            + ",\n".join(columns)
            + "\n);\n"
        )
