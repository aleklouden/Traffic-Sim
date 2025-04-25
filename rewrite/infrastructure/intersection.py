class Intersection:
    def __init__(self,vertex,type,x,y):
        self.vertex = vertex
        self.type = type
        self.x = x
        self.y = y

        self.connected_roads = []

    def position(self):
        return (self.x, self.y)
        