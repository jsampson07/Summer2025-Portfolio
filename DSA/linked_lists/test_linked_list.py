from linked_list import LinkedList
from node import Node
def main():
    """
    node1 = Node("Data")
    ll1 = LinkedList()
    print(ll1)
    ll1.insert_front(10)
    ll1.insert_front(100)
    ll1.insert_front(200)
    ll1.insert_front(69)
    print(ll1)
    ll1.delete_value(100)
    print(ll1)
    ll1.insert_end(420)
    print(ll1)
    node_found = ll1.search(200)
    print(node_found)
    print(len(ll1))
    """

    #reverse list
    ll1 = LinkedList()
    ll1.insert_front(10)
    ll1.insert_end(100)
    ll1.insert_end(200)
    ll1.insert_end(69)
    ll1.reverse()
    print(ll1)


if __name__ == "__main__":
    main()