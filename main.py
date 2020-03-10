#!/usr/bin/python3
from models.Packages import Packages
import models.HashTable
from models.Distances import address_table
from models.Distances import find_closest_destination
from models.Distances import distance_to_home

print("Name: Jarred Wilson")
print("Student ID #001277133")

packages = Packages()
package_list = packages.hash_table
truck1_distance = 0.0
truck2_distance = 0.0
truck3_distance = 0.0
truck1_packages = [13,14,15,16,29,30,31,34,37,40,1,4,7,39,8,32]
truck2_packages = [3,18,36,38,6,10,11,12,17,20,21,22,23,24,25,26]
truck3_packages = [9,19,27,28,33,35,2,5]
truck1_destinations = []
truck2_destinations = []
truck3_destinations = []
truck1_pos = 0
truck2_pos = 0
truck3_pos = 0

for index in truck1_packages:
    address = package_list.get(str(index))[1]
    address2 = address_table.get(address)[2]
    addressId = address_table.get(address)[0]

    if address == address2 and addressId not in truck1_destinations:
        truck1_destinations.append(addressId)

for index in truck2_packages:
    address = package_list.get(str(index))[1]
    address2 = address_table.get(address)[2]
    addressId = address_table.get(address)[0]

    if address == address2 and addressId not in truck2_destinations:
        truck2_destinations.append(addressId)

for index in truck3_packages:
    address = package_list.get(str(index))[1]
    address2 = address_table.get(address)[2]
    addressId = address_table.get(address)[0]

    if address == address2 and addressId not in truck3_destinations:
        truck3_destinations.append(addressId)

while True:
    if len(truck1_destinations) > 0:
        truck1_next = find_closest_destination(truck1_pos, truck1_destinations)
        truck1_pos = truck1_next[0]
        truck1_distance += float(truck1_next[1])
        truck1_destinations.remove(truck1_next[0])
        if len(truck1_destinations) < 1:
            truck1_distance += distance_to_home(truck1_pos)
            truck1_pos = 0
    
    if len(truck2_destinations) > 0:
        truck2_next = find_closest_destination(truck2_pos, truck2_destinations)
        truck2_pos = truck2_next[0]
        truck2_distance += float(truck2_next[1])
        truck2_destinations.remove(truck2_next[0])
        if len(truck2_destinations) < 1:
            truck2_distance += distance_to_home(truck2_pos)
            truck2_pos = 0

    if len(truck3_destinations) > 0:
        truck3_next = find_closest_destination(truck3_pos, truck3_destinations)
        truck3_pos = truck3_next[0]
        truck3_distance += float(truck3_next[1])
        truck3_destinations.remove(truck3_next[0])
        if len(truck3_destinations) < 1:
            truck3_distance += distance_to_home(truck3_pos)
            truck3_pos = 0

    if len(truck1_destinations) < 1 and len(truck2_destinations) < 1 and len(truck3_destinations) < 1:
        break



print("All packages delivered in " + str(truck1_distance + truck2_distance + truck3_distance) + " miles")

print("\n1) Package Lookup")
print("2) ")