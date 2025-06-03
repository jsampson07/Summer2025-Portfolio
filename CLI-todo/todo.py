#This is main src code
import json
from tasks_db import TaskDB
import argparse

def main():
    db = TaskDB() #create TaskDB instance to use throughout the code

    #created the main parser for the application
    parser = argparse.ArgumentParser(prog='todo', description='CLI Todo Application')
    #created subparser to handle specific subcommands
    subparsers = parser.add_subparsers(dest="command", required=True)

    #access "add", "list", "remove", etc inputs via COMMAND var

    #add subparser
    add_parser  = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("task", type=str, help="Name of task to add")
    add_parser.add_argument("--description", type=str, help="Add a description for the task (optional)")
    add_parser.add_argument("--due_date", type=str, help="Put in a due date (optional)")
    add_parser.add_argument("--completed", type=bool, help="Completed or not? (True or False)")
    add_parser.add_argument("priority", type=str, help="Put 'low', 'medium', or 'high' priority for your task")

    #list subparser
    #for list parsers we want to be able to list either all tasks or one task
    list_parser = subparsers.add_parser("list", help="List all your tasks")
        #below allows us to specify ALL (optional) OR a specific task
    list_parser.add_argument("task", type=str, help="Name of the task to list")

    #remove subparser
    remove_parser = subparsers.add_parser("remove", help="Remove a specified task")
    remove_parser.add_argument("remove_task", type=str, help="Name of the task to remove")


    args = parser.parse_args()

if __name__ == "__main__":
    main()