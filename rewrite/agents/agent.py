class Agent:

    def __init__(self, agent_id, reaction_time, look_ahead_distance, agent_length = 1, acceleration = 1, deacceleration = 1, mass = 500, speed_multiplier = 1):
        self.agent_id = agent_id

        #move attributes
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
        self.postion = 0 #meters far on a path

        