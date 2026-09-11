"""
000-10.py — Relationship
Conceptual definition of a relationship.
A Relationship describes a connection between two entities in a World.
"""
class Relationship:
    def __init__(self, subject, relation, target):
        self.subject = subject
        self.relation = relation
        self.target = target
    def matches(self, subject=None, relation=None, target=None):
        return ((subject is None or subject == self.subject) and (relation is None or relation == self.relation) and (target is None or target == self.target))
