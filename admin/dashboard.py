import tkinter as tk
from admin.add_event import add_event_window
from admin.delete_event import delete_event_window

def admin_dashboard():
    dash = tk.Toplevel()
    dash.title("Admin Dashboard")
    dash.geometry("320x220")
    dash.config(bg="#2e3f34")

    tk.Button(dash, text="➕ Add Event", command=add_event_window,
              bg="green", fg="white", width=24).pack(pady=16)
    tk.Button(dash, text="❌ Delete Event", command=delete_event_window,
              bg="red", fg="white", width=24).pack(pady=6)
