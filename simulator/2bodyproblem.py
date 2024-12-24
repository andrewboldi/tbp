from manim import *
import numpy as np

class TwoBodyProblem(Scene):
    def construct(self):
        # Constants
        G = 0.3  # Gravitational constant (increased to strengthen gravitational attraction)
        masses = [1, 1]  # Masses of the bodies (in kg)
        dt = 0.01  # Time step for the simulation

        # Initial positions and velocities (in arbitrary units)
        positions = [
            np.array([-1.0, 1.0, 0.0]),  # Initial position of body 1
            np.array([1.0, 0.0, 0.0])    # Initial position of body 2
        ]
        velocities = [
            np.array([0.3, 0.1, 0.0]),   # Initial velocity of body 1 (reduced to avoid high escape velocity)
            np.array([-0.1, -0.1, 0.0])   # Initial velocity of body 2 (reduced to avoid high escape velocity)
        ]

        # Create body objects
        bodies = [
            Dot(point=positions[0], color=BLUE),
            Dot(point=positions[1], color=RED)
        ]

        # Create trajectory lines
        trajectories = [
            TracedPath(bodies[0].get_center, stroke_color=BLUE, stroke_width=2),
            TracedPath(bodies[1].get_center, stroke_color=RED, stroke_width=2)
        ]

        # Add bodies and their trajectories to the scene
        self.add(*bodies, *trajectories)

        # Simulation loop
        for _ in range(4000):
            # Calculate forces on each body
            forces = [np.array([0.0, 0.0, 0.0]) for _ in range(len(bodies))]
            for i in range(len(bodies)):
                for j in range(len(bodies)):
                    if i != j:
                        r_ij = positions[j] - positions[i]
                        distance = np.linalg.norm(r_ij)
                        force_magnitude = G * masses[i] * masses[j] / distance**2
                        force_direction = r_ij / distance
                        forces[i] += force_magnitude * force_direction

            # Update velocities and positions based on the forces (Newton's second law)
            for i in range(len(bodies)):
                velocities[i] += forces[i] / masses[i] * dt
                positions[i] += velocities[i] * dt

                # Move the body objects to their new positions
                bodies[i].move_to(positions[i])

            # Wait for a short duration to create the animation effect
            self.wait(dt)

# To run this, use the manim command in your terminal:
# manim -pql -n 0,400 two_body_problem.py TwoBodyProblem  # Use -n to specify the frame range for faster rendering
