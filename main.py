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
    print()
    selected = input("Enter an option above: ")

    if selected == '0':
        sys.exit()
    if selected == '1':
        sim.reset()
        sim.run(input("Enter time in 'HH:MM' format: "))
        sim.print(int(input("\nEnter package ID: ")))
    if selected == '2':
        sim.reset()
        sim.run(input("\nEnter time in 'HH:MM' format: "))
        sim.print()