#######################################################
#
# Author: Christopher Cummings
# Test methodology for PEDAC algorithm
#
#######################################################

import sys
import time
import os.path as path
from ped import *
from car import *
from graphs import *

class Simulation(object):
    """
    Simulation Object
    """
    def __init__(self, name, options=list(), time_out=1000000):
        self.name = name
        self.simulated = False
        self.car = None
        self.track_car = list()
        self.pedestrian = None
        self.track_ped = list()
        self.time_out_value = time_out # time out at 1000 seconds by default
        self.abort = False
        self.total_time = None
        self.options = [i.lower() for i in options]
        self.approach_rate_graph = list()
        self.efficiency = 0
        self.paths = list()

    def add_car(self, name, x, y, dx, dy, z=0, dz=0, width=2, depth=2):
        """
        Define a car for the simulation.
        \param: x, y, z given as coordinates
        \param: dx, dy, dz given as initial rates in m/s
        \param: width, depth given in m
        """
        p = Pos(x, y, z)
        v = Velocity(dx/1000.0, dy/1000.0, dz/1000.0)
        self.car = Car(self, name, width, depth, p, v)

    def add_pedestrian(self, name, x, y, dx, dy, z=0, dz=0, radius=.5):
        """
        Define a pedestrian for the simulation.
        \param: x, y, z given as coordinates
        \param: dx, dy, dz given as initial rates in m/s
        \param: radius given in m
        """
        p = Pos(x, y, z) # pos on floor
        v = Velocity(dx/1000.0, dy/1000.0, dz/1000.0)
        self.pedestrian = Pedestrian(self, name, radius, p, v)

    def add_path(self, name, file):
        """
        Add path of velocities to Space Object with name 'name'.
        """
        if not path.isfile(file):
            print("Error adding path -- Path file could not be found.")
            return
        if self.car != None and self.pedestrian != None:
            if self.car.name != name and self.pedestrian.name != name:
                print("Error adding path -- Name does not match pedestrian or vehicle.")
                return
        else:
            print("Error adding path -- Need to add a pedestrian and a vehicle to add a path.")
            return
        self.paths.append(SpaceObjectPath(name, file))

    def remove_path(self, name):
        """
        Remove a path.
        """
        r = list()
        for path in self.paths:
            if path.name == name:
                r.append(path)
        for i in r:
            self.paths.remove(i)

    def stop(self):
        """
        Abort the simulation.
        """
        self.abort = True

    def has_been_simulated(self):
        """
        Has this simulation been simulated?
        """
        return self.simulated

    def display_run_header(self):
        """
        The header at the start of the run.
        """
        string = "\nStarting simulation of system.\nInitial Values:\n{}\n{}\n\n".format(
            self.car, self.pedestrian)
        print(string)

    def validate(self):
        """
        Make sure we can run the simulation properly.
        """
        valid = True
        message = ''

        if self.car == None:
            valid = False
            message = "Car doesn't exist in sumulation"
        if self.pedestrian == None:
            valid = False
            message = "Pedestrian doesn't exist in simulation"

        if self.car != None and self.pedestrian != None:
            if self.car.pos.x > self.pedestrian.pos.x:
                valid = False
                message = "Car needs to start to the left of the pedestrian. Pos.x < Pedestrain.Pos.x"

        if not valid:
            print("Error: Cannot run -- {}".format(message))
        return valid

    def map_paths(self):
        """
        Map the paths to the correct space objects.
        """
        for path in self.paths:
            if not path.valid:
                continue
            if path.name == self.car.name:
                self.car.path = path
            elif path.name == self.pedestrian.name:
                self.pedestrian.path = path

    def run(self):
        """
        Run this simulation.
        """
        # Validate the simulation.
        if not self.validate():
            return
        # Associate paths...
        self.map_paths()
        # Make the efficiency ghost car..
        ghost = EfficiencyGhostCar(self.car)
        self.display_run_header()
        count = 0
        while(not self.abort):
            self.car.tick()
            ghost.tick() # Establish efficiency as unchanging vel..
            car_speed = round(self.car.velocity.speed()*1000, 2)
            self.track_car.append((self.car.pos, car_speed))
            self.pedestrian.tick()
            ped_speed = round(self.pedestrian.velocity.speed()*1000, 2)
            self.track_ped.append((self.pedestrian.pos, ped_speed))
            if count >= self.time_out_value:
                self.stop()
            count += 1
        self.simulated = True
        self.total_time = count
        denom = ghost.get_efficiency_baseline()
        self.efficiency = ((ghost.distance/(self.car.efficiency_time/1000.0))/denom)*100.0

    def view_results(self):
        if not self.has_been_simulated():
            print("Error: must run simulation first... run()")
            return

        print("\n\nViewing results for simulation {}\n".format(self.name))
        string = "Made safe passage past the pedestrian."
        if self.car.impact or self.pedestrian.impact:
            string = "The car hit the pedestrian unfortunately.."
        print("Result: {}\n".format(string))
        print(self.car)
        print(self.pedestrian)
        print("Total simulated time: {} seconds".format(self.total_time/1000.0))
        print("\nEfficiency calculated by comparing simulated algorithm to an ideal 'ghost' car path with no pedestrian.")
        print("Efficiency calculation: {:.2f} %".format(self.efficiency))
        if '--graph' in self.options:
            LineGraph(self.approach_rate_graph, self.track_ped, self.track_car, self.total_time,
                self.car.acceleration_graph, self.car.distance_to_ped_graph)
        self.try_file_out()

    def try_file_out(self):
        """
        Output information in an output file of the users choosing.
        """
        file = None
        for opt in self.options:
            if '--file' in opt:
                file = opt
                break
        if file == None:
            return
        opt = file.split('=')
        if len(opt) < 2:
            return
        file = opt[1]
        with open(file, 'w') as export:
            print(self.track_ped, file=export)
            print(self.track_car, file=export)
            print(self.total_time, file=export)


OPTIONS = list()


def get_milli():
    """
    The miliseconds from the epoch..
    """
    return int(round(time.time()*1000))


def populate_options():
    """
    Put user specified options into the simulation.
    """
    global OPTIONS
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            OPTIONS.append(sys.argv[i])


def main():
    """
    Main function for the simulations.
    """
    global OPTIONS
    populate_options()
    sim = Simulation("Case1", options=OPTIONS)
    sim.add_car("car", 0, 0, 13.9, 0) # car starts at (0, 0) with velocity in positive x at 13.9m/s
    sim.add_pedestrian("ped", 35, -7, 0, 1.67) # ped at (35, -7) with velocity in positive y at 1.67m/s
    sim.add_path("ped", 'test_path.txt')
    sim.run()
    sim.view_results()


if __name__ == "__main__":
    main()
