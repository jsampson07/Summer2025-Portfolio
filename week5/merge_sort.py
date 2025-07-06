from typing import List

def merge_sort(arr: List[int]):
    # Base cases
    if len(arr) == 1:
        return
    # Create sub-arrs
    length = len(arr)
    midIndex = int(length/2)
    left = arr[0:midIndex]
    right = arr[midIndex:]
    merge_sort(left)
    merge_sort(right)

    i,j = 0,0
    # We want it to iterate until we are at the end of one of the arrays
    while ((i < len(left)) and (j < len(right))):
        if left[i] <= right[j]:
            arr[i+j] = left[i]
            i+=1
        else:
            arr[i+j] = right[j]
            j+=1
    # Iterate through "incomplete" array
    while i < len(left):
        arr[i+j] = left[i]
        i+=1
    while j < len(right):
        arr[i+j] = right[j]
        j+=1
    

def main():
    test_list = [1,6,3,4,10,9,0,69,420,36,2,24,21,19,17,34,50,69]
    merge_sort(test_list)
    print(f"The sorted list is:\n{test_list}")


if __name__ == "__main__":
    main()