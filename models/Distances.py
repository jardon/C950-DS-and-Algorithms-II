import csv
import datetime
from .HashTable import HashTable

address_data = list(csv.reader(open('data/distance_address.csv'), delimiter=','))
distance_data = list(csv.reader(open('data/distance_data.csv'), delimiter=','))
address_table = HashTable()

with open('data/distance_address.csv') as file:
            data = csv.reader(file, delimiter=',')

            for row in data:
                key = row[2]

                address_table.add(key, [row[0], row[1], key])

def find_closest_destination(start, destinations):
    closest_distance = 100.0
    closest_location = None
    for distance in range(0, start):
        if float(distance_data[start][distance]) < float(closest_distance) and distance in destinations:
            closest_location = distance
            closest_distance = distance_data[start][distance]
    for distance in range(start + 1, len(address_data)):
        if float(distance_data[distance][start]) < float(closest_distance) and distance in destinations:
            closest_location = distance
            closest_distance = distance_data[distance][start]

    return (closest_location, closest_distance)