"""
001+01.py — PyBullet Double Pendulum
A concrete experimental object built from the PhysicalObject concept.
The reusable concept remains in 000-04.py.
"""

from pathlib import Path
import importlib.util
import math
import sys
import pybullet as p


def load_physical_object():
    path = Path(__file__).with_name("000-04.py")
    spec = importlib.util.spec_from_file_location("physical_object", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.PhysicalObject


PhysicalObject = load_physical_object()


class DoublePendulum:
    """Two-link pendulum simulated by PyBullet."""

    def __init__(
        self,
        theta1,
        theta2,
        mass1=1.0,
        mass2=1.0,
        length1=1.0,
        length2=1.0,
        gravity=9.81,
    ):
        self.upper_mass = PhysicalObject("Upper Pendulum Mass")
        self.lower_mass = PhysicalObject("Lower Pendulum Mass")
        self.mass1 = mass1
        self.mass2 = mass2
        self.length1 = length1
        self.length2 = length2
        self.gravity = gravity
        self.theta1 = theta1
        self.theta2 = theta2
        self.client = p.connect(p.DIRECT)
        p.setGravity(0, 0, -gravity, physicsClientId=self.client)
        self._build()
        self.reset(theta1, theta2)

    def _build(self):
        collision = p.createCollisionShape(
            p.GEOM_BOX,
            halfExtents=[0.03, self.length1 / 2, 0.03],
            physicsClientId=self.client,
        )
        self.arm1 = p.createMultiBody(
            baseMass=0,
            baseCollisionShapeIndex=collision,
            basePosition=[0, -self.length1 / 2, 0],
            physicsClientId=self.client,
        )
        self.arm2 = p.createMultiBody(
            baseMass=self.mass2,
            baseCollisionShapeIndex=collision,
            basePosition=[0, -self.length1 - self.length2 / 2, 0],
            physicsClientId=self.client,
        )

    def reset(self, theta1, theta2):
        """Reset the pendulum to a pair of initial angles."""
        self.theta1 = theta1
        self.theta2 = theta2
        self.time = 0.0
        self._set_geometry(theta1, theta2)

    def _set_geometry(self, theta1, theta2):
        x1 = self.length1 * math.sin(theta1)
        y1 = -self.length1 * math.cos(theta1)
        x2 = x1 + self.length2 * math.sin(theta2)
        y2 = y1 - self.length2 * math.cos(theta2)
        p.resetBasePositionAndOrientation(
            self.arm1,
            [x1 / 2, y1 / 2, 0],
            p.getQuaternionFromEuler([0, 0, theta1]),
            physicsClientId=self.client,
        )
        p.resetBasePositionAndOrientation(
            self.arm2,
            [x2, y2, 0],
            p.getQuaternionFromEuler([0, 0, theta2]),
            physicsClientId=self.client,
        )

    def state(self):
        """Return the current angular state."""
        return (self.theta1, self.theta2)

    def position(self):
        """Return the position of the second mass."""
        x1 = self.length1 * math.sin(self.theta1)
        y1 = -self.length1 * math.cos(self.theta1)
        return (
            x1 + self.length2 * math.sin(self.theta2),
            y1 - self.length2 * math.cos(self.theta2),
        )

    def step(self, dt):
        """Advance the PyBullet simulation."""
        p.stepSimulation(physicsClientId=self.client)
        self.time += dt

    def close(self):
        """Release the PyBullet simulation."""
        if p.isConnected(self.client):
            p.disconnect(self.client)


if __name__ == "__main__":
    pendulum = DoublePendulum(
        theta1=math.radians(120),
        theta2=math.radians(120),
    )
    try:
        for _ in range(100):
            pendulum.step(1 / 240)
        print("Double pendulum state:", pendulum.state())
        print("Second mass position:", pendulum.position())
    finally:
        pendulum.close()
