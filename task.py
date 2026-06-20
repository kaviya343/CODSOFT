import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ---------- DATABASE ----------
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    priority TEXT NOT NULL,
    status TEXT NOT NULL
)
""")
conn.commit()

# ---------- FUNCTIONS ----------
def load_tasks():
    task_table.delete(*task_table.get_children())

    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    for row in rows:
        task_table.insert(
            "",
            tk.END,
            values=(row[0], row[1], row[2], row[3])
        )

    update_count()


def add_task():
    task = task_entry.get().strip()
    priority = priority_box.get()

    if not task:
        messagebox.showwarning("Warning", "Enter a task")
        return

    cursor.execute(
        "INSERT INTO tasks(task, priority, status) VALUES (?, ?, ?)",
        (task, priority, "Pending")
    )
    conn.commit()

    task_entry.delete(0, tk.END)
    load_tasks()


def delete_task():
    selected = task_table.focus()

    if not selected:
        messagebox.showwarning("Warning", "Select a task")
        return

    task_id = task_table.item(selected)["values"][0]

    cursor.execute(
        "DELETE FROM tasks WHERE id=?",
        (task_id,)
    )
    conn.commit()

    load_tasks()


def complete_task():
    selected = task_table.focus()

    if not selected:
        messagebox.showwarning("Warning", "Select a task")
        return

    task_id = task_table.item(selected)["values"][0]

    cursor.execute(
        "UPDATE tasks SET status='Completed' WHERE id=?",
        (task_id,)
    )
    conn.commit()

    load_tasks()


def update_count():
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM tasks WHERE status='Completed'"
    )
    completed = cursor.fetchone()[0]

    count_label.config(
        text=f"Total Tasks: {total}   |   Completed: {completed}"
    )


# ---------- GUI ----------
root = tk.Tk()
root.title("TaskFlow - Smart ToDo Manager")
root.geometry("850x550")
root.configure(bg="#1e1e2f")

title = tk.Label(
    root,
    text="TaskFlow - Smart ToDo Manager",
    font=("Segoe UI", 20, "bold"),
    bg="#1e1e2f",
    fg="white"
)
title.pack(pady=15)

# Input Frame
input_frame = tk.Frame(root, bg="#1e1e2f")
input_frame.pack(pady=10)

task_entry = tk.Entry(
    input_frame,
    width=35,
    font=("Segoe UI", 12)
)
task_entry.grid(row=0, column=0, padx=10)

priority_box = ttk.Combobox(
    input_frame,
    values=["High", "Medium", "Low"],
    width=12,
    state="readonly"
)
priority_box.grid(row=0, column=1)
priority_box.set("Medium")

add_btn = tk.Button(
    input_frame,
    text="Add Task",
    bg="#28a745",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    command=add_task
)
add_btn.grid(row=0, column=2, padx=10)

# Table
columns = ("ID", "Task", "Priority", "Status")

task_table = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=15
)

for col in columns:
    task_table.heading(col, text=col)

task_table.column("ID", width=60)
task_table.column("Task", width=350)
task_table.column("Priority", width=120)
task_table.column("Status", width=120)

task_table.pack(pady=15)

# Buttons
btn_frame = tk.Frame(root, bg="#1e1e2f")
btn_frame.pack()

complete_btn = tk.Button(
    btn_frame,
    text="Mark Complete",
    bg="#007bff",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    command=complete_task
)
complete_btn.grid(row=0, column=0, padx=10)

delete_btn = tk.Button(
    btn_frame,
    text="Delete Task",
    bg="#dc3545",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    command=delete_task
)
delete_btn.grid(row=0, column=1, padx=10)

count_label = tk.Label(
    root,
    text="",
    font=("Segoe UI", 11, "bold"),
    bg="#1e1e2f",
    fg="white"
)
count_label.pack(pady=15)

load_tasks()

root.mainloop()

conn.close()