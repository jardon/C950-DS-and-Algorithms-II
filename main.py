#!/usr/bin/python3
from models.Simulation import Simulation

print("Name: Jarred Wilson")
print("Student ID #001277133")

sim = Simulation()
sim.run("16:47")

print("All packages delivered in " + str(sim.get_total_distance()) + " miles")

print("\n1) Package Lookup")
print("2) ")