import logging

from src.models.contracts import (
    ApplicationIR,
    APISchema,
    EndpointSchema,
    ParameterSchema
)

logger = logging.getLogger(__name__)


class APIGenerator:
    """
    Generates API schema from Application IR.
    Creates CRUD endpoints for each entity with dynamic field mappings.
    """

    @staticmethod
    def generate(
        ir: ApplicationIR
    ) -> APISchema:
        """Generate REST API endpoints from IR entities"""

        endpoints = []

        for entity in ir.entities:
            base_path = f"/{entity.name}"

            # Extract field names for response documentation
            field_names = [attr.name for attr in entity.attributes]
            response_fields = field_names

            # GET (List) endpoint
            endpoints.append(
                EndpointSchema(
                    path=base_path,
                    method="GET",
                    entity_name=entity.name,
                    description=f"List all {entity.name} records",
                    parameters=[
                        ParameterSchema(
                            name="limit",
                            type="integer",
                            required=False,
                            description="Number of records to return"
                        ),
                        ParameterSchema(
                            name="offset",
                            type="integer",
                            required=False,
                            description="Number of records to skip"
                        )
                    ],
                    response_fields=response_fields,
                    requires_auth=True
                )
            )

            # POST (Create) endpoint
            create_params = [
                ParameterSchema(
                    name=attr.name,
                    type=attr.type,
                    required=not attr.nullable,
                    description=attr.description
                )
                for attr in entity.attributes
                if not attr.is_primary  # Exclude id from create params
            ]

            endpoints.append(
                EndpointSchema(
                    path=base_path,
                    method="POST",
                    entity_name=entity.name,
                    description=f"Create new {entity.name}",
                    parameters=create_params,
                    response_fields=response_fields,
                    requires_auth=True
                )
            )

            # GET (Read) endpoint with ID
            endpoints.append(
                EndpointSchema(
                    path=f"{base_path}/{{id}}",
                    method="GET",
                    entity_name=entity.name,
                    description=f"Get {entity.name} by ID",
                    parameters=[
                        ParameterSchema(
                            name="id",
                            type="uuid",
                            required=True,
                            description="Record ID"
                        )
                    ],
                    response_fields=response_fields,
                    requires_auth=True
                )
            )

            # PUT (Update) endpoint
            update_params = [
                ParameterSchema(
                    name=attr.name,
                    type=attr.type,
                    required=False,
                    description=attr.description
                )
                for attr in entity.attributes
                if not attr.is_primary
            ]

            endpoints.append(
                EndpointSchema(
                    path=f"{base_path}/{{id}}",
                    method="PUT",
                    entity_name=entity.name,
                    description=f"Update {entity.name}",
                    parameters=update_params,
                    response_fields=response_fields,
                    requires_auth=True
                )
            )

            # DELETE endpoint
            endpoints.append(
                EndpointSchema(
                    path=f"{base_path}/{{id}}",
                    method="DELETE",
                    entity_name=entity.name,
                    description=f"Delete {entity.name}",
                    parameters=[
                        ParameterSchema(
                            name="id",
                            type="uuid",
                            required=True,
                            description="Record ID"
                        )
                    ],
                    requires_auth=True
                )
            )

        return APISchema(
            endpoints=endpoints
        )
