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
