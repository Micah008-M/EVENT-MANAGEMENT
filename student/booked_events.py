import tkinter as tk
import sqlite3
import os
import csv
from utils.constants import DB_FILE, CSV_FILE

def view_booked_events(username):
    booked = tk.Toplevel()
    booked.title("My Booked Events")
    booked.geometry("420x420")
    booked.config(bg="#1e1e1e")

    tk.Label(booked, text=f" Booked Events - {username}",
             bg="#1e1e1e", fg="white", font=("Arial", 14, "bold")).pack(pady=10)

    if not os.path.isfile(CSV_FILE):
        tk.Label(booked, text="No bookings yet.", bg="#1e1e1e", fg="gray").pack(pady=20)
        return

    # Load valid events from database
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT name, date FROM events")
    valid_events = {(row[0], row[1]) for row in cur.fetchall()}
    conn.close()

    found = False
    valid_bookings = []

    with open(CSV_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Name"] == username:
                if (row["Event"], row["Date"]) in valid_events:
                    found = True
                    valid_bookings.append(row)

    if not found:
        tk.Label(booked, text="No active event bookings found.",
                 bg="#1e1e1e", fg="gray").pack(pady=20)
        return

    # Display bookings
    for row in valid_bookings:
        tk.Label(booked, text=f" {row['Date']} - {row['Event']}",
                 bg="#1e1e1e", fg="yellow", font=("Arial", 11, "bold")).pack(anchor="w", padx=15)
        tk.Label(booked, text=f" {row['Venue']}", bg="#1e1e1e", fg="white").pack(anchor="w", padx=15)
        tk.Label(booked, text=f" Tickets: {row['Tickets']}", bg="#1e1e1e", fg="lightgreen").pack(anchor="w", padx=15)
        tk.Label(booked, text="-"*60, bg="#1e1e1e", fg="gray").pack()
