"""
000-03.py — Animal

Conceptual definition of an animal.

An Animal is a living entity that can exist in a World.
Concrete animals are created by stories/worlds that use this concept.
"""


class Animal:
    """
    Concept of an animal.

    An Animal can:
    - have an identity
    - exist at a location
    - perceive its surroundings
    - move
    - remember events
    - have relationships
    """

    def __init__(self, name=None):
        self.name = name
        self.location = None
        self.memory = []
        self.relationships = {}

    def perceive(self, thing):
        ...

    def remember(self, event):
        self.memory.append(event)

    def move_to(self, place):
        self.location = place

    def relate_to(self, other, relationship):
        self.relationships[other] = relationship
