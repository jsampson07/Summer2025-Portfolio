#Measure DynamicArray append() implementation vs Python's built-in append()
from dynamic_array import DynamicArray
import time

def append_benchmark(n, runs=3):
    #want to get the average of all the runs (keep track in an array of times)
    python_time = []
    my_time = []
    for i in range(runs):
        start = time.perf_counter()
        my_list = DynamicArray()
        for i in range(n):
            my_list.append(i)
        elapsed_time = time.perf_counter() - start
        my_time.append(elapsed_time)

        start = time.perf_counter()
        py_list = []
        for i in range(n):
            py_list.append(i)
        elapsed_time = time.perf_counter() - start
        python_time.append(elapsed_time)
    #find the averages of all the times calculated
    my_total = 0
    for calc_time in my_time:
        my_total+=calc_time
    py_total = 0
    for calc_time in python_time:
        py_total+=calc_time
    return f"Average time for custom implementation is: {my_total}.\nAverage time for python implementation is: {py_total}"

def main():
    print(append_benchmark(1000))
    print(append_benchmark(10000))
    print(append_benchmark(100000))
    print(append_benchmark(1000000))
    print(append_benchmark(10000000)) #this one is really noticeable !!!
        #custom implementation is horrible, python implementation is <10 seconds better if not more

if __name__ == "__main__":
    main()