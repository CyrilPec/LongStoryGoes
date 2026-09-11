"""
014.py — Milo and the Red Ball
A small, cozy story demonstrating World, Animal, PhysicalObject, Observer, and Narrator.
"""
from world import World
from animal import Animal
from physical_object import PhysicalObject
from observer import Observer
from narrator import Narrator
world = World()
story = []
narrator = Narrator(story)
garden = {"id": "cozy_garden", "name": "Cozy Garden"}
milo = Animal("Milo")
milo_observer = Observer()
world.add_entity("milo", milo)
ball = PhysicalObject("Red Ball")
world.add_object("red_ball", ball)
narrator.observe("The afternoon was warm and quiet.")
narrator.observe("Milo was resting in the garden when he noticed a little red ball in the grass.")
milo_observer.observe(ball)
narrator.observe("Milo lifted his head and walked over to the ball.")
narrator.observe("He gave it a gentle push with his nose.")
narrator.observe("The red ball rolled slowly across the warm grass.")
narrator.observe("Milo followed it with a happy little bounce in his step.")
narrator.observe("When the ball finally stopped beneath the old tree, Milo curled up beside it.")
narrator.observe("The garden was quiet again, and Milo was perfectly happy.")
world.record({"event": "milo_found_ball", "observer": "milo", "object": "red_ball", "location": "cozy_garden"})
world.record({"event": "milo_played_with_ball", "observer": "milo", "object": "red_ball", "location": "cozy_garden"})
