"""PS 75 - Student Course Registration System (Python 3)"""
import os

FILE = "registrations.txt"
MAX_COURSES = 3


class Course:
    def __init__(self, code, title, capacity):
        self.code = code
        self.title = title
        self.capacity = capacity
        self.students = []  # enrolled student IDs

    def seats_left(self):
        return self.capacity - len(self.students)

    def is_full(self):
        return self.seats_left() <= 0


class Student:
    def __init__(self, sid, name):
        self.sid = sid
        self.name = name
        self.courses = []  # course codes


class RegistrationSystem:
    def __init__(self):
        self.courses = {
            "CS101": Course("CS101", "Programming", 2),
            "MA101": Course("MA101", "Mathematics", 30),
            "PH101": Course("PH101", "Physics", 30),
        }
        self.students = {}
        self.load()

    # ---------- file handling ----------
    def load(self):
        if not os.path.exists(FILE):
            return
        with open(FILE) as f:
            for line in f:
                parts = [p.strip() for p in line.strip().split(",")]
                if len(parts) != 3:
                    continue
                sid, name, code = parts
                if code not in self.courses:
                    continue
                st = self.students.setdefault(sid, Student(sid, name))
                if code not in st.courses:
                    st.courses.append(code)
                    self.courses[code].students.append(sid)

    def save(self):
        with open(FILE, "w") as f:
            for sid, st in self.students.items():
                for code in st.courses:
                    f.write(f"{sid},{st.name},{code}\n")

    # ---------- operations ----------
    def register(self, sid, name, code):
        course = self.courses.get(code)
        if course is None:
            return f"Course {code} does not exist."
        student = self.students.get(sid)
        if student and code in student.courses:
            return f"Student {sid} is already registered in {code}."
        if course.is_full():
            return f"Course {code} is full."
        if student and len(student.courses) >= MAX_COURSES:
            return f"Student {sid} cannot register for more than {MAX_COURSES} courses."
        if student is None:
            student = self.students[sid] = Student(sid, name)
        student.courses.append(code)
        course.students.append(sid)
        self.save()
        return (f"Registered: {student.name} ({sid}) in {code} - {course.title}.\n"
                f"Seats left: {course.seats_left()}")

    def drop(self, sid, code):
        student = self.students.get(sid)
        course = self.courses.get(code)
        if course is None:
            return f"Course {code} does not exist."
        if student is None or code not in student.courses:
            return f"Student {sid} is not registered in {code}."
        student.courses.remove(code)
        course.students.remove(sid)
        self.save()
        return f"{student.name} ({sid}) dropped {code}. Seats left: {course.seats_left()}"

    def view_student(self, sid):
        student = self.students.get(sid)
        if student is None:
            return f"Student {sid} not found."
        if not student.courses:
            return f"{student.name} ({sid}) has no registered courses."
        lines = [f"{student.name} ({sid}) is registered in:"]
        for code in student.courses:
            lines.append(f"  {code} - {self.courses[code].title}")
        return "\n".join(lines)

    def view_courses(self):
        lines = []
        for c in self.courses.values():
            lines.append(f"{c.code} - {c.title} | Capacity: {c.capacity} | "
                         f"Enrolled: {len(c.students)} | Seats left: {c.seats_left()}")
        return "\n".join(lines)


def main():
    system = RegistrationSystem()
    menu = ("\n1. Register\n2. Drop course\n3. View student\n"
            "4. View course list\n5. Exit")
    while True:
        print(menu)
        try:
            choice = input("Menu: ").strip().lower()
        except EOFError:
            break
        if choice in ("1", "register"):
            sid = input("Student ID: ").strip()
            name = input("Name: ").strip()
            code = input("Course: ").strip().upper()
            print(system.register(sid, name, code))
        elif choice in ("2", "drop", "drop course"):
            sid = input("Student ID: ").strip()
            code = input("Course: ").strip().upper()
            print(system.drop(sid, code))
        elif choice in ("3", "view", "view student"):
            print(system.view_student(input("Student ID: ").strip()))
        elif choice in ("4", "courses", "view course list"):
            print(system.view_courses())
        elif choice in ("5", "exit"):
            print("Goodbye!")
            break
        else:
            print("Invalid menu choice.")


if __name__ == "__main__":
    main()
