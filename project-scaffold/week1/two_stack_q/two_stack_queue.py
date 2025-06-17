#two stack queue implementation for heaps.py

class TwoStackQueue:
    def __init__(self):
        self.enq_stack = []
        self.deq_stack = []
    def enqueue(self, val):
        self.enq_stack.append(val)
    def dequeue(self):
        if self._isDequeueEmpty():
            if self._isEnqueueEmpty(): #if enq_stack is empty AND deq_stack is empty
                raise IndexError("Attempting to dequeue from an empty queue")
            #can prep for dequeue'ing
            while self.enq_stack:
                add_to_dq = self.enq_stack.pop()
                self.deq_stack.append(add_to_dq)
        deq_val = self.deq_stack.pop()
        return deq_val
    def _isDequeueEmpty(self):
        return len(self.deq_stack) == 0
    def _isEnqueueEmpty(self):
        return len(self.enq_stack) == 0