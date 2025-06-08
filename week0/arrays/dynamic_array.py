class DynamicArray:
    def __init__(self, capacity = 1):
        self.size = 0
        self.capacity = capacity
        self.buf = [None] * self.capacity #create a buffer of initial capacity

    def append(self, new_value):
        if self.size >= self.capacity: #if the buffer is full
            self.capacity = 2*self.capacity
            new_buf = [None] * self.capacity
            for i,elem in enumerate(self.buf):
                new_buf[i] = elem
            self.buf = new_buf
            self.buf[self.size] = new_value
            self.size+=1
            #copy elements over into new buffer
                #then insert new element
        else: #still room to add elements
            self.buf[self.size] = new_value
            self.size+=1
    def pop(self):
        if self.size == 0:
            raise Exception ("Empty List")
        pop_val = self.buf[self.size-1] #get last element
        self.buf[self.size-1] = None
        self.size-=1
        #sparse logic
        if self.size <= (self.capacity//4):
            #what if self.capacity == 1? we start with capacity = 1, add elem and them remove
            new_cap = max(self.capacity//2, 1)
            smaller_buf = [None] * new_cap
            for i in range(self.size):
                smaller_buf[i] = self.buf[i]
            self.buf = smaller_buf
            self.capacity = new_cap
        return pop_val
    #dunder methods used for len(), object[index], printing object
    def __len__(self):
        return self.size
    def __getitem__(self, index):
        if index >= self.size or index < 0:
            raise IndexError("Invalid index")
        return self.buf[index]
    def __repr__(self):
        return f"DynamicArray({[self.buf[i] for i in range(self.size)]}, capacity={self.capacity})"