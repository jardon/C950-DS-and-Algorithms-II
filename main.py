#!/usr/bin/python3
#Jarred Wilson
#001277133

from models.Simulation import Simulation
import sys

print("Name: Jarred Wilson")
print("Student ID #001277133")

sim = Simulation()
sim.run("16:47")

print("All packages delivered in " + str(sim.get_total_distance()) + " miles")

while True:
    print("\n1) Package Lookup")
    print("2) Check State")
    print("0) Exit Application\n")
    print("Enter an option above:")
    selected = input()

    if selected == '0':
        sys.exit()
    if selected == '1':
        print("\nEnter search criteria:")
        input()
    if selected == '2':
        print("\nEnter time in 'HH:MM' format:")
        sim.reset()
        sim.run(input())
        