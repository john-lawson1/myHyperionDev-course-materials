"""
=================================TASK MANAGER=================================
This program is a Task Manager, which has the following functionality:
- The user is required to log in with valid username and password
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
    '''The main Task Manager program'''
    # User log in & creation of curr_user variable for user specific functions
    curr_user = login()
    # Create tasks.txt file if it does not exist
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            pass
    # Present user with the MAIN MENU to select desired task manager action
    main_menu(curr_user)

def login():
    '''Log in to Task Manager with a valid username and password.'''
    # Create user.txt file with a default account if it does not exist
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as user_file:
            user_file.write("admin;password")
    # Read user.txt file to return dictionary of usernames and passwords
    username_password = read_userfile()        
    # User can only log in with a valid username and password
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
    return curr_user

def main_menu(curr_user):
    '''Present the MAIN MENU to the user'''
    while True:
        # User input converted to lower case for handling incorrect capitalisation
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
            reg_user()
        # Run add task function    
        elif menu == 'at':
            add_task()
        # Run view all tasks function
        elif menu == 'va':
            view_all()
        # Run view my tasks function
        elif menu == 'vm':
            view_mine(curr_user)  
        # Run generate reports function
        elif menu == 'gr':
            generate_reports()
        # Only allow admin user to run the display statistics function
        elif menu == 'ds' and curr_user == 'admin':
            display_stats()
        # Exit the program
        elif menu == 'ex':
            print('\nGoodbye!!!')
            exit()
        # Error handling for invalid user input
        else:
            print("\nYou have made a wrong choice, Please Try again")

def reg_user():
    '''Add a new user to the user.txt file'''
    # Read user.txt file to return dictionary of usernames and passwords
    username_password = read_userfile()
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
        # If the paswords match, add the user and password to the user.txt file
        print("New user added")
        username_password[new_username] = new_password  
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))
    # Notify user that the passwords do not match before returning to the MAIN MENU
    else:
        print("Passwords do no match")

def add_task():
    '''Allow a user to add a new task to task.txt file with the following: 
         - A username of the person to whom the task is assigned
         - A title of a task
         - A description of the task
         - The due date of the task
    '''
    # Read user.txt file to return dictionary of usernames and passwords
    username_password = read_userfile()
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
    # Get the current date to set as the task assigned date
    curr_date = date.today()
    # Add the task data to the file task.txt and default task completed to 'No'
    updated_tasks = read_tasks()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    updated_tasks.append(new_task)
    # Write the updated task list to the task.txt file
    write_tasks(updated_tasks)

def view_all():
    '''Reads all the tasks from the task list variable and
        calls the display_task function to print to the console
    '''
    # Displays all tasks in the task list
    for task in read_tasks():
        display_task(task)
            
def view_mine(curr_user):
    '''Reads only the user's tasks from the task list variable, then:
        - calls the display_task function to print to the console
        - gives the user the option to select a task to edit or
        return to the main menu
    '''   
    # Displays only the current user's tasks from the task list
    my_tasks = []
    my_task_ids = []
    tasks = read_tasks()
    for task in tasks:
        if task['username'] == curr_user:
            display_task(task)
            my_tasks.append(task)
            my_task_ids.append(task['index'])
    # Give user a choice to edit a task or return to the main menu
    task_choice = 0
    while task_choice != -1:
        try:
            # Error handling for invalid integer task# entry
            task_choice = int(input("Enter a valid Task# to edit or -1 to return to the main menu: "))
        # Error handling for non-integer entry 
        except ValueError:
            print("Invalid Task# selection.")
        # Prevent user from editing another user's task
        else:
            if task_choice != -1 and task_choice not in my_task_ids:
                print(f"\nTask {task_choice} is not assigned to you.")
            else:
                for task in my_tasks:
                    # Prevent user from editing a completed task
                    if task['index'] == task_choice and task['completed']:
                        print(f"\nTask {task_choice} is already marked as complete and cannot be edited.")
                    # Present user with the EDIT MENU where valid task entered
                    elif task['index'] == task_choice and not task['completed']:
                        edit_menu(task_choice, curr_user)
                        break         

def edit_menu(task_choice, curr_user):
    '''Present the EDIT MENU to the user'''
    while True:
        # User input converted to lower case for handling incorrect capitalisation
        edit_choice =  input("""\nEDIT MENU
Select one of the following Edit Options below:
tc - Mark task as complete
ua - Edit user assigned to task
dd - Edit task due date                     
ex - Exit to Main Menu
: """).lower()
        # Run edit completed function
        if edit_choice == "tc":
            edit_completed(task_choice, curr_user)        
        # Run edit assigned user function
        elif edit_choice == "ua":
            edit_assigneduser(task_choice, curr_user)
        # Run edit due date function
        elif edit_choice == "dd":
            edit_duedate(task_choice, curr_user)
        # Exit to MAIN MENU
        elif edit_choice == "ex":
            print("\nReturning to MAIN MENU...")
            break
        # Error handling for invalid user input
        else:
            print("You made an invalid choice, Please Try again")

def edit_completed(task_choice, curr_user):
    '''Enable user to change the completion status of a task'''
    # loop to update completion status of selected task in full task list
    updated_tasks = []
    for task in read_tasks(): 
        # Find task selected for editing
        if task['index'] == task_choice:
            # Update task to 'complete'
            task['completed'] = True
            print(f"\nTask marked as complete...")
            display_task(task)
        # Append each task to the updated task list
        updated_tasks.append(task)
    # Update the task file with the updated task list
    write_tasks(updated_tasks)
    # Return user to MAIN MENU as the user cannot edit a completed task
    main_menu(curr_user)

def edit_assigneduser(task_choice, curr_user):
    '''Enable user to change the user assigned to a task'''
    # Read user.txt file to return dictionary of usernames and passwords
    username_password = read_userfile()
    # Loop to update assigned user of selected task in full task list
    updated_tasks = []
    for task in read_tasks():
        # Find task selected for editing
        if task['index'] == task_choice:
            # Show task to user before edit
            print(f"\nTask before assigned user update:")
            display_task(task)    
            # Error handling to ensure assigned username exists
            new_taskuser = input("Name of person to reassign task to: ")
            while new_taskuser not in username_password.keys():
                print("User does not exist. Please enter a valid username")
                new_taskuser = input("Name of person assigned to task: ")
            task["username"] = new_taskuser 
            # Show task to user after edit
            print(f"\nTask after assigned user update:")
            display_task(task)
        # Append each task to the updated task list
        updated_tasks.append(task)
    # Update the task file with the updated task list
    write_tasks(updated_tasks)
    # Return user to MAIN MENU so the user cannot edit another user's task
    main_menu(curr_user)

def edit_duedate(task_choice, curr_user):
    '''Enable user to change the due date of a task'''
    # Loop to update task due date of selected task in full task list
    updated_tasks = []
    for task in read_tasks():
        # Find task selected for editing
        if task['index'] == task_choice:
            # Show task to user before edit
            print(f"\nTask before due date update:")
            display_task(task)
            # Error handling to ensure user enters a date in the correct format
            while True:
                try:
                    new_duedate = input("New due date of task (YYYY-MM-DD): ")
                    due_date_time = datetime.strptime(new_duedate, DATETIME_STRING_FORMAT)
                    break
                except ValueError:
                    print("Invalid datetime format. Please use the format specified")
            task["due_date"] = due_date_time  
            # Show task to user after edit
            print(f"\nTask after due date update:")
            display_task(task)
        # Append each task to the updated task list
        updated_tasks.append(task)
    # Update the task file with the updated task list
    write_tasks(updated_tasks)
    # Return user to MAIN MENU as the user cannot edit a completed task
    main_menu(curr_user)

def generate_reports():
    '''Generate a task report & a user report and saves them to two text files.'''
    # Section to create the task_overview.txt file
    with open("task_overview.txt", "w") as taskoverview_file:
        # Create a task list variable from the task list file
        task_dict = read_tasks()
        # Initialises counts and percentages as zero
        count_complete = 0
        count_incomplete = 0
        count_overdue = 0
        per_incomplete = 0
        per_overdue  = 0
        # loop to increment task count variables for specified conditions
        for t in task_dict:
            if t['completed'] == True:
                count_complete += 1
            else:
                if t['due_date'] < datetime.today():
                    count_overdue += 1
                    count_incomplete += 1
                else:
                    count_incomplete += 1
        # Calculate percentages with zero division error handling
        if len(task_dict) != 0:
            per_incomplete = 100 * count_incomplete / len(task_dict)
            per_overdue = 100 * count_overdue / len(task_dict)
        # Create string of task stats to be written to the task_overview.txt file in a readable format
        task_str = f"=======================TASK OVERVIEW=======================\n"
        task_str += f"Total number of tasks:      \t{len(task_dict)}\n"
        task_str += f"Number of completed tasks:  \t{count_complete}\n"
        task_str += f"Number of uncompleted tasks:\t{count_incomplete}\t {per_incomplete:.2f}% of total tasks\n"
        task_str += f"Number of overdue tasks:    \t{count_overdue}\t {per_overdue:.2f}% of total tasks\n"
        taskoverview_file.write(task_str)
    # Notify user that the updates to the task_overview.txt file are complete
    print(f"\nTask Overview file successfully updated.")
    # Section to create the user_overview.txt file
    with open("user_overview.txt", "w") as useroverview_file:
        # Read user.txt file to return dictionary of usernames and passwords
        username_password = read_userfile()
        # Create and append header rows for user_overview.txt in a readable format
        user_str = f"=======================USER OVERVIEW=======================\n"
        user_str += f"Total number of users:\t{len(username_password)}\n"
        user_str += f"Total number of tasks:\t{len(task_dict)}\n"
        useroverview_file.write(user_str)
        # loop to calculate stats for each user
        for k in username_password.keys():
            # Initialises counts and percentages as zero
            count_user_tasks = 0
            count_user_tasks_complete = 0
            count_user_tasks_incomplete = 0
            count_user_tasks_overdue = 0
            per_user_tasks = 0
            per_user_tasks_complete = 0
            per_user_tasks_incomplete = 0
            per_user_overdue = 0
            # loop to increment count variables for specified conditions
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
                # Calculate percentages with zero division error handling
                if len(task_dict) != 0:
                    per_user_tasks = 100 * count_user_tasks / len(task_dict)
                if count_user_tasks != 0:
                    per_user_tasks_complete = 100 * count_user_tasks_complete / count_user_tasks
                    per_user_tasks_incomplete = 100 * count_user_tasks_incomplete / count_user_tasks
                    per_user_overdue = 100 * count_user_tasks_overdue / count_user_tasks
            # Create string of stats for a user to be appended to the user_overview.txt file in a readable format
            user_str = f"\nUser: {k}\n"
            user_str += f"Total number of tasks:     \t{count_user_tasks}\t {per_user_tasks:.2f}% of total tasks\n"
            user_str += f"Number of complete tasks:  \t{count_user_tasks_complete}\t {per_user_tasks_complete:.2f}% of total user tasks\n"
            user_str += f"Number of incomplete tasks:\t{count_user_tasks_incomplete}\t {per_user_tasks_incomplete:.2f}% of total user tasks\n"
            user_str += f"Number of overdue tasks:   \t{count_user_tasks_overdue}\t {per_user_overdue:.2f}% of total user tasks\n"
            useroverview_file.write(user_str)
            # Notify user that the stats of a user have been appended to the user_overview.txt file
            print(f"User Overview file successfully updated for {k}.")
    # Notify user that the updates to the user_overview.txt file are complete
    print(f"User Overview file update completed successfully.\n")

def display_stats():
    '''Displays task and user statistics on screen (for admin user only)'''
    # Create task and user overview report files in case they have not already been created 
    generate_reports()
    # Read task_overview.txt file to print task overview report
    with open("task_overview.txt", "r") as taskoverview_file:
        print(taskoverview_file.read())
    # Read user_overview.txt file to print user overview report
    with open("user_overview.txt", "r") as useroverview_file:
        print(useroverview_file.read()) 

def read_userfile():
    '''Read user.txt file and create a dictionary of usernames and passwords.'''
    # Create a username_password dictionary from the user.txt file.
    with open("user.txt", "r") as user_file:
        user_data = user_file.read().split("\n")
        username_password = {}
        for user in user_data:
            username, password = user.split(';')
            username_password[username] = password
        return username_password

def read_tasks():
    '''Creates an indexed task list from the task file'''
    # Read in task data from the task.txt file
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

def display_task(task):
    '''Prints the tasks to the console'''
    # Create string of stats that can be printed to the console in a readable format
    disp_str = f"Task#: \t\t {task['index']}\n"
    disp_str += f"Task: \t\t {task['title']}\n"
    disp_str += f"Assigned to: \t {task['username']}\n"
    disp_str += f"Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    disp_str += f"Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    disp_str += f"Task Complete? \t {'Yes' if task['completed'] else 'No'}\n"
    disp_str += f"Task Description: \n {task['description']}\n"
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


# Run the main program function
if __name__ ==  "__main__":
    main()