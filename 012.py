```python
"""
STORY NODE 012
==============
NEWTON AND THE FALLING APPLE

This node introduces Isaac Newton as a persistent character and makes
PyBullet the first real physics backend of LongStoryGoes.

The story uses the famous falling-apple tradition as a narrative starting
point. It does not claim that the historical discovery happened exactly as
shown here. The important event is Newton asking why objects fall toward
Earth and whether the same principle could reach as far as the Moon.

Architecture:

    Story / English
          |
          v
      World Model
          |
          v
      PhysicsAdapter
          |
          v
        PyBullet

PyBullet calculates the falling object's motion. LongStoryGoes records the
meaning of what the character observes. Blender can later read the same
world state and visualize it.

Requirement:

    pip install pybullet
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Core world objects
# ---------------------------------------------------------------------------


@dataclass
class WorldObject:
    """A persistent object in the LongStoryGoes world."""

    id: str
    type: str
    name: str | None = None
    location: str | None = None

    geometry: dict[str, Any] = field(default_factory=dict)
    transform: dict[str, Any] = field(default_factory=dict)
    appearance: dict[str, Any] = field(default_factory=dict)

    properties: dict[str, Any] = field(default_factory=dict)
    state: dict[str, Any] = field(default_factory=dict)
    relationships: dict[str, Any] = field(default_factory=dict)

    def set_state(self, name: str, value: Any) -> None:
        self.state[name] = value


@dataclass
class Location(WorldObject):
    type: str = "location"


@dataclass
class Character(WorldObject):
    type: str = "character"

    def move_to(self, location: WorldObject) -> None:
        self.location = location.id

    def look_at(self, target: WorldObject) -> None:
        self.state["looking_at"] = target.id

    def observe(self, observation: str) -> None:
        observations = self.state.setdefault("observations", [])
        observations.append(observation)


@dataclass
class World:
    time: float = 0.0
    objects: dict[str, WorldObject] = field(default_factory=dict)
    history: list[dict[str, Any]] = field(default_factory=list)
    knowledge: list[dict[str, Any]] = field(default_factory=list)

    def add(self, obj: WorldObject) -> WorldObject:
        self.objects[obj.id] = obj
        return obj

    def record(self, event: dict[str, Any]) -> None:
        self.history.append(event)

    def learn(self, knowledge: dict[str, Any]) -> None:
        self.knowledge.append(knowledge)


class Story:
    def __init__(self, world: World):
        self.world = world
        self.observations: list[str] = []

    def observe(self, text: str) -> None:
        self.observations.append(text)


# ---------------------------------------------------------------------------
# Physics adapter
# ---------------------------------------------------------------------------


class PhysicsAdapter:
    """
    Small LongStoryGoes interface around PyBullet.

    The story world owns the meaning and identity of objects.
    PyBullet owns the mechanical calculation.
    """

    def __init__(self, gravity: float = -9.81):
        try:
            import pybullet as p
        except ImportError as exc:
            raise RuntimeError(
                "PyBullet is required for STORY NODE 012. "
                "Install it with: pip install pybullet"
            ) from exc

        self.p = p
        self.client = p.connect(p.DIRECT)

        if self.client < 0:
            raise RuntimeError(
                "Could not start the PyBullet physics server."
            )

        self.p.setGravity(
            0.0,
            0.0,
            gravity,
            physicsClientId=self.client,
        )

        self.p.setTimeStep(
            1.0 / 240.0,
            physicsClientId=self.client,
        )

        self.bodies: dict[str, int] = {}

    def add_static_plane(self, object_id: str) -> None:
        plane_shape = self.p.createCollisionShape(
            self.p.GEOM_PLANE,
            physicsClientId=self.client,
        )

        body = self.p.createMultiBody(
            baseMass=0.0,
            baseCollisionShapeIndex=plane_shape,
            physicsClientId=self.client,
        )

        self.bodies[object_id] = body

    def add_sphere(
        self,
        object_id: str,
        radius: float,
        mass: float,
        position: tuple[float, float, float],
    ) -> None:
        shape = self.p.createCollisionShape(
            self.p.GEOM_SPHERE,
            radius=radius,
            physicsClientId=self.client,
        )

        body = self.p.createMultiBody(
            baseMass=mass,
            baseCollisionShapeIndex=shape,
            basePosition=position,
            physicsClientId=self.client,
        )

        self.bodies[object_id] = body

    def step(self, steps: int = 1) -> None:
        for _ in range(steps):
            self.p.stepSimulation(
                physicsClientId=self.client
            )

    def position(
        self,
        object_id: str,
    ) -> tuple[float, float, float]:
        body = self.bodies[object_id]

        position, _ = self.p.getBasePositionAndOrientation(
            body,
            physicsClientId=self.client,
        )

        return tuple(position)

    def velocity(
        self,
        object_id: str,
    ) -> tuple[float, float, float]:
        body = self.bodies[object_id]

        linear, _ = self.p.getBaseVelocity(
            body,
            physicsClientId=self.client,
        )

        return tuple(linear)

    def close(self) -> None:
        if self.client >= 0:
            self.p.disconnect(self.client)
            self.client = -1


# ---------------------------------------------------------------------------
# The world
# ---------------------------------------------------------------------------


world = World(time=0.0)
story = Story(world)
physics = PhysicsAdapter(gravity=-9.81)


# ---------------------------------------------------------------------------
# Location and persistent character
# ---------------------------------------------------------------------------


garden = world.add(
    Location(
        id="newton_garden",
        name="Garden at Woolsthorpe",
        geometry={
            "shape": "garden",
            "ground": "grass",
        },
        properties={
            "open_sky": True,
            "historical_setting": "Woolsthorpe, Lincolnshire",
        },
    )
)


# This character is persistent.
# Later story nodes can refer to exactly the same person using this ID.

newton = world.add(
    Character(
        id="isaac_newton",
        name="Isaac Newton",
        location=garden.id,
        properties={
            "occupation": "natural philosopher",
            "later_known_for": [
                "laws of motion",
                "universal gravitation",
                "mathematics",
                "optics",
            ],
        },
        state={
            "curious": True,
            "thinking_about_gravity": False,
        },
    )
)


apple = world.add(
    WorldObject(
        id="newton_apple",
        type="apple",
        name="Apple",
        location=garden.id,
        geometry={
            "shape": "sphere",
            "radius_m": 0.04,
        },
        properties={
            "mass_kg": 0.10,
        },
        state={
            "fallen": False,
        },
    )
)


ground = world.add(
    WorldObject(
        id="newton_ground",
        type="ground",
        name="Ground",
        location=garden.id,
        properties={
            "static": True,
        },
    )
)


# ---------------------------------------------------------------------------
# Physical setup
# ---------------------------------------------------------------------------


physics.add_static_plane(ground.id)

physics.add_sphere(
    object_id=apple.id,
    radius=apple.geometry["radius_m"],
    mass=apple.properties["mass_kg"],
    position=(0.0, 0.0, 5.0),
)

apple.transform["position_m"] = physics.position(apple.id)


# ---------------------------------------------------------------------------
# Story begins
# ---------------------------------------------------------------------------


story.observe(
    "Newton sat beneath a tree and watched the ordinary world around him. "
    "An apple hung above the ground, held there by its stem."
)

newton.observe(
    "An apple is above the ground while its stem supports it."
)

newton.look_at(apple)

world.record(
    {
        "time": world.time,
        "event": "apple_observed_before_fall",
        "observer": newton.id,
        "object": apple.id,
        "position_m": apple.transform["position_m"],
    }
)


story.observe(
    "The apple fell. Newton did not merely see it fall; he asked why it "
    "fell toward the Earth instead of moving in some other direction."
)

newton.state["thinking_about_gravity"] = True


# Run the actual mechanical simulation for two seconds.
#
# PyBullet uses 240 simulation steps per second.
# 480 steps therefore represents two seconds of simulated time.

world.time = 0.0

physics.step(steps=480)

world.time = 2.0


apple.transform["position_m"] = physics.position(apple.id)

apple.state["velocity_m_s"] = physics.velocity(apple.id)

apple.state["fallen"] = (
    apple.transform["position_m"][2] <= 0.15
)


world.record(
    {
        "time": world.time,
        "event": "apple_fall_simulated",
        "object": apple.id,
        "position_m": apple.transform["position_m"],
        "velocity_m_s": apple.state["velocity_m_s"],
        "gravity_m_s2": -9.81,
        "physics_engine": "pybullet",
    }
)


story.observe(
    "The result was simple and repeatable: when released above the ground, "
    "the apple accelerated downward and eventually struck the ground."
)

newton.observe(
    "Objects near the Earth accelerate toward the Earth when no support "
    "holds them."
)


# ---------------------------------------------------------------------------
# From observation to a question
# ---------------------------------------------------------------------------


world.learn(
    {
        "subject": "gravity",
        "type": "observation",
        "observer": newton.id,
        "statement": (
            "A released object accelerates toward the Earth."
        ),
        "measurement": {
            "gravity_m_s2": -9.81,
        },
    }
)


story.observe(
    "But Newton's question grew larger. If the Earth could pull an apple "
    "downward, could the same influence extend much farther into space?"
)


world.learn(
    {
        "subject": "gravity",
        "type": "question",
        "author": newton.id,
        "statement": (
            "Does the influence that makes objects fall toward Earth "
            "extend into space?"
        ),
    }
)


world.record(
    {
        "time": world.time,
        "event": "question_about_universal_gravity",
        "observer": newton.id,
        "subject": "Earth and Moon",
    }
)


story.observe(
    "The falling apple had not given Newton the whole theory. It had given "
    "him a question large enough to lead from a garden to the motion of "
    "the Moon."
)


newton.state["research_question"] = "universal_gravity"


physics.close()


# ---------------------------------------------------------------------------
# Continuity
# ---------------------------------------------------------------------------


CONTINUITY = {
    "persistent_objects": [
        "isaac_newton",
        "newton_garden",
        "newton_apple",
        "newton_ground",
    ],

    "world_changes": [
        "Isaac Newton is introduced as a persistent character.",
        "The apple is physically simulated with PyBullet gravity.",
        "The apple falls and collides with the ground.",
        "The world records a measured gravitational observation.",
        "Newton forms the question of whether gravity extends into space.",
    ],

    "knowledge_added": [
        "A released object accelerates toward Earth.",
        "The gravity observation can be reproduced by the physics simulation.",
        "The next question concerns gravity beyond the immediate surroundings "
        "of Earth.",
    ],

    "next_node": "013.py",
}


if __name__ == "__main__":
    print("STORY NODE 012 - NEWTON AND THE FALLING APPLE")
    print(f"Character: {newton.name} ({newton.id})")
    print(f"Apple final position: {apple.transform['position_m']}")
    print(f"Apple final velocity: {apple.state['velocity_m_s']}")
    print(f"World time: {world.time:.2f} s")
    print("Physics backend: pybullet")

    print("\nStory:")

    for observation in story.observations:
        print(f"- {observation}")
```
