**DELIVERABLES**
    - Heaps implementation
    - Linked List implementation
        - Thorough implementation with methods such as reverse(),       remove_at_index(), and basic functionality
    - Two-stack queue implementation
**External Resources**
I completed two Codecademy courses on bash scripting, one called *"Learn Bash Scripting"* which covered topics such as bash script arguemnts, variables, keywords, aliases, and use of bash scripts. The other course was called *"Introduction to Linux: Bash Scripting"*, which covered topics such as bash script use cases, ability to link multiple commands and reuse scripts, automating repetitive tasks, and running scripts inside of other scripts. 
**Difficulties**
One difficulty I came across during week1 data structures heavy review/learning was implementing the reverse() method in the Linked List. Right off the bat, my intuition was to flip each of the next pointers of every node to the previous node, but I was doing this looping through every other node so I would get a result like the following:
    original list:
        n1 -> n2 -> n3 -> n4
        n1 <- n2 n3 <- n4
As you can tell, I would reverse the nodes but in groups of two losing track of the rest of the linked list, so I realized I had to connect the two nodes in between and that somehow I was skipping over nodes. I then realized that my approach was incorrect because I was starting from the second node and flipping every second node, whereas I wanted to start flipping from the first node as I need to redirect its next pointer to None, and I also realized that using a "prev" node variable too was going to significantly help me with the implementation.