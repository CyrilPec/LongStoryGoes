"""
000-06.py — Observer

Conceptual definition of an observer.

An Observer is an entity that can perceive
something within the World.

Observation belongs to the observer's perspective.
It is not the same thing as narration.
"""


class Observer:
    """
    Concept of an observer.

    An Observer can:
    - perceive things
    - remember observations
    - have a limited perspective
    """

    def __init__(self):
        self.observations = []

    def observe(self, thing):
        """
        Observe something.
        """
        self.observations.append(thing)
        return thing

    def remember(self, observation):
        """
        Remember an observation.
        """
        self.observations.append(observation)
