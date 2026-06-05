from src.state.dependency_graph import (
    DependencyGraph
)

graph = DependencyGraph()

graph.add_dependency(
    "Contact",
    "ContactTable"
)

graph.add_dependency(
    "ContactTable",
    "ContactAPI"
)

graph.add_dependency(
    "ContactAPI",
    "ContactPage"
)

impacted = (
    graph.get_impacted_nodes(
        "Contact"
    )
)

print(impacted)