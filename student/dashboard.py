import tkinter as tk
from student.calendar_page import open_calendar_page
from student.booked_events import view_booked_events

def student_dashboard(username):
    dash = tk.Toplevel()
    dash.title("Student Dashboard")
    dash.geometry("400x320")
    dash.config(bg="#203b2a")

    tk.Label(dash, text=f"Welcome, {username}", font=("Arial", 14, "bold"),
             bg="#203b2a", fg="white").pack(pady=20)
    tk.Button(dash, text="View Calendar & Register", width=25, height=2,
              command=lambda: open_calendar_page(username)).pack(pady=10)
    tk.Button(dash, text="Booked Events", width=25, height=2,
              command=lambda: view_booked_events(username)).pack(pady=10)
    tk.Button(dash, text="Logout", width=25, height=2, bg="red", fg="white",
              command=dash.destroy).pack(pady=10)
