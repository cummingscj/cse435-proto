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

    def take_action(self, dist, ped_vel, ped_pos):
        vel = ped_vel*1000.0
        print("CONTROLLER ACTION -- dist: {:.2f}, ped_vel: {}, ped_pos: {}".format(dist, vel, ped_pos))

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

    def __str__(self):
        return "Name: {}, Pos: {}, Vel: {}, Hit Ped: {}".format(self.name, self.pos, self.velocity, self.impact)

    def tick_every_tick(self):
        """
        Operations done EVERY tick.
        """
        # move the car and change the velocity by some amount (optional)
        self.move()

        # stop the simulation once the distance between ped and the car gets further
        # rather than closer -- The car has passed the ped safely
        dist = self.sensor.get_distance()
        if self.last_dist != None:
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

        # print the car position for tesing
        print("\nCar Pos: {}".format(self.pos))
        if self.sensor.ped != None:
            print("Ped Pos: {}".format(self.sensor.ped.pos))
        
        if dist == None or ped_vel == None:
            # No ped found yet
            self.sensor.seek_pedestrian_threat()
            return
        
        # ped is found and we need to take action
        self.controller.take_action(dist, ped_vel, ped_pos)

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
        self.acceleration = self.G*g/1000.0

    def apply_gas(self, g=.25):
        """
        Apply the gas to the car up to the steady state speed.
        .25*G is the MAX accelleration.
        \param: g is the fraction of G where G=9.81m/s^2
        """
        if g > .25:
            g = .25
        self.acceleration = self.G*g/1000.0
