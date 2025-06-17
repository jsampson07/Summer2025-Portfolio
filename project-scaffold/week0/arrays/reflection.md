## Testing Efficiency
**GOAL:**
    - Test the efficiency of custom built DynamicList with its append() method against python's built-in append() method for lists
    - Understand why any differences are so large
    - Understand the relationship with input to "run time"

**Post-Testing:**
    After running the tests using the time module and the perf_counter() function, I discovered that both my implementation and python's implementation had a similar append() time for the first two-three cases depending on what is considered "a small difference" but for the final three-four cases, this difference quickly increased. The most surprising jump in time was from one million elements to ten million elements (Case Four to Case Five). While all the others had smaller differences (by not even a second), it shot up by almost 10 seconds for these two particular cases. The "doubling" approach to expanding the array "dynamically" definitely was the core contributor to this spike in time, as we were no longer expanding our array by factors in the thousands, but rather by factors in the millions, and constantly having to copy over millions of elements on each "resize" definitely took a toll on the custom DynamicArray implementation.
        1. Case One (1000 elements)
            Difference = ~0.000895 seconds
        2. Case Two (10000 elements)
            Difference = ~0.005695 seconds
        3. Case Three (100000 elements)
            Difference = ~0.092611 seconds
        4. Case Four (1000000 elements)
            Difference = ~0.710269
        5. Case Five (10000000 elements)
            Difference = ~10.247103 seconds
**Conclusion:**
    It is clear while there are many different implementations to one problem, the consequences can be drastic. Having a wide range of knowledge to come up with different ways to approach a problem is one of the strongest suits someone can have in the realm of Computer Science.