from models.Packages import Packages
import models.HashTable
from models.Distances import address_table
from models.Distances import find_closest_destination
from models.Distances import distance_to_home

class Simulation:

    def __init__(self):
        self.package_list = Packages().hash_table
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

    def get_total_distance(self):
        return float(self.truck1_distance + self.truck2_distance + self.truck3_distance)

    def run(self):    
        for index in self.truck1_packages:
            address = self.package_list.get(str(index))[1]
            address2 = address_table.get(address)[2]
            addressId = address_table.get(address)[0]

            if address == address2 and addressId not in self.truck1_destinations:
                self.truck1_destinations.append(addressId)
                self.truck1_priority_destinations.append(addressId)

        for index in self.truck2_packages:
            address = self.package_list.get(str(index))[1]
            address2 = address_table.get(address)[2]
            addressId = address_table.get(address)[0]

            if address == address2 and addressId not in self.truck2_destinations:
                self.truck2_destinations.append(addressId)
                self.truck2_priority_destinations.append(addressId)

        for index in self.truck3_packages:
            address = self.package_list.get(str(index))[1]
            address2 = address_table.get(address)[2]
            addressId = address_table.get(address)[0]

            if address == address2 and addressId not in self.truck3_destinations:
                self.truck3_destinations.append(addressId)
                self.truck3_priority_destinations.append(addressId)

        while True:
            if len(self.truck1_priority_destinations) > 0:
                truck1_next = find_closest_destination(self.truck1_pos, self.truck1_priority_destinations)
                self.truck1_pos = truck1_next[0]
                self.truck1_distance += float(truck1_next[1])
                self.truck1_destinations.remove(truck1_next[0])
                self.truck1_priority_destinations.remove(truck1_next[0])
            elif len(self.truck1_destinations) > 0:
                truck1_next = find_closest_destination(self.truck1_pos, self.truck1_destinations)
                self.truck1_pos = truck1_next[0]
                self.truck1_distance += float(truck1_next[1])
                self.truck1_destinations.remove(truck1_next[0])
                if len(self.truck1_destinations) < 1:
                    self.truck1_distance += distance_to_home(self.truck1_pos)
                    self.truck1_pos = 0

            if len(self.truck2_priority_destinations) > 0:
                truck2_next = find_closest_destination(self.truck2_pos, self.truck2_priority_destinations)
                self.truck2_pos = truck2_next[0]
                self.truck2_distance += float(truck2_next[1])
                self.truck2_destinations.remove(truck2_next[0])
                self.truck2_priority_destinations.remove(truck2_next[0])
            elif len(self.truck2_destinations) > 0:
                truck2_next = find_closest_destination(self.truck2_pos, self.truck2_destinations)
                self.truck2_pos = truck2_next[0]
                self.truck2_distance += float(truck2_next[1])
                self.truck2_destinations.remove(truck2_next[0])
                if len(self.truck2_destinations) < 1:
                    self.truck2_distance += distance_to_home(self.truck2_pos)
                    self.truck2_pos = 0

            if len(self.truck3_priority_destinations) > 0:
                truck3_next = find_closest_destination(self.truck3_pos, self.truck3_priority_destinations)
                self.truck3_pos = truck3_next[0]
                self.truck3_distance += float(truck3_next[1])
                self.truck3_destinations.remove(truck3_next[0])
                self.truck3_priority_destinations.remove(truck3_next[0])
            elif len(self.truck3_destinations) > 0:
                truck3_next = find_closest_destination(self.truck3_pos, self.truck3_destinations)
                self.truck3_pos = truck3_next[0]
                self.truck3_distance += float(truck3_next[1])
                self.truck3_destinations.remove(truck3_next[0])
                if len(self.truck3_destinations) < 1:
                    self.truck3_distance += distance_to_home(self.truck3_pos)
                    self.truck3_pos = 0

            if len(self.truck1_destinations) < 1 and len(self.truck2_destinations) < 1 and len(self.truck3_destinations) < 1:
                break

