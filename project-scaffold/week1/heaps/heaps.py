#"mini heap" implementation

class MiniHeap:
    def __init__(self):
        self.heap = []
        self.heap.append(0) #start indexing at ind = 1
        
    def push(self, val):
        self.heap.append(val)
        #now i need to up-heap
        self._heapify()

    def pop(self):
        if len(self.heap) == 1:
            raise IndexError("Empty heap")
        #Base Case
        if len(self.heap) == 2: #one elem in our heap
            return self.heap.pop()
        root = self.heap[1]
        self.heap[1] = self.heap.pop()
        self._down_heap()
        return root
    
    def _heapify(self):
        parent_ind = (len(self.heap)-1) // 2
        new_val_ind = len(self.heap) - 1
        while parent_ind != 0:
            if self.heap[parent_ind] > self.heap[new_val_ind]: #swap cond.
                temp_val = self.heap[parent_ind]
                self.heap[parent_ind] = self.heap[new_val_ind]
                self.heap[new_val_ind] = temp_val
                new_val_ind = parent_ind
                parent_ind = new_val_ind // 2
            else: #if heap condition is satisfied ==> stop
                break

    def _down_heap(self): #_ because not intended to be called by external users
        curr_ind = 1
        left_child_ind = curr_ind*2
        right_child_ind = curr_ind*2 + 1
        max_index = len(self.heap) - 1
        while True:
            #if there are two children
            if left_child_ind <= max_index and right_child_ind <= max_index:
                left_child, right_child = self.heap[left_child_ind], self.heap[right_child_ind]
                if left_child < right_child:
                    #we want to check for swap of left and parent (curr)
                    if left_child < self.heap[curr_ind]: #swap condition
                        self.heap[left_child_ind] = self.heap[curr_ind]
                        self.heap[curr_ind] = left_child
                        #reassign index vars
                        curr_ind = left_child_ind
                        left_child_ind = curr_ind*2
                        right_child_ind = curr_ind*2 + 1
                    else:
                        break
                elif right_child < left_child:
                    if right_child < self.heap[curr_ind]:
                        self.heap[right_child_ind] = self.heap[curr_ind]
                        self.heap[curr_ind] = right_child
                        #reassign index vars
                        curr_ind = right_child_ind
                        left_child_ind = curr_ind*2
                        right_child_ind = curr_ind*2 + 1
                else: #the left and right child are equal (lets check left)
                    #we want to check for swap of left and parent (curr)
                    if left_child < self.heap[curr_ind]: #swap condition
                        self.heap[left_child_ind] = self.heap[curr_ind]
                        self.heap[curr_ind] = left_child
                        #reassign index vars
                        curr_ind = left_child_ind
                        left_child_ind = curr_ind*2
                        right_child_ind = curr_ind*2 + 1
                    else: #no swap is needed even with two two children
                        break

            #if there is one child (must be left, CANNOT be right child)
            elif left_child_ind == max_index:
                if self.heap[left_child_ind] < self.heap[curr_ind]:
                    temp = self.heap[curr_ind]
                    self.heap[curr_ind] = self.heap[left_child_ind]
                    self.heap[left_child_ind] = temp
                    break #we know child must be a leaf "node"
                else:
                    break
                
            #if there are no children
            else:
                break