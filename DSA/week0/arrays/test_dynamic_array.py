from dynamic_array import DynamicArray
def main():
    list1 = DynamicArray(10)
    print(len(list1))
    list1.append(10)
    list1.pop()
    list1.append(100)
    list1.append("value ahahaha")
    print(list1)
    print(list1[1])

if __name__ == "__main__":
    main()