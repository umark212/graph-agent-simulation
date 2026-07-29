import random
random.seed(00000000)

__name__ = "__main__"
#Task 1: WORLD design

class Node:
    def __init__(self, name):
        #stores node name and connected edges
        self.name = name
        self.edges = []

    def add_edge(self, edge):
        #adds an edge to this node
        self.edges.append(edge)

    def get_neighbours(self):
        #returns neighbouring nodes connected by edges
        neighbours = []
        for edge in self.edges:
            neighbours.append(edge.get_other_node(self))
        return neighbours

    def get_name(self):
        #Returns node name
        return self.name


class Edge:
    def __init__(self, node1, node2):
        #stores an undirected connection between 2 nodes
        self.node1 = node1
        self.node2 = node2

    def get_other_node(self, current_node):
        #returns the node on the other side of the edge
        if current_node == self.node1:
            return self.node2
        return self.node1

    def get_nodes(self):
        #returns both nodes of the edge
        return self.node1, self.node2


class Graph:
    def __init__(self):
        #Stores all nodes and edges in the graph
        self.nodes = {}
        self.edges = []

    def add_node(self, name):
        #adds a node to the graph
        self.nodes[name] = Node(name)

    def add_edge(self, name1, name2):
        #adds an undirected edge between 2 named nodes
        node1 = self.nodes[name1]
        node2 = self.nodes[name2]

        edge = Edge(node1, node2)
        self.edges.append(edge)

        node1.add_edge(edge)
        node2.add_edge(edge)

    def get_node(self, name):
        #returns a node by name
        return self.nodes[name]

    def get_all_nodes(self):
        #returns all nodes in the graph
        return list(self.nodes.values())

    def get_all_edges(self):
        #returns all edges in the graph
        return self.edges
    
    def get_node_names(self):
        #returns all node names in the graph
        return list(self.nodes.keys())


def build_small_graph_world():
    #Builds the 7 node 7 edge graph from the paper

    graph = Graph()

    #add nodes
    for name in ["v1", "v2", "v3", "v4", "v5", "v6", "v7"]:
        graph.add_node(name)

    #add edges based on the paper figure
    graph.add_edge("v1", "v2")
    graph.add_edge("v2", "v3")
    graph.add_edge("v3", "v4")
    graph.add_edge("v4", "v5")
    graph.add_edge("v3", "v6")
    graph.add_edge("v4", "v7")
    graph.add_edge("v6", "v7")

    return graph



#Task 2: WORLD metrics

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

            result[node.get_name()] = 1 / total_distance

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
    


#Task 3: Agent design

class Agent:
    def __init__(self, graph):
        #stores graph, current node, target node and visited path
        self.graph = graph
        self.current_node = None
        self.target_node = None
        self.memory = []

        #stores all shortest paths between node pairs
        self.shortest_paths = {}
        self.precompute_shortest_paths()

    def find_shortest_path(self, start_name, goal_name):
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
                    neighbour_name = neighbour.get_name()

                    if neighbour_name not in visited:
                        queue.append((neighbour_name, path + [neighbour_name]))

        return None

    def precompute_shortest_paths(self):
        #computes shortest paths between every pair of nodes once
        node_names = []

        for node in self.graph.get_all_nodes():
            node_names.append(node.get_name())

        for start_name in node_names:
            for goal_name in node_names:
                if start_name != goal_name:
                    self.shortest_paths[(start_name, goal_name)] = self.find_shortest_path(start_name, goal_name)

    def set_start_and_target(self, start_name, target_name):
        #sets the start node and target node for one episode
        self.current_node = start_name
        self.target_node = target_name
        self.memory = [start_name]

    def sense_current_node(self):
        #returns the current node name
        return self.current_node

    def get_memory(self):
        #returns the full visited path
        return self.memory

    def run_random_walk(self):
        #moves randomly until target is reached
        while self.current_node != self.target_node:
            current_graph_node = self.graph.get_node(self.current_node)
            neighbours = current_graph_node.get_neighbours()

            next_node = random.choice(neighbours).get_name()
            self.current_node = next_node
            self.memory.append(next_node)

        return self.memory

    def run_shortest_path_walk(self):
        #uses stored shortest path from start node to target node
        path = self.shortest_paths[(self.current_node, self.target_node)]
        self.memory = path
        self.current_node = self.target_node

        return self.memory    
    
    
#Task 4: Simulation

def run_simulations(graph):
    #runs 500 random walk and 500 shortest path simulations
    random_results = []
    shortest_results = []

    node_names = graph.get_node_names()

    for _ in range(500):
        start_name, target_name = random.sample(node_names, 2)

        agent = Agent(graph)
        agent.set_start_and_target(start_name, target_name)
        path = agent.run_random_walk()

        random_results.append(len(path))

    for _ in range(500):
        start_name, target_name = random.sample(node_names, 2)

        agent = Agent(graph)
        agent.set_start_and_target(start_name, target_name)
        path = agent.run_shortest_path_walk()

        shortest_results.append(len(path))

    return random_results, shortest_results



if __name__ == "__main__":
   
    #task 1 test
    graph = build_small_graph_world()

    print("Nodes:")
    for node in graph.get_all_nodes():
        print(node.get_name())

    print("\nEdges:")
    for edge in graph.get_all_edges():
        node1, node2 = edge.get_nodes()
        print(node1.get_name(), "-", node2.get_name())

    
    

    #task 2 test
    graph = build_small_graph_world()
    metrics = GraphMetrics(graph)

    degree = metrics.degree_centrality()
    closeness = metrics.closeness_centrality()
    betweenness = metrics.betweenness_centrality()

    print("Node | Degree | Closeness | Betweenness")
    for node_name in degree:
        print(
            node_name,
            "|",
            degree[node_name],
            "|",
            round(closeness[node_name], 4),
            "|",
            round(betweenness[node_name], 4)
        )


    #task 4 test
    random_results, shortest_results = run_simulations(graph)

    print("\nRandom walk average visited nodes:", sum(random_results) / len(random_results))
    print("Shortest path average visited nodes:", sum(shortest_results) / len(shortest_results))
