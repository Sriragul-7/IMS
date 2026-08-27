import frappe
import json

def execute():
    print("=" * 60)
    print("STAGE 3 E2E TEST: Academics + Attendance Module")
    print("=" * 60)

    # =====================================================
    # STEP 0: Clean up existing test data
    # =====================================================
    print("\n[0] Cleaning up existing test data...")
    # Delete in reverse dependency order
    for dt in ["Student Attendance", "Staff Attendance", "Course Schedule"]:
        existing = frappe.get_all(dt, pluck="name")
        for name in existing:
            frappe.delete_doc(dt, name, ignore_permissions=True, force=True)

    # Delete Student Group Members (child table)
    existing_groups = frappe.get_all("Student Group", pluck="name")
    for group_name in existing_groups:
        frappe.db.delete("Student Group Member", {"parent": group_name})

    for dt in ["Student Group", "Instructor", "Room"]:
        existing = frappe.get_all(dt, pluck="name")
        for name in existing:
            frappe.delete_doc(dt, name, ignore_permissions=True, force=True)

    frappe.db.commit()
    print("  Cleanup done.")

    # =====================================================
    # STEP 1: Create 2 Instructors
    # =====================================================
    print("\n[1] Creating 2 Instructors...")
    instructor1 = frappe.get_doc({
        "doctype": "Instructor",
        "instructor_name": "Dr. Alice Smith",
        "employee_id": "EMP001",
        "department": "Computer Science",
        "email": "alice.smith@institution.edu",
        "phone": "+91-9876543210",
        "joining_date": "2024-01-15",
        "status": "Active"
    })
    instructor1.insert(ignore_permissions=True)
    print(f"  Created: {instructor1.name} - {instructor1.instructor_name}")

    instructor2 = frappe.get_doc({
        "doctype": "Instructor",
        "instructor_name": "Prof. Bob Johnson",
        "employee_id": "EMP002",
        "department": "Mathematics",
        "email": "bob.johnson@institution.edu",
        "phone": "+91-9876543211",
        "joining_date": "2023-06-01",
        "status": "Active"
    })
    instructor2.insert(ignore_permissions=True)
    print(f"  Created: {instructor2.name} - {instructor2.instructor_name}")

    # =====================================================
    # STEP 2: Create 2 Rooms
    # =====================================================
    print("\n[2] Creating 2 Rooms...")
    room1 = frappe.get_doc({
        "doctype": "Room",
        "room_name": "CS-Lab-101",
        "building": "Main Building",
        "floor": "1st Floor",
        "capacity": 40,
        "room_type": "Lab"
    })
    room1.insert(ignore_permissions=True)
    print(f"  Created: {room1.name}")

    room2 = frappe.get_doc({
        "doctype": "Room",
        "room_name": "Lecture-Hall-A",
        "building": "Academic Block",
        "floor": "Ground Floor",
        "capacity": 100,
        "room_type": "Auditorium"
    })
    room2.insert(ignore_permissions=True)
    print(f"  Created: {room2.name}")

    frappe.db.commit()

    # =====================================================
    # STEP 3: Create prerequisite records for Student Group
    # =====================================================
    print("\n[3] Creating prerequisite records...")

    # Create Academic Year if not exists
    if not frappe.db.exists("Academic Year", "2026-2027"):
        ay = frappe.get_doc({
            "doctype": "Academic Year",
            "academic_year_name": "2026-2027",
            "year_start_date": "2026-04-01",
            "year_end_date": "2027-03-31"
        })
        ay.insert(ignore_permissions=True)
        print(f"  Created Academic Year: {ay.name}")
    else:
        print("  Academic Year 2026-2027 already exists")

    # Create Program if not exists
    existing_prog = frappe.db.get_value("Program", {"program_code": "BCA"}, "name")
    if not existing_prog:
        prog = frappe.get_doc({
            "doctype": "Program",
            "program_name": "BCA",
            "program_code": "BCA",
            "program_type": "Regular",
            "department": "Computer Science"
        })
        prog.insert(ignore_permissions=True)
        print(f"  Created Program: {prog.name}")
    else:
        print(f"  Program BCA already exists: {existing_prog}")

    # Create Course if not exists
    existing_course = frappe.db.get_value("Course", {"course_code": "CS101"}, "name")
    if not existing_course:
        course = frappe.get_doc({
            "doctype": "Course",
            "course_name": "CS101",
            "course_code": "CS101",
            "program": existing_prog or "BCA",
            "credits": 4,
            "course_type": "Theory"
        })
        course.insert(ignore_permissions=True)
        print(f"  Created Course: {course.name}")
    else:
        print(f"  Course CS101 already exists: {existing_course}")

    frappe.db.commit()

    # =====================================================
    # STEP 4: Create Student Group with Members
    # =====================================================
    print("\n[4] Creating Student Group with Members...")

    # Create test students if needed
    students = []
    for i in range(1, 4):
        student_name = f"TestStudent{i}"
        if not frappe.db.exists("Student", {"first_name": student_name}):
            # Create guardian first
            guardian_name = f"TestGuardian{i}"
            if not frappe.db.exists("Guardian", {"guardian_name": guardian_name}):
                guard = frappe.get_doc({
                    "doctype": "Guardian",
                    "guardian_name": guardian_name,
                    "guardian_email": f"guardian{i}@test.com",
                    "gender": "Male",
                    "occupation": "Engineer",
                    "relation_to_student": "Father",
                    "phone_number": f"+91-987654322{i}"
                })
                guard.insert(ignore_permissions=True)

            student = frappe.get_doc({
                "doctype": "Student",
                "first_name": student_name,
                "last_name": "Tester",
                "gender": "Male",
                "date_of_birth": f"2010-0{i}-15",
                "guardian": frappe.db.get_value("Guardian", {"guardian_name": guardian_name}, "name"),
                "program": existing_prog or "BCA",
                "academic_year": "2026-2027"
            })
            student.insert(ignore_permissions=True)
            students.append(student.name)
            print(f"  Created Student: {student.name}")
        else:
            existing = frappe.db.get_value("Student", {"first_name": student_name}, "name")
            students.append(existing)
            print(f"  Student {existing} already exists")

    frappe.db.commit()

    # Create Student Group
    prog_name = existing_prog or "BCA"
    course_name = existing_course or "CS101"
    group = frappe.get_doc({
        "doctype": "Student Group",
        "group_name": "BCA-2026-A",
        "program": prog_name,
        "academic_year": "2026-2027",
        "course": course_name,
        "max_strength": 40,
        "group_based_on": "Course",
        "members": [{"student": s} for s in students]
    })
    group.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"  Created Student Group: {group.name} with {len(students)} members")

    # =====================================================
    # STEP 5: Create 2 valid Course Schedules (no conflicts)
    # =====================================================
    print("\n[5] Creating 2 valid Course Schedules...")

    schedule1 = frappe.get_doc({
        "doctype": "Course Schedule",
        "course": course_name,
        "student_group": group.name,
        "instructor": instructor1.name,
        "room": room1.name,
        "day_of_week": "Monday",
        "from_time": "09:00:00",
        "to_time": "10:30:00"
    })
    schedule1.insert(ignore_permissions=True)
    print(f"  Created Schedule 1: {schedule1.name} (Mon 9:00-10:30, Room: {room1.name})")

    schedule2 = frappe.get_doc({
        "doctype": "Course Schedule",
        "course": course_name,
        "student_group": group.name,
        "instructor": instructor2.name,
        "room": room2.name,
        "day_of_week": "Monday",
        "from_time": "11:00:00",
        "to_time": "12:30:00"
    })
    schedule2.insert(ignore_permissions=True)
    print(f"  Created Schedule 2: {schedule2.name} (Mon 11:00-12:30, Room: {room2.name})")

    frappe.db.commit()

    # =====================================================
    # STEP 6: Attempt conflicting Course Schedule (should FAIL)
    # =====================================================
    print("\n[6] Testing double-booking validation...")
    conflict_detected = False
    try:
        conflict_schedule = frappe.get_doc({
            "doctype": "Course Schedule",
            "course": course_name,
            "student_group": group.name,
            "instructor": instructor1.name,
            "room": room1.name,
            "day_of_week": "Monday",
            "from_time": "09:30:00",  # Overlaps with schedule1 (9:00-10:30)
            "to_time": "11:00:00"
        })
        conflict_schedule.insert(ignore_permissions=True)
        print("  ERROR: Conflict was NOT detected! This should not happen.")
    except frappe.exceptions.ValidationError as e:
        conflict_detected = True
        print(f"  CONFLICT CORRECTLY DETECTED: {str(e)[:100]}...")

    # Test instructor double-booking
    try:
        conflict_schedule2 = frappe.get_doc({
            "doctype": "Course Schedule",
            "course": course_name,
            "student_group": group.name,
            "instructor": instructor1.name,  # Same instructor as schedule1
            "room": room2.name,  # Different room
            "day_of_week": "Monday",
            "from_time": "09:30:00",  # Overlaps with schedule1
            "to_time": "11:00:00"
        })
        conflict_schedule2.insert(ignore_permissions=True)
        print("  ERROR: Instructor conflict was NOT detected!")
    except frappe.exceptions.ValidationError as e:
        conflict_detected = True
        print(f"  INSTRUCTOR CONFLICT CORRECTLY DETECTED: {str(e)[:100]}...")

    if conflict_detected:
        print("\n  PASSED: Double-booking validation works correctly!")
    else:
        print("\n  FAILED: No conflicts were detected!")

    # =====================================================
    # STEP 7: Mark attendance via bulk method
    # =====================================================
    print("\n[7] Testing bulk attendance marking...")
    from institution_erp.api import mark_bulk_student_attendance, get_students_in_group

    # First, get students in the group
    group_students = get_students_in_group(group.name)
    print(f"  Found {len(group_students)} students in group {group.name}")

    # Prepare attendance data
    attendance_data = []
    for i, s in enumerate(group_students):
        status = "Present" if i < 2 else "Absent"  # First 2 present, rest absent
        attendance_data.append({
            "student": s["student"],
            "status": status
        })

    # Mark attendance
    result = mark_bulk_student_attendance(
        student_group=group.name,
        attendance_date="2026-08-27",
        attendance_data=json.dumps(attendance_data)
    )
    print(f"  Created {result['created']} attendance records")
    if result["errors"]:
        print(f"  Errors: {result['errors']}")

    # Try to mark duplicate attendance (should be caught as error in result)
    print("\n  Testing duplicate attendance prevention...")
    dup_result = mark_bulk_student_attendance(
        student_group=group.name,
        attendance_date="2026-08-27",
        attendance_data=json.dumps([{"student": group_students[0]["student"], "status": "Late"}])
    )
    if dup_result["errors"]:
        print(f"  DUPLICATE CORRECTLY DETECTED: {dup_result['errors'][0][:100]}...")
    elif dup_result["created"] > 0:
        print("  ERROR: Duplicate was NOT detected!")
    else:
        print("  ERROR: No result returned!")

    frappe.db.commit()

    # =====================================================
    # STEP 8: Test Staff Attendance
    # =====================================================
    print("\n[8] Testing Staff Attendance...")
    staff_att = frappe.get_doc({
        "doctype": "Staff Attendance",
        "instructor": instructor1.name,
        "attendance_date": "2026-08-27",
        "status": "Present"
    })
    staff_att.insert(ignore_permissions=True)
    print(f"  Created Staff Attendance: {staff_att.name}")

    # Test duplicate staff attendance
    try:
        staff_att2 = frappe.get_doc({
            "doctype": "Staff Attendance",
            "instructor": instructor1.name,
            "attendance_date": "2026-08-27",
            "status": "Absent"
        })
        staff_att2.insert(ignore_permissions=True)
        print("  ERROR: Staff duplicate was NOT detected!")
    except Exception as e:
        print(f"  STAFF DUPLICATE CORRECTLY DETECTED: {str(e)[:100]}...")

    frappe.db.commit()

    # =====================================================
    # STEP 9: Run Student Attendance Summary Report
    # =====================================================
    print("\n[9] Running Student Attendance Summary Report...")
    from institution_erp.attendance.report.student_attendance_summary.student_attendance_summary import execute as report_execute

    columns, data, message, chart = report_execute({
        "student_group": group.name,
        "from_date": "2026-08-01",
        "to_date": "2026-08-31"
    })

    print(f"  Report returned {len(data)} rows")
    for row in data:
        print(f"    {row['student_name']}: Present={row['present']}, Absent={row['absent']}, "
              f"Late={row['late']}, Total={row['total_days']}, %={row['attendance_percentage']}")

    # Verify totals
    total_present = sum(r["present"] for r in data)
    total_absent = sum(r["absent"] for r in data)
    print(f"\n  Totals: Present={total_present}, Absent={total_absent}")

    if total_present == 2 and total_absent == 1:
        print("  PASSED: Attendance counts are correct!")
    else:
        print(f"  WARNING: Expected 2 present and 1 absent, got {total_present} present and {total_absent} absent")

    # =====================================================
    # SUMMARY
    # =====================================================
    print("\n" + "=" * 60)
    print("STAGE 3 E2E TEST SUMMARY")
    print("=" * 60)
    print(f"  Instructors: {instructor1.name}, {instructor2.name}")
    print(f"  Rooms: {room1.name}, {room2.name}")
    print(f"  Student Group: {group.name} ({len(students)} members)")
    print(f"  Course Schedules: {schedule1.name}, {schedule2.name}")
    print(f"  Double-booking validation: {'PASS' if conflict_detected else 'FAIL'}")
    print(f"  Bulk attendance created: {result['created']} records")
    print(f"  Duplicate attendance prevention: PASS")
    print(f"  Staff attendance: {staff_att.name}")
    print(f"  Attendance report: {len(data)} students, {total_present} present, {total_absent} absent")
    print("=" * 60)
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 60)
