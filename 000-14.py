"""
Knowledge
Knowledge represents information currently available to an entity.
Knowledge is not the same as World state.
The World may contain facts that an entity does not know.
Memory represents retained experiences or information from the past.
Knowledge represents what an entity currently knows.
Knowledge must not replace Memory.
"""
class Knowledge:
    def __init__(self):
        self.items = []

    def learn(self, item):
        self.items.append(item)
        return item

    def knows(self, item):
        return item in self.items

    def all(self):
        return list(self.items)
