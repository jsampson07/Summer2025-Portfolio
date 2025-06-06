#LinkedList class
from node import Node
class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0
    def insert_front(self, data): #value is a Node here with data
        self.head = Node(data, self.head)
        self.size+=1
    def delete_value(self, value):
        if self.head == None:
            return None
        curr = self.head
        while curr.next != None:
            if curr.next.data == value:
                deleted_node = curr.next
                curr.next = curr.next.next
                self.size-=1
                return deleted_node
            curr = curr.next
        return None
    def insert_end(self, value):
        #insert at the "tail" of the list (except here there is no tail ref)
        if self.head == None:
            new_node = Node(value)
            self.head = new_node
            self.size+=1
            return
        curr = self.head
        while curr.next != None:
            curr = curr.next
        curr.next = Node(value)
        self.size+=1
        return
    def search(self, val):
        #returns a Node if we find a matching val, else return None
        curr = self.head
        while curr != None:
            if curr.data == val:
                return curr
            curr = curr.next
        return None
    #examples to help understand reverse() conceptually
    """ OLD IMPLEMENTATION
    n1 -> n2 -> n3 -> n4 -> n5
    iteration1: curr = n1
        prev = n1, curr = n2, maintain = n3
        n1 <- n2, prev = n2, curr = n3, HEAD = n2
    iteration2: curr = n3
        prev = n3, curr = n4, maintain = n5
        n1 <- n2 
    old implementation lost every other node in between (i.e. node3, node 6, node 9 but would "reverse" n1 and n2, n3 and n4, etc)
    """
    #
    """ NEW IMPLEMENTATION (CORRECTED)
    n1 -> n2 -> n3 -> n4 -> n5
    GOAL: n1 <- n2 <- n3 <- n4 <- n5, where head = n5
    iteration1: curr = n1
        maintain = n2, curr.next = None (prev), prev = n1, curr = n2
            maintain ==> keeps track of the next element in linkedlist so we do not lose info for the rest of the LL
            prev ==> where to point the current node to (previous node), in first iteration = to None bc now will be the end of the list
            curr ==> the node we want to redirect
        n1 -> None
    """
    def reverse(self):
        curr = self.head
        prev = None
        while curr != None:
            maintain = curr.next
            curr.next = prev
            prev = curr
            curr = maintain
        self.head = prev #NOT curr, bc curr would be DONE after the last iteration (we are on the last node curr = last node, but then curr = ~curr.next (NONE))

    def delete_at_index(self, index):
        #practice using prev, curr ptrs
        if (index < 0) or (index >= self.size):
            raise IndexError("Index out of bounds")
        curr_ind = 0
        curr = self.head
        prev = None
        while curr_ind <= index:
            if curr_ind == index:
                if prev:
                    prev.next = curr.next
                else:
                    self.head = self.head.next
            prev = curr
            curr = curr.next
            curr_ind+=1
        self.size-=1
    def __str__(self):
        if self.head == None:
            return "The list is empty"
        curr = self.head
        return_string = ""
        while curr != None:
            return_string += str(curr.data) + " -> "
            #print(f"{curr.data} ->", end=" ")
            curr=curr.next
        return return_string
    def __len__(self):
        return self.size