from src.models.contracts import (
    ApplicationIR,
    APISchema,
    EndpointSchema
)


class APIGenerator:

    @staticmethod
    def generate(
        ir: ApplicationIR
    ) -> APISchema:

        endpoints = []

        for entity in ir.entities:

            base_path = f"/{entity.name.lower()}"

            endpoints.extend([
                EndpointSchema(
                    path=base_path,
                    method="GET",
                    entity_name=entity.name,
                    description=f"List {entity.name}"
                    
                ),
                EndpointSchema(
                    path=base_path,
                    method="POST",
                    entity_name=entity.name,
                    description=f"Create {entity.name}"
                ),
                EndpointSchema(
                    path=f"{base_path}/{{id}}",
                    method="GET",
                    entity_name=entity.name,
                    description=f"Get {entity.name}"
                ),
                EndpointSchema(
                    path=f"{base_path}/{{id}}",
                    method="PUT",
                    entity_name=entity.name,
                    description=f"Update {entity.name}"
                ),
                EndpointSchema(
                    path=f"{base_path}/{{id}}",
                    method="DELETE",
                    entity_name=entity.name,
                    description=f"Delete {entity.name}"
                )
            ])

        return APISchema(
            endpoints=endpoints
        )