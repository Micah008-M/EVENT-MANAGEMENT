import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import sqlite3
import csv
import os
from datetime import datetime

DB_FILE = "events.db"

# ---------------- DATABASE ---------------- #
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # Create required tables
    cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        date TEXT NOT NULL,
        venue TEXT,
        description TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def seed_users():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    students = [
        ('neha', 'one'),
        ('daniya', 'two'),
        ('micah', 'three'),
        ('gauri', 'four'),
        ('sona', 'five'),
        ('antony', 'six'),
        ('varghese', 'seven'),
        ('tiya', 'eight'),
        ('naina','nine'),
        ('thomas','ten'),
        
        
    ]
    cur.executemany("INSERT OR IGNORE INTO students (username, password) VALUES (?, ?)", students)

    admins = [
        ('rinu', 'rinu123'),
        ('kavitha','kavitha123'),
        ('divya','divya123'),
        ('priya','priya123'),
        ('vinodhini','vinodhini123')
    ]
    cur.executemany("INSERT OR IGNORE INTO admins (username, password) VALUES (?, ?)", admins)

    conn.commit()
    conn.close()

# ---------------- ADMIN: ADD EVENT ---------------- #
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
            messagebox.showerror("Error", "Date must be YYYY-MM-DD or DD/MM/YYYY.")
            return
        iso_date = dt.strftime("%Y-%m-%d")

        try:
            conn = sqlite3.connect(DB_FILE)
            cur = conn.cursor()
            cur.execute("INSERT INTO events (name, date, venue, description) VALUES (?, ?, ?, ?)",
                        (name, iso_date, venue, desc))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("DB Error", str(e))
            return

        messagebox.showinfo("Success", f"Event '{name}' added on {iso_date}")
        admin.destroy()

    tk.Button(admin, text="Add Event", command=save_event, bg="green", fg="white", width=20).pack(pady=12)

# ---------------- ADMIN: DELETE EVENT ---------------- #
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

# ---------------- ADMIN DASHBOARD ---------------- #
def admin_dashboard():
    dash = tk.Toplevel()
    dash.title("Admin Dashboard")
    dash.geometry("320x220")
    dash.config(bg="#2e3f34")

    tk.Button(dash, text="➕ Add Event", command=add_event_window,
              bg="green", fg="white", width=24).pack(pady=16)
    tk.Button(dash, text="❌ Delete Event", command=delete_event_window,
              bg="red", fg="white", width=24).pack(pady=6)

# ---------------- STUDENT DASHBOARD ---------------- #
def student_dashboard(username):
    dash = tk.Toplevel()
    dash.title("Student Dashboard")
    dash.geometry("400x320")
    dash.config(bg="#203b2a")

    tk.Label(dash, text=f"Welcome, {username}", font=("Arial", 14, "bold"), bg="#203b2a", fg="white").pack(pady=20)
    tk.Button(dash, text="View Calendar & Register", width=25, height=2, command=lambda: open_calendar_page(username)).pack(pady=10)
    tk.Button(dash, text="Booked Events", width=25, height=2, command=lambda: view_booked_events(username)).pack(pady=10)
    tk.Button(dash, text="Logout", width=25, height=2, bg="red", fg="white", command=dash.destroy).pack(pady=10)

# ---------------- STUDENT: CALENDAR PAGE ---------------- #
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
            tk.Label(evf, text=f" {ename} ({selected_date})", bg="#1e1e1e", fg="yellow", font=("Arial", 12, "bold")).pack(anchor='w')
            tk.Label(evf, text=f" {venue}", bg="#1e1e1e", fg="yellow", font=("Arial", 11)).pack(anchor='w', pady=1)
            tk.Label(evf, text=f" {desc}", bg="#1e1e1e", fg="white", wraplength=480, justify='left').pack(anchor='w', pady=3)

            # Registration form
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
                file_exists = os.path.isfile("registrations.csv")
                with open("registrations.csv", "a", newline="") as f:
                    writer = csv.writer(f)
                    if not file_exists:
                        writer.writerow(["Name", "Roll", "Tickets", "Date", "Event", "Venue", "Description"])
                    writer.writerow([name_user, roll, tickets, selected_date, ename, venue, desc])
                messagebox.showinfo("Success", f"✅ Registered for {ename} on {selected_date}")

            tk.Button(evf, text="Book / Register", command=register_event,
                      bg="green", fg="white", font=("Arial", 11, "bold")).pack(pady=6)

    cal.bind("<<CalendarSelected>>", show_event_and_registration)

# ---------------- STUDENT: BOOKED EVENTS ---------------- #
def view_booked_events(username):
    booked = tk.Toplevel()
    booked.title("My Booked Events")
    booked.geometry("420x420")
    booked.config(bg="#1e1e1e")

    tk.Label(booked, text=f" Booked Events - {username}",
             bg="#1e1e1e", fg="white", font=("Arial", 14, "bold")).pack(pady=10)

    if not os.path.isfile("registrations.csv"):
        tk.Label(booked, text="No bookings yet.", bg="#1e1e1e", fg="gray").pack(pady=20)
        return

    # ---- Load current valid events from database ----
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT name, date FROM events")
    valid_events = {(row[0], row[1]) for row in cur.fetchall()}
    conn.close()

    found = False
    valid_bookings = []

    with open("registrations.csv", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Name"] == username:
                # Only display booking if event still exists
                if (row["Event"], row["Date"]) in valid_events:
                    found = True
                    valid_bookings.append(row)
                # Optional: Skip deleted events automatically

    if not found:
        tk.Label(booked, text="No active event bookings found.",
                 bg="#1e1e1e", fg="gray").pack(pady=20)
        return

    # ---- Display current valid bookings ----
    for row in valid_bookings:
        tk.Label(booked, text=f" {row['Date']} - {row['Event']}",
                 bg="#1e1e1e", fg="yellow", font=("Arial", 11, "bold")).pack(anchor="w", padx=15)
        tk.Label(booked, text=f" {row['Venue']}", bg="#1e1e1e", fg="white").pack(anchor="w", padx=15)
        tk.Label(booked, text=f" Tickets: {row['Tickets']}", bg="#1e1e1e", fg="lightgreen").pack(anchor="w", padx=15)
        tk.Label(booked, text="-"*60, bg="#1e1e1e", fg="gray").pack()

# ---------------- LOGIN PAGE ---------------- #
def login():
    name = name_entry.get().strip()
    password = password_entry.get().strip()

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("SELECT * FROM admins WHERE username=? AND password=?", (name, password))
    admin = cur.fetchone()
    if admin:
        messagebox.showinfo("Admin Login", f"Welcome Admin {name}!")
        admin_dashboard()
        conn.close()
        return

    cur.execute("SELECT * FROM students WHERE username=? AND password=?", (name, password))
    student = cur.fetchone()
    conn.close()

    if student:
        messagebox.showinfo("Login Success", f"Welcome {name}!")
        student_dashboard(name)
    else:
        messagebox.showerror("Error", "Invalid login!")

# ---------------- MAIN ROOT ---------------- #
init_db()git status
seed_users()

root = tk.Tk()
root.title('LOGIN PAGE')
root.geometry('530x250')
root.config(bg='#203b2a')

frame = tk.Frame(root, background='#203b2a')
git status
tk.Label(frame, text='Name:', background='#203b2a', fg='white',
          font=('Times New Roman', 20, 'bold'), pady=15).grid(row=0, column=0)
name_entry = tk.Entry(frame, background='white', fg='black', font=('Ink Free', 20, 'bold'))
name_entry.grid(row=0, column=1)

tk.Label(frame, text='Password:', background='#203b2a', fg='white',
          font=('Times New Roman', 20, 'bold'), pady=15).grid(row=1, column=0)
password_entry = tk.Entry(frame, bg='white', fg='black', font=('Ink Free', 20, 'bold'),show='*')
password_entry.grid(row=1, column=1)

tk.Button(frame, text='LOGIN', bg='#203b2a', fg='white', command=login, pady=10).grid(row=2, column=1, pady=10)

frame.pack()
root.mainloop()

