from rewrite.routing.pathfinder import dijkstra

class Agent:
    def __init__(self, agent_id, graph, start_vertex, end_vertex, reaction_time = .5, look_ahead_distance = 10, agent_length = 1, acceleration = 1, deacceleration = 1, mass = 500, speed_multiplier = 1):
        self.agent_id = agent_id

        #move attributes

        self.route = dijkstra(graph, start_vertex, end_vertex)
        self.route_index = 0
        self.route_index = 0

        self.finished = False

        self.speed = 0
        self.reaction_time = reaction_time
        self.look_ahead_distance = look_ahead_distance
        self.agent_length = agent_length
        self.acceleration = acceleration
        self.deacceleration = deacceleration
        self.mass = mass
        self.speed_multiplier = speed_multiplier

        
        self.current_road = self.route[0][0]
        self.current_lane = self.current_road.lanes[0]
        self.current_lane.agents.append(self)

        self.position = 0  # Initial position on the road
    def move_agent(self, dt=1.0):
        if self.finished:
             return
        #get next turn
        if self.route_index + 1 < len(self.route):
                turn = self.route[self.route_index + 1][1]
        else:
                turn = None

        #try to find if we need to switch to desired lane
        desired_lane_idx = self.desired_lane_index(turn)
        current_lane_idx = self.current_road.lanes.index(self.current_lane)

        if desired_lane_idx != current_lane_idx:
              direction = 1 if desired_lane_idx > current_lane_idx else -1
              next_idx = current_lane_idx + direction

              if 0 <= next_idx < len(self.current_road.lanes):
                    target_lane = self.current_road.lanes[next_idx]
                    
                    if self.is_lane_change_safe(target_lane):
                          self.current_lane.agents.remove(self)
                          target_lane.agents.append(self)
                          self.current_lane = target_lane
        
        # Get info about vehicle/agent ahead
        distance_ahead, speed_ahead, agent_ahead = self.obstacle_info()

        # Max allowed speed on this lane
        max_speed = self.speed_multiplier * self.current_lane.road.speed_limit
        #get info about speeding based on future obstacle distances

        if agent_ahead:
            if distance_ahead < self.look_ahead_distance:
                self.speed -= self.deacceleration * dt
            elif self.speed < min(speed_ahead, max_speed):
                 self.speed += self.acceleration * dt
        else:
             if self.speed < max_speed:
                  self.speed += self.acceleration * dt
        
        self.speed = max(0, min(self.speed, max_speed))
        self.position += self.speed * dt
        if self.position >= self.current_lane.length:
            overflow = self.position - self.current_lane.length
            self.advance_to_next_road()
            self.position += overflow  # carry over any extra distance


    def advance_to_next_road(self):
         if self.route_index + 1 < len(self.route):
              
              self.position = 0
              self.route_index += 1
              next_road = self.route[self.route_index][0]
              self.current_road = next_road
              self.current_lane = next_road.lanes[0]
         else:
              self.speed = 0
              
              self.finished = True
              
    
    def desired_lane_index(self, turn_direction):
            #sees where the best lane if they are turning left or right
            num_lanes = len(self.current_road.lanes)
            if turn_direction == "right":
                return num_lanes - 1
            elif turn_direction == "left":
                return 0
            else:
                return self.current_road.lanes.index(self.current_lane)
            

    def is_lane_change_safe(self, target_lane):
            #checks other lane if a vehicle is between their look ahead distance(both in front and behind)
            for agent in target_lane.agents:
                if abs(agent.position - self.position) < self.look_ahead_distance:
                    return False
            return True
        
           
        


    def obstacle_info(self):
        #find closest agent based on distance ahead
        closest = None
        min_distance = float('inf')

        for other in self.current_lane.agents:
                if other is not self and other.position > self.position:
                    distance = other.position - self.position
                    if distance < min_distance:
                        min_distance = distance
                        closest = other
        if closest:
                return min_distance, closest.speed, closest
        return None, None, None
    

    def position_on_road(self, graph):
        # Get position on the current road (x, y) for plotting
        current_road = self.current_road
        if current_road:
            start_x, start_y = graph.positions[current_road.from_vertex]
            end_x, end_y = graph.positions[current_road.to_vertex]
            total_length = current_road.length
            # Calculate the position as a ratio along the road
            ratio = self.position / total_length
            x = start_x + ratio * (end_x - start_x)
            y = start_y + ratio * (end_y - start_y)
            return x, y
        return 0, 0  # Default position if road is not set