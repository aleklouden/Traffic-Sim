from infrastructure.road import Road
import math

class Graph:
    def __instancecheck__(self):
        #initalize empty dictonary to store nodes and positions
        self.graph = {}
        self.positions = {}
    
    def add_node(self, vertex, x, y):
        #add the vertex to the graph
        if vertex not in self.graph:
            self.graph[vertex] = {}
            self.positions[vertex] = (x,y)

    def calculate_length(self, vertex1, vertex2):
        #find distance between nodes
        x1, y1 = self.positions.get(vertex1)
        x2, y2 = self.positions.get(vertex2)
        return math.sqrt((x2-x1)**2 + (y2-y1)**2)

    def add_road(self, from_vertex, to_vertex, lanes = 1, speed_limit = 50, name = None):
        length = self.calculate_length(from_vertex, to_vertex)
        road = Road(from_vertex, to_vertex, length, lanes, speed_limit, name)
        self.graph[from_vertex][to_vertex] = road

    
    