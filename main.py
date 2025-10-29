import tkinter as tk
from tkinter import messagebox
import sqlite3

from database.db_setup import init_db, seed_users
from admin.dashboard import admin_dashboard
from student.dashboard import student_dashboard
from utils.constants import DB_FILE

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

# ---- Initialize Database ----
init_db()
seed_users()

# ---- Main Tkinter Root ----
root = tk.Tk()
root.title('LOGIN PAGE')
root.geometry('530x250')
root.config(bg='#203b2a')

frame = tk.Frame(root, background='#203b2a')
frame.pack()

tk.Label(frame, text='Name:', bg='#203b2a', fg='white',
          font=('Times New Roman', 20, 'bold')).grid(row=0, column=0, pady=15)
name_entry = tk.Entry(frame, bg='white', fg='black', font=('Ink Free', 20, 'bold'))
name_entry.grid(row=0, column=1)

tk.Label(frame, text='Password:', bg='#203b2a', fg='white',
          font=('Times New Roman', 20, 'bold')).grid(row=1, column=0, pady=15)
password_entry = tk.Entry(frame, bg='white', fg='black', font=('Ink Free', 20, 'bold'), show='*')
password_entry.grid(row=1, column=1)

tk.Button(frame, text='LOGIN', bg='#203b2a', fg='white',
          command=login, pady=10).grid(row=2, column=1, pady=10)

root.mainloop()
