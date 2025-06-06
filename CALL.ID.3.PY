import sqlite3
import os
import csv
from tkinter import Tk, Label, Entry, Button, Listbox, Scrollbar, END, Toplevel, messagebox, StringVar, ttk

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

def update_caller(name, number, old_number):
    cursor.execute("UPDATE callers SET name = ?, number = ? WHERE number = ?", (name, number, old_number))
    conn.commit()
    update_listbox()

def search_callers():
    query = search_var.get()
    cursor.execute("SELECT name, number FROM callers WHERE name LIKE ? OR number LIKE ?", ('%' + query + '%', '%' + query + '%'))
    results = cursor.fetchall()
    caller_listbox.delete(0, END)
    for name, number in results:
        caller_listbox.insert(END, f"{name} - {number}")

def update_listbox():
    caller_listbox.delete(0, END)
    for name, number in fetch_callers():
        caller_listbox.insert(END, f"{name} - {number}")

def open_add_window():
    win = Toplevel(root)
    win.title("Add Caller")
    Label(win, text="Name:").pack()
    name_entry = Entry(win)
    name_entry.pack()
    Label(win, text="Number:").pack()
    number_entry = Entry(win)
    number_entry.pack()
    Button(win, text="Add", command=lambda: [add_caller(name_entry.get(), number_entry.get()), win.destroy()]).pack()

def open_edit_window():
    selected = caller_listbox.curselection()
    if selected:
        old_number = caller_listbox.get(selected[0]).split(" - ")[1]
        cursor.execute("SELECT name FROM callers WHERE number = ?", (old_number,))
        old_name = cursor.fetchone()[0]
        
        win = Toplevel(root)
        win.title("Edit Caller")
        Label(win, text="Name:").pack()
        name_entry = Entry(win)
        name_entry.insert(0, old_name)
        name_entry.pack()
        Label(win, text="Number:").pack()
        number_entry = Entry(win)
        number_entry.insert(0, old_number)
        number_entry.pack()
        Button(win, text="Update", command=lambda: [update_caller(name_entry.get(), number_entry.get(), old_number), win.destroy()]).pack()

def export_data():
    with open("callers_export.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Number"])
        writer.writerows(fetch_callers())
    messagebox.showinfo("Export", "Data exported to callers_export.csv")

def import_data():
    with open("callers_export.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            try:
                cursor.execute("INSERT INTO callers (name, number) VALUES (?, ?)", (row[0], row[1]))
            except sqlite3.IntegrityError:
                continue
    conn.commit()
    update_listbox()

def toggle_theme():
    if root.tk.call("ttk::style", "theme", "use") == "clam":
        root.tk.call("ttk::style", "theme", "use", "default")
    else:
        root.tk.call("ttk::style", "theme", "use", "clam")

root = Tk()
root.title("Caller ID System")
root.geometry("500x450")
search_var = StringVar()
Label(root, text="Search:").pack()
Entry(root, textvariable=search_var).pack()
Button(root, text="Search", command=search_callers).pack()
Button(root, text="Add Caller", command=open_add_window).pack()
Button(root, text="Edit Caller", command=open_edit_window).pack()
Button(root, text="Delete Caller", command=delete_caller).pack()
Button(root, text="Export", command=export_data).pack()
Button(root, text="Import", command=import_data).pack()
Button(root, text="Toggle Dark Mode", command=toggle_theme).pack()
caller_listbox = Listbox(root, width=50, height=10)
caller_listbox.pack()
scrollbar = Scrollbar(root, orient="vertical", command=caller_listbox.yview)
caller_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
update_listbox()
root.mainloop()
