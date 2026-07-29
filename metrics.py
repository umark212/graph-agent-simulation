class GraphMetrics:
    def __init__(self, graph):
        #stores the graph for metric calculations
        self.graph = graph

    def shortest_path(self, start_name, goal_name):
        #uses bfs to find one shortest path between 2 nodes
        queue = [(start_name, [start_name])]
        visited = []

        while queue:
            current_name, path = queue.pop(0)

            if current_name == goal_name:
                return path

            if current_name not in visited:
                visited.append(current_name)

                current_node = self.graph.get_node(current_name)
                for neighbour in current_node.get_neighbours():
                    if neighbour.get_name() not in visited:
                        queue.append((neighbour.get_name(), path + [neighbour.get_name()]))

        return None

    

    def degree_centrality(self):
        #degree centrality is number of connected neighbours
        result = {}

        for node in self.graph.get_all_nodes():
            result[node.get_name()] = len(node.get_neighbours())

        return result

    def closeness_centrality(self):
        #closeness centrality is 1 / sum of shortest path distances
        result = {}

        for node in self.graph.get_all_nodes():
            total_distance = 0

            for other_node in self.graph.get_all_nodes():
                if node.get_name() != other_node.get_name():
                    path = self.shortest_path(node.get_name(), other_node.get_name())
                    total_distance += len(path) - 1

                    #added a check if a valid path exists to avoid nonetype error
                    if path is not None:
                        total_distance += len(path) - 1
            #prevent zero division errors if a node is completely isolated
            result[node.get_name()] = 1 / total_distance if total_distance > 0 else 0.0

        return result

    def betweenness_centrality(self):
        #betweenness centrality is the number of shortest paths passing through a node
        result = {}

        for node in self.graph.get_all_nodes():
            result[node.get_name()] = 0

        node_names = [node.get_name() for node in self.graph.get_all_nodes()]

        for i in range(len(node_names)):
            for j in range(i + 1, len(node_names)):
                start = node_names[i]
                goal = node_names[j]

                path = self.shortest_path(start, goal)

                if path:
                    for node_name in path[1:-1]:
                        result[node_name] += 1

        return result
    
