"""
000-05.py — Narrator

The Narrator describes what happens in a story.

Narration is separate from observation:
    World → Narrator → Narration

The narrator may describe things that no individual character knows.
"""


class Narrator:
    def __init__(self, name=None):
        self.name = name
        self.narrations = []

    def narrate(self, text):
        """
        Add a piece of narration.

        Returns the text so simple existing stories can continue
        using the result directly.
        """
        self.narrations.append(text)
        return text

    def all_narrations(self):
        return list(self.narrations)

    def last_narration(self):
        if not self.narrations:
            return None

        return self.narrations[-1]
