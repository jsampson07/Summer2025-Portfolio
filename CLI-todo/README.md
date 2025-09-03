**DELIVERABLES**

    - hello.sh
    - CLI-todo app
    - dynamic array implementation, tests, benchmark

**How to Run CLI-todo app**

    run: python3 todo.py [flags] [--optional]
    **FLAGS**
        1. add <task_name> <priority>
            --description <description>
            --due_date <due_date>
            --completed
        2. remove <task>
        3. remall
        4. update <task>
            --taskname <new_task_name>
            --description <new_description>
            --due_date <new_due_date>
            --completed
            --priority <new_priority>
        4. list
            --task <task_name>
    
**Difficulties**

One difficulty I came across was implementing the "update" feature as at first I was struggling to find a way of how to not lose data if the user did not provide a value for a particular flag (i.e. "description"). The input would be treated as "None" and when passed into update() would hold None, but I quickly realized that I had all the current data in the tasks.json file so I could just grab the information if the provided fields from the user were empty.

