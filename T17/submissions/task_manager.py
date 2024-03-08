"""
=================================TASK MANAGER=================================
This program is a Task Manager, with the following functionality:
- The user is required to log in with valid username and password
- A new task file will be created if one does not already exist
- The user is presented with a MAIN MENU with the following options:
    ru - Register a user
    at - Add a task
    va - View all tasks
    vm - View my task
    gr - Generate reports
    ds - Display statistics (admin user only)
    ex - Exit

- The 'vm' option allows users to choose a task to edit
- The user is presented with an EDIT MENU with the following options:
    tc - Mark task as complete
    ua - Edit user assigned to task
    dd - Edit task due date                     
    ex - Exit to Main Menu

Notes: 
1. Use the following username and password to access the admin rights 
    username: admin
    password: password
2. Ensure you open the whole folder for this task in VS Code otherwise the 
program will look in your root directory for the text files.
"""

# Import libraries
import os
from datetime import datetime, date

# Set date string format
DATETIME_STRING_FORMAT = "%Y-%m-%d"

def main():
    #====Login Section====
    # If no user.txt file, write one with a default account
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")
    # Read in user_data
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")
    # Convert user data to a dictionary
    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password
    # log in with an existing account or the default account
    logged_in = False
    while not logged_in:
        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        # Error handling for invalid user
        if curr_user not in username_password.keys():
            print("User does not exist")
            continue
        # Error handling for incorrect user password
        elif username_password[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            print("Login Successful!")
            logged_in = True

    #====Prepare Task File Section====
    # Create tasks.txt if it doesn't exist
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            pass

    #====MAIN MENU Section====
    # Present the MAIN MENU to the user and convert user input to lower case
    while True:
        menu = input('''\nMAIN MENU
Select one of the following Options below:
ru - Register a user
at - Add a task
va - View all tasks
vm - View my tasks
gr - Generate reports
ds - Display statistics (admin user only)
ex - Exit
: ''').lower()
        # Run register user function
        if menu == 'ru':
            reg_user(username_password)
        # Run add task function    
        elif menu == 'at':
            add_task(username_password)
        # Run view all tasks function
        elif menu == 'va':
            view_all()
        # Run view my tasks function
        elif menu == 'vm':
            view_mine(curr_user, username_password)  
        # Only allow admin user to display the number of users and tasks
        elif menu == 'gr':
            generate_reports(username_password)
        # Run generate reports function
        elif menu == 'ds' and curr_user == 'admin':
            '''Modify the menu option that allows the admin to display statistics so that
                the reports generated are read from tasks.txt and user.txt and displayed
                on the screen in a user-friendly manner. If these text files don’t exist
                because the user hasn’t selected to generate them yet), first call the code
                to generate the text files.
            '''
            num_users = len(username_password.keys())
            num_tasks = len(read_tasks())
            print("-----------------------------------")
            print(f"Number of users: \t\t {num_users}")
            print(f"Number of tasks: \t\t {num_tasks}")
            print("-----------------------------------")    
        # Exits the program
        elif menu == 'ex':
            print('\nGoodbye!!!')
            exit()
        # Error handling for invalid user input
        else:
            print("\nYou have made a wrong choice, Please Try again")

def read_tasks():
    '''Creates an indexed task list from the task file'''
    # Read in task data
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]
    # Create an indexed task list from task data
    task_list = []
    for index, t_str in enumerate(task_data,1):
        curr_t = {}
        # Split by semicolon and manually add each component
        task_components = t_str.split(";")
        curr_t['index'] = index
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False
        task_list.append(curr_t)
    return task_list

def display_task(t):
    '''Prints the tasks to the console in the format of Output 2
        presented in the task pdf (i.e. includes spacing and labelling)
    '''
    disp_str = f"Task#: \t\t {t['index']}\n"
    disp_str += f"Task: \t\t {t['title']}\n"
    disp_str += f"Assigned to: \t {t['username']}\n"
    disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    disp_str += f"Task Complete? \t {'Yes' if t['completed'] else 'No'}\n"
    disp_str += f"Task Description: \n {t['description']}\n"
    print(f"{'_' * 60}\n{disp_str}")

def write_tasks(updated_tasks):
    '''Writes the updated task list to the task file'''
    # Open the task file and repopulate with the updated task list
    with open("tasks.txt", "w") as task_file:
        # Convert indexed task list back to a semicolon separated task format
        task_list_to_write = []
        for t in updated_tasks:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        # Write each semicolon separated task to the task file
        task_file.write("\n".join(task_list_to_write))
    print("Task file successfully updated.")

def generate_reports(username_password):
    '''When the user chooses to generate reports, two text files, called
        task_overview.txt and user_overview.txt, should be generated. Both
        these text files should output data in a user-friendly, easy to read manner.

            o task_overview.txt should contain:
                ▪ The total number of tasks that have been generated and
                tracked using the task_manager.py.
                ▪ The total number of completed tasks.
                ▪ The total number of uncompleted tasks.
                ▪ The total number of tasks that haven’t been completed and
                that are overdue.
                ▪ The percentage of tasks that are incomplete.
                ▪ The percentage of tasks that are overdue.

            o user_overview.txt should contain:
                ▪ The total number of users registered with task_manager.py.
                ▪ The total number of tasks that have been generated and
                tracked using task_manager.py.
                ▪ For each user also describe:
                ▪ The total number of tasks assigned to that user.
                ▪ The percentage of the total number of tasks that have
                been assigned to that user
                ▪ The percentage of the tasks assigned to that user that
                have been completed
                ▪ The percentage of the tasks assigned to that user that
                must still be completed
                ▪ The percentage of the tasks assigned to that user that
                has not yet been completed and are overdue
    '''

    if not os.path.exists("task_overview.txt"):
        with open("task_overview.txt", "w") as default_file:
            pass

    task_dict = read_tasks()
    count_complete = 0
    count_incomplete = 0
    count_overdue = 0
    for t in task_dict:
        if t['completed'] == True:
            count_complete += 1
        else:
            if t['due_date'] < datetime.today():
                count_overdue += 1
                count_incomplete += 1
            else:
                count_incomplete += 1
        
    if len(task_dict) == 0:
        per_incomplete = 0
    else: per_incomplete = 100 * count_incomplete / len(task_dict)
    if len(task_dict) == 0:
        per_overdue  = 0
    else: per_overdue = 100 * count_overdue / len(task_dict)
    print(f"=======================TASK OVERVIEW=======================")
    print(f"Total number of tasks:\t\t{len(task_dict)}")
    print(f"number of completed tasks:\t{count_complete}")
    print(f"number of uncompleted tasks:\t{count_incomplete}\t {per_incomplete:.2f}% of total tasks")
    print(f"number of overdue tasks:\t{count_overdue}\t {per_overdue:.2f}% of total tasks")
    
    task_str = f"=======================TASK OVERVIEW=======================\n"
    task_str += f"Total number of tasks:\t\t\t{len(task_dict)}\n"
    task_str += f"Number of completed tasks:\t\t{count_complete}\n"
    task_str += f"Number of uncompleted tasks:\t{count_incomplete}\t {per_incomplete:.2f}% of total tasks\n"
    task_str += f"Number of overdue tasks:\t\t{count_overdue}\t {per_overdue:.2f}% of total tasks\n"

    with open("task_overview.txt", "w") as taskoverview_file:
        taskoverview_file.write(task_str)
        print(f"\nTask Overview file successfully updated.\n")

    '''When the user chooses to generate reports, two text files, called
        task_overview.txt and user_overview.txt, should be generated. Both
        these text files should output data in a user-friendly, easy to read manner.

            o user_overview.txt should contain:
                ▪ The total number of users registered with task_manager.py.
                ▪ The total number of tasks that have been generated and
                tracked using task_manager.py.
                ▪ For each user also describe:
                ▪ The total number of tasks assigned to that user.
                ▪ The percentage of the total number of tasks that have
                been assigned to that user
                ▪ The percentage of the tasks assigned to that user that
                have been completed
                ▪ The percentage of the tasks assigned to that user that
                must still be completed
                ▪ The percentage of the tasks assigned to that user that
                has not yet been completed and are overdue
    '''
    
    if not os.path.exists("user_overview.txt"):
        with open("user_overview.txt", "w") as default_file:
            pass

    with open("user_overview.txt", "w") as taskoverview_file:
        print(f"=======================USER OVERVIEW=======================")
        print(f"Total number of users:\t\t{len(username_password)}")
        print(f"Total number of tasks:\t\t{len(task_dict)}")
        
        user_str = f"=======================USER OVERVIEW=======================\n"
        user_str += f"Total number of users:\t\t{len(username_password)}\n"
        user_str += f"Total number of tasks:\t\t{len(task_dict)}\n"
        taskoverview_file.write(user_str)
    
        for k in username_password.keys():
            
            count_user_tasks = 0
            count_user_tasks_complete = 0
            count_user_tasks_incomplete = 0
            count_user_tasks_overdue = 0
            per_user_tasks = 0
            per_user_tasks_complete = 0
            per_user_tasks_incomplete = 0
            per_user_overdue = 0

            for t in task_dict:
                if t['username'] ==  k and t['completed'] == True:
                    count_complete += 1
                    count_user_tasks += 1
                    count_user_tasks_complete += 1
                elif t['username'] ==  k and t['due_date'] < datetime.today():
                    count_overdue += 1
                    count_incomplete += 1
                    count_user_tasks += 1
                    count_user_tasks_overdue += 1
                    count_user_tasks_incomplete += 1
                elif t['username'] ==  k:
                    count_incomplete += 1
                    count_user_tasks += 1
                    count_user_tasks_incomplete += 1
            
                if len(task_dict) != 0:
                    per_user_tasks = 100 * count_user_tasks / len(task_dict)
            
                if count_user_tasks != 0:
                    per_user_tasks_complete = 100 * count_user_tasks_complete / count_user_tasks
                    per_user_tasks_incomplete = 100 * count_user_tasks_incomplete / count_user_tasks
                    per_user_overdue = 100 * count_user_tasks_overdue / count_user_tasks

            print(f"\nUser: {k}")
            print(f"Total number of tasks:\t\t{count_user_tasks}\t {per_user_tasks:.2f}% of total tasks")
            print(f"Number of completed tasks:\t{count_user_tasks_complete}\t {per_user_tasks_complete:.2f}% of total tasks")
            print(f"Number of incomplete tasks:\t{count_user_tasks_incomplete}\t {per_user_tasks_incomplete:.2f}% of total tasks")
            print(f"Number of overdue tasks:\t{count_user_tasks_overdue}\t {per_user_overdue:.2f}% of total tasks")
            
            user_str = f"\nUser: {k}\n"
            user_str += f"Total number of tasks:\t\t{count_user_tasks}\t {per_user_tasks:.2f}% of total tasks\n"
            user_str += f"Number of complete tasks:\t{count_user_tasks_complete}\t {per_user_tasks_complete:.2f}% of total tasks\n"
            user_str += f"Number of incomplete tasks:\t{count_user_tasks_incomplete}\t {per_user_tasks_incomplete:.2f}% of total tasks\n"
            user_str += f"Number of overdue tasks:\t{count_user_tasks_overdue}\t {per_user_overdue:.2f}% of total tasks\n"
                
            taskoverview_file.write(user_str)
            print(f"\nUser Overview file successfully updated for {k}.")

    print(f"\nUser Overview file update completed successfully.")

def reg_user(username_password):
    '''Add a new user to the user.txt file'''
    # Request input of a new username
    new_username = input("New Username: ")
    # Check if the user already exists
    while new_username in username_password.keys():
        print("Username already exists. Please add user with a different username.")
        # Allow user to enter a different username
        new_username = input("New Username: ")
    # Request input of a new password
    new_password = input("New Password: ")
    # Request input of password confirmation
    confirm_password = input("Confirm Password: ")
    # Check if the new password and confirmed password are the same
    if new_password == confirm_password:
        # If they are the same, add them to the user.txt file
        print("New user added")
        username_password[new_username] = new_password  
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))
    # Present a message if passwords do not match
    else:
        print("Passwords do no match")

def add_task(username_password):
    '''Allow a user to add a new task to task.txt file
        by prompting the user for the following: 
         - A username of the person whom the task is assigned to,
         - A title of a task,
         - A description of the task and 
         - the due date of the task.
    '''
    # Request input of an existing username for the task
    task_username = input("Name of person assigned to task: ")
    # Check if username exists
    while task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        # Allow user to enter an existing username for the task
        task_username = input("Name of person assigned to task: ")
    # Request user to enter a title for the task
    task_title = input("Title of Task: ")
    # Request user to enter a description for the task
    task_description = input("Description of Task: ")
    # Request user to enter a due date for the task, in a specified format
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")
    # Get the current date
    curr_date = date.today()
    updated_tasks = read_tasks()
    # Add the task data to the file task.txt and default task completed to 'No'
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    updated_tasks.append(new_task)
    write_tasks(updated_tasks)

def view_all():
    '''Reads all the tasks from the task list variable and
        calls the display_task function to print to the console
    '''
    # Displays all tasks in the task list
    for t in read_tasks():
        display_task(t)
            
def view_mine(curr_user, username_password):
    '''Reads only the user's tasks from the task list variable, then:
        - calls the display_task function to print to the console
        - gives the user the option to select a task to edit or
        return to the main menu
    '''   
    # Displays only the current user's tasks from the task list
    my_tasks = []
    for t in read_tasks():
        if t['username'] == curr_user:
            display_task(t)
            my_tasks.append(t['index'])
    # Give user a choice to edit a task or return to the main menu
    task_choice = 0
    while task_choice != -1:
        try:
            # Error handling for invalid integer task# entry
            if task_choice not in my_tasks:
                task_choice = int(input("Enter a Task# to edit or -1 to return to the main menu: "))
            # Present user with the EDIT MENU where valid task entered
            else:
                edit_menu(task_choice, username_password)
                break
        # Error handling for non-integer entry 
        except ValueError:
            print("Invalid Task# selection.") 

def edit_menu(task_choice, username_password):
    '''Present the EDIT MENU to the user and convert user input to lower case'''
    # Present the EDIT MENU to the user and convert user input to lower case
    while True:
        edit_choice =  input("""\nEDIT MENU
Select one of the following Edit Options below:
tc - Mark task as complete
ua - Edit user assigned to task
dd - Edit task due date                     
ex - Exit to Main Menu
: """).lower()
        # Run edit completed function
        if edit_choice == "tc":
            edit_completed(task_choice)        
        # Run edit assigned user function
        elif edit_choice == "ua":
            edit_assigneduser(task_choice, username_password)
        # Run edit due date function
        elif edit_choice == "dd":
            edit_duedate(task_choice)
        # Exit to MAIN MENU
        elif edit_choice == "ex":
            print("\nReturning to MAIN MENU...")
            break
        # Error handling for invalid user input
        else:
            print("You made an invalid choice, Please Try again")

def edit_completed(task_choice):
    '''Enable user to change the completion status of a task'''
    updated_tasks = []
    for t in read_tasks(): 
        # Find task selected for editing
        if t['index'] == task_choice:
            # Prevent user from editing a completed task
            if t["completed"]:
                print("\nTask is already marked as complete.")
            else:
                t["completed"] = True
                print(f"\nTask marked as complete...")
                display_task(t)
        # Create updated task list
        updated_tasks.append(t)
    # Update the task file
    write_tasks(updated_tasks)

def edit_assigneduser(task_choice, username_password):
    '''Enable user to change the user assigned to a task'''
    updated_tasks = []
    for t in read_tasks():
        # Find task selected for editing
        if t['index'] == task_choice:
            # Prevent user from editing a completed task
            if t["completed"]:
                print("A completed task cannot be edited.")
                break
            # Show task to user before edit
            print(f"\nTask before assiged user update:")
            display_task(t)    
            # Error handling to ensure assigned username exists
            new_taskuser = input("Name of person to reassign task to: ")
            while new_taskuser not in username_password.keys():
                print("User does not exist. Please enter a valid username")
                new_taskuser = input("Name of person assigned to task: ")
            t["username"] = new_taskuser 
            # Show task to user after edit
            print(f"\nTask after assigned user update:")
            display_task(t)
        updated_tasks.append(t)
    # Update the task file
    write_tasks(updated_tasks)

def edit_duedate(task_choice):
    '''Enable user to change the due date of a task'''
    curr_tasks = []
    for t in read_tasks():
        # Find task selected for editing
        if t['index'] == task_choice:
            # Prevent user from editing a completed task
            if t["completed"]:
                print("A completed task cannot be edited.")
                break  
            # Show task to user before edit
            print(f"\nTask before due date update:")
            display_task(t)
            # Error handling to ensure user enters a date in the correct format
            while True:
                try:
                    new_duedate = input("New due date of task (YYYY-MM-DD): ")
                    due_date_time = datetime.strptime(new_duedate, DATETIME_STRING_FORMAT)
                    break
                except ValueError:
                    print("Invalid datetime format. Please use the format specified")
            t["due_date"] = due_date_time  
            # Show task to user after edit
            print(f"\nTask after due date update:")
            display_task(t)
        curr_tasks.append(t)
    # Update the task file
    write_tasks(curr_tasks)


# Run the main program function
if __name__ ==  "__main__":
    main()