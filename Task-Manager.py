import getpass
import csv
import random
import os

# Load existing registered users from CSV file
def load_registered_users_csv(filename):
    print("Loading registered users....")
    # Create dictionary to store username and password
    registered_users_csv = {}
    # Try block to check for errors (if file doesn't exist in this case)
    try:
        # Use 'with' statement instead of file.close() after code runs
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            # Create variable reader
            reader = csv.reader(file)
            for row in reader:
                # row[0] is the username, row[1] is the password in the dictionary
                registered_users_csv[row[0]] = row[1]
    except FileNotFoundError:
        print(f'{filename} not found. Starting with a blank user list.')
    return registered_users_csv

# Save registered users to CSV file
def save_registered_users_csv(registered_users_csv, filename):
    print("Saving registered users...")
    # Use 'with' statement instead of file.close() after code runs
    # mode='w' is write mode
    # encoding='utf-8' is character encoding standard
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        # Create variable writer
        writer = csv.writer(file)
        # Use .items() to return username and password as a pair/tuple
        for user_name, password in registered_users_csv.items():
            # Use csv method writerow() and brackets for variables to go in dictionary
            writer.writerow([user_name, password])

# Creating function for NEW register_user()
def register_user():
    print("Registering new user...")
    # Define/declare global variable
    global registered_users
    # Create a while loop incase username is taken
    while True:
        user_name = input('Please enter a username: ')
        if user_name in registered_users:
            print('This username is already registered. Please try again.')
        else:
            # Hide password using getpass module and getpass function
            password = getpass.getpass('Please enter your password: ')
            # Store username and password in dictionary
            registered_users[user_name] = password
            # Save new entries to users.csv
            save_registered_users_csv(registered_users, 'users.csv')
            print(f'Thank you, {user_name}. Your username and password have been accepted. Registration complete.')
            #create task tracker list
            task_tracker = load_task_tracker('tasks.csv')           
            while True:
                display_menu()
                select = input("Please enter your menu selection: ")
                if select == '1':
                     add_task(task_tracker)
                elif select == '2':
                    view_task_tracker(task_tracker)
                elif select == '3':
                    mark_task(task_tracker)
                elif select == '4':
                    delete_task(task_tracker)
                elif select == '5':
                    save_task_tracker(task_tracker, 'tasks.csv')
                    exit_program()
                    break
                else:
                    print("Invalid selection. Please enter 1-5 only.")              
            # Break if username is unique and don't loop back
            break
            
#define the exit_program function
def exit_program():
    print('You have left the task tracker.')

def save_task_tracker(task_tracker, filename):
    header = ['ID', 'Task', 'Status']
    #mode='w' is write mode
    #encoding='utf-8' is character encoding standard
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        #csv.DictWriter is a predefined class in Python's csv module and data is in a dictionary. Could use csv.writer if only in lists
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(task_tracker)
    print('Tasks saved to', filename)

#loading task tracker after login
def load_task_tracker(filename):
    print("Loading task tracker...")
    task_tracker = []
    try:
        #use 'with' statement instead of file.close() after code runs
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                task_tracker.append(row)
    except FileNotFoundError:
        print(f"{filename} not found. Starting with a blank task tracker.")
    return task_tracker


#1. add tasks with random ID
def add_task(task_tracker):
    #produce a random ID number
    ID = random.randint(1, 1000)
    Task = input("Enter a task: ")
    Status = 'Pending'
    task_tracker.append({'ID': ID, 'Task': Task, 'Status': Status})
    print("task added!")

#2. define function to view the task tracker
def view_task_tracker(task_tracker):
    print('These are your existing tasks: ')
    #enumerate loops through the task_tracker starting at 1. instead of 0
    for i, task in enumerate(task_tracker, start=1):
        print(f"{i}. {task['ID']} - {task['Task']}: {task['Status']}")
        
#3. define function to mark task complete
def mark_task(task_tracker):
    #change to integer since user will input a number
    task_id = int(input("Enter the ID of the task status you would like to update: "))
    for task in task_tracker:
        #match ID from the dictionary to the ID entered
        if int(task['ID']) == task_id:
            if task['Status'] == 'Pending':
                task['Status'] = 'Complete'
                print(f"Task {task_id} has been marked complete.")
            else:
                print(f"Task {task_id} has already been completed.")
            return
    print(f"Task {task_id} not found.")

#4. define function to delete a task
def delete_task(task_tracker):
    task_id = int(input("Enter the ID of the task you would like to delete: "))
    for task in task_tracker:
        if int(task['ID']) == task_id:
           task_tracker.remove(task)
           print(f"Task {task_id} has been deleted.")
           break
    else:
        print(f"Task {task_id} not found.")
                  
#menu
def display_menu():
    print("\nMenu:")
    print("1. Add a task")
    print("2. View tasks")
    print("3. Mark a task complete")
    print("4. Delete a task")
    print("5. Logout")

# Login
def login_user():
    print("Logging in...")
    global registered_users
    user_name = input('Please enter your username: ')
    # getpass.getpass instead of input to hide password
    password = getpass.getpass('Please enter your password: ')
    # Check to see if username is in dictionary and if the password matches it
    if user_name in registered_users and registered_users[user_name] == password:
        print(f'Login successful! You may now use the Task Manager')
        task_tracker = load_task_tracker('tasks.csv')
        while True:
            display_menu()
            select = input("Please enter your menu selection: ")
            if select == '1':
                 add_task(task_tracker)
            elif select == '2':
                view_task_tracker(task_tracker)
            elif select == '3':
                mark_task(task_tracker)
            elif select == '4':
                delete_task(task_tracker)
            elif select == '5':
                save_task_tracker(task_tracker, 'tasks.csv')
                exit_program()
                break
            else:
                print("Invalid selection. Please enter 1-5 only.")        
    else:
        print(f'Login failed. Please check your username and password and try again.')

# Load previous users
registered_users = load_registered_users_csv('users.csv')

#__name__ is a built-in variable in Python assigned to the module name. __name__ is set to __main__ when run directly vs an imported script
if __name__ == "__main__":
    while True:
        # Menu to select login or register
        print('1. Register a new user')
        print('2. Login existing user')
        choice = input('Please choose an option: ')
        if choice == '1':
            register_user()
        elif choice == '2':
            login_user()
            break
        else:
            print('Invalid choice. Please enter 1 or 2.')
