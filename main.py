import random
random.seed(00000000)
from graph import build_small_graph_world
from metrics import GraphMetrics
from agent import Agent

__name__ = "__main__"
#Task 1: WORLD design





#Task 2: WORLD metrics



#Task 3: Agent design


    
    
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
