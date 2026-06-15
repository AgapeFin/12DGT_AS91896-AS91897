import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

root = tk.Tk()
root.title("Homework Planner")
root.geometry("900x500")


# Sidebar
sidebar = tk.Frame(root, bg="#dddddd", width=150)
sidebar.pack(side="left", fill="y")

tk.Button(
    sidebar,
    text="Homework",
    width=15,
    
).pack(pady=20)

tk.Button(
    sidebar,
    text="Add Task",
    width=15,

).pack(pady=20)

tk.Button(
    sidebar,
    text="Exit",
    width=15,
    command=root.destroy
).pack(pady=20)

# Main Area
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

title_label = tk.Label(
    main_frame,
    text="Welcome Student",
    font=("Arial", 20, "bold")
)
title_label.pack(pady=20)

content_frame = tk.Frame(main_frame)
content_frame.pack()

# Upcoming
upcoming_frame = tk.Frame(content_frame)
upcoming_frame.pack(side="left", padx=30)

tk.Label(
    upcoming_frame,
    text="Upcoming Tasks",
    font=("Arial", 12, "bold")
).pack()

upcoming_list = tk.Listbox(
    upcoming_frame,
    width=30,
    height=10
)
upcoming_list.pack()

# Completed
completed_frame = tk.Frame(content_frame)
completed_frame.pack(side="left", padx=30)

tk.Label(
    completed_frame,
    text="Completed Tasks",
    font=("Arial", 12, "bold")
).pack()

completed_list = tk.Listbox(
    completed_frame,
    width=30,
    height=10
)
completed_list.pack()

total_label = tk.Label(
    main_frame,
    text="Total Tasks: 0",
    font=("Arial", 12)
)
total_label.pack(pady=20)



root.mainloop()