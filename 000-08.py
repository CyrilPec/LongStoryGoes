"""
000-08.py — Place
Conceptual definition of a place.
A Place is where entities and objects can exist and events can happen.
"""
class Place:
    def __init__(self, name=None):
        self.name = name
        self.contents = []
    def add(self, thing):
        if thing not in self.contents:
            self.contents.append(thing)
        return thing
    def remove(self, thing):
        if thing in self.contents:
            self.contents.remove(thing)
        return thing
    def contains(self, thing):
        return thing in self.contents
