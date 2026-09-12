"""
000-01-01.py — Authoritative Physical World
Evolution of 000-01.py.
The original World concept remains unchanged.
This version adds an experimental physical simulation layer.
The World is authoritative: experiments and agents can request actions,
but only the World can validate and change physical state.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
import math
import numpy as np
import pybullet as p


@dataclass
class PhysicalMaterial:
    id: str
    density: float
    hardness: float
    stiffness: float
    strength: float


@dataclass
class PhysicalBody:
    id: str
    body_id: int
    mass: float
    size: Tuple[float, float, float]
    position: Tuple[float, float, float]
    material: str
    dynamic: bool = True


@dataclass
class PhysicalConnection:
    id: str
    first: str
    second: str
    type: str
    strength: float
    penetration: float
    created_at: int


@dataclass(frozen=True)
class PhysicalEvent:
    time: int
    actor: str
    action: str
    result: str
    target: Optional[str] = None


class World:
    """
    The authoritative physical World.

    External code must request physical changes through act().
    """

    def __init__(self, physics: bool = True) -> None:
        self.time: int = 0
        self.locations: Dict[str, Dict[str, Any]] = {}
        self.characters: Dict[str, Dict[str, Any]] = {}
        self.items: Dict[str, Dict[str, Any]] = {}
        self.history: List[PhysicalEvent] = []
        self.materials: Dict[str, PhysicalMaterial] = {}
        self.physical_bodies: Dict[str, PhysicalBody] = {}
        self.connections: Dict[str, PhysicalConnection] = {}
        self.physics_enabled = physics
        self.client: Optional[int] = None
        self._build_world()
        self._build_materials()
        if physics:
            self._start_physics()

    def _build_world(self) -> None:
        self.locations = {
            "village": {
                "id": "village",
                "name": "Old Village",
                "description": "A small village beside a dark forest.",
                "exits": {
                    "forest": "forest",
                    "house": "house",
                },
            },
            "forest": {
                "id": "forest",
                "name": "Forest",
                "description": "A quiet forest. The trees are old and dense.",
                "exits": {
                    "village": "village",
                },
            },
            "house": {
                "id": "house",
                "name": "Miller's House",
                "description": "A small wooden house.",
                "exits": {
                    "village": "village",
                },
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

    def _build_materials(self) -> None:
        self.materials["wood"] = PhysicalMaterial(
            id="wood",
            density=600.0,
            hardness=3.0,
            stiffness=10.0,
            strength=40.0,
        )

        self.materials["steel"] = PhysicalMaterial(
            id="steel",
            density=7850.0,
            hardness=6.0,
            stiffness=200.0,
            strength=400.0,
        )

    def _start_physics(self) -> None:
        self.client = p.connect(p.DIRECT)
        p.setGravity(
            0.0,
            0.0,
            -9.81,
            physicsClientId=self.client,
        )
        self._create_ground()

    def _create_ground(self) -> None:
        if self.client is None:
            return

        shape = p.createCollisionShape(
            p.GEOM_BOX,
            halfExtents=[10.0, 10.0, 0.05],
            physicsClientId=self.client,
        )

        p.createMultiBody(
            baseMass=0.0,
            baseCollisionShapeIndex=shape,
            basePosition=[0.0, 0.0, -0.05],
            physicsClientId=self.client,
        )

    def add_material(
        self,
        material_id: str,
        density: float,
        hardness: float,
        stiffness: float,
        strength: float,
    ) -> None:
        if density <= 0:
            raise ValueError("Density must be positive.")
        if hardness <= 0:
            raise ValueError("Hardness must be positive.")
        if stiffness <= 0:
            raise ValueError("Stiffness must be positive.")
        if strength <= 0:
            raise ValueError("Strength must be positive.")

        self.materials[material_id] = PhysicalMaterial(
            id=material_id,
            density=density,
            hardness=hardness,
            stiffness=stiffness,
            strength=strength,
        )

    def add_physical_object(
        self,
        object_id: str,
        mass: float,
        size: Tuple[float, float, float],
        position: Tuple[float, float, float],
        material: str,
        dynamic: bool = True,
    ) -> Dict[str, Any]:
        if not self.physics_enabled or self.client is None:
            return {
                "ok": False,
                "error": "Physics is disabled.",
            }

        if object_id in self.physical_bodies:
            return {
                "ok": False,
                "error": "Physical object already exists.",
            }

        if material not in self.materials:
            return {
                "ok": False,
                "error": f"Unknown material: {material}.",
            }

        if mass <= 0:
            return {
                "ok": False,
                "error": "Mass must be positive.",
            }

        if len(size) != 3 or any(value <= 0 for value in size):
            return {
                "ok": False,
                "error": "All dimensions must be positive.",
            }

        half_extents = np.asarray(size, dtype=float) / 2.0

        shape = p.createCollisionShape(
            p.GEOM_BOX,
            halfExtents=half_extents.tolist(),
            physicsClientId=self.client,
        )

        body_id = p.createMultiBody(
            baseMass=mass if dynamic else 0.0,
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
            material=material,
            dynamic=dynamic,
        )

        return {
            "ok": True,
            "object": object_id,
            "body_id": body_id,
            "material": material,
            "mass": mass,
        }

    def physical_state(self, object_id: str) -> Dict[str, Any]:
        body = self._physical_body(object_id)

        if self.client is None:
            raise RuntimeError("Physics is not connected.")

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
            "material": body.material,
            "mass": body.mass,
        }

    def distance(self, first: str, second: str) -> float:
        first_position = np.asarray(
            self.physical_state(first)["position"],
            dtype=float,
        )
        second_position = np.asarray(
            self.physical_state(second)["position"],
            dtype=float,
        )

        return float(np.linalg.norm(first_position - second_position))

    def density_from_mass_and_size(
        self,
        mass: float,
        size: Tuple[float, float, float],
    ) -> float:
        volume = float(np.prod(np.asarray(size, dtype=float)))

        if volume <= 0:
            raise ValueError("Volume must be positive.")

        return mass / volume

    def tick(self, minutes: int = 1) -> None:
        if minutes < 0:
            raise ValueError("Time cannot move backwards.")

        for _ in range(minutes):
            self.time += 1

            if self.physics_enabled and self.client is not None:
                for _ in range(60):
                    p.stepSimulation(
                        physicsClientId=self.client,
                    )

    def observe(self, character_id: str) -> Dict[str, Any]:
        character = self._character(character_id)
        location = self.locations[character["location"]]

        visible_characters = [
            {
                "id": character_data["id"],
                "name": character_data["name"],
                "alive": character_data["alive"],
            }
            for character_data in self.characters.values()
            if character_data["location"] == character["location"]
            and character_data["id"] != character_id
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

        physical_objects = {
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
            "physical_objects": physical_objects,
            "connections": {
                connection_id: {
                    "first": connection.first,
                    "second": connection.second,
                    "type": connection.type,
                    "strength": connection.strength,
                    "penetration": connection.penetration,
                }
                for connection_id, connection in self.connections.items()
            },
        }

    def act(
        self,
        actor_id: str,
        action: str,
        target: Optional[str] = None,
        destination: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        actor = self._character(actor_id)

        if not actor["alive"]:
            return self._reject(
                actor_id,
                action,
                "Actor is dead.",
            )

        parameters = parameters or {}

        if action == "wait":
            self.tick(1)
            return self._accept(
                actor_id,
                action,
                "Time advanced by one minute.",
            )

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
            return self._create_physical(
                actor_id,
                target,
                parameters,
            )

        if action == "fastener":
            return self._fastener(
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

        return self._reject(
            actor_id,
            action,
            "Unknown action.",
        )

    def _create_physical(
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

        required = (
            "mass",
            "size",
            "position",
            "material",
        )

        for key in required:
            if key not in parameters:
                return self._reject(
                    actor_id,
                    "create_physical",
                    f"Missing parameter: {key}.",
                )

        result = self.add_physical_object(
            object_id=target,
            mass=float(parameters["mass"]),
            size=tuple(parameters["size"]),
            position=tuple(parameters["position"]),
            material=str(parameters["material"]),
        )

        if not result["ok"]:
            return self._reject(
                actor_id,
                "create_physical",
                result["error"],
            )

        self.tick(1)

        return self._accept(
            actor_id,
            "create_physical",
            f"Created physical object {target}.",
            target,
        )

    def _fastener(
        self,
        actor_id: str,
        target: Optional[str],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        if target is None:
            return self._reject(
                actor_id,
                "fastener",
                "No fastener supplied.",
            )

        other = parameters.get("other")

        if other is None:
            return self._reject(
                actor_id,
                "fastener",
                "No target object supplied.",
            )

        if target not in self.physical_bodies:
            return self._reject(
                actor_id,
                "fastener",
                "Fastener does not exist.",
            )

        if other not in self.physical_bodies:
            return self._reject(
                actor_id,
                "fastener",
                "Target object does not exist.",
            )

        fastener_body = self.physical_bodies[target]
        target_body = self.physical_bodies[other]

        fastener_material = self.materials[fastener_body.material]
        target_material = self.materials[target_body.material]

        distance = self.distance(target, other)

        contact_limit = float(
            parameters.get("contact_limit", 0.10)
        )

        if distance > contact_limit:
            return self._reject(
                actor_id,
                "fastener",
                f"Fastener is not in contact with target. "
                f"Distance={distance:.5f} m.",
            )

        hammer = parameters.get("hammer")

        if hammer is None:
            return self._reject(
                actor_id,
                "fastener",
                "A hammer impact is required.",
            )

        hammer_mass = float(
            hammer.get("mass", 0.0)
        )

        impact_velocity = float(
            hammer.get("impact_velocity", 0.0)
        )

        impact_factor = float(
            hammer.get("impact_factor", 1.0)
        )

        if hammer_mass <= 0:
            return self._reject(
                actor_id,
                "fastener",
                "Hammer mass must be positive.",
            )

        if impact_velocity <= 0:
            return self._reject(
                actor_id,
                "fastener",
                "Hammer impact velocity must be positive.",
            )

        impact_energy = (
            0.5
            * hammer_mass
            * impact_velocity
            * impact_velocity
            * impact_factor
        )

        tip_diameter = min(
            fastener_body.size[0],
            fastener_body.size[1],
        )

        tip_area = (
            math.pi
            * (tip_diameter / 2.0) ** 2
        )

        pressure = (
            impact_energy
            / max(tip_area, 1e-12)
        )

        hardness_ratio = (
            fastener_material.hardness
            / max(
                target_material.hardness,
                1e-12,
            )
        )

        strength_threshold = (
            target_material.strength
            * 1_000_000.0
        )

        penetration_score = (
            pressure
            / max(
                strength_threshold,
                1.0,
            )
        ) * hardness_ratio

        penetration = min(
            fastener_body.size[2],
            max(
                0.0,
                penetration_score
                * fastener_body.size[2],
            ),
        )

        minimum_penetration = (
            fastener_body.size[2] * 0.10
        )

        if penetration < minimum_penetration:
            return self._reject(
                actor_id,
                "fastener",
                "Impact was insufficient to create "
                "a meaningful penetration.",
            )

        connection_strength = (
            target_material.strength
            * penetration
            * tip_diameter
            * hardness_ratio
        )

        connection_id = (
            f"{target}_{other}_"
            f"{len(self.connections) + 1}"
        )

        self.connections[connection_id] = PhysicalConnection(
            id=connection_id,
            first=target,
            second=other,
            type="fastener",
            strength=connection_strength,
            penetration=penetration,
            created_at=self.time,
        )

        self.tick(1)

        return self._accept(
            actor_id,
            "fastener",
            f"Fastener penetrated approximately "
            f"{penetration:.6f} m and formed "
            f"connection {connection_id}.",
            target,
        )

    def _move(
        self,
        actor: Dict[str, Any],
        destination: Optional[str],
    ) -> Dict[str, Any]:
        if destination is None:
            return self._reject(
                actor["id"],
                "move",
                "No destination supplied.",
            )

        current = self.locations[actor["location"]]

        if destination not in current["exits"]:
            return self._reject(
                actor["id"],
                "move",
                f"{current['name']} has no exit "
                f"to {destination}.",
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
            f"{actor['name']} moved from "
            f"{old_location} to {destination_id}.",
        )

    def _take(
        self,
        actor: Dict[str, Any],
        target: Optional[str],
    ) -> Dict[str, Any]:
        if target is None:
            return self._reject(
                actor["id"],
                "take",
                "No item supplied.",
            )

        item = self.items.get(target)

        if item is None or not item["exists"]:
            return self._reject(
                actor["id"],
                "take",
                "Item does not exist.",
            )

        if item["owner"] is not None:
            return self._reject(
                actor["id"],
                "take",
                "Item is already owned.",
            )

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
            return self._reject(
                actor["id"],
                "drop",
                "No item supplied.",
            )

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
            return self._reject(
                actor["id"],
                "ring",
                "Only the village bell can ring.",
            )

        if actor["location"] != "village":
            return self._reject(
                actor["id"],
                "ring",
                "The bell is not here.",
            )

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

        return {
            "ok": False,
            "time": self.time,
            "action": action,
            "error": reason,
        }

    def _character(
        self,
        character_id: str,
    ) -> Dict[str, Any]:
        if character_id not in self.characters:
            raise KeyError(
                f"Unknown character: {character_id}"
            )

        return self.characters[character_id]

    def _physical_body(
        self,
        object_id: str,
    ) -> PhysicalBody:
        if object_id not in self.physical_bodies:
            raise KeyError(
                f"Unknown physical object: {object_id}"
            )

        return self.physical_bodies[object_id]

    def state(self) -> Dict[str, Any]:
        physical_objects = {
            object_id: self.physical_state(object_id)
            for object_id in self.physical_bodies
        }

        return {
            "time": self.time,
            "characters": {
                character_id: {
                    "name": character["name"],
                    "location": character["location"],
                    "alive": character["alive"],
                    "inventory": list(character["inventory"]),
                }
                for character_id, character in self.characters.items()
            },
            "items": {
                item_id: dict(item)
                for item_id, item in self.items.items()
            },
            "physical_objects": physical_objects,
            "connections": {
                connection_id: {
                    "first": connection.first,
                    "second": connection.second,
                    "type": connection.type,
                    "strength": connection.strength,
                    "penetration": connection.penetration,
                    "created_at": connection.created_at,
                }
                for connection_id, connection in self.connections.items()
            },
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
            f"[{event.time:03d}] "
            f"{event.actor}: {event.result}"
            for event in self.history
        )

    def close(self) -> None:
        if (
            self.client is not None
            and p.isConnected(self.client)
        ):
            p.disconnect(self.client)


class Agent:
    """
    Minimal interface for an AI-controlled character.

    The Agent can observe and request actions.
    The Agent cannot directly mutate World state.
    """

    def __init__(
        self,
        world: World,
        character_id: str,
    ) -> None:
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

    try:
        anna = Agent(world, "anna")

        plank = world.act(
            "anna",
            "create_physical",
            target="plank_test",
            parameters={
                "mass": 1.0,
                "size": (2.0, 0.2, 0.2),
                "position": (0.0, 0.0, 1.0),
                "material": "wood",
            },
        )

        assert plank["ok"]

        nail = world.act(
            "anna",
            "create_physical",
            target="nail_test",
            parameters={
                "mass": 0.001,
                "size": (0.004, 0.004, 0.08),
                "position": (0.0, 0.0, 1.11),
                "material": "steel",
            },
        )

        assert nail["ok"]

        result = anna.act(
            "fastener",
            target="nail_test",
            parameters={
                "other": "plank_test",
                "hammer": {
                    "mass": 1.0,
                    "impact_velocity": 5.0,
                    "impact_factor": 1.0,
                },
            },
        )

        assert result["ok"]
        assert len(world.connections) == 1

        print("000-01-01 self_test: OK")
    finally:
        world.close()


if __name__ == "__main__":
    self_test()
