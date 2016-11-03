#######################################################
#
# Author: Christopher Cummings
# Test methodology for PEDAC algorithm
# These are the abstract classes and utilities used.
#
#######################################################

import math

class SpaceObject(object):
    """
    Space object abstract base class.
    """
    def __init__(self, sim, name, pos, velocity):
        self.pos = pos # center of the object
        self.name = name # to identify the object
        self.velocity = velocity
        self.steady_state_velocity = velocity # never change!
        self.impact = False
        self.sim = sim
        self.G = 9.81
        self.acceleration = Velocity()

    def get_dist(self, space_object):
        """
        Distance to another space object.
        """
        x = space_object.pos.x - self.pos.x
        y = space_object.pos.y - self.pos.y
        z = space_object.pos.z - self.pos.z
        r = x**2 + y**2 + z**2
        return math.sqrt(r)

    def pos_on_floor(self):
        """
        Returns the position of the object always on the floor.
        """
        return Pos(self.pos.x, self.pos.y, 0)

    def tick(self):
        """
        Abstract method for tick called every millisecond.
        """
        # This is the child class responsibility
        raise NotImplimentedError("Tick")

    def change_velocity(self):
        """
        Ability for the space object to change velocity by some random amount?
        Make sure velocity is in mm/s.
        """
        # This is the child class responsibility
        raise NotImplimentedError("Change Velocity")

    def move(self):
        """
        Move this space object by the velocity. Called every millisecond.
        """
        self.velocity += self.acceleration # accelleration is mm/s every second == mm/s^2
        if self.velocity > self.steady_state_velocity:
            self.velocity = self.steady_state_velocity
            self.acceleration = Velocity()
        pos = Pos(self.velocity.dx, self.velocity.dy, self.velocity.dz)
        self.pos += pos

    def area(self):
        """
        Abstract method to cover a specific area?
        """
        # This is the child class responsibility
        raise NotImplimentedError("Area")


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

    def __repr__(self):
        return self.__str__()

    def dist_to(self, pos):
        """
        Distance to the next pos.
        """
        p = Pos(pos.x - self.x, pos.y - self.y, pos.z - self.z)
        return p.dist_from_orig()

    def dist_from_orig(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)


class Velocity(object):
    def __init__(self, x=0, y=0, z=0):
        self.dx = x
        self.dy = y
        self.dz = z

    def __add__(self, vel):
        x = self.dx + vel.dx
        y = self.dy + vel.dy
        z = self.dz + vel.dz
        return Velocity(x, y, z)

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

    def __gt__(self, vel):
        return self.speed() > vel.speed()

    def __lt__(self, vel):
        return self.speed() < vel.speed()

    def __ge__(self, vel):
        return self.speed() >= vel.speed()

    def __le__(self, vel):
        return self.speed() <= vel.speed()

    def __str__(self):
        return "Vel<{:.2f}, {:.2f}, {:.2f}>".format(self.dx, self.dy, self.dz)

    def __repr__(self):
        return self.__str__()

    def speed(self):
        """
        Return the speed of this velocity vector.
        """
        r = self.dx**2 + self.dy**2 + self.dz**2
        return math.sqrt(r)

    def unit_vector(self):
        """
        Return the velocity as a unit vector.
        """
        s = 1/self.speed()
        return s*self


class NotImplimentedError(Exception):
    """
    Error raised when abstract methods are called.
    """
    def __init__(self, method="Method", obj="this object"):
        super(NotImplimentedError, self).__init__("Not Implimented Error: {} is not implimented for {}.".format(method, obj))