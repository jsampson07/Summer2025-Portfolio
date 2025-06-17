import json
import os
from datetime import datetime

"""
task info:
    - task name - str (REQUIRED)
    - description (of task) - str (OPTIONAL)
    - task due date - (DATETIME format) (OPTIONAL)
    - completed (True or False) - boolean
    - priority - str (Low, Medium, High)
"""

#note: datetime.strptime(str_to_convert, <format_of_date>) - string --> datetime object
#      datetimeObject.strftime(<format_of_date>) - datetime --> string

class TaskDB:
    def __init__ (self, filename="tasks.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            new_file = open(self.filename, "w")
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
                print(f"You already have {tname} as a task.")
                return
        
        #Logic to add task to DB
        if isinstance(due_date, datetime): #if due_date is provided ensure convert to str (otherwise not supported JSON type)
            due_date = due_date.strftime("%m-%d-%Y")
        task_to_add = {"Task Name": task_name, "Description": description, "Due Date": due_date, "Completed": completed, "Priority": priority}
        file_data.append(task_to_add)
        file = open(self.filename, "w")
        json.dump(file_data, file, indent=2)
        file.close()
        print(f"Added {task_name} to your to-do list!")
    def removetask(self, task_name):
        file_data = self.load()
        removed = False
        for ind, tasks in enumerate(file_data):
            tname = tasks["Task Name"]
            if tname.lower() == task_name.lower():
                #MAYBE add functionality of double checking if user really wants to DELETE the task

                del file_data[ind] #remove the task and its information (ITS ENTIRE DICTIONARY)
                file = open(self.filename, "w")
                json.dump(file_data, file, indent=2)
                file.close()
                removed = True
                print(f"Successfully removed your {task_name} task!")
                break
        if not removed:
            print(f"{task_name} does not exist. Could not remove.")
    def get_all_tasks(self):
        all_tasks = self.load()
        print(f"Here are all your tasks...\n")
        for task in all_tasks:
            name = task["Task Name"]
            print(f"{name}:")
            for key,value in task.items():
                print(f"\t{key}: {value}")
    def get_task(self, task_name):
        file_data = self.load() #we now have a list (type = list)
        #Logic to check if task already exists
        found_task = False
        for task_info in file_data:
            #task_info is each dict (task and its other info)
            tname = task_info["Task Name"]
            if tname.lower() == task_name.lower():
                found_task = True
                print(f"{tname}:")
                for key,value in task_info.items():
                    print(f"\t{key}: {value}")
        if not found_task:
            print(f"You do not have a {task_name} task.")
    def update_task(self, task_name, new_name, description, due_date, completed, priority):
        file_data = self.load()
        for ind, task_info in enumerate(file_data):
            tname = task_info["Task Name"]
            if tname.lower() == task_name.lower():
                #do the logic here if we found a task that matches

                #if ANY of these fields are empty assume we want to take previously saved values
                if not new_name:
                    new_name = task_name
                if not description:
                    description = task_info["Description"]
                if not due_date: #retrieve old value first
                    due_date = task_info["Due Date"]
                if not completed:
                    completed = task_info["Completed"]
                if not priority:
                    priority = task_info["Priority"]
                if isinstance(due_date, datetime): #if it is a datetime object (NOT empty)
                    due_date = due_date.strftime("%m-%d-%Y")
                file_data[ind] = {"Task Name": new_name,
                "Description": description,
                "Due Date": due_date,
                "Completed": completed,
                "Priority": priority}
                file = open(self.filename, "w")
                json.dump(file_data, file, indent=2)
                file.close()
                print(f"Successfully updated your {task_name} task!")
                return
        print(f"{task_name} does not exist. Can only update a valid task.")
    def remove_all(self):
        file = open(self.filename, "w")
        json.dump([], file)
        file.close()
        print("Removed all tasks.")

