# Implement solution to the "Activity Selection" problem using greedy algorithm

""" 
Problem Definition:

Given 'n' activities with start times in start[] and finish times in finish[]
FIND the MAXIMUM number of activities someone can perform with NO overlap

"""
def activity_selection(start, finish):
    if len(start) != len(finish):
        raise Exception("Please verify you have a start and end time for every activity")
    if len(start) == len(finish) == 0:
        raise Exception("Please make sure you have activities to select from")
    # Let's create a list of tuples
    act_list = []
    for i in range(len(start)):
        act_list.append((start[i], finish[i]))
    # We now have a list of tuples (activities) ==> [(s1,f1), (s2, f2), ... (sn, fn)]
    sorted_activities = sorted(act_list, key=lambda act: act[1])
    selected_list = []
    num_activities = 0
    selected_finish = float("-inf")
    for s, f in sorted_activities:
        if s > selected_finish:  #I do not allow overlap here just bc in my mind I count activity i.e. ending at 5 and another starting at 5 as overlapping
            selected_finish = f
            selected_list.append((s,f))
            num_activities+=1
    return selected_list, num_activities


def main():
    s = [1,3,0,5,8,10]
    f = [2,4,6,7,9,10]

    acts, num_acts = activity_selection(s, f)

    print(f"The number of activities that can be completed is: {num_acts}")
    print(f"The activity selections that make this possible are:\n{acts}")


if __name__ == "__main__":
    main()