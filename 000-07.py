"""
000-07.py — Time
Conceptual definition of Time.
Time provides a shared progression for a World and allows events to have temporal meaning.
"""
class Time:
    def __init__(self, value=0.0):
        self.value = value
    def now(self):
        return self.value
    def advance(self, amount):
        self.value += amount
        return self.value
    def elapsed_since(self, moment):
        return self.value - moment
    def mark(self):
        return self.value
