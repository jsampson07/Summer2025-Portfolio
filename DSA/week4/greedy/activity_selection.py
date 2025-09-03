# Implement solution to the "Activity Selection" problem using greedy algorithm

""" 
Problem Definition:

Given 'n' activities with start times in start[] and finish times in finish[]
FIND the MAXIMUM number of activities someone can perform with NO overlap

"""
import argparse

def activity_selection(start, finish):
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
    parser = argparse.ArgumentParser(prog="Efficient Activities",
                                     description="Given start and finish times of activities" \
                                     "know the most efficient way to complete as many activities as possible")
    
    parser.add_argument("-s", "--start", type=str, required=True,
                        help="List of start times separated by commas i.e. 1,3,2,6,4,10")
    parser.add_argument("-f", "--finish", type=str, required=True,
                        help="List of finish times separated by commas i.e. 1,3,2,6,4,10")
    args = parser.parse_args()
    
    start_times = (args.start).split(",")
    s = [int(time) for time in start_times]
    finish_times = (args.finish).split(",")
    f = [int(time) for time in finish_times]
    if len(s) != len(f):
        raise Exception("Please verify you have a start and end time for every activity")

    acts, num_acts = activity_selection(s, f)

    print(f"The number of activities that can be completed is: {num_acts}")
    print(f"The activity selections that make this possible are:\n{acts}")


if __name__ == "__main__":
    main()