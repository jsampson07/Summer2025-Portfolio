from linked_list import LinkedList
from node import Node
from HashMapEntry import HashMapEntry

class HashMap:
    def __init__(self, capacity = 13):
        self.capacity = capacity
        self.map = [LinkedList() for _ in range(self.capacity)]
        self.size = 0
    def put(self, key, val):
        index = self._hashfunc(key)
        #if there is no pair at hashfuct value
        entry = HashMapEntry(key,val)
        if self.map[index].is_Empty is None:
            self.map[index].insert_front(entry)
            self.size+=1
        else:
            LL = self.map[index]
            curr = LL.head
            while curr:
                if curr.data.key == key:
                    curr.data.value = val
                curr = curr.next
            self.map[index].insert_front(entry)
    def remove(self, key):
        pair_index = self._hashfunc(key)
        if self.map[pair_index].is_Empty() is None:
            raise RuntimeError(f"{key} is not a valid key")
        LL = self.map[pair_index]
        curr = LL.head
        prev = None
        while curr:
            if curr.data.key == key:
                if prev:
                    prev.next = curr.next
                    return
                else:
                    #Case for if remove from head
                    LL.delete_at_index(0)
                    return
            prev = curr
            curr = curr.next
        raise RuntimeError(f"{key} is not a valid key")
    def get(self, key):
        #retrieve the (key,val) pair
        index = self._hashfunc(key)
        if self.map[index].is_Empty():
            return f"No key,value pair with {key} as key"
        LL = self.map[index]
        curr = LL.head
        while curr:
            if curr.data.key == key:
                return curr.data.value
            curr = curr.next
        #return f"No key,value pair with {key} as key"


    def debug_str(self):
        lines = []
        for i, bucket in enumerate(self.map):
            if bucket is None or bucket.head is None:
                # no list at this index
                lines.append(f"{i}: []")
            else:
                # traverse the linked list at bucket
                entries = []
                curr = bucket.head
                while curr:
                    entry = curr.data    # or curr.value if that's how you named it
                    entries.append(f"{entry.key}:{entry.value}")
                    curr = curr.next
                lines.append(f"{i}: [{', '.join(entries)}]")
        return "\n".join(lines)
            

    def _hashfunc(self, key):
        return hash(key) % self.capacity
    def __str__(self):
        pairs = []
        for LL in self.map:
            if LL is None:
                continue
            curr = LL.head
            while curr:
                entry = curr.data
                pairs.append(f"{entry.key}: {entry.value}")
                curr = curr.next
        return "{ " + ", ".join(pairs) + " }"