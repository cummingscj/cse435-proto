#######################################################
#
# Author: Christopher Cummings
#
# Test methodology for PEDAC algorithm
#
#######################################################

import time
from ped import *
from car import *

class Simulation(object):
    def __init__(self, name):
        self.name = name
        self.simulated = False
        self.car = None
        self.pedestrian = None
        self.abort = False
        self.total_time = None

    def def_car(self, name, x, y, dx, dy):
        p = Pos(x, y, 0) # pos on floor
        dx /= 1000.0
        dy /= 1000.0 # get the change per mm
        v = Velocity(dx, dy, 0) # not changing in the z
        self.car = Car(self, name, 2, 2, p, v)

    def def_pedestrian(self, name, x, y, dx, dy):
        p = Pos(x, y, 0) # pos on floor
        dx /= 1000.0
        dy /= 1000.0 # get the change per mm
        v = Velocity(dx, dy, 0) # not changing in the z
        self.pedestrian = Pedestrian(self, name, .5, p, v)

    def abort_sim(self):
        self.abort = True

    def simulate(self, seconds=None):
        print("\nStarting simulation of system.\nInitial Values:\n")
        print(self.car)
        print(self.pedestrian)
        print()
        stamp = get_milli()
        milli = seconds * 1000
        while(get_milli() - stamp < milli and not self.abort):
            time.sleep(1/1000.0)
            self.car.tick()
            self.pedestrian.tick()
        self.simulated = True
        self.total_time = get_milli() - stamp

    def view_results(self):
        if not self.simulated:
            print("Error: Call simulate() first...")
            return
        print("\n\nViewing Results")
        print(self.car)
        print(self.pedestrian)
        print("Total time: {} seconds".format(self.total_time/1000.0))


def get_milli():
    """
    The miliseconds from the epoch..
    """
    return int(round(time.time()*1000))


def main():
    sim = Simulation("Case1")
    sim.def_car("car", 0, 0, 13.9, 0) # car starts at (0, 0) with velocity in positive x at 13.9m/s
    sim.def_pedestrian("ped", 35, -7, 0, 1.67) # ped at (35, -7) with velocity in positive y at 1.67m/s
    try:
        seconds = int(input("How many seconds: "))
    except:
        exit(1)
    sim.simulate(seconds)
    sim.view_results()


if __name__ == "__main__":
    main()
