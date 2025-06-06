import json
import os
from tkinter import Tk, Label, Entry, Button, Listbox, Scrollbar, END

# File to store caller data
db_file = "caller_database.json"

# Load caller database
def load_data():
    if os.path.exists(db_file):
        with open(db_file, "r") as file:
            return json.load(file)
    return {}

# Save caller database
def save_data():
    with open(db_file, "w") as file:
        json.dump(caller_database, file, indent=4)

caller_database = load_data()

# GUI Functions
def add_caller():
    name = name_entry.get()
    number = number_entry.get()
    if name and number:
        caller_database[number] = name
        save_data()
        update_listbox()
        name_entry.delete(0, END)
        number_entry.delete(0, END)

# Update Listbox
def update_listbox():
    caller_listbox.delete(0, END)
    for number, name in caller_database.items():
        caller_listbox.insert(END, f"{name} - {number}")

# Delete caller
def delete_caller():
    selected = caller_listbox.curselection()
    if selected:
        number = caller_listbox.get(selected[0]).split(" - ")[1]
        del caller_database[number]
        save_data()
        update_listbox()

# GUI Setup
root = Tk()
root.title("Caller ID System")
root.geometry("400x400")

Label(root, text="Name:").pack()
name_entry = Entry(root)
name_entry.pack()

Label(root, text="Number:").pack()
number_entry = Entry(root)
number_entry.pack()

Button(root, text="Add Caller", command=add_caller).pack()
Button(root, text="Delete Caller", command=delete_caller).pack()

caller_listbox = Listbox(root, width=50, height=10)
caller_listbox.pack()
update_listbox()

scrollbar = Scrollbar(root, orient="vertical", command=caller_listbox.yview)
caller_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

root.mainloop()
