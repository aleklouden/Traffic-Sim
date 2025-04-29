from rewrite.infrastructure.road import Road
from rewrite.infrastructure.intersection import Intersection
import math

class Graph:
    def __init__(self):
        # Initialize empty dictionaries to store nodes, intersections, and positions
        self.graph = {}
        self.intersections = {}
        self.positions = {}
    
    def add_node(self, vertex, type, x, y):
        # Add the vertex to the graph
        if vertex not in self.graph:
            intersection = Intersection(vertex, type, x, y)
            self.intersections[vertex] = intersection
            self.graph[vertex] = {}
            self.positions[vertex] = (x, y)
    
    def calculate_length(self, vertex1, vertex2):
        # Calculate the distance between two nodes
        x1, y1 = self.positions.get(vertex1)
        x2, y2 = self.positions.get(vertex2)
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def add_road(self, from_vertex, to_vertex, lanes=1, speed_limit=50, name=None):
        # Adds a road using the Road class and adds connections to intersections
        length = self.calculate_length(from_vertex, to_vertex)
        road = Road(from_vertex, to_vertex, length, lanes, speed_limit, name)
        self.graph[from_vertex][to_vertex] = road
        self.intersections[from_vertex].add_exit(road)
        self.intersections[to_vertex].add_entrance(road)
    
    def get_turn_direction(self, road1, road2):
        # Get the turn direction an agent will be moving at an intersection (straight, left, right)
        A = self.positions[road1.from_vertex]
        B = self.positions[road1.to_vertex]
        C = self.positions[road2.to_vertex]

        # Vectors for angles
        v1 = (B[0] - A[0], B[1] - A[1])
        v2 = (C[0] - B[0], C[1] - B[1])

        # Normalize and calculate angle
        def normalize(v):
            length = math.hypot(v[0], v[1])
            return (v[0] / length, v[1] / length) if length else (0, 0)
        
        v1 = normalize(v1)
        v2 = normalize(v2)

        dot = v1[0] * v2[0] + v1[1] * v2[1]
        det = v1[0] * v2[1] - v1[1] * v2[0]
        angle = math.atan2(det, dot)
        degrees = math.degrees(angle)

        if -30 <= degrees <= 30:
            return "straight"
        elif degrees > 30:
            return "left"
        elif degrees < -30:
            return "right"
        return "unknown"
