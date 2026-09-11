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
