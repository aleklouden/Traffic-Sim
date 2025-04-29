class Intersection:
    def __init__(self,vertex,type,x,y):
        self.vertex = vertex
        self.type = type
        self.x = x
        self.y = y

        self.exit_roads = []
        self.entrance_roads = []

    def add_entrance(self, road):
        self.entrance_roads.append(road)

    def add_exit(self,road):
        self.exit_roads.append(road)

    def position(self):
        return (self.x, self.y)

    def can_proceed(self, agent):
        #is overidden by the other classes
        pass

class TrafficLight(Intersection):
    def __init__(self, vertex, type, x, y):
        super().__init__(vertex, type, x, y)

    
        