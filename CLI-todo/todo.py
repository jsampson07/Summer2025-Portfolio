#This is main src code
import json
from tasks_db import TaskDB
import argparse
from datetime import datetime

def validate_date(date):
    try:
        return datetime.strptime(date, "%m-%d-%Y")
    except ValueError:
        raise argparse.ArgumentTypeError("Due-Date must be in the format MM-DD-YYYY")

def main():
    db = TaskDB() #create TaskDB instance to use throughout the code

    #created the main parser for the application
    parser = argparse.ArgumentParser(prog='todo', description='CLI Todo Application')
    #created subparser to handle specific subcommands
    subparsers = parser.add_subparsers(dest="command", required=True)

    #access "add", "list", "remove", etc inputs via COMMAND var
    #for any arguments not specified (if optional) value = None (blank)

    #add subparser
    add_parser  = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("task", type=str, help="Name of task to add")
    add_parser.add_argument("--description", type=str, help="Add a description for the task (optional)")
    add_parser.add_argument("--due_date", type=validate_date, help="Put in a due date (optional)")
    add_parser.add_argument("--completed", action="store_true", help="Completed or not? (True or False)")
        #action keyword argument ==> "store_true" stores True if flag is present
    add_parser.add_argument("priority", type=str, help="Put 'low', 'medium', or 'high' priority for your task")

    #list subparser
    #for list parsers we want to be able to list either all tasks or one task
    list_parser = subparsers.add_parser("list", help="List all your tasks")
        #below allows us to specify ALL (optional) OR a specific task
    list_parser.add_argument("--task", type=str, help="Name of the task to list")

    #remove subparser
    remove_parser = subparsers.add_parser("remove", help="Remove a specified task")
    remove_parser.add_argument("task", type=str, help="Name of the task to remove")
    
    remove_all_parser = subparsers.add_parser("remall", help="Remove all tasks") #mainly used for testing

    #update subparser
    update_parser = subparsers.add_parser("update", help="Update an existing task")
    update_parser.add_argument("task", type=str, help="Name of task to update")
    update_parser.add_argument("--taskname", type=str, help="new name")
    update_parser.add_argument("--description", type=str, help="Add a description for the task (optional)")
    update_parser.add_argument("--due_date", type=validate_date, help="Put in a due date (optional)")
    update_parser.add_argument("--completed", action="store_true", help="Completed or not? (True or False)")
        #action keyword argument ==> "store_true" stores True if flag is present
    update_parser.add_argument("--priority", type=str, help="Put 'low', 'medium', or 'high' priority for your task")

    args = parser.parse_args()
    #print(type(args))
    #args creates a Namespace object that has all attributes assigned to it for current iteration
        #i.e. args.command, args.priority, args.task (does not matter abt subparsers --> the overall argparse.Namspace obj has all attributes)
    if args.command == "add":
        db.addtask(args.task, args.description, args.due_date, args.completed, args.priority)
    elif args.command == "list":
        if args.task:
            db.get_task(args.task)
        else:
            db.get_all_tasks()
    elif args.command == "remove":
        db.removetask(args.task)
    elif args.command == "update":
        db.update_task(args.task, args.taskname, args.description, args.due_date, args.completed, args.priority)
    elif args.command == "remall":
        db.remove_all()

if __name__ == "__main__":
    main()