import sqlite3
import os
import csv
import tkinter as tk
from tkinter import ttk, messagebox

# Database setup
db_file = "caller_database.db"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS callers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    number TEXT UNIQUE NOT NULL
)
""")
conn.commit()

def fetch_callers():
    cursor.execute("SELECT name, number FROM callers ORDER BY name")
    return cursor.fetchall()

def add_caller(name, number):
    if name and number:
        try:
            cursor.execute("INSERT INTO callers (name, number) VALUES (?, ?)", (name, number))
            conn.commit()
            update_listbox()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Caller number already exists!")

def delete_caller():
    selected = caller_listbox.curselection()
    if selected:
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this caller?")
        if confirm:
            number = caller_listbox.get(selected[0]).split(" - ")[1]
            cursor.execute("DELETE FROM callers WHERE number = ?", (number,))
            conn.commit()
            update_listbox()

def update_listbox():
    caller_listbox.delete(0, tk.END)
    for name, number in fetch_callers():
        caller_listbox.insert(tk.END, f"{name} - {number}")

def open_add_window():
    win = tk.Toplevel(root)
    win.title("Add Caller")
    win.geometry("300x200")
    tk.Label(win, text="Name:", font=("Arial", 12)).pack(pady=5)
    name_entry = tk.Entry(win, font=("Arial", 12))
    name_entry.pack()
    tk.Label(win, text="Number:", font=("Arial", 12)).pack(pady=5)
    number_entry = tk.Entry(win, font=("Arial", 12))
    number_entry.pack()
    tk.Button(win, text="Add", font=("Arial", 12), command=lambda: [add_caller(name_entry.get(), number_entry.get()), win.destroy()]).pack(pady=10)

root = tk.Tk()
root.title("Caller ID System")
root.geometry("500x500")
root.configure(bg="#f0f0f0")

frame = tk.Frame(root, bg="#d1e7f0", padx=20, pady=20)
frame.pack(pady=20, fill="both", expand=True)

search_var = tk.StringVar()
tk.Label(frame, text="Search:", font=("Arial", 12), bg="#d1e7f0").grid(row=0, column=0, padx=5, pady=5)
tk.Entry(frame, textvariable=search_var, font=("Arial", 12), width=25).grid(row=0, column=1, padx=5, pady=5)

caller_listbox = tk.Listbox(frame, font=("Arial", 12), width=50, height=10)
caller_listbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

scrollbar = tk.Scrollbar(frame, orient="vertical", command=caller_listbox.yview)
caller_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.grid(row=1, column=2, sticky="ns")

button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack()

tk.Button(button_frame, text="Add Caller", font=("Arial", 12), bg="#4CAF50", fg="white", width=15, command=open_add_window).grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Delete Caller", font=("Arial", 12), bg="#f44336", fg="white", width=15, command=delete_caller).grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Exit", font=("Arial", 12), bg="#555", fg="white", width=15, command=root.quit).grid(row=0, column=2, padx=5, pady=5)

update_listbox()
root.mainloop()
