from infrastructure.road import Road
from infrastructure.intersection import Intersection
import math

class Graph:
    def __init__(self):
        #initalize empty dictonary to store nodes and positions
        self.graph = {}
        self.intersections = {}
    
    def add_node(self, vertex, type, x, y):
        #add the vertex to the graph
        if vertex not in self.graph:
            #adds intesertion portion to graph
            intersection = Intersection(vertex, type, x, y)
            self.intersections[vertex] = intersection
            self.graph[vertex] = {}
            
            

    def calculate_length(self, vertex1, vertex2):
        #find distance between nodes
        x1, y1 = self.positions.get(vertex1)
        x2, y2 = self.positions.get(vertex2)
        return math.sqrt((x2-x1)**2 + (y2-y1)**2)

    def add_road(self, from_vertex, to_vertex, lanes = 1, speed_limit = 50, name = None):
        #adds road using road class and adds connections to intersection
        length = self.calculate_length(from_vertex, to_vertex)
        road = Road(from_vertex, to_vertex, length, lanes, speed_limit, name)
        self.graph[from_vertex][to_vertex] = road

        #adds connected road to intersection
        self.intersections[from_vertex].connected_roads.append(road)
    
    