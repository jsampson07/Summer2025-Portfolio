#Node class
class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next
    def __str__(self):
        return str(self.data)
    """
    def __eq__(self, other):
        if self.data > other.data: #self > other
            return 1
        elif self.data < other.data: #self < other
            return -1
        else: #self = other
            return 0
    """