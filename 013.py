"""
013.py — The Wolf

A short story using the conceptual World, Human,
Animal, and PhysicalObject definitions.
"""

from world import World
from human import Human
from animal import Animal
from physical_object import PhysicalObject


world = World()

traveler = Human("Elias")
wolf = Animal("Wolf")
stone = PhysicalObject("Stone")

world.add_entity("elias", traveler)
world.add_entity("wolf", wolf)
world.add_object("stone", stone)


# The story begins.

traveler.perceive(wolf)
wolf.perceive(traveler)

traveler.remember("I saw a wolf in the forest.")

wolf.remember("A human approached.")

traveler.move_to("forest")
wolf.move_to("forest")
stone.move_to("forest")

world.record({
    "event": "meeting",
    "human": traveler.name,
    "animal": wolf.name,
    "place": "forest",
})

world.advance(1.0)
