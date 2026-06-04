from src.models.contracts import (
    ApplicationIR,
    AuthSchema,
    RoleSchema
)


class AuthGenerator:

    @staticmethod
    def generate(
        ir: ApplicationIR
    ) -> AuthSchema:

        roles = []

        for role in ir.roles:

            roles.append(
                RoleSchema(
                    name=role,
                    permissions=[]
                )
            )

        return AuthSchema(
            roles=roles
        )