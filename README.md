# Student Management Portal
Assignment 3 — End-to-End Portal Design

A console-based Student Management Portal written in Python 3, with an optional web interface built using Flask.

---

## Team Members
| Member | Roll Number |
|--------|-------------|
| Maham Humayun Sawhney | 25L-5068 |
| Syeda Batool Fatima Rizvi | 25L-5189 |

---

## Portal Type
Student Management Portal — manages student records including ID, name, age, course, marks, and grade.

---

## Features
- Login system with username and password (max 3 attempts)
- View all student records
- Add new student with input validation
- Search by student ID or name
- Update existing records
- Delete records with confirmation
- Generate summary report (totals, averages, grade and course breakdown)
- All data saved to CSV and JSON files automatically

---

## Project Files

| File | Description |
|------|-------------|
| `portal.py` | Console version — all required assignment functions |
| `app.py` | Web version using Flask |
| `data/users.json` | Stores login credentials |
| `data/students.csv` | Stores student records |
| `reports/summary_report.txt` | Auto-generated report file |
| `templates/` | HTML pages for the web version |
| `requirements.txt` | Python packages needed (Flask only) |
| `run_frontend.bat` | Double-click to start the web version |
| `run_console.bat` | Double-click to start the console version |

---

## Requirements
- Python 3.8 or higher
- Flask (web version only)

---

## Setup on a New Laptop

1. Install Python from https://www.python.org/downloads/  
   Make sure to tick **Add Python to PATH** during install.

2. Open a terminal inside the project folder.

3. Create a virtual environment:
   ```
   py -3.12 -m venv venv
   ```

4. Install Flask:
   ```
   venv\Scripts\pip install flask
   ```

5. Run the web portal:
   ```
   venv\Scripts\python app.py
   ```
   Then open: http://localhost:5000

   Or just double-click **run_frontend.bat** after step 3 and 4.

---

## Run Console Version
```
python portal.py
```
Or double-click **run_console.bat**

---

## Login Credentials
| Username | Password | Role  |
|----------|----------|-------|
| admin    | admin123 | admin |
| maham    | pass123  | staff |

---

## Data File Formats

**data/users.json**
```json
[
  { "username": "admin", "password": "admin123", "role": "admin" }
]
```

**data/students.csv**
```
student_id,name,age,course,marks,grade
S001,Ali Hassan,20,Computer Science,85.0,A
```

---

## Error Handling

| Error | Location | Behaviour |
|-------|----------|-----------|
| FileNotFoundError | load_data() | Creates an empty file and continues |
| PermissionError | save_data(), report | Shows error message, no crash |
| ValueError | add_record(), update_record() | Rejects non-numeric age or marks |
| json.JSONDecodeError | load_users() | Shows corrupted file message |
| Blank input | Login and add forms | Shows warning, re-prompts |
| Duplicate ID | add_record() | Rejects the record and shows error |

---

## Work Division

| Task | Maham Humayun | Syeda Batool |
|------|---------------|--------------|
| user_login() | Yes | |
| add_record() | | Yes |
| search_record() | Yes | |
| generate_report() | Yes | |
| File handling | | Yes |
| Exception handling | Yes | |
| Main menu loop | Yes | |
| Web frontend (app.py) | | Yes |
| Notebook | Yes | |
| Report and README | | Yes |

---

## GitHub
See github_link.txt
