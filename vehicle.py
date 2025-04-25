@ -21,6 +21,10 @@ class Vehicle:
        self.finished = False
        #mass for momentum when crashing
        self.mass = mass

        #weather conditions for vehicle
        self.weather = weather
        self.weather_effects(weather)
        
        self.vehicle_length = vehicle_length
        #get route and keep track of which path we are on in the array
@ -42,6 +46,20 @@ class Vehicle:
                agent_id=self.vehicle_id,
                data=data or {}
            )
    def weather_effects(self, weather = "clear"):
        """ adjust vehicle behavior based on weather conditions."""
        if weather == "snow":
            self.acceleration *=0.6
            self.deceleration*= 0.6
            self.speed_max *= 0.75
        elif weather == "rain":
            self.acceleration *=0.8
            self.deceleration*= 0.8
            self.speed_max *= 0.85
        elif weather =="fog":
            self.look_ahead_distance *= 0.6
        elif weather == "clear":
            pass

    def get_route(self):

        return self.graph.path_finder(self.start, self.end)
    
    
    def move(self, dt = 1.0):
    def move(self, dt = 1.0, weather = "clear"):
        """
        Inputs: vehicle, speed(distance over time)
        Inputs: vehicle, speed(distance over time), what weather the vehicle is currently going through.

        Outputs: none

        Description: moves a vehicle/agent forward a certain distance depeding on factors
        like speed, driver craziness, acceleration, etc
        """

        self.weather_effects(weather)
        if self.logger:  # Safe to call even if logger is None
            self.logger.log_event(
                event_type="vehicle_moved",
                agent_id=self.vehicle_id,
                data={"distance": self.distance_on_path}
            )

        #checks if crashed and doesn't move if it is
        if self.crashed:
            return
        
        #gets closest vehicle/object to this one
        obstacle_distance, obstacle_speed, obstacle = self.obstacle_info()

        #max speed a vehicle will reach based on limit and factor over
        max_speed = self.speed_max * self.curr_path.speed_limit
        
        #if there is a vehicle ahead of them
        if obstacle_distance is not None:
            #find stopping distance
            stopping_distance = self.stopping_distance()
            #if the stopping distance is longer than the vehicle ahead, it crashes
            if obstacle_distance <= stopping_distance:

                #combined deceleration for cars to find stopping distance
                combined_deacceleration = (self.deacceleration * self.mass + obstacle.deacceleration * obstacle.mass) / (self.mass + obstacle.mass)
                # Gradually decrease the speed of both vehicles and update their positions
                while self.speed > 0 and obstacle.speed > 0:
                    self.speed = max(0, self.speed - combined_deacceleration * dt)
                    obstacle.speed = max(0, obstacle.speed - combined_deacceleration * dt)

                    # Update distance traveled by each vehicle after the crash
                    self.distance_on_path += self.speed * dt
                    obstacle.distance_on_path += obstacle.speed * dt
                    
                    # Check if the vehicles have stopped
                    if self.speed == 0 or obstacle.speed == 0:
                        # Record the final crash positions (last known position when both vehicles stop)
                        self.crash_position = self.vehicle_position()
                        obstacle.crash_position = obstacle.vehicle_position()

                        # Mark both vehicles as crashed
                        self.crashed = True
                        obstacle.crashed = True
                        return

                return



            #see if the vehicle sees other object and can stop before vehicle length
            elif obstacle_distance < self.look_ahead_distance:
                #if vehicle is faster than object, slow down based on that
                if obstacle_speed is not None and obstacle_speed < self.speed:

                    #set speed to get towards the speed of object ahead
                    self.speed = max(0, self.speed - self.acceleration * dt)
            else:
                #otherwise continue the max speed or accelerate to it
                self.speed = min(max_speed, self.speed + self.acceleration * dt)

        #if no obstacles, reach max speed
        else:
            self.speed = min(max_speed, self.speed + self.acceleration * dt)

        #get distance traveled in this time and remaining
        distance_traveled = self.speed * dt
        remaining_distance = self.curr_path.length - self.distance_on_path

        #if still space on path 
        if distance_traveled < remaining_distance:
            self.distance_on_path += distance_traveled
        #if it is at the end of route(i.e index on route goes from A-B/last node)
        elif self.index_on_route == len(self.route)-1:
            #remove agent from route as it found final destination
            if not self.finished:
                self.curr_path.remove_agent(self)
                self.finished = True
            return
        #check if the new path is open
        else:
            #get next vertex and path to check if the vehicle can move
            next_vertex = self.route[self.index_on_route + 1]
            next_path = self.graph.paths[self.route[self.index_on_route]][next_vertex]

            #store whether they can move and how much space/distance is required on the next path to move
            entrence_clear = True
            safe_distance = 2

            #check if entrence is clear
            for vehicle in next_path.agents:
                if vehicle.distance_on_path <= safe_distance:
                    entrence_clear = False
                    break
            #if the vehicle can move, add them to the next path
            if entrence_clear:
                #move to next route
                self.index_on_route += 1

                #remove agent from path and add to new one
                self.curr_path.remove_agent(self)
                self.curr_path = next_path
                self.curr_path.add_agent(self)

                #reset distance on path
                self.distance_on_path = 0

            #otherwise set speed to 0 since they cannot move
            else:
                self.speed = 0

            if self.index_on_route == len(self.route)-1 and \
                self.distance_on_path >= self.curr_path.length:
            
                self._complete_journey()
                return True  # Signal that vehicle should be removed
        return False
    
    def _complete_journey(self):
        """Clean up vehicle upon destination arrival"""
        self.curr_path.remove_agent(self)
        if self.logger:
            self.logger.log_event(
                event_type="trip_completed",
                agent_id=self.vehicle_id,
                data={
                    "route": self.route,
                    "duration": time.time() - self.start_time
                }
            )

    def obstacle_info(self):
        """
        Inputs: vehicle/agent

        Output: distance and speed of vehicle ahead

        Description: find the closest vehicle/object to the vehicle you are looking at
        """

        #checking closest agent/vehicle to the current/selected one
        for other_agent in sorted(self.curr_path.agents, key = lambda v: v.distance_on_path):
            #see if another agent/vehicle is on this path infront of this vehicle(above since below is behind them)
            if other_agent is not self and other_agent.distance_on_path > self.distance_on_path:

                #find distance and speed of the other vehicle to eventually find
                distance_between = other_agent.distance_on_path - self.distance_on_path
                return distance_between, other_agent.speed,other_agent
        #if no obstacle is found
        return None, None, None
            
    def stopping_distance(self):
        """
        Inputs: vehicle

        Output: distance it takes to stop the vehicle based on speed and deaceleration

        Description: calculates the distance it takes to stop based on reaction time, speed, and deaccelearion of the car
        """
        
        #distance traveled before reacting
        reaction_distance = self.reaction_time * self.speed

        #breaking distance based on deaceleration formula
        breaking_distance = (self.speed ** 2) / (2* self.deacceleration)

        return reaction_distance + breaking_distance


    def vehicle_position(self):
        """ 
        Inputs: vehicle

        Outputs: the x and y coordinate it is located at

        Description: find where the vehicle is located on the map/graph
        """
        start_position = self.graph.get_pos(self.curr_path.start_vertex)
        end_position = self.graph.get_pos(self.curr_path.end_vertex)

        #if it is at the start
        if self.curr_path.length == 0:
            return start_position['x'], start_position['y'],
        
        #percent done on track/path
        t = self.distance_on_path / self.curr_path.length

        #find x and y using linear interpolation
        x = start_position['x'] + t * (end_position['x'] - start_position['x'])
        y = start_position['y'] + t * (end_position['y'] - start_position['y'])

        #return position
        return x,y
        
    




    