from models.Packages import Packages
import models.HashTable
from models.Distances import address_table
from models.Distances import find_closest_destination
from models.Distances import distance_to_home
import datetime

class Simulation:

    # Static variables
    package_list = Packages().hash_table
    speed = 18 / 60

    # Calls the self function that sets all inital values
    # wanted to be able to reset the same simulation which is why those assignments are outside of the constructor
    def __init__(self):
        self.reset()
        
    # Sets all instance variables to be used and resets them on call
    def reset(self):
        self.truck1_distance = 0.0
        self.truck2_distance = 0.0
        self.truck3_distance = 0.0
        self.truck1_packages = [13,14,15,16,29,30,31,34,37,40,1,4,7,39,8,32]
        self.truck2_packages = [3,18,36,38,6,10,11,12,17,20,21,22,23,24,25,26]
        self.truck3_packages = [9,19,27,28,33,35,2,5]
        self.truck1_priority = [13,14,15,16,29,30,31,34,37,40]
        self.truck2_priority = [6,20,25]
        self.truck3_priority = []
        self.truck1_destinations = []
        self.truck2_destinations = []
        self.truck3_destinations = []
        self.truck1_priority_destinations = []
        self.truck2_priority_destinations = []
        self.truck3_priority_destinations = []
        self.truck1_pos = 0
        self.truck2_pos = 0
        self.truck3_pos = 0
        self.truck1_curr_pos = 0.0
        self.truck2_curr_pos = 0.0
        self.truck3_curr_pos = 0.0
        self.truck1_goal = 0.0
        self.truck2_goal = 0.0
        self.truck3_goal = 0.0
        self.truck1_returned = False
        self.truck2_returned = False
        self.truck3_returned = False
        self.truck1_departed = False
        self.truck2_departed = False
        self.truck3_departed = False
        self.package_deliveries = [None] * 41
        Simulation.package_list.add("9", ['9','300 State St','Salt Lake City','UT','84103','EOD','2','Wrong address listed'])

    # Method for getting the total distance travelled at the current state of the sim
    def get_total_distance(self):
        return float(self.truck1_distance + self.truck2_distance + self.truck3_distance)

    # This function builds the destination lists based off of the package lists provided
    # Performs operations for each truck
    # Operates at O(N)
    def __build_lists(self):
        for index in self.truck1_packages:
            address = Simulation.package_list.get(str(index))[1]
            addressId = address_table.get(address)[0]

            if addressId not in self.truck1_destinations:
                self.truck1_destinations.append(addressId)
                if index in self.truck1_priority:
                    self.truck1_priority_destinations.append(addressId)

        for index in self.truck2_packages:
            address = Simulation.package_list.get(str(index))[1]
            addressId = address_table.get(address)[0]

            if addressId not in self.truck2_destinations:
                self.truck2_destinations.append(addressId)
                if index in self.truck2_priority:
                    self.truck2_priority_destinations.append(addressId)

        for index in self.truck3_packages:
            address = Simulation.package_list.get(str(index))[1]
            addressId = address_table.get(address)[0]

            if addressId not in self.truck3_destinations:
                self.truck3_destinations.append(addressId)
                if index in self.truck3_priority:
                    self.truck3_priority_destinations.append(addressId)

    # Facilitates the process for unloading Packages
    # Removes packages from the lists as they are delivered
    # Added this functionality to help with tracking deliveries
    # Operates at O(N)
    def __unload(self, truck_list, priority_list, location):
        self.removal_list = []
        for index in truck_list:
            address = Simulation.package_list.get(str(index))[1]
            addressId = address_table.get(address)[0]

            if addressId == str(location):
                self.removal_list.append(index)
                self.package_deliveries[index] = self.current_time.time()

        for item in self.removal_list:
            truck_list.remove(item)
            if item in priority_list:
                priority_list.remove(item) 

    # Main section of code used to perform the simulation
    # Keeps track of all trucks and packages 
    # Technically has a worst case of O(inf) if the loop doesnt break correctly
    def run(self, time):  
        # Handles setting up time constraints  
        self.sim_end = datetime.datetime.strptime(time, '%H:%M').time()
        self.current_time = datetime.datetime.strptime('08:00', '%H:%M')
        self.__build_lists()

        # Sets the initial next destination for all trucks 
        # If there is a priority package on the truck, the it will choose the closes priority package
        if len(self.truck1_priority_destinations) > 0:
            self.truck1_next = find_closest_destination(self.truck1_pos, self.truck1_priority_destinations)
        elif len(self.truck1_destinations) > 0:
            self.truck1_next = find_closest_destination(self.truck1_pos, self.truck1_destinations)
        self.truck1_goal = float(self.truck1_next[1])

        if len(self.truck2_priority_destinations) > 0:
            self.truck2_next = find_closest_destination(self.truck2_pos, self.truck2_priority_destinations)
        elif len(self.truck2_destinations) > 0:
            self.truck2_next = find_closest_destination(self.truck2_pos, self.truck2_destinations)
        self.truck2_goal = float(self.truck2_next[1])

        if len(self.truck3_priority_destinations) > 0:
            self.truck3_next = find_closest_destination(self.truck3_pos, self.truck3_priority_destinations)
        elif len(self.truck3_destinations) > 0:
            self.truck3_next = find_closest_destination(self.truck3_pos, self.truck3_destinations)
        self.truck3_goal = float(self.truck3_next[1])

        self.truck1_departed = True

        # Loop runs while a truck still has a package on it
        # Trucks deliver priority items first
        # Since each priority lists are just sublists of the truck lists, loop is broken when all truck lists are empty
        # Loop also can end if the time based stop point is reached
        while not ((len(self.truck1_destinations) < 1 and len(self.truck2_destinations) < 1 and len(self.truck3_destinations) < 1) or (self.current_time.time() >= self.sim_end)):

            # increments time by a minute each loop
            self.current_time += datetime.timedelta(minutes=1)

            # Sends off truck 2 and 3 at certain triggers
            if self.current_time.time() == datetime.datetime.strptime('09:05:00', '%H:%M:%S').time():
                self.truck2_departed = True
            if self.truck1_returned and self.current_time.time() >= datetime.datetime.strptime('10:20:00', '%H:%M:%S').time():
                Simulation.package_list.add("9", ["9","410 S State St","Salt Lake City","UT","84111","EOD","2","None"])
                self.truck3_departed = True

            # Adds distance to trucks total distance and current location en route to next location
            if not self.truck1_returned and self.truck1_departed:
                self.truck1_curr_pos += Simulation.speed
                self.truck1_distance += Simulation.speed
            if not self.truck2_returned and self.truck2_departed:
                self.truck2_curr_pos += Simulation.speed
                self.truck2_distance += Simulation.speed
            if not self.truck3_returned and self.truck3_departed:
                self.truck3_curr_pos += Simulation.speed
                self.truck3_distance += Simulation.speed

            # Logic for trucks destination handling
            # Fetches the closest destination in the correct list
            # Calls unload when it reaches the next destination
            # Trucks deliver all packages and then return back to the hub
            # Truck 1
            if self.truck1_curr_pos >= self.truck1_goal:
                self.truck1_curr_pos -= self.truck1_goal 
                self.truck1_pos = self.truck1_next[0]    
                self.__unload(self.truck1_packages, self.truck1_priority, self.truck1_pos)
                self.truck1_destinations.remove(self.truck1_next[0])
                if len(self.truck1_priority_destinations) > 0:
                    self.truck1_priority_destinations.remove(self.truck1_next[0])
                if len(self.truck1_priority_destinations) > 0:
                    self.truck1_next = find_closest_destination(self.truck1_pos, self.truck1_priority_destinations)
                elif len(self.truck1_destinations) > 0:
                    self.truck1_next = find_closest_destination(self.truck1_pos, self.truck1_destinations)
                elif len(self.truck1_destinations) < 1 and self.truck1_next[0] != 0:
                        self.truck1_destinations.append(0)
                        self.truck1_next = (0, distance_to_home(self.truck1_pos))
                self.truck1_goal = float(self.truck1_next[1])                

            # Truck 2
            if self.truck2_curr_pos >= self.truck2_goal:
                self.truck2_curr_pos -= self.truck2_goal
                self.truck2_pos = self.truck2_next[0]
                self.__unload(self.truck2_packages, self.truck2_priority, self.truck2_pos)
                self.truck2_destinations.remove(self.truck2_next[0])
                if len(self.truck2_priority_destinations) > 0:
                    self.truck2_priority_destinations.remove(self.truck2_next[0])
                if len(self.truck2_priority_destinations) > 0:
                    self.truck2_next = find_closest_destination(self.truck2_pos, self.truck2_priority_destinations)
                elif len(self.truck2_destinations) > 0:
                    self.truck2_next = find_closest_destination(self.truck2_pos, self.truck2_destinations)
                elif len(self.truck2_destinations) < 1 and self.truck2_next[0] != 0:
                        self.truck2_destinations.append(0)
                        self.truck2_next = (0, distance_to_home(self.truck2_pos))
                self.truck2_goal = float(self.truck2_next[1])

            # Truck 3
            if self.truck3_curr_pos >= self.truck3_goal:
                self.truck3_curr_pos -= self.truck3_goal
                self.truck3_pos = self.truck3_next[0]
                self.__unload(self.truck3_packages, self.truck3_priority, self.truck3_pos)
                self.truck3_destinations.remove(self.truck3_next[0])
                if len(self.truck3_priority_destinations) > 0:
                    self.truck3_priority_destinations.remove(self.truck3_next[0])
                if len(self.truck3_priority_destinations) > 0:
                    self.truck3_next = find_closest_destination(self.truck3_pos, self.truck3_priority_destinations)
                elif len(self.truck3_destinations) > 0:
                    self.truck3_next = find_closest_destination(self.truck3_pos, self.truck3_destinations)
                elif len(self.truck3_destinations) < 1 and self.truck3_next[0] != 0:
                        self.truck3_destinations.append(0)
                        self.truck3_next = (0, distance_to_home(self.truck3_pos))
                self.truck3_goal = float(self.truck3_next[1])

            # Sets the truck returned boolean so that it stops counting mileage after it has returned to the hub
            if len(self.truck1_destinations) < 1:
                self.truck1_returned = True
            if len(self.truck2_destinations) < 1:
                self.truck2_returned = True
            if len(self.truck3_destinations) < 1:
                self.truck3_returned = True

    # Print function for outputting the state of the simulation
    # Can also print state of individual package
    def print(self, id=None):
        if id is None:
            for index in range(1,41):
                self.package = Simulation.package_list.get(str(index))
                print("\nPackage ID: " + self.package[0])
                print("Address: " + self.package[1])
                print("City: " + self.package[2])
                print("State: " + self.package[3])
                print("Zip: " + self.package[4])
                print("Deliver by: " + self.package[5])
                print("Weight (kg): " + self.package[6])
                print("Note: " + self.package[7])

                if self.package_deliveries[index] is not None:
                    print("Delivery Status: Delivered at " + str(self.package_deliveries[index]))
                else:
                    print("Deliver Status: Out for Delivery")
        else:
            self.package = Simulation.package_list.get(str(id))
            print("\nPackage ID: " + self.package[0])
            print("Address: " + self.package[1])
            print("City: " + self.package[2])
            print("State: " + self.package[3])
            print("Zip: " + self.package[4])
            print("Deliver by: " + self.package[5])
            print("Weight (kg): " + self.package[6])
            print("Note: " + self.package[7])

            if self.package_deliveries[id] is not None:
                print("Delivery Status: Delivered at " + str(self.package_deliveries[id]))
            else:
                print("Deliver Status: Out for Delivery")
        return
