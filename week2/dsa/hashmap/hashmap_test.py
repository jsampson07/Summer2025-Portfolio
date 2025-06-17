from hashmap import HashMap

def main():
    #Test put()
    my_map = HashMap()
    my_map.put(10, "Hello There")
    my_map.put(24, "Oh man")
    my_map.put(17, "APT")
    my_map.put(4, "FOUR SCORE")
    print(my_map.debug_str())

    #Test remove()
    my_map.remove(17)
    my_map.remove(4)
    print(my_map.debug_str())

    val1 = my_map.get(100)
    val2 = my_map.get(17)
    val3 = my_map.get(10)
    print(val1)
    print(val2)
    print(val3)


if __name__ == "__main__":
    main()