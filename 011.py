```python
"""
STORY NODE 012
==============
THE WARM CUP

The world is being researched.

Not by a laboratory with white walls and serious people,
but by a small kitchen where the important scientific equipment
includes a kettle, a spoon, a lemon, a cup of tea, and one very
curious cat.

The world does not explain its rules immediately.

It lets them be discovered.

Physics is something that happens.
Chemistry is something that changes.
English is what makes the experiment interesting.

The cat has arrived before anyone invited it.
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
class Character(WorldObject):
    type: str = "character"

    def move_to(self, location: WorldObject) -> None:
        self.location = location.id

    def look_at(self, target: WorldObject) -> None:
        self.state["looking_at"] = target.id


@dataclass
class Animal(Character):
    type: str = "animal"


@dataclass
class World:
    """The persistent state of the world."""

    time: float = 0.0
    objects: dict[str, WorldObject] = field(default_factory=dict)
    history: list[dict[str, Any]] = field(default_factory=list)

    def add(self, obj: WorldObject) -> WorldObject:
        self.objects[obj.id] = obj
        return obj


class Story:
    """English gives meaning to changes in the world."""

    def __init__(self, world: World):
        self.world = world
        self.observations: list[str] = []

    def observe(self, text: str) -> None:
        self.observations.append(text)


# ---------------------------------------------------------------------------
# THE KITCHEN
# ---------------------------------------------------------------------------

world = World(time=10.0)
story = Story(world)

kitchen = world.add(
    WorldObject(
        id="kitchen",
        type="location",
        name="Kitchen",
        geometry={
            "shape": "room",
            "width": 4.0,
            "length": 5.0,
            "height": 2.7,
        },
        properties={
            "warm": True,
            "dry": True,
            "has_water": True,
        },
        state={
            "quiet": True,
            "window_open": True,
        },
    )
)


table = world.add(
    WorldObject(
        id="kitchen_table",
        type="table",
        name="Kitchen Table",
        location=kitchen.id,
        geometry={
            "shape": "box",
            "width": 1.2,
            "length": 2.0,
            "height": 0.75,
        },
        appearance={
            "material": "wood",
        },
        state={
            "stable": True,
        },
    )
)


kettle = world.add(
    WorldObject(
        id="kettle",
        type="kettle",
        name="Kettle",
        location=kitchen.id,
        geometry={
            "shape": "kettle",
            "capacity_liters": 1.5,
        },
        state={
            "empty": False,
            "water_temperature_c": 22.0,
            "heating": False,
            "boiling": False,
        },
    )
)


cup = world.add(
    WorldObject(
        id="blue_cup",
        type="cup",
        name="Blue Cup",
        location=kitchen.id,
        geometry={
            "shape": "cylinder",
            "radius": 0.04,
            "height": 0.10,
        },
        appearance={
            "material": "ceramic",
            "color": "blue",
        },
        state={
            "empty": True,
            "temperature_c": 22.0,
        },
    )
)


water = world.add(
    WorldObject(
        id="water",
        type="liquid",
        name="Water",
        location=kettle.id,
        properties={
            "chemical_formula": "H2O",
            "phase": "liquid",
            "volume_liters": 0.4,
        },
        state={
            "temperature_c": 22.0,
        },
    )
)


tea = world.add(
    WorldObject(
        id="tea",
        type="substance",
        name="Tea",
        location=kitchen.id,
        properties={
            "soluble_in": "water",
            "origin": "tea_leaves",
        },
        state={
            "dry": True,
            "dissolved": False,
        },
    )
)


lemon = world.add(
    WorldObject(
        id="lemon",
        type="fruit",
        name="Lemon",
        location=kitchen.id,
        properties={
            "contains": ["water", "citric_acid"],
        },
        state={
            "whole": True,
            "cut": False,
        },
    )
)


spoon = world.add(
    WorldObject(
        id="spoon",
        type="utensil",
        name="Spoon",
        location=kitchen.id,
        geometry={
            "shape": "spoon",
        },
        appearance={
            "material": "metal",
        },
        state={
            "temperature_c": 22.0,
        },
    )
)


cat = world.add(
    Animal(
        id="street_cat",
        name="Cat",
        location=kitchen.id,
        appearance={
            "fur": "dark",
        },
        state={
            "condition": "curious",
            "hungry": True,
            "wet": False,
        },
        relationships={
            "previous_location": "street",
        },
    )
)


# ---------------------------------------------------------------------------
# OBSERVATION 1
# ---------------------------------------------------------------------------

story.observe(
    "The kitchen was warm and quiet, except for the kettle making "
    "the small impatient noises of water that had not yet decided "
    "whether to boil."
)

kettle.state["heating"] = True

world.time += 1.0


# ---------------------------------------------------------------------------
# PHYSICS EXPERIMENT
# ---------------------------------------------------------------------------

story.observe(
    "The cat discovered that the spoon was much easier to move "
    "when nobody was watching."
)

cat.look_at(spoon)

spoon.state["moving"] = True
spoon.state["motion"] = "slow_slide"

world.history.append(
    {
        "time": world.time,
        "event": "spoon_slid",
        "object": spoon.id,
        "cause": "unknown",
    }
)

story.observe(
    "Unfortunately for the spoon, the cat was now watching."
)

spoon.state["moving"] = False
spoon.state["motion"] = "stopped"

world.time += 0.5


# ---------------------------------------------------------------------------
# HEAT TRANSFER
# ---------------------------------------------------------------------------

water.state["temperature_c"] = 80.0
kettle.state["water_temperature_c"] = 80.0

story.observe(
    "The water became hot. Heat moved from the kettle into the water, "
    "as heat has a habit of doing when given enough time."
)

world.history.append(
    {
        "time": world.time,
        "event": "water_heated",
        "object": water.id,
        "temperature_c": water.state["temperature_c"],
    }
)

world.time += 1.0


# ---------------------------------------------------------------------------
# CHEMISTRY
# ---------------------------------------------------------------------------

story.observe(
    "The tea entered the cup and slowly stopped being a separate thing."
)

tea.state["dry"] = False
tea.state["dissolved"] = True

cup.state["empty"] = False
cup.relationships["contains"] = [water.id, tea.id]

world.history.append(
    {
        "time": world.time,
        "event": "tea_dissolved",
        "substance": tea.id,
        "solvent": water.id,
        "location": cup.id,
    }
)


story.observe(
    "The water changed colour. It was still water, but now it carried "
    "a little history from the leaves."
)

water.state["temperature_c"] = 78.0
water.properties["contains_dissolved"] = [tea.id]

cup.state["liquid"] = "tea"

world.time += 1.0


# ---------------------------------------------------------------------------
# LEMON EXPERIMENT
# ---------------------------------------------------------------------------

lemon.state["whole"] = False
lemon.state["cut"] = True

story.observe(
    "The lemon was cut open. It immediately revealed that chemistry "
    "had been hiding inside it all along."
)

lemon.state["juice_available"] = True
lemon.state["citric_acid_available"] = True

world.time += 0.5


story.observe(
    "A few drops fell into the tea."
)

cup.state["liquid"] = "tea_with_lemon"

cup.properties["contains"] = [
    water.id,
    tea.id,
    "lemon_juice",
]

cup.state["acidity"] = "increased"

world.history.append(
    {
        "time": world.time,
        "event": "lemon_added",
        "location": cup.id,
        "changes": [
            "citric_acid_added",
            "acidity_increased",
        ],
    }
)


story.observe(
    "Nothing exploded, which everyone agreed was a successful experiment."
)

world.time += 1.0


# ---------------------------------------------------------------------------
# A SMALL SURPRISE
# ---------------------------------------------------------------------------

story.observe(
    "The cat put one paw beside the cup and discovered that the table "
    "was warm where the cup had been standing."
)

table.state["warm_spot"] = True
table.state["warm_spot_temperature_c"] = 31.0

world.history.append(
    {
        "time": world.time,
        "event": "heat_transferred_to_table",
        "source": cup.id,
        "target": table.id,
    }
)


story.observe(
    "The cat considered this important information."
)

cat.state["knowledge"] = [
    "hot things can warm other things",
    "spoons move when nobody watches",
    "tea becomes tea by becoming less like dry leaves",
]


# ---------------------------------------------------------------------------
# THE STRANGE PART
# ---------------------------------------------------------------------------

world.time += 1.0

story.observe(
    "Then the spoon became warm."
)

spoon.state["temperature_c"] = 35.0

story.observe(
    "The spoon had not touched the tea."
)

spoon.state["contact_with_cup"] = False
spoon.state["contact_with_tea"] = False


world.history.append(
    {
        "time": world.time,
        "event": "spoon_warmed_without_direct_contact",
        "object": spoon.id,
        "cause": "unknown",
    }
)


story.observe(
    "The cat looked at the spoon."
)

cat.look_at(spoon)

story.observe(
    "The spoon looked innocent."
)

spoon.state["appears_innocent"] = True


# ---------------------------------------------------------------------------
# RESEARCH RESULT
# ---------------------------------------------------------------------------

research_result = {
    "physics": [
        "heat transfers between objects",
        "temperature changes over time",
        "objects can move and stop",
        "motion may have an unknown cause",
    ],
    "chemistry": [
        "tea dissolves in water",
        "lemon adds acidity",
        "mixing changes properties without creating a new object identity",
    ],
    "unknown": [
        "the spoon became warm without direct contact with the tea",
        "the spoon previously moved without an observed cause",
    ],
}


world.history.append(
    {
        "time": world.time,
        "event": "research_result_recorded",
        "location": kitchen.id,
        "research": research_result,
    }
)


story.observe(
    "The world had not explained itself."
)

story.observe(
    "It had only demonstrated something, which was probably more useful."
)


# ---------------------------------------------------------------------------
# CONTINUITY
# ---------------------------------------------------------------------------

CONTINUITY = {
    "persistent_objects": [
        "kitchen",
        "kitchen_table",
        "kettle",
        "blue_cup",
        "water",
        "tea",
        "lemon",
        "spoon",
        "street_cat",
    ],

    "world_changes": [
        "water was heated",
        "tea dissolved in water",
        "lemon increased the acidity of the drink",
        "heat transferred from the cup to the table",
        "the spoon became warm without direct contact",
        "the cat gained observations about the physical world",
    ],

    "research_questions": [
        "How did the spoon move?",
        "How did the spoon become warm?",
        "Can physical rules change?",
        "Can chemistry affect the strange behaviour?",
        "What happens if the experiment is repeated?",
    ],

    "connections_to_previous_nodes": [
        "the cat from the street is now in the kitchen",
        "the cat appears to have followed the world rather than a normal path",
    ],

    "next_node": "013.py",
}
```
