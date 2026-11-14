import json
import csv
import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "smp_secret_2024"

# file paths
USERS_FILE   = "data/users.json"
RECORDS_FILE = "data/students.csv"
REPORT_FILE  = "reports/summary_report.txt"
HEADERS      = ["student_id", "name", "age", "course", "marks", "grade"]


def calculate_grade(marks):
    """Return A, B, C, D or F based on marks out of 100."""
    if marks >= 80:
        return "A"
    elif marks >= 65:
        return "B"
    elif marks >= 50:
        return "C"
    elif marks >= 40:
        return "D"
    else:
        return "F"


def load_data():
    """Read students.csv and return a list of student dictionaries."""
    students = []
    try:
        with open(RECORDS_FILE, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                students.append(row)
    except FileNotFoundError:
        save_data([])
    return students


def save_data(students):
    """Write the students list to students.csv."""
    try:
        if not os.path.exists("data"):
            os.makedirs("data")
        with open(RECORDS_FILE, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=HEADERS)
            writer.writeheader()
            for student in students:
                writer.writerow(student)
    except PermissionError:
        print(f"Warning: could not write to '{RECORDS_FILE}' (file may be open in another program). Changes not saved.")


def load_users():
    """Read users.json and return the list of users."""
    try:
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


@app.route("/", methods=["GET", "POST"])
def login():
    """Login page — check username and password against users.json."""
    error = ""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            error = "Please enter both username and password."
        else:
            users = load_users()
            for user in users:
                if user["username"] == username and user["password"] == password:
                    session["username"] = username
                    session["role"]     = user["role"]
                    return redirect(url_for("view_all"))
            error = "Incorrect username or password."

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    """Clear session and redirect to login."""
    session.clear()
    return redirect(url_for("login"))


@app.route("/view")
def view_all():
    """Show all student records in a table."""
    if "username" not in session:
        return redirect(url_for("login"))
    students = load_data()
    return render_template("view.html", students=students)


@app.route("/add", methods=["GET", "POST"])
def add_student():
    """Add a new student — validate inputs then save to file."""
    if "username" not in session:
        return redirect(url_for("login"))

    message = ""
    success = False

    if request.method == "POST":
        student_id = request.form.get("student_id", "").strip().upper()
        name       = request.form.get("name", "").strip()
        age        = request.form.get("age", "").strip()
        course     = request.form.get("course", "").strip()
        marks_str  = request.form.get("marks", "").strip()

        if not student_id or not name or not age or not course or not marks_str:
            message = "All fields are required."
        else:
            try:
                age_val = int(age)
                if age_val < 10 or age_val > 80:
                    message = "Age must be between 10 and 80."
                else:
                    try:
                        marks_val = float(marks_str)
                        if marks_val < 0 or marks_val > 100:
                            message = "Marks must be between 0 and 100."
                        else:
                            students  = load_data()
                            duplicate = any(s["student_id"] == student_id for s in students)
                            if duplicate:
                                message = f"Student ID '{student_id}' already exists."
                            else:
                                grade = calculate_grade(marks_val)
                                students.append({
                                    "student_id": student_id,
                                    "name":       name,
                                    "age":        str(age_val),
                                    "course":     course,
                                    "marks":      str(marks_val),
                                    "grade":      grade
                                })
                                save_data(students)
                                message = f"Student '{name}' added. Grade: {grade}"
                                success = True
                    except ValueError:
                        message = "Marks must be a number (e.g. 75 or 88.5)."
            except ValueError:
                message = "Age must be a whole number."

    return render_template("add.html", message=message, success=success)


@app.route("/search", methods=["GET", "POST"])
def search_student():
    """Search students by ID or name."""
    if "username" not in session:
        return redirect(url_for("login"))

    results  = []
    searched = False

    if request.method == "POST":
        search_by = request.form.get("search_by", "name")
        keyword   = request.form.get("keyword", "").strip()
        searched  = True

        if keyword:
            students = load_data()
            for s in students:
                if search_by == "student_id" and s["student_id"] == keyword.upper():
                    results.append(s)
                elif search_by == "name" and keyword.lower() in s["name"].lower():
                    results.append(s)

    return render_template("search.html", results=results, searched=searched)


@app.route("/update", methods=["GET", "POST"])
def update_student():
    """Find a student by ID and update their record."""
    if "username" not in session:
        return redirect(url_for("login"))

    found   = None
    message = ""
    success = False

    if request.method == "POST":
        action = request.form.get("action")

        if action == "find":
            student_id = request.form.get("student_id", "").strip().upper()
            for s in load_data():
                if s["student_id"] == student_id:
                    found = s
                    break
            if not found:
                message = f"ID '{student_id}' not found."

        elif action == "save":
            student_id = request.form.get("student_id", "").strip().upper()
            students   = load_data()
            invalid    = []
            for s in students:
                if s["student_id"] == student_id:
                    s["name"]   = request.form.get("name", s["name"]).strip()
                    s["course"] = request.form.get("course", s["course"]).strip()
                    try:
                        age_val = int(request.form.get("age", s["age"]))
                        if 10 <= age_val <= 80:
                            s["age"] = str(age_val)
                        else:
                            invalid.append("age must be between 10 and 80")
                    except ValueError:
                        invalid.append("age must be a whole number")
                    try:
                        marks_val = float(request.form.get("marks", s["marks"]))
                        if 0 <= marks_val <= 100:
                            s["marks"] = str(marks_val)
                            s["grade"] = calculate_grade(marks_val)
                        else:
                            invalid.append("marks must be between 0 and 100")
                    except ValueError:
                        invalid.append("marks must be a number")
                    found   = s
                    success = not invalid
                    if invalid:
                        message = "Not updated: " + "; ".join(invalid) + " - previous value kept."
                    else:
                        message = "Record updated successfully."
                    break
            save_data(students)

    return render_template("update.html", found=found, message=message, success=success)


@app.route("/delete", methods=["GET", "POST"])
def delete_student():
    """Find a student by ID and delete after confirmation."""
    if "username" not in session:
        return redirect(url_for("login"))

    found   = None
    message = ""
    success = False

    if request.method == "POST":
        action = request.form.get("action")

        if action == "find":
            student_id = request.form.get("student_id", "").strip().upper()
            for s in load_data():
                if s["student_id"] == student_id:
                    found = s
                    break
            if not found:
                message = f"ID '{student_id}' not found."

        elif action == "confirm_delete":
            student_id = request.form.get("student_id", "").strip().upper()
            students   = load_data()
            students   = [s for s in students if s["student_id"] != student_id]
            save_data(students)
            message = "Record deleted."
            success = True

    return render_template("delete.html", found=found, message=message, success=success)


@app.route("/report")
def report():
    """Generate a summary report and save it to a text file."""
    if "username" not in session:
        return redirect(url_for("login"))

    students     = load_data()
    marks_list   = []
    grade_count  = {}
    course_count = {}

    for s in students:
        try:
            marks_list.append(float(s["marks"]))
        except ValueError:
            pass
        grade_count[s["grade"]]   = grade_count.get(s["grade"], 0) + 1
        course_count[s["course"]] = course_count.get(s["course"], 0) + 1

    stats = {
        "total":   len(students),
        "average": round(sum(marks_list) / len(marks_list), 2) if marks_list else 0,
        "highest": max(marks_list) if marks_list else 0,
        "lowest":  min(marks_list) if marks_list else 0
    }

    try:
        if not os.path.exists("reports"):
            os.makedirs("reports")
        with open(REPORT_FILE, "w") as f:
            f.write("STUDENT MANAGEMENT PORTAL REPORT\n")
            f.write("=" * 40 + "\n")
            f.write(f"Total Students : {stats['total']}\n")
            f.write(f"Average Marks  : {stats['average']}\n")
            f.write(f"Highest Marks  : {stats['highest']}\n")
            f.write(f"Lowest Marks   : {stats['lowest']}\n\n")
            f.write("Grade Distribution:\n")
            for g in sorted(grade_count):
                f.write(f"  Grade {g}: {grade_count[g]}\n")
            f.write("\nStudents Per Course:\n")
            for c, count in course_count.items():
                f.write(f"  {c}: {count}\n")
    except PermissionError:
        pass

    return render_template("report.html",
                           stats=stats,
                           grade_count=grade_count,
                           course_count=course_count)


if __name__ == "__main__":
    print("Starting Student Management Portal...")
    print("Open your browser at: http://localhost:5000")
    app.run(debug=True)
