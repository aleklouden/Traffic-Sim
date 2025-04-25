from routing.pathfinder import dijkstra

class Agent:
    def __init__(self, agent_id, graph, start_vertex, end_vertex, reaction_time = .5, look_ahead_distance = 10, agent_length = 1, acceleration = 1, deacceleration = 1, mass = 500, speed_multiplier = 1):
        self.agent_id = agent_id

        #move attributes
        self.route = dijkstra(graph, start_vertex, end_vertex) or []
        self.speed = 0
        self.reaction_time = reaction_time
        self.look_ahead_distance = look_ahead_distance
        self.agent_length = agent_length
        self.acceleration = acceleration
        self.deacceleration = deacceleration
        self.mass = mass
        self.speed_multiplier = speed_multiplier

        #road/lane info
        self.current_road = None
        self.current_lane = None
        self.postion = 0 #distance on path

    def move_agent(self):
        pass
    
    def change_lanes(self):
         pass
    def obstacle_info(self):
            """
            Inputs: vehicle/agent

            Output: distance and speed of vehicle ahead

            Description: find the closest vehicle/object to the vehicle you are looking at
            """

            #checking closest agent/vehicle to the current/selected one
            for other_agent in sorted(self.curr_lane.agents, key = lambda v: v.position):
                #see if another agent/vehicle is on this path infront of this vehicle(above since below is behind them)
                if other_agent is not self and other_agent.position > self.postion:

                    #find distance and speed of the other vehicle to eventually find
                    distance_between = other_agent.positon - self.position
                    return distance_between, other_agent.speed,other_agent
            #if no obstacle is found
            return None, None, None