class RequirementsGenerator:

    @staticmethod
    def generate() -> str:

        requirements = [
            "flask>=3.0.0"
        ]

        return "\n".join(
            requirements
        )