#!/usr/bin/python3
from models.Simulation import Simulation
# from models.Simulation import run
# from models.Simulation import get_total_distance

print("Name: Jarred Wilson")
print("Student ID #001277133")

sim = Simulation()
sim.run()

print("All packages delivered in " + str(sim.get_total_distance()) + " miles")

print("\n1) Package Lookup")
print("2) ")