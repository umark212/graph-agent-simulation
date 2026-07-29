import random
from graph import Graph

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
