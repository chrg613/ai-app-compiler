import logging

from src.models.contracts import (
    ApplicationIR,
    AuthSchema,
    RoleSchema,
    PermissionSchema
)

logger = logging.getLogger(__name__)


class AuthGenerator:
    """
    Generates authentication and authorization schema from Application IR.
    Creates roles with dynamic permissions based on entities and features.
    """

    # Standard permissions that can be mapped to resources
    STANDARD_PERMISSIONS = {
        "view": "Read access",
        "create": "Create access",
        "edit": "Update access",
        "delete": "Delete access",
        "admin": "Administrative access",
        "manage": "Management access"
    }

    @staticmethod
    def generate(
        ir: ApplicationIR
    ) -> AuthSchema:
        """Generate auth schema with roles and permissions from IR"""

        roles = []

        # Generate admin role if exists
        admin_permissions = [
            PermissionSchema(
                name="admin_access",
                description="Full administrative access",
                resource="all",
                action="admin"
            ),
            PermissionSchema(
                name="manage_users",
                description="Manage user accounts",
                resource="users",
                action="manage"
            ),
            PermissionSchema(
                name="view_analytics",
                description="View system analytics",
                resource="analytics",
                action="view"
            )
        ]

        # Add entity-specific permissions for admin
        for entity in ir.entities:
            admin_permissions.extend([
                PermissionSchema(
                    name=f"manage_{entity.name.lower()}",
                    description=f"Manage {entity.name} records",
                    resource=entity.name.lower(),
                    action="manage"
                )
            ])

        if "admin" in ir.roles:
            roles.append(
                RoleSchema(
                    name="admin",
                    description="Administrator with full access",
                    permissions=admin_permissions
                )
            )

        # Generate user role (standard)
        user_permissions = []

        for entity in ir.entities:
            user_permissions.extend([
                PermissionSchema(
                    name=f"view_{entity.name.lower()}",
                    description=f"View {entity.name} records",
                    resource=entity.name.lower(),
                    action="view"
                ),
                PermissionSchema(
                    name=f"create_{entity.name.lower()}",
                    description=f"Create {entity.name} records",
                    resource=entity.name.lower(),
                    action="create"
                ),
                PermissionSchema(
                    name=f"edit_{entity.name.lower()}",
                    description=f"Edit own {entity.name} records",
                    resource=entity.name.lower(),
                    action="edit"
                )
            ])

        # Add feature-based permissions
        if "payments" in [f.lower() for f in ir.features]:
            user_permissions.append(
                PermissionSchema(
                    name="make_payment",
                    description="Make payments",
                    resource="payments",
                    action="create"
                )
            )

        if "user" in ir.roles or "user" not in [r.name for r in roles]:
            roles.append(
                RoleSchema(
                    name="user",
                    description="Standard user access",
                    permissions=user_permissions
                )
            )

        # Generate other custom roles
        for role_name in ir.roles:
            if role_name not in ["admin", "user"]:
                custom_permissions = []

                # Generate role-specific permissions
                for entity in ir.entities:
                    custom_permissions.append(
                        PermissionSchema(
                            name=f"view_{entity.name.lower()}",
                            description=f"View {entity.name}",
                            resource=entity.name.lower(),
                            action="view"
                        )
                    )

                roles.append(
                    RoleSchema(
                        name=role_name,
                        description=f"{role_name} role",
                        permissions=custom_permissions
                    )
                )

        return AuthSchema(
            roles=roles
        )
