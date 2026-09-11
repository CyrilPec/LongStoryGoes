"""
000-01.py — The World
"""
class World:
    """
    Conceptual definition of a world.

    A World has:
        - time
        - entities
        - places
        - objects
        - relationships
        - history

    Stories may instantiate this concept, inherit from it,
    or extend it with their own rules.
    """

    def __init__(self, time=0.0):
        self.time = time

        self.entities = {}
        self.places = {}
        self.objects = {}

        self.relationships = []
        self.history = []

    def add_entity(self, entity_id, entity):
        self.entities[entity_id] = entity
        return entity

    def add_place(self, place_id, place):
        self.places[place_id] = place
        return place

    def add_object(self, object_id, obj):
        self.objects[object_id] = obj
        return obj

    def get(self, entity_id):
        if entity_id in self.entities:
            return self.entities[entity_id]

        if entity_id in self.places:
            return self.places[entity_id]

        if entity_id in self.objects:
            return self.objects[entity_id]

        raise KeyError(f"Unknown world entity: {entity_id}")

    def record(self, event):
        self.history.append(event)

    def advance(self, amount):
        self.time += amount

