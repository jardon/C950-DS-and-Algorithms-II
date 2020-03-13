import csv
from .HashTable import HashTable

class Packages:

    # Static variables
    # Holds two hash tables based off of data csvs
    hash_table = HashTable()

    # Constructor
    # Only method to set up static variables
    # O(N)
    def __init__(self):
        with open('data/package_file.csv') as file:
            self.data = csv.reader(file, delimiter=',')

            for row in self.data:
                self.key = row[0]

                Packages.hash_table.add(self.key, [self.key, row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
        


