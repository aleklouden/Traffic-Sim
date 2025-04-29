from rewrite.agents.agent import Agent

class Lane:
    def __init__(self, index, length):
        #lane index on road, length, vehicles
        self.index = index
        self.length = length
        self.agents = []

        self.road = None
        
        self.left = None
        self.right = None
    
    def set_neighbors(self, left, right):
        self.left = left
        self.right = right

    def set_road(self,road):
        self.road = road

    def add_agent(self,agent):
        agent.current_lane = self
        self.agents.append(agent)

   