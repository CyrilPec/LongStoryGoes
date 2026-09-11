"""
STORY NODE 019
==============

THE BRIDGE

This node continues the LongStoryGoes experiment:

    Python defines the persistent world.
    English describes what the world means.
    History records what happened.
    Blender visualises the world.

The important experiment here is continuity.

Three characters exist in the same world:

    Anna
    Boris
    Mira

The story describes a bridge between the village and the forest.

Mira changes the bridge.

Anna later encounters the changed world.

The bridge does not return to its original state simply because
Anna was not present when the change happened.

The same Python world can be read by a human, interpreted by a PC,
and visualised by v1_importer.py.

No bpy is used here.
"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# World model
# ---------------------------------------------------------------------------


@dataclass
class WorldObject:
    """
    Persistent object in the LongStoryGoes world.

    This follows the object model already used by 010.py and consumed
    by v1_importer.py.
    """

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


@dataclass
class World:
    """
    The persistent world represented by this story node.
    """

    time: float = 0.0

    objects: dict[str, WorldObject] = field(default_factory=dict)

    history: list[dict[str, Any]] = field(default_factory=list)

    def add(self, obj: WorldObject) -> WorldObject:
        self.objects[obj.id] = obj
        return obj


class Story:
    """
    Human-readable narrative attached to the world.

    The observations are deliberately plain English.

    A future PC can consume the same observations that a human reads.
    """

    def __init__(self, world: World):
        self.world = world
        self.observations: list[str] = []

    def observe(self, text: str) -> None:
        self.observations.append(text)


# ---------------------------------------------------------------------------
# Create world
# ---------------------------------------------------------------------------


world = World(time=0.0)

story = Story(world)


# ---------------------------------------------------------------------------
# Places
# ---------------------------------------------------------------------------


village = world.add(
    Location(
        id="village",
        name="Village",
        geometry={
            "shape": "open_area",
            "ground": "grass",
        },
        transform={
            "position": (0.0, 0.0, 0.0),
            "scale": (1.0, 1.0, 1.0),
        },
        properties={
            "public": True,
            "open_sky": True,
        },
        state={
            "time_of_day": "morning",
        },
    )
)


forest = world.add(
    Location(
        id="forest",
        name="Forest",
        geometry={
            "shape": "open_area",
            "ground": "grass",
        },
        transform={
            "position": (12.0, 0.0, 0.0),
            "scale": (1.2, 1.2, 1.0),
        },
        properties={
            "public": True,
            "open_sky": True,
        },
        state={
            "quiet": True,
        },
    )
)


river = world.add(
    Location(
        id="river",
        name="River",
        geometry={
            "shape": "plane",
        },
        transform={
            "position": (6.0, 0.0, -0.05),
            "scale": (1.0, 0.35, 1.0),
        },
        properties={
            "water": True,
        },
        state={
            "flow": "slow",
        },
    )
)


# ---------------------------------------------------------------------------
# The bridge
# ---------------------------------------------------------------------------


bridge = world.add(
    WorldObject(
        id="old_bridge",
        type="bridge",
        name="Old Wooden Bridge",
        location="river",
        geometry={
            "shape": "box",
            "size": (5.0, 1.5, 0.35),
        },
        transform={
            "position": (6.0, 0.0, 0.35),
            "rotation": (0.0, 0.0, 0.0),
            "scale": (1.0, 1.0, 1.0),
        },
        appearance={
            "material": "old_wood",
        },
        properties={
            "connects": ["village", "forest"],
            "destructible": True,
            "old": True,
        },
        state={
            "condition": "broken",
            "passable": False,
            "supports_people": False,
        },
        relationships={
            "crosses": river.id,
            "leads_to": forest.id,
            "leads_from": village.id,
        },
    )
)


# ---------------------------------------------------------------------------
# Characters
# ---------------------------------------------------------------------------


anna = world.add(
    Character(
        id="anna",
        name="Anna",
        location=village.id,
        geometry={
            "shape": "character",
        },
        transform={
            "position": (-2.0, 0.0, 0.0),
        },
        state={
            "condition": "calm",
            "knows_bridge": True,
            "knows_bridge_broken": True,
        },
        relationships={
            "lives_in": village.id,
        },
    )
)


boris = world.add(
    Character(
        id="boris",
        name="Boris",
        location=village.id,
        geometry={
            "shape": "character",
        },
        transform={
            "position": (-1.0, 1.5, 0.0),
        },
        state={
            "condition": "working",
        },
        relationships={
            "lives_in": village.id,
        },
    )
)


mira = world.add(
    Character(
        id="mira",
        name="Mira",
        location=forest.id,
        geometry={
            "shape": "character",
        },
        transform={
            "position": (11.0, 0.0, 0.0),
        },
        state={
            "condition": "tired",
        },
        relationships={
            "came_from": forest.id,
        },
    )
)


# ---------------------------------------------------------------------------
# Objects
# ---------------------------------------------------------------------------


lamp = world.add(
    WorldObject(
        id="oil_lamp",
        type="lamp",
        name="Oil Lamp",
        location=anna.id,
        geometry={
            "shape": "cylinder",
            "radius": 0.18,
            "depth": 0.35,
        },
        transform={
            "position": (-2.0, -0.4, 0.8),
        },
        appearance={
            "material": "brass",
        },
        state={
            "lit": False,
        },
        relationships={
            "held_by": anna.id,
        },
    )
)


axe = world.add(
    WorldObject(
        id="old_axe",
        type="axe",
        name="Old Axe",
        location=mira.id,
        geometry={
            "shape": "box",
            "size": (0.12, 0.12, 1.2),
        },
        transform={
            "position": (11.4, 0.0, 0.7),
        },
        appearance={
            "material": "wood_and_iron",
        },
        state={
            "condition": "usable",
        },
        relationships={
            "held_by": mira.id,
        },
    )
)


# ---------------------------------------------------------------------------
# Node 019 — the actual story
# ---------------------------------------------------------------------------


story.observe(
    "Morning had reached the village when Anna walked toward the river."
)


story.observe(
    "The old wooden bridge had once connected the village with the forest."
)


story.observe(
    "Now the bridge was broken."
)


bridge.state["condition"] = "broken"
bridge.state["passable"] = False


world.time += 1.0


world.history.append(
    {
        "time": world.time,
        "event": "bridge_already_broken",
        "location": bridge.id,
        "objects": [
            bridge.id,
        ],
        "cause": "previous_story",
        "irreversible": True,
    }
)


story.observe(
    "Mira had broken it earlier in the morning."
)


world.time += 1.0


world.history.append(
    {
        "time": world.time,
        "event": "mira_broke_bridge",
        "location": bridge.id,
        "actors": [
            mira.id,
        ],
        "objects": [
            axe.id,
            bridge.id,
        ],
        "cause": "Mira used the old axe.",
        "irreversible": True,
    }
)


story.observe(
    "Mira had not intended to destroy the only crossing, "
    "but the old wood could no longer support its own weight."
)


bridge.state["condition"] = "collapsed"
bridge.state["passable"] = False
bridge.state["supports_people"] = False


world.time += 1.0


story.observe(
    "A section of the bridge had fallen into the river."
)


world.history.append(
    {
        "time": world.time,
        "event": "bridge_collapsed",
        "location": bridge.id,
        "objects": [
            bridge.id,
            river.id,
        ],
        "irreversible": True,
    }
)


# ---------------------------------------------------------------------------
# Anna observes the changed world
# ---------------------------------------------------------------------------


anna.state["looking_at"] = bridge.id


story.observe(
    "Anna stopped at the river and looked at the broken bridge."
)


story.observe(
    "She could see that there was no safe way to cross."
)


world.time += 1.0


world.history.append(
    {
        "time": world.time,
        "event": "anna_observed_bridge",
        "location": village.id,
        "actors": [
            anna.id,
        ],
        "objects": [
            bridge.id,
        ],
    }
)


# ---------------------------------------------------------------------------
# The world continues without the player
# ---------------------------------------------------------------------------


story.observe(
    "Boris remained in the village."
)


boris.state["condition"] = "working"


world.time += 1.0


world.history.append(
    {
        "time": world.time,
        "event": "boris_continued_working",
        "location": village.id,
        "actors": [
            boris.id,
        ],
    }
)


# ---------------------------------------------------------------------------
# Continuity
# ---------------------------------------------------------------------------
#
# This section is deliberately explicit.
#
# It tells a future node what must remain true.
# ---------------------------------------------------------------------------


CONTINUITY = {
    "persistent_objects": [
        village.id,
        forest.id,
        river.id,
        bridge.id,
        anna.id,
        boris.id,
        mira.id,
        lamp.id,
        axe.id,
    ],

    "world_changes": [
        "the old bridge is broken",
        "the bridge is no longer passable",
        "a section of the bridge collapsed into the river",
        "Anna knows that the bridge is broken",
        "Mira caused the bridge to break",
    ],

    "irreversible_events": [
        "mira_broke_bridge",
        "bridge_collapsed",
    ],

    "characters": {
        anna.id: {
            "location": anna.location,
            "knows": [
                "the bridge is broken",
            ],
        },

        boris.id: {
            "location": boris.location,
        },

        mira.id: {
            "location": mira.location,
            "caused": [
                "mira_broke_bridge",
            ],
        },
    },

    "objects": {
        bridge.id: {
            "state": bridge.state.copy(),
        },

        lamp.id: {
            "location": lamp.location,
            "state": lamp.state.copy(),
        },

        axe.id: {
            "location": axe.location,
            "state": axe.state.copy(),
        },
    },

    "next_node": None,
}


# ---------------------------------------------------------------------------
# Optional consistency check
# ---------------------------------------------------------------------------
#
# This can be run directly with:
#
#     python 019.py
#
# It is not required by the Blender importer.
# ---------------------------------------------------------------------------


def check_continuity() -> None:
    """
    Verify the facts that this story node promises to preserve.
    """

    assert bridge.state["condition"] == "collapsed"
    assert bridge.state["passable"] is False

    assert lamp.location == anna.id
    assert axe.location == mira.id

    assert anna.location == village.id
    assert boris.location == village.id
    assert mira.location == forest.id

    assert any(
        event["event"] == "mira_broke_bridge"
        for event in world.history
    )

    assert any(
        event["event"] == "bridge_collapsed"
        for event in world.history
    )


if __name__ == "__main__":
    check_continuity()

    print("LongStoryGoes story node 019")
    print("--------------------------------")
    print()

    for observation in story.observations:
        print(observation)

    print()
    print("World time:", world.time)
    print("Objects:", len(world.objects))
    print("History events:", len(world.history))
    print("Continuity check: OK")
