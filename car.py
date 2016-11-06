#######################################################
#
# Author: Christopher Cummings
#
# Test methodology for PEDAC algorithm
#
#######################################################

from objects import *

class Controller(object):
    def __init__(self, car):
        self.car = car

    def algorithm(self, time_to_impact, time_to_stop, current_dist,
            car_speed, projected_dist, rate_approaching):
        """
        This is the main algorithm for the controller.
        Everything given is in s, m, or m/s
        \return apply_break: Should the car apply some break?
        \return how_much: the fraction of max g the car should accelerate by.
        """

        apply_break = False
        how_much = None

        dist_to_stop = (6.867/2)*time_to_stop**2

        if dist_to_stop > projected_dist:
            apply_break = True
            how_much = (dist_to_stop/projected_dist)*.7*.02
        else:
            if car_speed < self.car.steady_state_velocity.speed():
                how_much = .25


        return apply_break, how_much

    def take_action(self, ped_vel, ped_pos):
        #if self.car.velocity.speed() == self.car.steady_state_velocity.speed():
        #    self.apply_break(.008)

        #if self.car.velocity.speed()*1000.0 < 10:
        #    self.apply_gas()

        apply_break, how_much = self.p_hit_ped(ped_pos, ped_vel)

        if apply_break:
            self.apply_break(how_much)
        else:
            if how_much != None:
                self.apply_gas(how_much)

    def p_hit_ped(self, ped_pos, ped_vel):
        """
        Return the probability of the car hitting the pedestrian.
        """
        dist = ped_pos.dist_from_orig() # current distance from car

        # Get projections 100ms from now
        ped_proj_rel_to_car_now = self.projection(ped_pos, ped_vel, 100)
        car_proj_hundred = self.projection(Pos(), self.car.velocity, 100)

        # Get the projected resultant vector (next ped_pos to be called...)
        next_rel_vector = ped_proj_rel_to_car_now - car_proj_hundred

        # Get the distance for the next projected ped_pos
        next_dist = next_rel_vector.dist_from_orig()

        # Add in error for worst case...
        #next_dist -= .5

        # Get the rate in which we are approaching mm/ms
        rate = (dist - next_dist)/100

        # Time to impact s
        time_to_impact = dist/(rate*1000)

        # Time it takes to stop ms (at max break)
        max_decell = self.car.G*.7/1000.0
        tts = self.car.velocity.speed()/max_decell # (mm/ms)/(mm/ms^2)=ms

        # Document the rate we are approaching
        self.car.sim.approach_rate_graph.append(rate*1000)

        print("\n\nCar pos: ********************************** {:<30} (m)".format(str(self.car.pos)))
        print("Ped pos: ********************************** {:<30} (m)".format(str(self.car.sensor.ped.pos)))
        print("Ped pos relative to car: ****************** {:<30} (m)".format(str(ped_pos)))
        print("Car velocity vector: ********************** {:<30} (m/s)".format(str(self.car.velocity*1000)))
        print("Ped velocity vector: ********************** {:<30} (m/s)".format(str(ped_vel*1000)))
        print("Time until impact: ************************ {:<30.4f} (s)".format(time_to_impact))
        print("Time it will take to stop at max break: *** {:<30.4f} (s)".format(tts))
        print("Current distance: ************************* {:<30.2f} (m)".format(dist))
        print("100ms from now distance (best guess): ***** {:<30.2f} (m)".format(next_dist))
        print("Current car speed: ************************ {:<30.2f} (m/s)".format(self.car.velocity.speed()*1000))
        print("Rate we are approaching (best guess): ***** {:<30.4f} (m/s)".format(rate*1000))
        print("\nTime: {:.4f} (s)".format(self.car.time/1000.0))
        print("\n________________________________________________________________________________")

        return self.algorithm(time_to_impact, tts, dist, self.car.velocity.speed()*1000,
            next_dist, rate*1000)
        
    def projection(self, pos, vel, time):
        """
        \param time: time in ms for projection
        """
        x = pos.x + (vel.dx*time)
        y = pos.y + (vel.dy*time)
        z = pos.z + (vel.dz*time)
        return Pos(x, y, z)

    def apply_break(self, g=.7):
        self.car.apply_break(g)

    def apply_gas(self, g=.25):
        self.car.apply_gas(g)



class Sensor(object):
    def __init__(self, car):
        self.car = car
        self.ped = None

    def seek_pedestrian_threat(self):
        """
        Look to see if there is a pedestrian threat.
        """
        if self.car.sim.pedestrian.get_dist(self.car) < 60:
            self.ped = self.car.sim.pedestrian

    def get_distance(self):
        """
        Get the distance to the pedestrian.
        """
        if self.ped != None:
            return self.car.get_dist(self.ped)
        return None

    def get_ped_pos_rel(self):
        """
        Get the pedestrians relative position from the car.
        """
        if self.ped != None:
            return self.ped.pos - self.car.pos
        return None

    def get_ped_velocity(self):
        """
        Get the pedestrians velocity. Not relative to the car!
        """
        if self.ped != None:
            return self.ped.velocity
        return None

    def check_impact(self):
        """
        Did the car hit the pedestrian?
        """
        impact = False
        dist = self.get_distance()
        if dist != None:
            if self.ped != None:
                if dist <= self.ped.radius:
                    impact = True
        if impact:
            self.car.impact = True
            if self.ped != None:
                self.ped.impact = True
            self.car.sim.stop()
        return impact



class Car(SpaceObject):
    def __init__(self, sim, name, width, depth, pos, velocity):
        super(Car, self).__init__(sim, name, pos, velocity)
        self.width = width
        self.depth = depth
        self.controller = Controller(self)
        self.sensor = Sensor(self)
        self.sensor_timer = 0
        self.last_dist = None
        self.break_on = False
        self.acceleration_graph = list()
        self.distance_to_ped_graph = list()
        self.time = 0 # time in ms

    def __str__(self):
        return "Name: {}, Pos: {}, Vel: {}, Hit Ped: {}".format(self.name, self.pos, self.velocity, self.impact)

    def tick_every_tick(self):
        """
        Operations done EVERY tick.
        """
        # move the car and change the velocity by some amount (optional)
        self.move()
        self.time += 1

        # document the cars acceleration
        acc = self.acceleration.speed()
        self.acceleration_graph.append(acc)

        # document the distance to the pedestrian
        di = self.sensor.get_distance()
        if di == None:
            di = 0
        self.distance_to_ped_graph.append(di)

        # stop the simulation once the distance between ped and the car gets further
        # rather than closer -- The car has passed the ped safely
        dist = self.sensor.get_distance()
        if self.last_dist != None and dist < 10:
            if dist > self.last_dist:
                self.sim.stop()
        self.last_dist = dist

        # check to see if impact with ped has occured after moving
        self.impact = self.sensor.check_impact()

    def tick_sensor_packets(self):
        """
        Operations done when the car recieves packets from the sensor.
        Every 100 ms.
        """
        # get the distance and the relative velocity to the ped
        dist = self.sensor.get_distance()
        ped_vel = self.sensor.get_ped_velocity()
        ped_pos = self.sensor.get_ped_pos_rel()
        
        if dist == None or ped_vel == None:
            # No ped found yet
            self.sensor.seek_pedestrian_threat()
            return
        
        # ped is found and we need to take action
        self.controller.take_action(ped_vel, ped_pos)

    def tick(self):
        # Do the operations that happen EVERY tick
        self.tick_every_tick()

        # the below info is relayed from the sensor which only sends packets every 100ms
        if self.sensor_timer < 100:
            self.sensor_timer += 1
            return
        self.sensor_timer = 0

        # Do the operations that happen on ticks sensor info is recieved
        self.tick_sensor_packets()

    def apply_break(self, g=.7):
        """
        Apply the break to the car. .7*G is the MAX deceleration.
        \param: g is the fraction of G to apply where G=9.81m/s^2
        """
        if g > .7:
            g = .7
        unit_vel_vector = self.velocity.unit_vector() # get the direction.
        self.acceleration = ((self.G*g*-1)/1000.0)*unit_vel_vector
        self.break_on = True

    def apply_gas(self, g=.25):
        """
        Apply the gas to the car up to the steady state speed.
        .25*G is the MAX accelleration.
        \param: g is the fraction of G where G=9.81m/s^2
        """
        if g > .25:
            g = .25
        unit_vel_vector = self.velocity.unit_vector() # get the direction.
        self.acceleration = ((self.G*g)/1000.0)*unit_vel_vector
        self.break_on = False
