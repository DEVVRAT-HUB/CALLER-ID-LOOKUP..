import sqlite3
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk 
import webbrowser

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
    win.geometry("300x250")
    win.configure(bg="#1e1e1e")
    tk.Label(win, text="Name:", font=("Arial", 12), fg="white", bg="#1e1e1e").pack(pady=5)
    name_entry = tk.Entry(win, font=("Arial", 12))
    name_entry.pack()
    tk.Label(win, text="Number:", font=("Arial", 12), fg="white", bg="#1e1e1e").pack(pady=5)
    number_entry = tk.Entry(win, font=("Arial", 12))
    number_entry.pack()
    tk.Button(win, text="Add", font=("Arial", 12), bg="#4CAF50", fg="white", 
              command=lambda: [add_caller(name_entry.get(), number_entry.get()), win.destroy()]).pack(pady=10)

def search_callers():
    query = search_var.get().lower()
    caller_listbox.delete(0, tk.END)
    for name, number in fetch_callers():
        if query in name.lower() or query in number:
            caller_listbox.insert(tk.END, f"{name} - {number}")

def toggle_theme():
    if root.cget("bg") == "#1e1e1e":
        root.configure(bg="#f0f0f0")
        frame.configure(bg="#d1e7f0")
    else:
        root.configure(bg="#1e1e1e")
        frame.configure(bg="#252526")

def dial_selected_number():
    selected = caller_listbox.curselection()
    if selected:
        number = caller_listbox.get(selected[0]).split(" - ")[1]
        number = ''.join(filter(str.isdigit, number))
        url = f"tel:{number}"
        try:
            webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to dial: {e}")
    else:
        messagebox.showerror("Error", "Please select a contact first!")

def whatsapp_selected_number():
    selected = caller_listbox.curselection()
    if selected:
        number = caller_listbox.get(selected[0]).split(" - ")[1]
        number = ''.join(filter(str.isdigit, number))
        url = f"https://wa.me/{number}"
        try:
            webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open WhatsApp: {e}")
    else:
        messagebox.showerror("Error", "Please select a contact first!")

# GUI
root = tk.Tk()
root.title("Caller ID System")
root.geometry("600x550")
root.configure(bg="#1e1e1e")

frame = tk.Frame(root, bg="#252526", padx=20, pady=20)
frame.pack(pady=20, fill="both", expand=True)

# Logo
if os.path.exists("logo.png"):
    logo_img = Image.open("logo.png").resize((50, 50))
    logo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(frame, image=logo, bg="#252526")
else:
    logo_label = tk.Label(frame, text="Caller ID System", font=("Arial", 18), fg="white", bg="#252526")

logo_label.grid(row=0, column=0, columnspan=3, pady=10)

# Search Bar
search_var = tk.StringVar()
tk.Label(frame, text="Search:", font=("Arial", 12), fg="white", bg="#252526").grid(row=1, column=0, padx=5, pady=5)
tk.Entry(frame, textvariable=search_var, font=("Arial", 12), width=25).grid(row=1, column=1, padx=5, pady=5)
tk.Button(frame, text="Search", font=("Arial", 12), command=search_callers).grid(row=1, column=2, padx=5, pady=5)

# Caller Listbox
caller_listbox = tk.Listbox(frame, font=("Arial", 12), width=50, height=10, bg="#1e1e1e", fg="white")
caller_listbox.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

scrollbar = tk.Scrollbar(frame, orient="vertical", command=caller_listbox.yview)
caller_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.grid(row=2, column=3, sticky="ns")

# Buttons
button_frame = tk.Frame(root, bg="#1e1e1e")
button_frame.pack()

tk.Button(button_frame, text="Add Caller", font=("Arial", 12), bg="#4CAF50", fg="white", width=15, command=open_add_window).grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Delete Caller", font=("Arial", 12), bg="#f44336", fg="white", width=15, command=delete_caller).grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Toggle Theme", font=("Arial", 12), bg="#008CBA", fg="white", width=15, command=toggle_theme).grid(row=0, column=2, padx=5, pady=5)
tk.Button(button_frame, text="Exit", font=("Arial", 12), bg="#555", fg="white", width=15, command=root.quit).grid(row=0, column=3, padx=5, pady=5)

# New Buttons: Dial & WhatsApp
tk.Button(button_frame, text="Dial Number", font=("Arial", 12), bg="#25D366", fg="white", width=15, command=dial_selected_number).grid(row=1, column=0, padx=5, pady=5)
tk.Button(button_frame, text="WhatsApp", font=("Arial", 12), bg="#128C7E", fg="white", width=15, command=whatsapp_selected_number).grid(row=1, column=1, padx=5, pady=5)

update_listbox()
root.mainloop()
