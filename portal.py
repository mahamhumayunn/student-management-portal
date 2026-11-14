import json
import csv
import os

# file paths
USERS_FILE   = "data/users.json"
RECORDS_FILE = "data/students.csv"
REPORT_FILE  = "reports/summary_report.txt"

# column headers for the CSV file
HEADERS = ["student_id", "name", "age", "course", "marks", "grade"]


def calculate_grade(marks):
    """Return A, B, C, D or F based on the marks given."""
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


def load_data(filepath):
    """Read student records from the CSV file and return them as a list."""
    students = []
    try:
        with open(filepath, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                students.append(row)
    except FileNotFoundError:
        print(f"  Note: '{filepath}' was not found. Starting with no records.")
        save_data(filepath, [])
    except PermissionError:
        print(f"  Error: Cannot read '{filepath}'. Check file permissions.")
    return students


def save_data(filepath, students):
    """Write the students list back to the CSV file."""
    try:
        folder = os.path.dirname(filepath)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)
        with open(filepath, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=HEADERS)
            writer.writeheader()
            for student in students:
                writer.writerow(student)
    except PermissionError:
        print(f"  Error: Cannot write to '{filepath}'. Check file permissions.")


def user_login():
    """
    Ask for username and password, check against users.json.
    Give up to 3 attempts. Return (username, role) or (None, None).
    """
    print("\n" + "=" * 40)
    print("        STUDENT PORTAL - LOGIN")
    print("=" * 40)

    try:
        with open(USERS_FILE, "r") as file:
            users = json.load(file)
    except FileNotFoundError:
        print("  Error: User file not found. Contact admin.")
        return None, None
    except json.JSONDecodeError:
        print("  Error: User file is corrupted.")
        return None, None

    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        username = input("  Username: ").strip()
        password = input("  Password: ").strip()

        if not username or not password:
            print("  Username and password cannot be blank.\n")
            attempts += 1
            continue

        for user in users:
            if user["username"] == username and user["password"] == password:
                print(f"\n  Login successful. Welcome, {username}! Role: {user['role']}")
                return username, user["role"]

        attempts += 1
        left = max_attempts - attempts
        if left > 0:
            print(f"  Wrong username or password. {left} attempt(s) remaining.\n")
        else:
            print("  Too many failed attempts. Access denied.")

    return None, None


def add_record(students):
    """
    Collect new student details, validate them, and save to file.
    Rejects duplicate IDs and non-numeric age or marks.
    """
    print("\n--- Add New Student ---")

    student_id = input("  Student ID (e.g. S006): ").strip().upper()
    if not student_id:
        print("  Error: Student ID cannot be blank.")
        return students

    # check for duplicate ID
    for s in students:
        if s["student_id"] == student_id:
            print(f"  Error: ID '{student_id}' already exists.")
            return students

    name = input("  Full Name: ").strip()
    if not name:
        print("  Error: Name cannot be blank.")
        return students

    try:
        age = int(input("  Age: ").strip())
        if age < 10 or age > 80:
            print("  Error: Age must be between 10 and 80.")
            return students
    except ValueError:
        print("  Error: Age must be a whole number.")
        return students

    course = input("  Course: ").strip()
    if not course:
        print("  Error: Course cannot be blank.")
        return students

    try:
        marks = float(input("  Marks (0-100): ").strip())
        if marks < 0 or marks > 100:
            print("  Error: Marks must be between 0 and 100.")
            return students
    except ValueError:
        print("  Error: Marks must be a number like 75 or 88.5.")
        return students

    grade = calculate_grade(marks)

    new_student = {
        "student_id": student_id,
        "name":       name,
        "age":        str(age),
        "course":     course,
        "marks":      str(marks),
        "grade":      grade
    }

    students.append(new_student)
    save_data(RECORDS_FILE, students)
    print(f"  Done! '{name}' added with grade {grade}.")
    return students


def search_record(students):
    """
    Search students by ID (exact) or by name (partial match).
    Print matching results or a not-found message.
    """
    print("\n--- Search Student ---")
    print("  1. Search by Student ID")
    print("  2. Search by Name")
    choice = input("  Choose (1 or 2): ").strip()

    if choice == "1":
        key   = input("  Enter Student ID: ").strip().upper()
        field = "student_id"
    elif choice == "2":
        key   = input("  Enter name (or part of it): ").strip().lower()
        field = "name"
    else:
        print("  Invalid choice.")
        return

    results = []
    for s in students:
        if field == "student_id" and s["student_id"] == key:
            results.append(s)
        elif field == "name" and key in s["name"].lower():
            results.append(s)

    if results:
        print(f"\n  Found {len(results)} record(s):\n")
        print_table(results)
    else:
        print("  No matching student found.")


def generate_report(students):
    """
    Calculate summary stats (total, average, highest, lowest marks,
    grade counts, course counts) and save to a text file.
    """
    print("\n--- Summary Report ---")

    if not students:
        print("  No records to report on.")
        return

    total        = len(students)
    marks_list   = []
    grade_count  = {}
    course_count = {}

    for s in students:
        try:
            marks_list.append(float(s["marks"]))
        except ValueError:
            pass

        g = s["grade"]
        c = s["course"]
        grade_count[g]  = grade_count.get(g, 0) + 1
        course_count[c] = course_count.get(c, 0) + 1

    avg_marks = sum(marks_list) / len(marks_list) if marks_list else 0
    max_marks = max(marks_list) if marks_list else 0
    min_marks = min(marks_list) if marks_list else 0

    lines = [
        "=" * 45,
        "      STUDENT MANAGEMENT PORTAL REPORT",
        "=" * 45,
        f"  Total Students  : {total}",
        f"  Average Marks   : {avg_marks:.2f}",
        f"  Highest Marks   : {max_marks:.2f}",
        f"  Lowest Marks    : {min_marks:.2f}",
        "",
        "  Grade Distribution:"
    ]
    for g in sorted(grade_count):
        lines.append(f"    Grade {g}: {grade_count[g]} student(s)")
    lines.append("")
    lines.append("  Students Per Course:")
    for c, count in course_count.items():
        lines.append(f"    {c}: {count} student(s)")
    lines.append("=" * 45)

    for line in lines:
        print(line)

    try:
        folder = os.path.dirname(REPORT_FILE)
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(REPORT_FILE, "w") as f:
            for line in lines:
                f.write(line + "\n")
        print(f"\n  Report saved to '{REPORT_FILE}'.")
    except PermissionError:
        print("  Could not save report file.")
    finally:
        print("  Report generation complete.")


def view_all_records(students):
    """Print all student records in a table."""
    print("\n--- All Student Records ---")
    if not students:
        print("  No records found.")
        return
    print(f"  Total: {len(students)} student(s)\n")
    print_table(students)


def update_record(students):
    """
    Find a student by ID and let the user update their details.
    Press Enter to keep any existing value unchanged.
    """
    print("\n--- Update Student Record ---")
    student_id = input("  Enter Student ID to update: ").strip().upper()

    found = None
    for s in students:
        if s["student_id"] == student_id:
            found = s
            break

    if not found:
        print(f"  Error: ID '{student_id}' not found.")
        return students

    print(f"  Updating: {found['name']}  (press Enter to keep current value)")

    new_name = input(f"  Name [{found['name']}]: ").strip()
    if new_name:
        found["name"] = new_name

    new_age = input(f"  Age [{found['age']}]: ").strip()
    if new_age:
        try:
            age_val = int(new_age)
            if 10 <= age_val <= 80:
                found["age"] = str(age_val)
            else:
                print("  Age out of range. Keeping old value.")
        except ValueError:
            print("  Invalid age. Keeping old value.")

    new_course = input(f"  Course [{found['course']}]: ").strip()
    if new_course:
        found["course"] = new_course

    new_marks = input(f"  Marks [{found['marks']}]: ").strip()
    if new_marks:
        try:
            marks_val = float(new_marks)
            if 0 <= marks_val <= 100:
                found["marks"] = str(marks_val)
                found["grade"] = calculate_grade(marks_val)
                print(f"  Grade updated to: {found['grade']}")
            else:
                print("  Marks out of range. Keeping old value.")
        except ValueError:
            print("  Invalid marks. Keeping old value.")

    save_data(RECORDS_FILE, students)
    print("  Record updated successfully.")
    return students


def delete_record(students):
    """Find a student by ID and delete after confirmation."""
    print("\n--- Delete Student Record ---")
    student_id = input("  Enter Student ID to delete: ").strip().upper()

    found = None
    for s in students:
        if s["student_id"] == student_id:
            found = s
            break

    if not found:
        print(f"  Error: ID '{student_id}' not found.")
        return students

    print(f"  About to delete: {found['name']} ({found['student_id']})")
    confirm = input("  Are you sure? (yes/no): ").strip().lower()

    if confirm == "yes":
        students.remove(found)
        save_data(RECORDS_FILE, students)
        print("  Record deleted.")
    else:
        print("  Delete cancelled.")

    return students


def print_table(students):
    """Print a list of student records as a formatted table."""
    print(f"  {'ID':<8} {'Name':<20} {'Age':<5} {'Course':<20} {'Marks':<7} {'Grade'}")
    print("  " + "-" * 68)
    for s in students:
        print(f"  {s['student_id']:<8} {s['name']:<20} {s['age']:<5} {s['course']:<20} {s['marks']:<7} {s['grade']}")


def display_menu():
    """Print the main menu."""
    print("\n" + "=" * 40)
    print("   STUDENT MANAGEMENT PORTAL")
    print("=" * 40)
    print("  1. View All Students")
    print("  2. Add New Student")
    print("  3. Search Student")
    print("  4. Update Student Record")
    print("  5. Delete Student Record")
    print("  6. Generate Report")
    print("  7. Exit")
    print("=" * 40)


def main():
    """
    Entry point. Handles login, loads data, then runs the
    main menu loop until the user chooses to exit.
    """
    print("\n" + "=" * 40)
    print("   STUDENT MANAGEMENT PORTAL")
    print("   Python Console Version")
    print("=" * 40)

    username, role = user_login()
    if not username:
        print("\n  Exiting portal.")
        return

    students = load_data(RECORDS_FILE)

    while True:
        display_menu()
        choice = input("  Enter choice (1-7): ").strip()

        if choice == "1":
            view_all_records(students)
        elif choice == "2":
            students = add_record(students)
        elif choice == "3":
            search_record(students)
        elif choice == "4":
            students = update_record(students)
        elif choice == "5":
            students = delete_record(students)
        elif choice == "6":
            generate_report(students)
        elif choice == "7":
            print("\n  Goodbye!")
            break
        else:
            print("  Invalid choice. Enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
