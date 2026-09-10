```python
"""
STORY NODE 009
==============
THE ROOM IS NO LONGER EMPTY

This is the first node written as real Python rather than as
English sentences mixed directly into Python syntax.

The Python objects describe what exists and what can happen.
The English inside story.observe() describes what those changes mean.

No Blender code is used here. A future Blender importer can read the
world objects and their geometry, transforms, appearance, state, and
relationships.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Small world model
# ---------------------------------------------------------------------------


@dataclass
class WorldObject:
    """A persistent object that exists in the written world."""

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

    def relate_to(self, name: str, target: "WorldObject") -> None:
        self.relationships[name] = target.id


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

    def touch(self, target: WorldObject) -> None:
        self.state["touching"] = target.id


@dataclass
class Link:
    id: str
    source: str
    target: str
    condition: str
    reason: str
    time: float


@dataclass
class World:
    """The persistent state shared by story nodes."""

    time: float = 0.0
    objects: dict[str, WorldObject] = field(default_factory=dict)
    history: list[dict[str, Any]] = field(default_factory=list)

    def add(self, obj: WorldObject) -> WorldObject:
        self.objects[obj.id] = obj
        return obj

    def get(self, object_id: str) -> WorldObject:
        return self.objects[object_id]


class Story:
    """Narrative layer: English adds meaning to world state."""

    def __init__(self, world: World):
        self.world = world
        self.observations: list[str] = []

    def observe(self, text: str) -> None:
        self.observations.append(text)


# ---------------------------------------------------------------------------
# Existing world state entering node 009
# ---------------------------------------------------------------------------

# In the eventual runtime these objects will be loaded from the persistent
# world state created by earlier story nodes. For this node we define the
# objects explicitly so the file is understandable and executable on its own.

world = World(time=20.0)
story = Story(world)

room = world.add(
    Location(
        id="room",
        name="Room",
        properties={"depth": "unknown"},
        state={"entered_again": True},
    )
)

screen = world.add(
    WorldObject(
        id="screen",
        type="screen",
        name="Screen",
        location=room.id,
        geometry={"shape": "rectangle"},
        state={"active": True, "input_available": True},
    )
)

sentence = world.add(
    WorldObject(
        id="sentence",
        type="sentence",
        name="The door was open.",
        location=screen.id,
        properties={
            "text": "The door was open.",
            "meaning": "current",
        },
        state={"alive": True},
    )
)

cursor = world.add(
    WorldObject(
        id="screen_cursor",
        type="cursor",
        name="Cursor",
        location=screen.id,
        geometry={
            "shape": "line",
            "width": 0.02,
            "height": 0.18,
            "depth": 0.001,
        },
        appearance={"material": "light"},
        state={
            "visible": True,
            "blinking": True,
            "active": True,
            "blink_count": 1,
        },
        relationships={
            "screen": screen.id,
            "sentence": sentence.id,
        },
    )
)

boy = world.add(
    Character(
        id="boy",
        name="Boy",
        location=room.id,
        state={"condition": "alert"},
    )
)

reflection = world.add(
    WorldObject(
        id="boy_reflection",
        type="reflection",
        name="Reflection",
        location=room.id,
        appearance={"material": "reflection"},
        state={
            "independent": True,
            "position": "beside_screen",
        },
        relationships={"source": boy.id},
    )
)


# ---------------------------------------------------------------------------
# Node 009
# ---------------------------------------------------------------------------

story.observe(
    "The room was familiar, but it no longer behaved like the room the boy had left."
)

boy.state["condition"] = "watchful"
boy.look_at(reflection)

story.observe(
    "The reflection was no longer an image in the room. It was another presence in it."
)

reflection.state["attention"] = boy.id
reflection.relationships["facing"] = boy.id

world.time += 1.0
world.history.append(
    {
        "time": world.time,
        "event": "boy_and_reflection_faced_each_other",
        "location": room.id,
        "actors": [boy.id, reflection.id],
    }
)

# The cursor is not merely a visual detail. It is an active part of the
# written world because it marks a place where another statement can appear.

cursor.state["blink_count"] += 1
cursor.state["waiting"] = True
screen.state["input_available"] = True

story.observe(
    "The blinking cursor marked an empty place where the next part of the world could be written."
)

# The boy approaches the screen without touching it.
boy.look_at(screen)
boy.state["position"] = "in_front_of_screen"
world.time += 2.0

world.history.append(
    {
        "time": world.time,
        "event": "boy_approached_screen",
        "location": room.id,
        "actors": [boy.id],
        "objects": [screen.id, sentence.id, cursor.id],
    }
)

story.observe(
    "He did not know whether the screen was waiting for him or for the reflection."
)

# The reflection moves first. This is important because its independence is
# now demonstrated by an action rather than only stored as a property.
reflection.state["position"] = "beside_cursor"
reflection.state["attention"] = cursor.id
world.time += 1.0

world.history.append(
    {
        "time": world.time,
        "event": "reflection_approached_cursor",
        "location": room.id,
        "actors": [reflection.id],
        "objects": [screen.id, cursor.id],
    }
)

story.observe(
    "The reflection reached toward the empty line, while the boy remained still."
)

# The reflection does not need a physical keyboard to interact with the
# written world. For now it creates an intention rather than text.
reflection.state["intention"] = "write"
reflection.relationships["intends_to"] = screen.id

world.time += 1.0
world.history.append(
    {
        "time": world.time,
        "event": "reflection_intended_to_write",
        "location": room.id,
        "actors": [reflection.id],
        "objects": [screen.id, cursor.id],
    }
)

story.observe(
    "For the first time, the boy understood that the next sentence might not belong to him."
)

boy.state["understanding"] = "the_reflection_can_change_the_story"

# The current sentence remains alive. It is not replaced by the new event.
# This keeps the earlier story as persistent world state.
sentence.state["alive"] = True
screen.state["input_available"] = True

next_scene = Link(
    id="room_to_010",
    source=room.id,
    target="010.py",
    condition="the reflection intends to write",
    reason="The reflection is ready to produce the next change in the written world.",
    time=world.time,
)

world.history.append(
    {
        "time": world.time,
        "event": "node_009_completed",
        "location": room.id,
        "actors": [boy.id, reflection.id],
        "objects": [screen.id, sentence.id, cursor.id],
        "links": [next_scene.id],
    }
)


# ---------------------------------------------------------------------------
# Continuity
# ---------------------------------------------------------------------------

CONTINUITY = {
    "persistent_objects": [
        "boy",
        "room",
        "screen",
        "sentence",
        "cursor",
        "boy_reflection",
    ],
    "world_changes": [
        "the reflection is an independent presence inside the room",
        "the cursor remains an active input point",
        "the sentence remains alive and current",
        "the reflection now intends to write",
        "the boy understands that the next sentence may come from the reflection",
    ],
    "next_node": "010.py",
}
```
