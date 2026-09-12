"""
001-01-01.py — Physical World Evolution
Evolution of 001-01.py.
The original World API is preserved.
PyBullet provides physical simulation.
NumPy provides numerical measurements.
Only World.act() may change authoritative world state.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
import math
import numpy as np
import pybullet as p


@dataclass
class PhysicalBody:
    id: str
    body_id: int
    mass: float
    size: Tuple[float, float, float]
    position: Tuple[float, float, float]
    dynamic: bool = True


@dataclass(frozen=True)
class PhysicalEvent:
    time: int
    actor: str
    action: str
    result: str
    target: Optional[str] = None


class World:
    """
    Authoritative world with an optional physical simulation.

    Existing 001-01 behaviour is preserved:
        observe()
        act()
        tick()
        state()
        narrative()
        Agent

    New physical state can only be changed through World.act().
    """

    def __init__(self, physics: bool = True) -> None:
        self.time: int = 0
        self.locations: Dict[str, Any] = {}
        self.characters: Dict[str, Any] = {}
        self.items: Dict[str, Any] = {}
        self.history: List[Any] = []
        self.physical_bodies: Dict[str, PhysicalBody] = {}
        self.physical_events: List[PhysicalEvent] = []
        self.physics_enabled = physics
        self.client = None
        self._build_world()
        if physics:
            self._start_physics()

    def _build_world(self) -> None:
        self.locations = {
            "village": {
                "id": "village",
                "name": "Old Village",
                "description": "A small village beside a dark forest.",
                "exits": {"forest": "forest", "house": "house"},
            },
            "forest": {
                "id": "forest",
                "name": "Forest",
                "description": "A quiet forest.",
                "exits": {"village": "village"},
            },
            "house": {
                "id": "house",
                "name": "Miller's House",
                "description": "A small wooden house.",
                "exits": {"village": "village"},
            },
        }
        self.characters = {
            "anna": {
                "id": "anna",
                "name": "Anna",
                "location": "village",
                "alive": True,
                "inventory": [],
            },
            "boris": {
                "id": "boris",
                "name": "Boris",
                "location": "house",
                "alive": True,
                "inventory": [],
            },
            "mira": {
                "id": "mira",
                "name": "Mira",
                "location": "forest",
                "alive": True,
                "inventory": [],
            },
        }
        self.items = {
            "lamp": {
                "id": "lamp",
                "name": "Oil Lamp",
                "location": "house",
                "owner": None,
                "state": "normal",
                "exists": True,
            },
            "axe": {
                "id": "axe",
                "name": "Woodcutter's Axe",
                "location": "forest",
                "owner": None,
                "state": "normal",
                "exists": True,
            },
            "bell": {
                "id": "bell",
                "name": "Village Bell",
                "location": "village",
                "owner": None,
                "state": "normal",
                "exists": True,
            },
            "bridge": {
                "id": "bridge",
                "name": "Old Wooden Bridge",
                "location": "forest",
                "owner": None,
                "state": "intact",
                "exists": True,
            },
        }

    def _start_physics(self) -> None:
        self.client = p.connect(p.DIRECT)
        p.setGravity(0, 0, -9.81, physicsClientId=self.client)
        self._create_ground()

    def _create_ground(self) -> None:
        shape = p.createCollisionShape(
            p.GEOM_BOX,
            halfExtents=[10, 10, 0.05],
            physicsClientId=self.client,
        )
        p.createMultiBody(
            baseMass=0,
            baseCollisionShapeIndex=shape,
            basePosition=[0, 0, -0.05],
            physicsClientId=self.client,
        )

    def add_physical_object(
        self,
        object_id: str,
        mass: float = 1.0,
        size: Tuple[float, float, float] = (1.0, 1.0, 1.0),
        position: Tuple[float, float, float] = (0.0, 0.0, 1.0),
        dynamic: bool = True,
    ) -> Dict[str, Any]:
        """
        Register a physical object.

        This method creates an object only through the World.
        Experiments should request creation through act().
        """

        if not self.physics_enabled:
            return self._reject(
                "system",
                "create_physical",
                "Physics is disabled.",
            )

        if object_id in self.physical_bodies:
            return self._reject(
                "system",
                "create_physical",
                "Physical object already exists.",
            )

        half_extents = np.asarray(size, dtype=float) / 2.0

        shape = p.createCollisionShape(
            p.GEOM_BOX,
            halfExtents=half_extents.tolist(),
            physicsClientId=self.client,
        )

        body_id = p.createMultiBody(
            baseMass=mass if dynamic else 0,
            baseCollisionShapeIndex=shape,
            basePosition=position,
            physicsClientId=self.client,
        )

        self.physical_bodies[object_id] = PhysicalBody(
            id=object_id,
            body_id=body_id,
            mass=mass,
            size=size,
            position=position,
            dynamic=dynamic,
        )

        return {
            "ok": True,
            "object": object_id,
            "body_id": body_id,
        }

    def physical_state(self, object_id: str) -> Dict[str, Any]:
        """Return measured physical state from PyBullet."""

        body = self.physical_bodies.get(object_id)

        if body is None:
            raise KeyError(f"Unknown physical object: {object_id}")

        position, orientation = p.getBasePositionAndOrientation(
            body.body_id,
            physicsClientId=self.client,
        )

        velocity, angular_velocity = p.getBaseVelocity(
            body.body_id,
            physicsClientId=self.client,
        )

        return {
            "id": object_id,
            "position": tuple(position),
            "orientation": tuple(orientation),
            "velocity": tuple(velocity),
            "angular_velocity": tuple(angular_velocity),
        }

    def distance(self, first: str, second: str) -> float:
        """Measure Euclidean distance between two physical objects."""

        a = np.asarray(self.physical_state(first)["position"])
        b = np.asarray(self.physical_state(second)["position"])

        return float(np.linalg.norm(a - b))

    def tick(self, minutes: int = 1) -> None:
        if minutes < 0:
            raise ValueError("Time cannot move backwards.")

        for _ in range(minutes):
            self.time += 1
            if self.physics_enabled:
                for _ in range(60):
                    p.stepSimulation(physicsClientId=self.client)

    def observe(self, character_id: str) -> Dict[str, Any]:
        character = self._character(character_id)
        location = self.locations[character["location"]]

        visible_characters = [
            {
                "id": c["id"],
                "name": c["name"],
                "alive": c["alive"],
            }
            for c in self.characters.values()
            if c["location"] == character["location"]
            and c["id"] != character_id
        ]

        visible_items = [
            {
                "id": item["id"],
                "name": item["name"],
                "state": item["state"],
            }
            for item in self.items.values()
            if item["exists"]
            and item["location"] == character["location"]
            and item["owner"] is None
        ]

        physical = {
            object_id: self.physical_state(object_id)
            for object_id in self.physical_bodies
        }

        return {
            "time": self.time,
            "character": {
                "id": character["id"],
                "name": character["name"],
                "alive": character["alive"],
                "inventory": [
                    self.items[item_id]["name"]
                    for item_id in character["inventory"]
                    if self.items[item_id]["exists"]
                ],
            },
            "location": {
                "id": location["id"],
                "name": location["name"],
                "description": location["description"],
                "exits": dict(location["exits"]),
            },
            "characters": visible_characters,
            "items": visible_items,
            "physical_objects": physical,
        }

    def act(
        self,
        actor_id: str,
        action: str,
        target: Optional[str] = None,
        destination: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        The only public mutation interface.

        Physical actions are validated here before PyBullet is changed.
        """

        actor = self._character(actor_id)

        if not actor["alive"]:
            return self._reject(actor_id, action, "Actor is dead.")

        parameters = parameters or {}

        if action == "wait":
            self.tick(1)
            return self._accept(actor_id, action, "Time advanced.")

        if action == "move":
            return self._move(actor, destination)

        if action == "take":
            return self._take(actor, target)

        if action == "drop":
            return self._drop(actor, target)

        if action == "ring":
            return self._ring(actor, target)

        if action == "break":
            return self._break(actor, target)

        if action == "create_physical":
            return self._create_physical_action(
                actor_id,
                target,
                parameters,
            )

        if action == "move_physical":
            return self._move_physical_action(
                actor_id,
                target,
                parameters,
            )

        if action == "connect_physical":
            return self._connect_physical_action(
                actor_id,
                target,
                parameters,
            )

        if action == "look":
            return {
                "ok": True,
                "action": "look",
                "observation": self.observe(actor_id),
            }

        return self._reject(actor_id, action, "Unknown action.")

    def _create_physical_action(
        self,
        actor_id: str,
        target: Optional[str],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:

        if target is None:
            return self._reject(
                actor_id,
                "create_physical",
                "No object supplied.",
            )

        if target in self.physical_bodies:
            return self._reject(
                actor_id,
                "create_physical",
                "Object already exists.",
            )

        size = tuple(parameters.get("size", (1.0, 1.0, 1.0)))
        mass = float(parameters.get("mass", 1.0))
        position = tuple(parameters.get("position", (0.0, 0.0, 1.0)))

        if len(size) != 3 or any(value <= 0 for value in size):
            return self._reject(
                actor_id,
                "create_physical",
                "Invalid physical dimensions.",
            )

        if mass < 0:
            return self._reject(
                actor_id,
                "create_physical",
                "Mass cannot be negative.",
            )

        result = self.add_physical_object(
            target,
            mass=mass,
            size=size,
            position=position,
        )

        if not result["ok"]:
            return result

        self.tick(1)

        return self._accept(
            actor_id,
            "create_physical",
            f"Created physical object {target}.",
            target,
        )

    def _move_physical_action(
        self,
        actor_id: str,
        target: Optional[str],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:

        if target not in self.physical_bodies:
            return self._reject(
                actor_id,
                "move_physical",
                "Physical object does not exist.",
            )

        if "position" not in parameters:
            return self._reject(
                actor_id,
                "move_physical",
                "No position supplied.",
            )

        position = tuple(parameters["position"])

        if len(position) != 3:
            return self._reject(
                actor_id,
                "move_physical",
                "Position must contain three coordinates.",
            )

        body = self.physical_bodies[target]

        if not body.dynamic:
            return self._reject(
                actor_id,
                "move_physical",
                "Static objects cannot be moved this way.",
            )

        p.resetBasePositionAndOrientation(
            body.body_id,
            position,
            [0, 0, 0, 1],
            physicsClientId=self.client,
        )

        self.tick(1)

        return self._accept(
            actor_id,
            "move_physical",
            f"Moved {target}.",
            target,
        )

    def _connect_physical_action(
        self,
        actor_id: str,
        target: Optional[str],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:

        other = parameters.get("other")

        if target not in self.physical_bodies:
            return self._reject(
                actor_id,
                "connect_physical",
                "First object does not exist.",
            )

        if other not in self.physical_bodies:
            return self._reject(
                actor_id,
                "connect_physical",
                "Second object does not exist.",
            )

        if target == other:
            return self._reject(
                actor_id,
                "connect_physical",
                "An object cannot connect to itself.",
            )

        separation = self.distance(target, other)

        if separation > float(parameters.get("max_distance", 0.25)):
            return self._reject(
                actor_id,
                "connect_physical",
                f"Objects are too far apart: {separation:.4f}.",
            )

        a = self.physical_bodies[target]
        b = self.physical_bodies[other]

        constraint = p.createConstraint(
            a.body_id,
            -1,
            b.body_id,
            -1,
            p.JOINT_FIXED,
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            physicsClientId=self.client,
        )

        self.tick(1)

        return self._accept(
            actor_id,
            "connect_physical",
            f"Connected {target} to {other}. Constraint {constraint}.",
            target,
        )

    def _move(
        self,
        actor: Dict[str, Any],
        destination: Optional[str],
    ) -> Dict[str, Any]:

        if destination is None:
            return self._reject(actor["id"], "move", "No destination supplied.")

        current = self.locations[actor["location"]]

        if destination not in current["exits"]:
            return self._reject(
                actor["id"],
                "move",
                f"{current['name']} has no exit to {destination}.",
            )

        destination_id = current["exits"][destination]

        if (
            destination_id == "forest"
            and self.items["bridge"]["state"] == "broken"
        ):
            return self._reject(
                actor["id"],
                "move",
                "The bridge is broken.",
            )

        old_location = actor["location"]
        actor["location"] = destination_id
        self.tick(1)

        return self._accept(
            actor["id"],
            "move",
            f"{actor['name']} moved from {old_location} to {destination_id}.",
        )

    def _take(
        self,
        actor: Dict[str, Any],
        target: Optional[str],
    ) -> Dict[str, Any]:

        if target is None:
            return self._reject(actor["id"], "take", "No item supplied.")

        item = self.items.get(target)

        if item is None or not item["exists"]:
            return self._reject(actor["id"], "take", "Item does not exist.")

        if item["owner"] is not None:
            return self._reject(actor["id"], "take", "Item is already owned.")

        if item["location"] != actor["location"]:
            return self._reject(
                actor["id"],
                "take",
                "Item is not at the actor's location.",
            )

        item["location"] = None
        item["owner"] = actor["id"]
        actor["inventory"].append(item["id"])
        self.tick(1)

        return self._accept(
            actor["id"],
            "take",
            f"{actor['name']} took {item['name']}.",
        )

    def _drop(
        self,
        actor: Dict[str, Any],
        target: Optional[str],
    ) -> Dict[str, Any]:

        if target is None:
            return self._reject(actor["id"], "drop", "No item supplied.")

        if target not in actor["inventory"]:
            return self._reject(
                actor["id"],
                "drop",
                "Actor does not possess that item.",
            )

        item = self.items[target]
        actor["inventory"].remove(target)
        item["owner"] = None
        item["location"] = actor["location"]
        self.tick(1)

        return self._accept(
            actor["id"],
            "drop",
            f"{actor['name']} dropped {item['name']}.",
        )

    def _ring(
        self,
        actor: Dict[str, Any],
        target: Optional[str],
    ) -> Dict[str, Any]:

        if target != "bell":
            return self._reject(actor["id"], "ring", "Only the bell can ring.")

        if actor["location"] != "village":
            return self._reject(actor["id"], "ring", "The bell is not here.")

        self.tick(1)

        return self._accept(
            actor["id"],
            "ring",
            "The village bell rings.",
        )

    def _break(
        self,
        actor: Dict[str, Any],
        target: Optional[str],
    ) -> Dict[str, Any]:

        if target != "bridge":
            return self._reject(
                actor["id"],
                "break",
                "That object cannot be broken.",
            )

        bridge = self.items["bridge"]

        if bridge["location"] != actor["location"]:
            return self._reject(
                actor["id"],
                "break",
                "The bridge is not here.",
            )

        if bridge["state"] == "broken":
            return self._reject(
                actor["id"],
                "break",
                "The bridge is already broken.",
            )

        if "axe" not in actor["inventory"]:
            return self._reject(
                actor["id"],
                "break",
                "An axe is required.",
            )

        bridge["state"] = "broken"
        self.tick(1)

        return self._accept(
            actor["id"],
            "break",
            "The old wooden bridge breaks.",
        )

    def _accept(
        self,
        actor_id: str,
        action: str,
        result: str,
        target: Optional[str] = None,
    ) -> Dict[str, Any]:

        event = PhysicalEvent(
            time=self.time,
            actor=actor_id,
            action=action,
            result=result,
            target=target,
        )

        self.history.append(event)
        self.physical_events.append(event)

        return {
            "ok": True,
            "time": self.time,
            "action": action,
            "result": result,
            "target": target,
        }

    def _reject(
        self,
        actor_id: str,
        action: str,
        reason: str,
    ) -> Dict[str, Any]:

        event = PhysicalEvent(
            time=self.time,
            actor=actor_id,
            action=action,
            result=f"REJECTED: {reason}",
        )

        self.history.append(event)
        self.physical_events.append(event)

        return {
            "ok": False,
            "time": self.time,
            "action": action,
            "error": reason,
        }

    def _character(self, character_id: str) -> Dict[str, Any]:
        if character_id not in self.characters:
            raise KeyError(f"Unknown character: {character_id}")
        return self.characters[character_id]

    def state(self) -> Dict[str, Any]:
        physical = {
            object_id: self.physical_state(object_id)
            for object_id in self.physical_bodies
        }

        return {
            "time": self.time,
            "characters": {
                key: {
                    "name": value["name"],
                    "location": value["location"],
                    "alive": value["alive"],
                    "inventory": list(value["inventory"]),
                }
                for key, value in self.characters.items()
            },
            "items": {
                key: dict(value)
                for key, value in self.items.items()
            },
            "physical_objects": physical,
            "history": [
                {
                    "time": event.time,
                    "actor": event.actor,
                    "action": event.action,
                    "result": event.result,
                    "target": event.target,
                }
                for event in self.history
            ],
        }

    def narrative(self) -> str:
        if not self.history:
            return "Nothing has happened yet."

        return "\n".join(
            f"[{event.time:03d}] {event.actor}: {event.result}"
            for event in self.history
        )

    def close(self) -> None:
        if self.client is not None and p.isConnected(self.client):
            p.disconnect(self.client)


class Agent:
    """An agent may observe and request actions, but cannot mutate World."""

    def __init__(self, world: World, character_id: str):
        self.world = world
        self.character_id = character_id

    def observe(self) -> Dict[str, Any]:
        return self.world.observe(self.character_id)

    def act(
        self,
        action: str,
        target: Optional[str] = None,
        destination: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        return self.world.act(
            self.character_id,
            action,
            target=target,
            destination=destination,
            parameters=parameters,
        )


def self_test() -> None:
    world = World()

    anna = Agent(world, "anna")

    result = anna.act(
        "create_physical",
        target="test_block",
        parameters={
            "mass": 1.0,
            "size": (1.0, 1.0, 1.0),
            "position": (0.0, 0.0, 2.0),
        },
    )

    assert result["ok"]
    assert "test_block" in world.physical_bodies

    state = world.physical_state("test_block")
    assert len(state["position"]) == 3

    result = anna.act(
        "create_physical",
        target="test_block",
    )

    assert not result["ok"]

    result = anna.act(
        "connect_physical",
        target="test_block",
        parameters={"other": "missing"},
    )

    assert not result["ok"]

    world.close()
    print("001-01-01 self_test: OK")


if __name__ == "__main__":
    self_test()
