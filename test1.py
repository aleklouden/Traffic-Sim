from rewrite.routing.graph import Graph
from rewrite.agents.agent import Agent
from rewrite.simulation.simulation import TrafficSimulation
from rewrite.routing.pathfinder import dijkstra

def main():
    # Create a graph and add nodes and roads
    graph = Graph()
    graph.add_node('A', 'stop', 0, 0)
    graph.add_node('B', 'stop', 50, 0)
    graph.add_node('C', 'stop', 0, -50)
    graph.add_node('D', 'stop', 50, -50)

    # Add roads
    graph.add_road('A', 'B')
    graph.add_road('B', 'A')

    graph.add_road('A', 'C')
    graph.add_road('C', 'A')

    graph.add_road('B', 'D')
    graph.add_road('D', 'B')

    graph.add_road('C', 'D')
    graph.add_road('D', 'C')

    # Run Dijkstra's algorithm to find the shortest path from A to D
    #route = dijkstra(graph, 'A', 'D')
    
    #print(route)  # This will print the route with the turn directions

    # Create a TrafficSimulation instance
    simulation = TrafficSimulation(graph)

    # Create agents (vehicles) that will traverse the graph
    agent1 = Agent(1, graph,'A', 'D')  # Example: Agent starts at A and is headed to D
    agent2 = Agent(2, graph,'B', 'C')  # Another agent starting at B and heading to C

    print(agent1.current_road)
    # Add agents to the simulation
    simulation.add_agent(agent1)
    #imulation.add_agent(agent2)

    # Run the simulation
    simulation.run()

if __name__ == "__main__":
    main()
