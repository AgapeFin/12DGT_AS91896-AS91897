import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# DATA ---------------------
# Name of the file where homework will be saved and loaded
DATA_FILE = "homework.json"

# this list keeps all the homework tasks (while the app is still on)
homework_data = []

COLOUR_PRIORITY = {"Higher_Priority": "#d000ff", "Medium_Priority": "#ff006f", "Lower_Priority": "#ff8400" }

COLOUR_STATUS = {"Complete":"#5988FF", "Incomplete":"#FF0000"}

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

## for each task added, a row will be added in the table here
    for task in homework_data:

        tree.insert("", tk.END, values=(task["subject"], task["task"], task["due_date"], task["priority"], task["status"]))

    tree.pack(fill="both", expand=True, padx=20, pady=10)

 ## This function will show the add HOMEWORK PAGE ---------------------------
def show_add_task():

    clear_content()

    tk.Label(
        content_frame,
        text="Add Homework",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    ## frame widget to just placehold the text boxes
    form = tk.Frame(content_frame)
    form.pack()

    # frame widget - subject
    tk.Label(form, text="Subject").grid(row=0, column=0, pady=5)

    subject = ttk.Combobox(form, values=["Maths", "English","Science","History","PE", "Other"])

    subject.grid(row=0, column=1)

    # frame widget - task
    tk.Label(form, text="Task").grid(row=1, column=0, pady=5)

    task_entry = tk.Entry(form, width=30)
    task_entry.grid(row=1, column=1)

    # frame widget - due date
    tk.Label(form, text="Due Date").grid(row=2, column=0, pady=5)

    due_entry = tk.Entry(form, width=30)
    due_entry.grid(row=2, column=1)

    # frame widget - priority
    tk.Label(form, text="Priority").grid(row=3, column=0, pady=5)

    priority = ttk.Combobox(form, values=["High", "Medium", "Low"])

    priority.grid(row=3, column=1)

    ## function that will be used when the save homework button is pressed
    def add_homework():

        # this makes sure nothing is left blank
        if (subject.get() =="" or task_entry.get() =="" or due_entry.get() =="" or priority.get() ==""):
            messagebox.showerror("Error", "Please complete all fields.")
            return
        ## when a new task is added, it will be added to the homework_data
        homework_data.append({"subject": subject.get(), "task": task_entry.get(), "due_date": due_entry.get(), "priority": priority.get(), "status": "Incomplete"})

        save_data() # then saves to JSON file

        messagebox.showinfo("Success", "Homework Added!") ## Pop up message (happens after append)

        show_dashboard() ## return to dashboard

    tk.Button(content_frame, text="Save Homework", command=add_homework).pack(pady=20) ## the button that will  save the homework using the command


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