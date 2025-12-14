import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import re


# DATABASE SETUP
conn = sqlite3.connect("lost_and_found.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    category TEXT,
    location TEXT,
    date TEXT,
    status TEXT
)
""")
conn.commit()


# MAIN WINDOW
root = tk.Tk()
root.title("Lost and Found Tracker")
root.geometry("750x520")
root.configure(bg="#d9d9d9")

def on_close():
    conn.commit()
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)


# FRAMES
home_frame = tk.Frame(root, bg="#f2f2f2")
lost_item_frame = tk.Frame(root, bg="#ffe6e6")
found_item_frame = tk.Frame(root, bg="#e6ffe6")
view_item_frame = tk.Frame(root, bg="#e6f0ff")

for f in (home_frame, lost_item_frame, found_item_frame, view_item_frame):
    f.place(relwidth=1, relheight=1)


# NAVIGATION FUNCTIONS
def show_home():
    home_frame.lift()

def show_lost():
    lost_item_frame.lift()

def show_found():
    found_item_frame.lift()

def show_view():
    refresh_item_list()
    view_item_frame.lift()


# HOME FRAME
tk.Label(home_frame, text="Lost and Found Tracker",
         font=("Arial", 24, "bold"),
         fg="darkblue", bg="#f2f2f2").pack(pady=20)

tk.Label(home_frame, text="Welcome to LocateIT",
         font=("Arial", 18), bg="#f2f2f2").pack(pady=10)

tk.Button(home_frame, text="View Items",
          font=("Arial", 16), width=22,
          command=show_view).pack(pady=8)

tk.Button(home_frame, text="Report Lost Item",
          font=("Arial", 16), width=22,
          command=show_lost).pack(pady=8)

tk.Button(home_frame, text="Report Found Item",
          font=("Arial", 16), width=22,
          command=show_found).pack(pady=8)


# COMMON DATA
categories = ["Electronics", "Clothing", "Accessories", "Documents", "Others"]
labels = ["Item Name", "Description", "Category", "Location", "Date (YYYY-MM-DD)"]


# LOST ITEM FRAME
tk.Label(lost_item_frame, text="Report Lost Item",
         font=("Arial", 22, "bold"),
         bg="#ffe6e6").pack(pady=15)

lost_form = tk.Frame(lost_item_frame, bg="#ffe6e6")
lost_form.pack()

lost_entries = {}

for i, lbl in enumerate(labels):
    tk.Label(lost_form, text=lbl + ":", font=("Arial", 14),
             bg="#ffe6e6").grid(row=i, column=0, sticky="w", pady=5)

    if lbl == "Category":
        entry = ttk.Combobox(lost_form, values=categories, width=28)
    else:
        entry = tk.Entry(lost_form, width=30)

    entry.grid(row=i, column=1, pady=5)
    lost_entries[lbl] = entry

def save_lost():
    data = {k: v.get().strip() for k, v in lost_entries.items()}

    if "" in data.values():
        messagebox.showwarning("Missing Info", "Complete all fields.")
        return

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", data["Date (YYYY-MM-DD)"]):
        messagebox.showerror("Invalid Date", "Use YYYY-MM-DD format.")
        return

    cursor.execute("""
        INSERT INTO items (name, description, category, location, date, status)
        VALUES (?, ?, ?, ?, ?, 'Lost')
    """, (data["Item Name"], data["Description"],
          data["Category"], data["Location"],
          data["Date (YYYY-MM-DD)"]))

    conn.commit()
    messagebox.showinfo("Saved", "Lost item saved!")

    for e in lost_entries.values():
        e.delete(0, tk.END)

tk.Button(lost_item_frame, text="Save Item",
          font=("Arial", 16),
          bg="#ff9999",
          command=save_lost).pack(pady=10)

tk.Button(lost_item_frame, text="Back",
          font=("Arial", 14),
          command=show_home).pack()


# FOUND ITEM FRAME
tk.Label(found_item_frame, text="Report Found Item",
         font=("Arial", 22, "bold"),
         bg="#e6ffe6").pack(pady=15)

found_form = tk.Frame(found_item_frame, bg="#e6ffe6")
found_form.pack()

found_entries = {}

for i, lbl in enumerate(labels):
    tk.Label(found_form, text=lbl + ":", font=("Arial", 14),
             bg="#e6ffe6").grid(row=i, column=0, sticky="w", pady=5)

    if lbl == "Category":
        entry = ttk.Combobox(found_form, values=categories, width=28)
    else:
        entry = tk.Entry(found_form, width=30)

    entry.grid(row=i, column=1, pady=5)
    found_entries[lbl] = entry

def save_found():
    data = {k: v.get().strip() for k, v in found_entries.items()}

    if "" in data.values():
        messagebox.showwarning("Missing Info", "Complete all fields.")
        return

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", data["Date (YYYY-MM-DD)"]):
        messagebox.showerror("Invalid Date", "Use YYYY-MM-DD format.")
        return

    cursor.execute("""
        INSERT INTO items (name, description, category, location, date, status)
        VALUES (?, ?, ?, ?, ?, 'Found')
    """, (data["Item Name"], data["Description"],
          data["Category"], data["Location"],
          data["Date (YYYY-MM-DD)"]))

    conn.commit()
    messagebox.showinfo("Saved", "Found item saved!")

    for e in found_entries.values():
        e.delete(0, tk.END)

tk.Button(found_item_frame, text="Save Item",
          font=("Arial", 16),
          bg="#99ff99",
          command=save_found).pack(pady=10)

tk.Button(found_item_frame, text="Back",
          font=("Arial", 14),
          command=show_home).pack()


# VIEW ITEMS FRAME
tk.Label(view_item_frame, text="Items List",
         font=("Arial", 22, "bold"),
         bg="#e6f0ff").pack(pady=15)

tk.Button(view_item_frame, text="← Back",
          command=show_home).place(x=10, y=10)

table_frame = tk.Frame(view_item_frame)
table_frame.pack(fill="both", expand=True, padx=10)

columns = ("id", "desc", "cat", "status", "date")

item_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

# HEADINGS
item_table.heading("id", text="ID")
item_table.heading("desc", text="Description")
item_table.heading("cat", text="Category")
item_table.heading("status", text="Status")
item_table.heading("date", text="Date")

# COLUMN WIDTHS 
item_table.column("id", width=50, anchor="center", stretch=False)
item_table.column("desc", width=220, stretch=True)
item_table.column("cat", width=120, anchor="center")
item_table.column("status", width=100, anchor="center")
item_table.column("date", width=120, anchor="center")

# SCROLLBAR
scroll_x = ttk.Scrollbar(table_frame, orient="horizontal", command=item_table.xview)
item_table.configure(xscrollcommand=scroll_x.set)

item_table.pack(fill="both", expand=True)
scroll_x.pack(fill="x")

def refresh_item_list():
    item_table.delete(*item_table.get_children())
    cursor.execute("SELECT id, description, category, status, date FROM items")
    for row in cursor.fetchall():
        item_table.insert("", tk.END, values=row)

def get_selected_id():
    selected = item_table.selection()
    if not selected:
        return None
    return item_table.item(selected[0])["values"][0]

def delete_item():
    item_id = get_selected_id()
    if not item_id:
        messagebox.showwarning("Select Item", "Choose an item first.")
        return
    cursor.execute("DELETE FROM items WHERE id=?", (item_id,))
    conn.commit()
    refresh_item_list()

def mark_returned():
    item_id = get_selected_id()
    if not item_id:
        messagebox.showwarning("Select Item", "Choose an item first.")
        return
    cursor.execute("UPDATE items SET status='Returned' WHERE id=?", (item_id,))
    conn.commit()
    refresh_item_list()

btn_frame = tk.Frame(view_item_frame, bg="#e6f0ff")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Delete",
          width=12, command=delete_item).grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text="Mark as Returned",
          width=18, command=mark_returned).grid(row=0, column=1, padx=10)


# ======START APP======
home_frame.lift()
root.mainloop()
