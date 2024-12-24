#!./bin/python3
import numpy as np
import time

G = 0.3
masses = [1, 1]
dt = 0.01

positions = [
    np.array([-1.0, 1.0, 0.0]),
    np.array([1.0, 0.0, 0.0])
]
velocities = [
    np.array([0.3, 0.1, 0.0]),
    np.array([-0.1, -0.1, 0.0])
]

while True:
    if m1 + m
    testing = []

    forces = [np.array([0.0, 0.0, 0.0]) for _ in range(len(positions))]
    for i in range(len(positions)):
        for j in range(len(positions)):
            if i != j:
                r_ij = positions[j] - positions[i]
                distance = np.linalg.norm(r_ij)
                force_magnitude = G * masses[i] * masses[j] / distance**2
                force_direction = r_ij / distance
                forces[i] += force_magnitude * force_direction

    for i in range(len(positions)):
        velocities[i] += forces[i] / masses[i] * dt
        positions[i] += velocities[i] * dt

    if expr
#    print(positions)
