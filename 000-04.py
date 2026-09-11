"""
000-04.py — PhysicalObject

Conceptual definition of a physical object.

A PhysicalObject is a non-living physical thing that can exist
in a World and occupy a location.
"""


class PhysicalObject:
    """
    Concept of a physical object.

    A PhysicalObject can:
    - have an identity
    - have a physical location
    - have physical properties
    - be moved
    - interact with other entities
    """

    def __init__(self, name=None):
        self.name = name
        self.location = None
        self.properties = {}

    def move_to(self, place):
        self.location = place

    def set_property(self, name, value):
        self.properties[name] = value

    def get_property(self, name):
        return self.properties.get(name)
