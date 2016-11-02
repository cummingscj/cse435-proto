#######################################################
#
# Author: Christopher Cummings
#
# Test methodology for PEDAC algorithm
#
#######################################################

from objects import *

class Pedestrian(SpaceObject):

    def __init__(self, sim, name, radius, pos, velocity):
        self.radius = radius
        super(Pedestrian, self).__init__(sim, name, pos, velocity)

    def __str__(self):
        return "Name: {}, Pos: {}, Vel: {}, Dead: {}".format(self.name, self.pos, self.velocity, self.impact)

    def tick(self):
        self.move()
        self.change_velocity()

    def change_velocity(self):
        pass
