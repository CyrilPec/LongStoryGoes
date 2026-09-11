"""
000-01.py — The World

The World is created once.

Everything that happens later exists inside this World.
Story files do not create a new world.
They continue the existing one.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class World:
    """
    The persistent conceptual world.

    The World contains:
    - entities
    - places
    - objects
    - relationships
    - events
    - time
    - state

    A story is an observation/change of this world,
    not a replacement for it.
    """

    time: float = 0.0

    entities: dict[str, Any] = field(default_factory=dict)
    places: dict[str, Any] = field(default_factory=dict)
    objects: dict[str, Any] = field(default_factory=dict)

    relationships: list[dict[str, Any]] = field(default_factory=list)
    history: list[dict[str, Any]] = field(default_factory=list)

    def add_entity(self, entity_id: str, entity: Any):
        self.entities[entity_id] = entity
        return entity

    def add_place(self, place_id: str, place: Any):
        self.places[place_id] = place
        return place

    def add_object(self, object_id: str, obj: Any):
        self.objects[object_id] = obj
        return obj

    def get(self, entity_id: str):
        if entity_id in self.entities:
            return self.entities[entity_id]

        if entity_id in self.places:
            return self.places[entity_id]

        if entity_id in self.objects:
            return self.objects[entity_id]

        raise KeyError(f"Unknown world entity: {entity_id}")

    def record(self, event: dict[str, Any]):
        self.history.append(event)

    def advance(self, amount: float):
        self.time += amount
