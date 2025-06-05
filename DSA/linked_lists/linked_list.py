#LinkedList class
from node import Node
class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0
    def insert_front(self, data): #value is a Node here with data
        new_node = Node(data, self.head)
        self.head = new_node
        self.size+=1
    def delete_value(self, value):
        if self.head == None:
            return None
        deleted_node = None
        if self.head.data == value:
            deleted_node = self.head
            self.head = self.head.next
            self.size-=1
            return deleted_node
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
        if self.head.next == None:
            new_node = Node(value)
            self.head.next = new_node
            self.size+=1
            return
        curr = self.head
        while curr.next != None:
            curr = curr.next
        curr.next = Node(value)
        self.size+=1
        return
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