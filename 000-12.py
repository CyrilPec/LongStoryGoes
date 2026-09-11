"""
000-12.py — State
Conceptual definition of a state.
A State describes the condition of an entity or object at a particular moment.
"""
class State:
    def __init__(self, values=None):
        self.values = values or {}
    def set(self, name, value):
        self.values[name] = value
    def get(self, name, default=None):
        return self.values.get(name, default)
    def has(self, name):
        return name in self.values
