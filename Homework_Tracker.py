import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# DATA ---------------------
# Name of the file where homework will be saved and loaded
DATA_FILE = "homework.json"

# this list keeps all the homework tasks (while the app is still on)
homework_data = []

COLOUR_PRIORITY = {"High": "#d000ff", "Medium": "#ff006f", "Low": "#ff8400"}

COLOUR_STATUS = {"Complete":"#5988FF", "Incomplete":"#FF0000"}

def load_data(): ## Loads saved homework tasks from the JSON file and puts in homework_data*
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
    title = tk.Label(content_frame, text="Welcome Back!", font=("Arial", 20, "bold"))
    title.pack(pady=15)

    tk.Label(content_frame, text="Upcoming Tasks", font=("Arial", 14, "bold")).pack(anchor="w", padx=20)

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

    tk.Label(content_frame, text="Completed Tasks", font=("Arial", 14, "bold")).pack(anchor="w", padx=20, pady=(10, 0))

    completed_list = tk.Listbox(content_frame, width=70, height=5)
    completed_list.pack(padx=20)

    ## loops through every task and adds it to the completed list if it's marked as complete
    for task in homework_data:

        if task["status"] =="Complete":
            completed_list.insert(tk.END, f"✓ {task['subject']} - {task['task']}")
            completed_list.itemconfig(tk.END, bg=COLOUR_STATUS["Complete"])

    ## Shows a summary of the total tasks and completed tasks
    summary = tk.Label(content_frame, text=f"Total Tasks: {len(homework_data)}    Completed: {completed_count}", font=("Arial", 12))
    summary.pack(pady=20)
# ------
def get_selected_index(tree): # finds home data inxex the selected task in the treeview widget
    selection = tree.selection()
    if not selection:
        messagebox.showerror("error", "please Select a task first")
        return None
    return int(selection[0]) # uses the homeork data index as an id

def edit_selected_index(tree):
    index = get_selected_index(tree)
    if index is None:
        return
    show_add_task(edit_index=index) # Opens the addd/edit form already with the data of selected task.


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
    ## This function will show the homework paege shown as a table
    clear_content()

    tk.Label(content_frame, text="Homework", font=("Arial", 20, "bold")).pack(pady=15)
    ## Homework page will be shown here using a treeview widget.
    tree = ttk.Treeview(content_frame, columns=("Subject", "Task", "Due Date", "Priority", "Status"), show="headings")

    headings = ["Subject", "Task", "Due Date", "Priority", "Status"]

## sets the column header text and header width for each column
    for heading in headings:
        tree.heading(heading, text=heading)
        tree.column(heading, width=120)

    for priority, colour in COLOUR_PRIORITY.items(): # Create colour for each priorty level for rows
        tree.tag_configure(priority, background=colour)
    tree.tag_configure("Complete", background=COLOUR_STATUS["Complete"])

    for index, task in enumerate(homework_data): # Add each task to the treeview with right colours
        # Completed tasks will be blue, if not then will be basaed on priority level
        tag = "Complete" if task["status"] == "Complete" else task["priority"]
        tree.insert("", tk.END, iid=str(index), values=(task["subject"], task["task"], task["due_date"], task["priority"], task["status"]), tags=(tag,),)

    tree.pack(fill="both", expand=True, padx=20, pady=10)

    button_row = tk.Frame(content_frame)
    button_row.pack(pady=10)
    #buttons for edit delete and toggle complete task
    tk.Button(button_row, text="Edit", command=lambda: edit_selected_index(tree)).pack(side="left", padx=5)
    tk.Button(button_row, text="Delete", command=lambda: delete_index(tree)).pack(side="left", padx=5)
    tk.Button(button_row, text="Toggle Complete", command=lambda: complete_toggle(tree)).pack(side="left", padx=5)

subject_box = None
task_box = None
due_box = None
priority_box = None

def add_homework():
    if(subject_box.get() == "" or task_box.get() == "" or due_box.get() == "" or priority_box.get() == ""):
        messagebox.showerror("erorr", "Please complete all fields.")
        return

    new_task = {"subject": subject_box.get(), "task": task_box.get(), "due_date": due_box.get(), "priority": priority_box.get(), "status": "Incomplete",}

    if editing_index is None:
        homework_data.append(new_task)
        messagebox.showinfo("success", "Homework added")
    else:
        new_task["status"] = homework_data[editing_index]["status"]
        homework_data[editing_index] = new_task
        messagebox.showinfo("success", "Homework updated")
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

    tk.Label(content_frame, text=page_title, font=("Arial", 20, "bold")).pack(pady=20)

    form = tk.Frame(content_frame) # just a frame widget that placeholds the textboxes
    form.pack()

    tk.Label(form, text="Subject").grid(row=0, column=0, pady=5)
    subject_box = ttk.Combobox(form, values=["Maths", "English", "Science", "History", "PE", "Other"])
    subject_box.grid(row=0, column=1)

    tk.Label(form, text="task").grid(row=1, column=0, pady=5)
    task_box = tk.Entry(form, width=30)
    task_box.grid(row=1, column=1)

    tk.Label(form, text="Due date").grid(row=2, column=0, pady=5)
    due_box = tk.Entry(form, width=30)
    due_box.grid(row=2, column=1)

    tk.Label(form, text="Priority").grid(row=3, column=0, pady=5)
    priority_box = ttk.Combobox(form, values=["High", "Medium", "Low"])
    priority_box.grid(row=3, column=1)

    if editing_index is not None:
        task = homework_data[edit_index]
        subject_box.set(task["subject"])
        task_box.insert(0, task["task"])
        due_box.insert(0, task["due_date"])
        priority_box.set(task["priority"])

    if edit_index is not None:
        button_text = "update Homework"
    else:
        button_text = "Save Homrwork"

    tk.Button(content_frame, text=button_text, command=add_homework).pack(pady=20)


# shows the statistics page (placeholder for now)
def show_statistics():

    clear_content()

    tk.Label(content_frame, text="Statistics Page (Sprint 3)", font=("Arial", 18)).pack(pady=50)

# shows the help page (placeholder for now)
def show_help():

    clear_content()

    tk.Label(content_frame, text="Help Page", font=("Arial", 18)).pack(pady=50)


# Main Window (Everything below this line will run once when program start) --------------------
root = tk.Tk()
root.title("Homework Planner")
root.geometry("900x650")

load_data() ## any saved data from before will be loaded here when program starts

header = tk.Frame(root) # the main header at the top of window
header.pack(fill="x")

title = tk.Label(header,text="HOMEWORK PLANNER", font=("Arial", 18, "bold")) #Main title of the app

title.pack(pady=10)

navbar = tk.Frame(root, bg="#FFFFFF") # The main navigation bar to navigate between pages.
navbar.pack(fill="x")

# Buttons labels in navigation bar
buttons = [("Dashboard", show_dashboard), ("Homework", show_homework), ("Add Task", show_add_task), ("Statistics", show_statistics), ("Help", show_help), ("Exit", root.destroy)]

for text, command in buttons: 

    tk.Button(navbar, text=text, command=command).pack(side="left", padx=5, pady=5)

content_frame = tk.Frame(root) ## the "content_frame" is the main page area so that the function clear_content() can remove
content_frame.pack(fill="both", expand=True)


show_dashboard()

root.mainloop()