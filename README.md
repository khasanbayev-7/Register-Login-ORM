# 🔐 Register/Login System with SQLAlchemy ORM (No Flask)

This is a clean, powerful, and secure user authentication system written in Python **without using any web framework** (like Flask or Django). It uses **SQLAlchemy ORM** to interact with a local **SQLite database**, and works entirely from the command line.

---

## 🚀 Features

- 📝 **User Registration** with:
  - Username
  - Email (validated)
  - Phone number (Uzbek format: +998xxxxxxxxx)
  - Address
  - Date of birth (YYYY-MM-DD)
  - Gender (Male/Female)
  - Job
  - Password (with strength check)

- 🔐 **User Login**  
- 🗑️ **User Deletion**  
- 🛠️ **Admin Panel**  
  - View all users  
  - Delete any user  
  - Update any user’s data  
- 💪 **Password Strength Checker** (Easy, Medium, Strong)
- 🎯 Fully terminal-based — no external UI
- ⚙️ Pure Python + SQLAlchemy — **no Flask**

---

## 🧠 Password Strength Logic

The password strength is checked based on:
- Length (minimum 8 characters)
- Use of lowercase, uppercase, digits, and symbols

🟢 **Strong**: Contains all character types  
🟡 **Medium**: Missing one type  
🔴 **Weak**: Only letters or only digits

---

## 💾 Technologies Used

| Component     | Description             |
|---------------|--------------------------|
| Python 3.x     | Core language            |
| SQLite         | Database engine          |
| SQLAlchemy ORM | Database abstraction     |
| `re` module    | Input validation         |

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/khasanbayev-7/Register-Login-ORM.git
cd Register-Login-ORM
