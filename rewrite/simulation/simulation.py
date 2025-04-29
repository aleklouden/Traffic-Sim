import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class TrafficSimulation:
    def __init__(self, graph):
        self.graph = graph
        self.agents = []
        self.fig, self.ax = plt.subplots()

    def add_agent(self, agent):
        self.agents.append(agent)

    def update_agents(self, dt):
        for agent in self.agents:
            agent.move_agent(dt)  # Corrected call, only passing the time step

    def redraw_agents(self):
        self.ax.clear()
        for agent in self.agents:
            x, y = agent.position_on_road(self.graph)
            self.ax.plot(x, y, 'go', markersize=10)

        # Drawing roads and nodes (optional)
        for node, intersection in self.graph.intersections.items():
            self.ax.plot(intersection.x, intersection.y, 'ro')
            self.ax.text(intersection.x, intersection.y, node, fontsize=12, ha='right')

    def animate(self, frame):
        dt = 1.0
        self.update_agents(dt)
        self.redraw_agents()

    def run(self, dt=1.0, total_time=10.0):
        ani = FuncAnimation(self.fig, self.animate, frames=int(total_time / dt), interval=dt * 1000, blit=False)
        plt.show()
