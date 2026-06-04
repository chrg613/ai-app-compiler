from collections import defaultdict


class DependencyGraph:

    def __init__(self):

        self.graph = defaultdict(list)

    def add_dependency(
        self,
        parent: str,
        child: str
    ):

        self.graph[parent].append(
            child
        )

    def get_impacted_nodes(
        self,
        start_node: str
    ):

        visited = set()

        impacted = set()

        def dfs(node):

            if node in visited:
                return

            visited.add(node)

            for child in self.graph[node]:

                impacted.add(child)

                dfs(child)

        dfs(start_node)

        return impacted