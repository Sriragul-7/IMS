import frappe

def execute():
    records = frappe.get_all("Student Attendance", fields=["name", "student", "attendance_date", "course_schedule", "status"])
    print("Attendance records:")
    for r in records:
        print(f"  {r.name}: student={r.student}, date={r.attendance_date}, schedule={repr(r.course_schedule)}, status={r.status}")

    if records:
        student = records[0].student
        result = frappe.db.sql(
            "SELECT name FROM `tabStudent Attendance` WHERE student = %s AND attendance_date = %s AND (course_schedule IS NULL OR course_schedule = '')",
            (student, "2026-08-27"),
        pluck="name",
        )
        print(f"\nManual duplicate check for {student}: {result}")
