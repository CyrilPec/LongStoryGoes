"""
000-09.py — Event
Conceptual definition of an event.
An Event represents something that happens in the World at a particular time and place.
"""
class Event:
    def __init__(self, type=None, time=None, place=None, actor=None, target=None, data=None):
        self.type = type
        self.time = time
        self.place = place
        self.actor = actor
        self.target = target
        self.data = data or {}
