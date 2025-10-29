# 🎟️ Event Management System (Tkinter + SQLite)

A desktop-based Event Management application built using **Python**, **Tkinter**, **SQLite**, and **tkcalendar**.

This system allows **Admins** to manage events (add/delete), and **Students** to view events on a calendar, register for them, and see their booked events.

---

## 📁 Project Structure
event_manager/
│
├── main.py # Entry point - Login Page
│
├── database/
│ ├── init.py
│ └── db_setup.py # Database initialization & seeding
│
├── admin/
│ ├── init.py
│ ├── dashboard.py # Admin Dashboard (menu)
│ ├── add_event.py # Add new event form
│ └── delete_event.py # Delete event interface
│
├── student/
│ ├── init.py
│ ├── dashboard.py # Student Dashboard
│ ├── calendar_page.py # Calendar + Registration page
│ └── booked_events.py # View registered events
│
├── utils/
│ ├── init.py
│ └── constants.py # Shared constants (e.g., DB_FILE, CSV_FILE)
│
└── assets/
└── registrations.csv # Created automatically for event bookings

---

## 🚀 Features

### 👨‍💼 Admin Portal
- Add new events with date, venue, and description  
- Delete existing events  
- Manage event database directly  

### 🎓 Student Portal
- Login with student credentials  
- View all upcoming events on a calendar  
- Register for events (stored in `registrations.csv`)  
- View only **active bookings** (auto-filters deleted events)  

### 💾 Data Storage
- SQLite database (`events.db`) stores:
  - Events
  - Admins
  - Students  
- CSV file (`registrations.csv`) stores student registrations  

---

## 🧩 Requirements

Make sure you have **Python 3.8+** installed.

Install dependencies using:

```bash
pip install tkcalendar


