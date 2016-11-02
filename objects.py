#######################################################
#
# Author: Christopher Cummings
#
# Test methodology for PEDAC algorithm
#
#######################################################

import math

class Pos(object):
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, pos):
        x = self.x + pos.x
        y = self.y + pos.y
        z = self.z + pos.z
        return Pos(x, y, z)

    def __sub__(self, pos):
        x = self.x - pos.x
        y = self.y - pos.y
        z = self.z - pos.z
        return Pos(x, y, z)

    def __str__(self):
        return "Pos({:.2f}, {:.2f}, {:.2f})".format(self.x, self.y, self.z)


class Velocity(object):
    def __init__(self, x=0, y=0, z=0):
        self.dx = x
        self.dy = y
        self.dz = z

    def __sub__(self, vel):
        x = self.dx - vel.dx
        y = self.dy - vel.dy
        z = self.dz - vel.dz
        return Velocity(x, y, z)

    def __mul__(self, scal):
        x = self.dx*scal
        y = self.dy*scal
        z = self.dz*scal
        return Velocity(x, y, z)

    def __rmul__(self, scal):
        return self.__mul__(scal)

    def __str__(self):
        return "Vel<{:.2f}, {:.2f}, {:.2f}>".format(self.dx, self.dy, self.dz)


class NotImplimentedError(Exception):
    def __init__(self, method="Method", obj="this object"):
        super(NotImplimentedError, self).__init__("Not Implimented Error: {} is not implimented for {}.".format(method, obj))


class SpaceObject(object):

    def __init__(self, sim, name, pos, velocity):
        self.pos = pos # center of the object
        self.name = name # to identify the object
        self.velocity = velocity
        self.impact = False
        self.sim = sim

    def get_dist(self, space_object):
        x = space_object.pos.x - self.pos.x
        y = space_object.pos.y - self.pos.y
        z = space_object.pos.z - self.pos.z
        r = x**2 + y**2 + z**2
        return math.sqrt(r)

    def tick(self):
        # This is the child class responsibility
        raise NotImplimentedError("Tick")

    def change_velocity(self):
        # This is the child class responsibility
        raise NotImplimentedError("Change Velocity")

    def move(self):
        pos = Pos(self.velocity.dx, self.velocity.dy, self.velocity.dz)
        self.pos += pos

    def area(self):
        # This is the child class responsibility
        raise NotImplimentedError("Area")
