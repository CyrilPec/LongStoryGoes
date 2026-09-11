"""
000-01.py — World
The World is the common state of the fictional universe.
It contains entities, places, objects, events, and time.
It does not know anything about Blender, TUI, audio, or other renderers.
"""
class World:
    def __init__(self, time=None):
        self.time = time
        self.entities = {}
        self.places = {}
        self.objects = {}
        self.events = []
    def add(self, thing):
        collection = self._collection_for(thing)
        collection[thing.id] = thing
        return thing
    def add_entity(self, id, entity):
        entity.id = id
        self.entities[id] = entity
        return entity
    def add_place(self, id, place):
        place.id = id
        self.places[id] = place
        return place
    def add_object(self, id, obj):
        obj.id = id
        self.objects[id] = obj
        return obj
    def record(self, event):
        self.events.append(event)
        return event
    def get(self, id):
        return self.entities.get(id) or self.places.get(id) or self.objects.get(id)
    def advance(self, amount):
        if self.time is not None:
            return self.time.advance(amount)
        return None
    def all(self):
        return list(self.entities.values()) + list(self.places.values()) + list(self.objects.values())
    def _collection_for(self, thing):
        name = getattr(thing, "type", "")
        if name == "place":
            return self.places
        if name in {"physical_object", "object"}:
            return self.objects
        return self.entities
