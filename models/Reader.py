import csv
from .HashTable import HashTable

class Reader:

    hash_table = HashTable()
    locations = HashTable()

    def __init__(self):
        with open('data/package_file.csv') as file:
            self.data = csv.reader(file, delimiter=',')

            for row in self.data:
                self.key = row[0]

                Reader.hash_table.add(self.key, [self.key, row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
        


