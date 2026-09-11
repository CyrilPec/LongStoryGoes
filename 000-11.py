"""
000-11.py — Action
Conceptual definition of an action.
An Action describes something an entity can do.
"""
class Action:
    def __init__(self, name, actor=None, target=None, data=None):
        self.name = name
        self.actor = actor
        self.target = target
        self.data = data or {}
    def perform(self):
        return {"action": self.name, "actor": self.actor, "target": self.target, "data": self.data}
