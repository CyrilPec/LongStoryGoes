"""
015.py — The Little Bird
A short story using the new world concepts.
"""
from world import World
from animal import Animal
from observer import Observer
from place import Place
from action import Action
from event import Event
from state import State
from memory import Memory
from time import Time
from narrator import Narrator
world = World()
time = Time()
story = []
narrator = Narrator(story)
garden = Place("Quiet Garden")
bird = Animal("Little Bird")
observer = Observer()
memory = Memory()
state = State({"mood": "curious", "flying": False})
world.add_entity("bird", bird)
world.add_place("garden", garden)
observer.observe(garden)
memory.remember("A quiet garden with a tall old tree.")
narrator.observe("The morning was soft and golden in the quiet garden.")
narrator.observe("A little bird rested on a branch and listened to the wind.")
state.set("mood", "curious")
action = Action("fly", actor=bird, target=garden)
action.perform()
state.set("flying", True)
event = Event("bird_flew", time=time.now(), place=garden, actor=bird)
world.record(event)
memory.remember(event)
narrator.observe("Suddenly, the little bird opened its wings and flew into the morning sky.")
time.advance(1.0)
state.set("flying", False)
narrator.observe("A moment later, it returned to the same branch, carrying a tiny green leaf.")
memory.remember("The bird returned with a tiny green leaf.")
narrator.observe("It tucked the leaf beneath its feathers and settled down peacefully.")
