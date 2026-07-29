import random
random.seed(00000000)
from graph import build_small_graph_world
from metrics import GraphMetrics
from agent import Agent
from simulation import run_simulations

__name__ = "__main__"

def main():
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



if __name__ == "__main__":
   main()
    
