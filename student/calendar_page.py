import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import sqlite3
import csv
import os
from datetime import datetime
from utils.constants import DB_FILE, CSV_FILE

def open_calendar_page(username):
    root1 = tk.Toplevel()
    root1.title("Calendar Page")
    root1.geometry("520x640")
    root1.config(bg="#1e1e1e")

    cal = Calendar(root1, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.pack(expand=True, fill="both", padx=10, pady=10)

    # Highlight event dates
    def highlight_events():
        try:
            cal.calevent_remove('event_date')
        except Exception:
            pass
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT date FROM events")
        rows = cur.fetchall()
        conn.close()

        cal.tag_config('event_date', background='#2e3f34', foreground='white')
        for (edate,) in rows:
            try:
                dt = datetime.strptime(edate, "%Y-%m-%d").date()
                cal.calevent_create(dt, "Event", 'event_date')
            except:
                continue

    highlight_events()
    tk.Button(root1, text="Refresh events", command=highlight_events, bg="#2e3f34", fg="white").pack(pady=6)

    def show_event_and_registration(event):
        selected_date = cal.get_date()

        for w in root1.pack_slaves():
            if w not in (cal,):
                w.destroy()

        event_frame = tk.Frame(root1, bg="#1e1e1e")
        event_frame.pack(fill='both', expand=False, padx=10, pady=6)

        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT name, venue, description FROM events WHERE date=?", (selected_date,))
        events = cur.fetchall()
        conn.close()

        if not events:
            tk.Label(event_frame, text=f"No events on {selected_date}", bg="#1e1e1e", fg="red",
                     font=("Arial", 12, "bold")).pack(pady=10)
            return

        for (ename, venue, desc) in events:
            evf = tk.Frame(event_frame, bg="#1e1e1e", pady=6)
            evf.pack(fill='x', expand=False, pady=4)
            tk.Label(evf, text=f" {ename} ({selected_date})", bg="#1e1e1e", fg="yellow",
                     font=("Arial", 12, "bold")).pack(anchor='w')
            tk.Label(evf, text=f" {venue}", bg="#1e1e1e", fg="yellow", font=("Arial", 11)).pack(anchor='w', pady=1)
            tk.Label(evf, text=f" {desc}", bg="#1e1e1e", fg="white", wraplength=480,
                     justify='left').pack(anchor='w', pady=3)

            form = tk.Frame(evf, bg="#1e1e1e")
            form.pack(anchor='w', pady=4)

            tk.Label(form, text="Name:", bg="#1e1e1e", fg="white").grid(row=0, column=0, sticky='w')
            name_entry = tk.Entry(form)
            name_entry.grid(row=0, column=1, padx=6)
            name_entry.insert(0, username)

            tk.Label(form, text="Roll Number / ID:", bg="#1e1e1e", fg="white").grid(row=1, column=0, sticky='w')
            roll_entry = tk.Entry(form)
            roll_entry.grid(row=1, column=1, padx=6)

            tk.Label(form, text="Number of Tickets:", bg="#1e1e1e", fg="white").grid(row=2, column=0, sticky='w')
            tickets_entry = tk.Entry(form, width=5)
            tickets_entry.grid(row=2, column=1, padx=6)
            tickets_entry.insert(0, "1")

            def register_event():
                roll = roll_entry.get().strip()
                tickets = tickets_entry.get().strip()
                name_user = name_entry.get().strip()
                if not roll:
                    messagebox.showerror("Error", "Roll Number is required!")
                    return
                file_exists = os.path.isfile(CSV_FILE)
                with open(CSV_FILE, "a", newline="") as f:
                    writer = csv.writer(f)
                    if not file_exists:
                        writer.writerow(["Name", "Roll", "Tickets", "Date", "Event", "Venue", "Description"])
                    writer.writerow([name_user, roll, tickets, selected_date, ename, venue, desc])
                messagebox.showinfo("Success", f"✅ Registered for {ename} on {selected_date}")

            tk.Button(evf, text="Book / Register", command=register_event,
                      bg="green", fg="white", font=("Arial", 11, "bold")).pack(pady=6)

    cal.bind("<<CalendarSelected>>", show_event_and_registration)
