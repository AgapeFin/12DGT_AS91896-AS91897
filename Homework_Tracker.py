import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from datetime import datetime
import json
import os

# DATA ---------------------
# Name of the file where homework will be saved and loaded
DATA_FILE = "homework.json"

# this list keeps all the homework tasks (while the app is still on)
homework_data = []

COLOUR_PRIORITY = {"High": "#d000ff", "Medium": "#ff006f", "Low": "#ff8400"}

COLOUR_STATUS = {"Complete":"#5988FF", "Incomplete":"#FF0000"}

# stops a task/due date field from breaking the layout with huge input
MAX_FIELD_LENGTH = 40

def limit_length(new_value):
    ## Tkinter calls this on every keystroke; returning False blocks the edit
    return len(new_value) <= MAX_FIELD_LENGTH

def is_valid_date(text):
    ## Checks the due date is a real calendar date in DD/MM/YYYY format
    try:
        datetime.strptime(text, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def load_data(): ## Loads saved homework tasks from the JSON file and puts in homework_data
    global homework_data

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            homework_data = json.load(file)

def save_data(): ## The homework_data from before is written so that tasks won't be lost after app closes
    with open(DATA_FILE, "w") as file:
        json.dump(homework_data, file, indent=4)

#clear content function ----------
def clear_content(): ## removes all the widgets that are currently being shown
    for widget in content_frame.winfo_children():
        widget.destroy()

#show dashboard function ----------------------
def show_dashboard(): ## just shows the main dashboard page

    clear_content()
    #shows the main welcome message and upcoming tasks
    title = ttk.Label(content_frame, text="Welcome Back!", font=("Arial", 20, "bold"))
    title.pack(pady=15)

    ttk.Label(content_frame, text="Upcoming Tasks", font=("Arial", 14, "bold")).pack(anchor="w", padx=20)

    # shows the tasks in a listbox
    upcoming_list = tk.Listbox(content_frame, width=70, height=8)
    upcoming_list.pack(padx=20, pady=5)

    completed_count = 0

    ## loops through every task once, then sorts into "upcoming" or just count it if it already complete
    for task in homework_data:

        if task["status"] =="Complete":
            completed_count += 1
        else:
            upcoming_list.insert(tk.END, f"{task['subject']} - {task['task']} ({task['due_date']})")
            colour = COLOUR_PRIORITY.get(task["priority"], "#FFFFFF")
            upcoming_list.itemconfig(tk.END, bg=colour)

    ttk.Label(content_frame, text="Completed Tasks", font=("Arial", 14, "bold")).pack(anchor="w", padx=20, pady=(10, 0))

    completed_list = tk.Listbox(content_frame, width=70, height=5)
    completed_list.pack(padx=20)

    ## loops through every task and adds it to the completed list if it's marked as complete
    for task in homework_data:

        if task["status"] =="Complete":
            completed_list.insert(tk.END, f"✓ {task['subject']} - {task['task']}")
            completed_list.itemconfig(tk.END, bg=COLOUR_STATUS["Complete"])

    ## Shows a summary of the total tasks and completed tasks
    summary = ttk.Label(content_frame, text=f"Total Tasks: {len(homework_data)}    Completed: {completed_count}", font=("Arial", 12))
    summary.pack(pady=20)
# ------
def get_selected_index(tree): # finds the homework_data index for the selected task in the treeview widget
    selection = tree.selection()
    if not selection:
        messagebox.showerror("Error", "Please select a task first.")
        return None
    return int(selection[0]) # uses the homework_data index as an id

def edit_selected_index(tree):
    index = get_selected_index(tree)
    if index is None:
        return
    show_add_task(edit_index=index) # Opens the add/edit form already with the data of selected task.


def delete_index(tree):
    index = get_selected_index(tree)
    if index is None:
        return
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?")
    if not confirm:
        return
    
    homework_data.pop(index) # removes the task from homework_data
    save_data() # saves the updated homework_data to the JSON file
    show_homework()
    messagebox.showinfo("Deleted", "Task has been deleted successfully.")

def complete_toggle(tree):
    index = get_selected_index(tree)
    if index is None:
        return
    task = homework_data[index]
    if task["status"] == "Complete":
        task["status"] = "Incomplete"
    else:
        task["status"] = "Complete"
    save_data()
    show_homework()


def show_homework():
    ## This function will show the homework page shown as a table
    clear_content()

    ttk.Label(content_frame, text="Homework", font=("Arial", 20, "bold")).pack(pady=15)
    ## Homework page will be shown here using a treeview widget.
    tree = ttk.Treeview(content_frame, columns=("Subject", "Task", "Due Date", "Priority", "Status"), show="headings")

    headings = ["Subject", "Task", "Due Date", "Priority", "Status"]

## sets the column header text and header width for each column
    for heading in headings:
        tree.heading(heading, text=heading)
        tree.column(heading, width=120)

    for priority, colour in COLOUR_PRIORITY.items(): # Create colour for each priority level for rows
        tree.tag_configure(priority, background=colour)
    tree.tag_configure("Complete", background=COLOUR_STATUS["Complete"])

    for index, task in enumerate(homework_data): # Add each task to the treeview with the right colours
        # Completed tasks will be blue, if not then will be based on priority level
        tag = "Complete" if task["status"] == "Complete" else task["priority"]
        tree.insert("", tk.END, iid=str(index), values=(task["subject"], task["task"], task["due_date"], task["priority"], task["status"]), tags=(tag,),)

    tree.pack(fill="both", expand=True, padx=20, pady=10)

    button_row = ttk.Frame(content_frame)
    button_row.pack(pady=10)
    #buttons for edit delete and toggle complete task
    ttk.Button(button_row, text="Edit", command=lambda: edit_selected_index(tree)).pack(side="left", padx=5)
    ttk.Button(button_row, text="Delete", command=lambda: delete_index(tree)).pack(side="left", padx=5)
    ttk.Button(button_row, text="Toggle Complete", command=lambda: complete_toggle(tree)).pack(side="left", padx=5)

subject_box = None
task_box = None
due_box = None
priority_box = None

def add_homework():
    if(subject_box.get() == "" or task_box.get() == "" or due_box.get() == "" or priority_box.get() == ""):
        messagebox.showerror("Error", "Please complete all fields.")
        return

    if not is_valid_date(due_box.get()):
        messagebox.showerror("Error", "Please enter the due date as DD/MM/YYYY.")
        return

    new_task = {"subject": subject_box.get(), "task": task_box.get(), "due_date": due_box.get(), "priority": priority_box.get(), "status": "Incomplete",}

    if editing_index is None:
        homework_data.append(new_task)
        messagebox.showinfo("Success", "Homework added.")
    else:
        new_task["status"] = homework_data[editing_index]["status"]
        homework_data[editing_index] = new_task
        messagebox.showinfo("Success", "Homework updated.")
    save_data()
    show_dashboard()

def show_add_task(edit_index=None):
    global subject_box, task_box, due_box, priority_box, editing_index
    editing_index = edit_index
    clear_content()

    if edit_index is not None:
        page_title = "Edit Homework"
    else:
        page_title = "Add Homework"

    ttk.Label(content_frame, text=page_title, font=("Arial", 20, "bold")).pack(pady=20)

    form = ttk.Frame(content_frame) # just a frame widget to hold the textboxes
    form.pack()

    ttk.Label(form, text="Subject").grid(row=0, column=0, pady=5)
    subject_box = ttk.Combobox(form, values=["Maths", "English", "Science", "History", "PE", "Other"])
    subject_box.grid(row=0, column=1)

    # %P passes Tkinter the proposed new text so limit_length can check it
    vcmd = (root.register(limit_length), "%P")

    ttk.Label(form, text="Task").grid(row=1, column=0, pady=5)
    task_box = tk.Entry(form, width=30, validate="key", validatecommand=vcmd)
    task_box.grid(row=1, column=1)

    ttk.Label(form, text="Due date (DD/MM/YYYY)").grid(row=2, column=0, pady=5)
    due_box = tk.Entry(form, width=30, validate="key", validatecommand=vcmd)
    due_box.grid(row=2, column=1)

    ttk.Label(form, text="Priority").grid(row=3, column=0, pady=5)
    priority_box = ttk.Combobox(form, state="readonly", values=["High", "Medium", "Low"])
    priority_box.grid(row=3, column=1)

    if editing_index is not None:
        task = homework_data[edit_index]
        subject_box.set(task["subject"])
        task_box.insert(0, task["task"])
        due_box.insert(0, task["due_date"])
        priority_box.set(task["priority"])

    if edit_index is not None:
        button_text = "Update Homework"
    else:
        button_text = "Save Homework"

    ttk.Button(content_frame, text=button_text, command=add_homework).pack(pady=20)


# shows the help page - explains how to use the app
def show_help():

    clear_content()

    ttk.Label(content_frame, text="Help Page", font=("Arial", 20, "bold")).pack(pady=20)

    help_text = ("Dashboard - shows some upcoming tasks and completed tasks, gives a quick summary\n\n"
                 "Homework - shows every task in a table, colour-coded by status (blue if completed), by priority with high being purple, medium being pink, low as orange.\n\n"
                 "Select a row and either:\n"
                 "Edit: Reopens the form with the task's details prefilled\n"
                 "Delete: removes the task (asks to confirm first)\n"
                 "Toggle Complete: Switches the task between Complete and Incomplete\n\n"
                 "Add Task - Fill in the form; Subject, Task, Due Date and Priority. Then, click Save Homework. All fields are REQUIRED. Due Date must be a real date in DD/MM/YYYY format. Task/Due Date have a character limit (40).\n\n"
                 "Exit - Closes app. Note: Tasks are saved automatically any time you add, edit, delete, or toggle. Data won't be lost.")

    ttk.Label(content_frame, text=help_text, font=("Arial", 12), justify="left", wraplength=700).pack(padx=30, pady=10, anchor="w")


# Main Window (Everything below this line will run once when program start) --------------------
root = ThemedTk(theme="arc") # using arc as main theme
root.title("Homework Planner")
root.geometry("900x650")

load_data() ## any saved data from before will be loaded here when program starts

header = ttk.Frame(root) # the main header at the top of window
header.pack(fill="x")

title = ttk.Label(header,text="HOMEWORK PLANNER", font=("Arial", 18, "bold")) #Main title of the app

title.pack(pady=10)

navbar = ttk.Frame(root) # The main navigation bar to navigate between pages.
navbar.pack(fill="x")

# Buttons labels in navigation bar
buttons = [("Dashboard", show_dashboard), ("Homework", show_homework), ("Add Task", show_add_task), ("Help", show_help), ("Exit", root.destroy)]

for text, command in buttons: 

    ttk.Button(navbar, text=text, command=command).pack(side="left", padx=5, pady=5)

content_frame = ttk.Frame(root) ## the "content_frame" is the main page area so that the function clear_content() can remove
content_frame.pack(fill="both", expand=True)


show_dashboard()

root.mainloop()