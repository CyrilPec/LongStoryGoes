"""
000-05.py — Narrator

Conceptual definition of a narrator.

A Narrator communicates what happens in a story
to an audience. It does not define how the story
is rendered.

The same narration can later be rendered as:
- text
- TUI
- audio
- another presentation format
"""


class Narrator:
    """
    Concept of a narrator.

    A Narrator observes the story and communicates
    narration to the audience.
    """

    def __init__(self, story):
        self.story = story

    def observe(self, text):
        """
        Add narration to the story.
        """
        return self.story.observe(text)

    def describe(self, text):
        """
        Describe something for the audience.
        """
        return self.story.observe(text)

    def say(self, text):
        """
        Narrate spoken text.
        """
        return self.story.observe(text)
