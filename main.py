import random
random.seed(00000000)
from graph import build_small_graph_world
from metrics import GraphMetrics

__name__ = "__main__"
#Task 1: WORLD design





#Task 2: WORLD metrics



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

        if path is not None:
            shortest_results.append(len(path))
        else:
            #handle disconnected pairs by appending a 0 or ignoring them
            pass


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
