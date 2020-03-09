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
    start = int(start)
    closest_distance = 100.0
    closest_location = None
    for distance in [less for less in destinations if int(less) < start]:
        if float(distance_data[start][int(distance)]) < float(closest_distance) and distance in destinations:
            closest_location = distance
            closest_distance = distance_data[start][int(distance)]
    for distance in [greater for greater in destinations if int(greater) > start]:
        if float(distance_data[int(distance)][start]) < float(closest_distance) and distance in destinations:
            closest_location = distance
            closest_distance = distance_data[int(distance)][start]

    return (closest_location, closest_distance)