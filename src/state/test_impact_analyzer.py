from src.state.impact_analyzer import (
    ImpactAnalyzer
)

impacted_nodes = [
    "ContactTable",
    "ContactAPI",
    "ContactPage"
]

components = (
    ImpactAnalyzer.analyze(
        impacted_nodes
    )
)

print(components)