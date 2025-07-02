#Implement solution to minimum number of coins as change for specific amount

def total_coins(coins, order, owe):
    #Lets say we owe 39 cents
    #for every iteration we want to find the coin that is closest to the amt we owe
    coins.sort()
    count = 0
    while owe != 0:
        max_c = float('-inf')
        for c in coins:
            if (c > max_c) and (c <= owe):
                max_c = c
            else:
                break
        owe -= max_c
        order.append(max_c)
        count+=1
    return count, order


def main():
    change = input("Please give me the change I owe you: ")
    if "." in change:
        new_change = change.split(".")
        final_change = new_change[0]
    else:
        final_change = int(change)
    change = int(final_change)

    coins = [1,2,5,10]
    order_of_change = []

    num_coins, change_used = total_coins(coins, order_of_change, change)
    print(f"The total number of coins needed for {change} cents is {num_coins} coins.")
    print(f"The coin(s) that were used: {change_used}")


if __name__ == "__main__":
    main()