import json
import os

#I want to be able to:
"""
1) add tasks
2) remove tasks
3) update tasks
4) look at my tasks (read the entire file)
    i.e. readall()
5) look at ONLY a specific task (read json file and then parse until find the task name)
    i.e. readtask(TASK NAME)
"""

"""
task info:
    - task name - str (REQUIRED)
    - description (of task) - str (OPTIONAL)
    - task due date - (DATETIME format) (OPTIONAL)
    - completed (True or False) - boolean
    - priority - str (Low, Medium, High)
"""
class TaskDB:
    def __init__ (self, filename="tasks.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            new_file = open(self.filename)
            json.dump([], new_file)
    def load(self): #used to load information from the json file
        file = open(self.filename)
        json_data = json.load(file)
        file.close()
        return  json_data #returns a LIST
    def addtask(self, task_name, description, due_date, completed, priority):
        file_data = self.load() #we now have a list (type = list)
        #Logic to check if task already exists
        for task_info in file_data:
            #task_info is each dict (task and its other info)
            tname = task_info["Task Name"]
            if tname.lower() == task_name.lower():
                print("You already have {tname} as a task.")
                return
        #Logic to add task to DB
        task_to_add = {"Task Name": task_name, "Description": description, "Due Date": due_date, "Completed": completed, "Priority": priority}
        file_data.append(task_to_add)
        file = open(self.filename, "w")
        json.dump(file_data, file, indent=2)
        file.close()
        print("Added {task_name} to your to-do list!")
    def removetask(self, task_name):
        file_data = self.load()
        for ind, tasks in enumerate(file_data):
            tname = tasks["Task Name"]
            if tname.lower() == task_name.lower():
                #MAYBE add functionality of double checking if user really wants to DELETE the task

                del file_data[ind] #remove the task and its information (ITS ENTIRE DICTIONARY)
                file = open(self.filename, "w")
                json.dump(file_data, file, indent=2)
                file.close()
                print("Successfully removed your {task_name} task!")
        print("{task_name} does not exist. Could not remove.")
    def get_all_tasks(self):
        all_tasks = self.load()
        print("Here are all your tasks:\n{all_tasks}")
    def get_task(self, task_name):
        file_data = self.load() #we now have a list (type = list)
        #Logic to check if task already exists
        for task_info in file_data:
            #task_info is each dict (task and its other info)
            tname = task_info["Task Name"]
            if tname.lower() == task_name.lower():
                print("Here is your task and its correspinding information:\n{task_info}")
        print("You do not have a {task_name} task.")