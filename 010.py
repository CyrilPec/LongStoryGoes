```python
"""
STORY NODE 010
==============
THE GIRL ON THE PLAYGROUND

A new place and a new character.
The story does not need to explain the connection immediately.
The world can contain places that are not yet connected by a visible path.

Python defines the playground, the girl, the objects, actions, and changes.
English inside story.observe() gives those changes meaning.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class WorldObject:
    """A persistent object in the world."""

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

    def sit_on(self, target: WorldObject) -> None:
        self.state["sitting_on"] = target.id


@dataclass
class World:
    time: float = 0.0
    objects: dict[str, WorldObject] = field(default_factory=dict)
    history: list[dict[str, Any]] = field(default_factory=list)

    def add(self, obj: WorldObject) -> WorldObject:
        self.objects[obj.id] = obj
        return obj


class Story:
    def __init__(self, world: World):
        self.world = world
        self.observations: list[str] = []

    def observe(self, text: str) -> None:
        self.observations.append(text)


# ---------------------------------------------------------------------------
# The playground
# ---------------------------------------------------------------------------

world = World(time=0.0)
story = Story(world)

playground = world.add(
    Location(
        id="playground",
        name="Playground",
        geometry={
            "shape": "open_area",
            "ground": "sand",
        },
        properties={
            "public": True,
            "open_sky": True,
        },
        state={"quiet": True},
    )
)

swing = world.add(
    WorldObject(
        id="playground_swing",
        type="swing",
        name="Swing",
        location=playground.id,
        geometry={
            "shape": "swing",
            "seat_height": 1.0,
        },
        state={
            "occupied": False,
            "moving": False,
        },
    )
)

ball = world.add(
    WorldObject(
        id="red_ball",
        type="ball",
        name="Red Ball",
        location=playground.id,
        geometry={
            "shape": "sphere",
            "radius": 0.12,
        },
        appearance={
            "material": "rubber",
        },
        state={
            "moving": False,
        },
    )
)

girl = world.add(
    Character(
        id="girl",
        name="Girl",
        location=playground.id,
        state={
            "condition": "curious",
            "alone": True,
        },
    )
)


# ---------------------------------------------------------------------------
# Node 010
# ---------------------------------------------------------------------------

story.observe(
    "The playground was almost empty. A girl sat on the swing, "
    "listening to the wind move through the trees."
)

girl.sit_on(swing)

swing.state["occupied"] = True
swing.state["moving"] = True
swing.state["motion"] = "slow"

world.time += 1.0

world.history.append(
    {
        "time": world.time,
        "event": "girl_swinging",
        "location": playground.id,
        "actors": [girl.id],
        "objects": [swing.id],
    }
)


story.observe(
    "Then she noticed a red ball lying in the sand "
    "where she was certain there had been nothing before."
)

girl.look_at(ball)
girl.state["curious"] = True

world.time += 1.0

ball.state["moving"] = True
ball.state["motion"] = "one_small_roll"
ball.state["direction"] = "toward_girl"

world.history.append(
    {
        "time": world.time,
        "event": "ball_rolled",
        "location": playground.id,
        "objects": [ball.id],
        "target": girl.id,
    }
)


story.observe(
    "The ball rolled across the sand and stopped exactly beneath the swing."
)

ball.state["moving"] = False
ball.state["position"] = "beneath_swing"


# The girl reaches down, but does not pick it up yet.

girl.state["position"] = "leaning_down"
girl.state["reaching_for"] = ball.id

world.time += 1.0

story.observe(
    "She reached for it. Before her fingers touched the ball, "
    "she heard someone say her name."
)

girl.state["heard_voice"] = True
girl.state["heard_name"] = True

world.history.append(
    {
        "time": world.time,
        "event": "girl_heard_unknown_voice",
        "location": playground.id,
        "actors": [girl.id],
        "objects": [ball.id],
        "knowledge_added": "someone_here_knows_the_girls_name",
    }
)


story.observe(
    "She stopped moving. There was still nobody else on the playground."
)

girl.state["condition"] = "alert"
girl.state["looking_for_source"] = True

world.time += 1.0


story.observe(
    "The swing continued to move, although the girl was no longer pushing it."
)

swing.state["motion"] = "continuing_without_push"
swing.state["moving"] = True

world.history.append(
    {
        "time": world.time,
        "event": "swing_continued_alone",
        "location": playground.id,
        "object": swing.id,
        "cause": "unknown",
    }
)


# ---------------------------------------------------------------------------
# Continuity
# ---------------------------------------------------------------------------

CONTINUITY = {
    "persistent_objects": [
        "playground",
        "playground_swing",
        "red_ball",
        "girl",
    ],
    "world_changes": [
        "the girl discovers the red ball",
        "the ball rolled toward the girl without an identified cause",
        "the girl heard an unknown voice say her name",
        "the girl cannot see anyone else on the playground",
        "the swing continues moving without the girl pushing it",
    ],
    "next_node": None,
}
```
