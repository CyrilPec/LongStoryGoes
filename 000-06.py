"""
000-06.py — Observer

An Observer perceives things in the world.

Observation is separate from memory and knowledge:
    Observer → Observation → Memory → Knowledge

The observer does not automatically remember or know what it observes.
"""


class Observer:
    def __init__(self, name=None):
        self.name = name
        self.observations = []

    def observe(self, subject):
        """
        Observe a subject and store the observation.

        The returned value is the observed subject itself so that
        existing simple stories can continue to use it directly.
        """
        self.observations.append(subject)
        return subject

    def has_observed(self, subject):
        return subject in self.observations

    def all_observations(self):
        return list(self.observations)

    def perceive(self, subject):
        """
        Alias for observe().

        Kept as a separate method because 'perceive' may later represent
        richer perception while observe() remains the simple API.
        """
        return self.observe(subject)
