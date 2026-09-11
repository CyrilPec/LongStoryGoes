class Human:
    """
    Concept of a human being.

    A Human can:
    - exist in a World
    - have identity
    - have a location
    - perceive
    - act
    - remember
    - form relationships
    - change over time
    """

    def __init__(self, name=None):
        self.name = name
        self.location = None
        self.memory = []
        self.relationships = {}

    def perceive(self, thing):
        ...

    def remember(self, event):
        self.memory.append(event)

    def move_to(self, place):
        self.location = place

    def relate_to(self, human, relationship):
        self.relationships[human] = relationship
