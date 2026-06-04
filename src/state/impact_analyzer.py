class ImpactAnalyzer:

    COMPONENT_MAP = {
        "Table": "Database",
        "API": "API",
        "Page": "UI",
        "Role": "Auth"
    }

    @staticmethod
    def analyze(
        impacted_nodes
    ):

        affected_components = set()

        for node in impacted_nodes:

            for key, component in (
                ImpactAnalyzer
                .COMPONENT_MAP
                .items()
            ):

                if key in node:

                    affected_components.add(
                        component
                    )

        return affected_components
    
# TODO:
# Replace string matching
# with typed dependency nodes.