import random

from agent import Agent

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
