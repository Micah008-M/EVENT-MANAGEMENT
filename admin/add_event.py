import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import sqlite3
from utils.constants import DB_FILE

def add_event_window():
    admin = tk.Toplevel()
    admin.title("Admin - Add Event")
    admin.geometry("420x420")
    admin.config(bg="#2e3f34")

    tk.Label(admin, text="Event Name:", bg="#2e3f34", fg="white").pack(pady=5)
    entry_name = tk.Entry(admin, width=35)
    entry_name.pack(pady=5)

    tk.Label(admin, text="Event Date (YYYY-MM-DD or DD/MM/YYYY):", bg="#2e3f34", fg="white").pack(pady=5)
    entry_date = tk.Entry(admin, width=35)
    entry_date.pack(pady=5)

    tk.Label(admin, text="Venue:", bg="#2e3f34", fg="white").pack(pady=5)
    entry_venue = tk.Entry(admin, width=35)
    entry_venue.pack(pady=5)

    tk.Label(admin, text="Description:", bg="#2e3f34", fg="white").pack(pady=5)
    entry_desc = tk.Text(admin, width=35, height=6)
    entry_desc.pack(pady=5)

    def save_event():
        name = entry_name.get().strip()
        date_text = entry_date.get().strip()
        venue = entry_venue.get().strip()
        desc = entry_desc.get("1.0", tk.END).strip()

        if not name or not date_text:
            messagebox.showerror("Error", "Event Name and Date required!")
            return

        dt = None
        for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
            try:
                dt = datetime.strptime(date_text, fmt)
                break
            except ValueError:
                continue

        if dt is None:
            messagebox.showerror("Error", "Date format invalid.")
            return

        iso_date = dt.strftime("%Y-%m-%d")

        try:
            conn = sqlite3.connect(DB_FILE)
            cur = conn.cursor()
            cur.execute("INSERT INTO events (name, date, venue, description) VALUES (?, ?, ?, ?)",
                        (name, iso_date, venue, desc))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Event '{name}' added on {iso_date}")
            admin.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("DB Error", str(e))

    tk.Button(admin, text="Add Event", command=save_event, bg="green", fg="white", width=20).pack(pady=12)
