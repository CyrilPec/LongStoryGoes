"""
000-13.py — Memory
Conceptual definition of memory.
Memory allows an observer to retain events or experiences from the past.
"""
class Memory:
    def __init__(self):
        self.items = []
    def remember(self, item):
        self.items.append(item)
        return item
    def recall(self, index=-1):
        if not self.items:
            return None
        return self.items[index]
    def all(self):
        return list(self.items)
