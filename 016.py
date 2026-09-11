"""
016.py — The Cat by the Window
A short, cozy story using the world concepts.
"""
from world import World
from animal import Animal
from physical_object import PhysicalObject
from place import Place
from observer import Observer
from narrator import Narrator
from time import Time
from action import Action
from event import Event
from state import State
from memory import Memory
world = World()
time = Time()
story = []
narrator = Narrator(story)
window = PhysicalObject("Old Window")
room = Place("Quiet Room")
cat = Animal("Luna")
observer = Observer()
memory = Memory()
state = State({"mood": "sleepy", "awake": True})
world.add_place("quiet_room", room)
world.add_object("old_window", window)
world.add_entity("luna", cat)
observer.observe(window)
narrator.observe("Rain tapped softly against the old window.")
narrator.observe("Luna wandered into the quiet room and looked for a warm place to rest.")
action = Action("rest", actor=cat, target=window)
action.perform()
state.set("mood", "peaceful")
event = Event("cat_resting", time=time.now(), place=room, actor=cat, target=window)
world.record(event)
memory.remember(event)
narrator.observe("She curled up beside the window and listened to the gentle rain.")
time.advance(1.0)
state.set("awake", False)
memory.remember("Luna fell asleep beside the window.")
narrator.observe("Soon Luna was asleep, warm and peaceful, while the rain continued outside.")
