import tkinter as tk
from tkinter import messagebox
import sqlite3
from utils.constants import DB_FILE

def delete_event_window():
    del_win = tk.Toplevel()
    del_win.title("Admin - Delete Event")
    del_win.geometry("420x320")
    del_win.config(bg="#2e3f34")

    tk.Label(del_win, text="Select Event to Delete:", bg="#2e3f34", fg="white").pack(pady=5)

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, name, date FROM events ORDER BY date")
    events = cur.fetchall()
    conn.close()

    if not events:
        tk.Label(del_win, text="No events to delete.", bg="#2e3f34", fg="white").pack(pady=20)
        return

    event_var = tk.StringVar()
    event_var.set(f"{events[0][0]} - {events[0][1]} ({events[0][2]})")
    event_list = [f"{e[0]} - {e[1]} ({e[2]})" for e in events]
    dropdown = tk.OptionMenu(del_win, event_var, *event_list)
    dropdown.pack(pady=10)

    def delete_selected_event():
        selected = event_var.get()
        event_id = int(selected.split(" - ")[0])
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("DELETE FROM events WHERE id=?", (event_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Deleted", "Event deleted successfully!")
        del_win.destroy()

    tk.Button(del_win, text="Delete Event", command=delete_selected_event,
              bg="red", fg="white").pack(pady=10)
