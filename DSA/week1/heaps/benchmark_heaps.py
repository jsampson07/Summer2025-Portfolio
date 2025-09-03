#Used to benchmark push/pop operations on both custom heap implementation and python's built-in heapq (push/pop operations)
from heaps import MiniHeap
import heapq
import time
def heap_pop_benchmark(num, run=1):
    #benchmark 100,000 push operations
    my_time = []
    py_time = []
    for i in range(run):
        start = time.perf_counter()
        my_heap = MiniHeap()
        for i in range(num):
            my_heap.push(i)
        elapsed = time.perf_counter() - start
        my_time.append(elapsed)

        py_heap = []
        start = time.perf_counter()
        for i in range(num):
            heapq.heappush(py_heap, i)
        elapsed = time.perf_counter() - start
        py_time.append(elapsed)
    my_avg = sum(my_time)/len(my_time)
    py_avg = sum(py_time)/len(py_time)
    return f"Average time for custom implementation is: {my_avg}.\nAverage time for python implementation is: {py_avg}"
    

def main():
    print(heap_pop_benchmark(100000000))
    """
    h = MiniHeap()
    for x in [5, 3, 8, 1, 6, 2]:
        h.push(x)
    # Internally, the array (ignoring index 0) should be a valid min-heap.
    # Now popping all elements should give you sorted order:
    result = [h.pop() for _ in range(len(h.heap)-1)]
    print(result)
    assert result == sorted([5,3,8,1,6,2])

    h2 = MiniHeap()
    h2.push(2)
    popped = h2.pop()
    print(popped)
    """
    """
    h3 = MiniHeap()
    for num in [1,4,4,7,8,4,9,10,420,7,8,1,69]:
        h3.push(num)
    result2 = [h3.pop() for _ in range(len(h3.heap) - 1)]
    print(result2)
    """
if __name__ == "__main__":
    main()