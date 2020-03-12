from models.Packages import Packages
import models.HashTable
from models.Distances import address_table
from models.Distances import find_closest_destination
from models.Distances import distance_to_home
import datetime

class Simulation:

    package_list = Packages().hash_table
    speed = 18 / 60

    def __init__(self):
        self.reset()
        
    def reset(self):
        self.truck1_distance = 0.0
        self.truck2_distance = 0.0
        self.truck3_distance = 0.0
        self.truck1_packages = [13,14,15,16,29,30,31,34,37,40,1,4,7,39,8,32]
        self.truck2_packages = [3,18,36,38,6,10,11,12,17,20,21,22,23,24,25,26]
        self.truck3_packages = [9,19,27,28,33,35,2,5]
        self.truck1_priority = [13,30,31,37,40]
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

    def get_total_distance(self):
        return float(self.truck1_distance + self.truck2_distance + self.truck3_distance)

    def __build_lists(self):
        for index in self.truck1_packages:
            address = Simulation.package_list.get(str(index))[1]
            addressId = address_table.get(address)[0]

            if addressId not in self.truck1_destinations:
                self.truck1_destinations.append(addressId)
                self.truck1_priority_destinations.append(addressId)

        for index in self.truck2_packages:
            address = Simulation.package_list.get(str(index))[1]
            addressId = address_table.get(address)[0]

            if addressId not in self.truck2_destinations:
                self.truck2_destinations.append(addressId)
                self.truck2_priority_destinations.append(addressId)

        for index in self.truck3_packages:
            address = Simulation.package_list.get(str(index))[1]
            addressId = address_table.get(address)[0]

            if addressId not in self.truck3_destinations:
                self.truck3_destinations.append(addressId)
                self.truck3_priority_destinations.append(addressId)

    def __unload(self, truck_list, priority_list, location):
        for index in truck_list:
            address = Simulation.package_list.get(str(index))[1]
            addressId = address_table.get(address)[0]

            if addressId == str(location):
                truck_list.remove(index)
                if index in priority_list:
                    priority_list.remove(index)
                self.package_deliveries[index] = self.current_time.time()

    def run(self, time):    
        self.sim_end = datetime.datetime.strptime(time, '%H:%M').time()
        self.current_time = datetime.datetime.strptime('08:00', '%H:%M')
        self.__build_lists()

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

        while True:
            if self.current_time.time() >= self.sim_end:
                break

            self.current_time += datetime.timedelta(minutes=1)
            if self.current_time.time() == datetime.datetime.strptime('09:05:00', '%H:%M:%S').time():
                self.truck2_departed = True
            if self.truck1_returned and self.current_time.time() >= datetime.datetime.strptime('10:20:00', '%H:%M:%S').time():
                self.truck3_departed = True

            if not self.truck1_returned and self.truck1_departed:
                self.truck1_curr_pos += Simulation.speed
                self.truck1_distance += Simulation.speed
            if not self.truck2_returned and self.truck2_departed:
                self.truck2_curr_pos += Simulation.speed
                self.truck2_distance += Simulation.speed
            if not self.truck3_returned and self.truck3_departed:
                self.truck3_curr_pos += Simulation.speed
                self.truck3_distance += Simulation.speed

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

            if len(self.truck1_destinations) < 1:
                self.truck1_returned = True
            if len(self.truck2_destinations) < 1:
                self.truck2_returned = True
            if len(self.truck3_destinations) < 1:
                self.truck3_returned = True

            if len(self.truck1_destinations) < 1 and len(self.truck2_destinations) < 1 and len(self.truck3_destinations) < 1:
                break
