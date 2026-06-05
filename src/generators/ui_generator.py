import logging

from src.models.contracts import (
    ApplicationIR,
    UISchema,
    PageSchema,
    ComponentSchema
)

logger = logging.getLogger(__name__)


class UIGenerator:
    """
    Generates UI schema from Application IR.
    Creates pages and components dynamically based on entities and features.
    """

    @staticmethod
    def generate(
        ir: ApplicationIR
    ) -> UISchema:
        """Generate UI pages and components from IR"""

        pages = []

        # Landing/Home page
        pages.append(
            PageSchema(
                name="Home",
                route="/",
                description="Landing page with app overview",
                components=[
                    ComponentSchema(
                        name="Header",
                        type="header",
                        properties={
                            "title": ir.app_name,
                            "description": ir.description
                        }
                    ),
                    ComponentSchema(
                        name="Navigation",
                        type="nav",
                        properties={}
                    ),
                    ComponentSchema(
                        name="HeroSection",
                        type="section",
                        properties={}
                    )
                ],
                requires_auth=False
            )
        )

        # Dashboard page (if features mention dashboard)
        if any("dashboard" in f.lower() for f in ir.features):
            pages.append(
                PageSchema(
                    name="Dashboard",
                    route="/dashboard",
                    description="Main dashboard view",
                    components=[
                        ComponentSchema(
                            name="StatsCards",
                            type="stat_cards",
                            properties={}
                        ),
                        ComponentSchema(
                            name="ChartPanel",
                            type="chart",
                            properties={}
                        )
                    ],
                    requires_auth=True,
                    required_roles=["admin", "user"]
                )
            )

        # Entity pages - list and detail for each entity
        for entity in ir.entities:
            # List page
            pages.append(
                PageSchema(
                    name=f"{entity.name}List",
                    route=f"/{entity.name.lower()}",
                    description=f"List all {entity.name} records",
                    components=[
                        ComponentSchema(
                            name="Table",
                            type="table",
                            entity_binding=entity.name,
                            properties={
                                "columns": [attr.name for attr in entity.attributes],
                                "sortable": True,
                                "filterable": True
                            }
                        ),
                        ComponentSchema(
                            name="CreateButton",
                            type="button",
                            properties={"label": f"New {entity.name}"}
                        )
                    ],
                    requires_auth=True
                )
            )

            # Create/Edit form page
            pages.append(
                PageSchema(
                    name=f"{entity.name}Form",
                    route=f"/{entity.name.lower()}/form",
                    description=f"Create/Edit {entity.name}",
                    components=[
                        ComponentSchema(
                            name="Form",
                            type="form",
                            entity_binding=entity.name,
                            properties={
                                "fields": [
                                    {
                                        "name": attr.name,
                                        "type": attr.type,
                                        "required": not attr.nullable,
                                        "description": attr.description
                                    }
                                    for attr in entity.attributes
                                    if not attr.is_primary
                                ]
                            }
                        )
                    ],
                    requires_auth=True
                )
            )

        # Feature pages
        for feature in ir.features:
            # Skip if already handled
            if feature.lower() in ["dashboard", "authentication"]:
                continue

            pages.append(
                PageSchema(
                    name=f"{feature.replace(' ', '')}Page",
                    route=f"/{feature.lower().replace(' ', '-')}",
                    description=f"{feature} section",
                    components=[
                        ComponentSchema(
                            name=f"{feature}View",
                            type="feature_view",
                            properties={"feature_name": feature}
                        )
                    ],
                    requires_auth=True
                )
            )

        # Admin pages if admin role exists
        if "admin" in ir.roles:
            pages.append(
                PageSchema(
                    name="AdminPanel",
                    route="/admin",
                    description="Admin management interface",
                    components=[
                        ComponentSchema(
                            name="UserManagement",
                            type="table",
                            entity_binding="User",
                            properties={}
                        ),
                        ComponentSchema(
                            name="SystemLogs",
                            type="logs",
                            properties={}
                        )
                    ],
                    requires_auth=True,
                    required_roles=["admin"]
                )
            )

        return UISchema(
            pages=pages
        )
