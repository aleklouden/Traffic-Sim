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

    def should_yeild(self, from_road, to_road, turning_direction, agent):
        return False
    
#supe
class StopSignIntersection(Intersection):
    def should_yield(self, from_road, to_road, turning_direction, agent):
        # Yield if any other vehicle has priority (simple example)
        for other_agent in self.get_agents_incoming():
            if other_agent != agent and other_agent.arrival_time < agent.arrival_time:
                return True
        return False
    
class RoundaboutIntersection(Intersection):
    def should_yield(self, from_road, to_road, turning_direction, agent):
        # Yield to agents already in the roundabout
        for other_agent in self.get_agents_in_roundabout():
            if other_agent != agent:
                return True
        return False

class TrafficLightIntersection(Intersection):
    def __init__(self, vertex, type, x, y):
        super().__init__(vertex, type, x, y)
        self.light_state = {}  # {road: 'green' | 'red' | 'yellow'}

    def should_yield(self, from_road, to_road, turning_direction, agent):
        state = self.light_state.get(from_road)
        if state != 'green':
            return True
        if turning_direction == 'right':
            # maybe allow right-on-red after stop
            return False
        return False
    
        