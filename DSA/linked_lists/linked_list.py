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
    def reverse(self): #reverse the linked list
        #iterate self.size-1 times
        curr = self.head
        prev = None
        while curr != None:
            #prev = curr
            #curr = curr.next
            maintain = curr.next
            curr.next = prev
            prev = curr #added this line here
            curr = maintain
        self.head = prev

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