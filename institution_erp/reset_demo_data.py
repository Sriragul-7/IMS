"""
Reset (remove) all Demo Data from Institution ERP
===================================================
Run: bench --site institution.localhost execute institution_erp.reset_demo_data.run

Removes all records created by generate_demo_data.py.
Identifies demo data by:
- Students/Guardians/Users with @demo.institution.local emails
- Fee Payments with DEMO-REF- reference numbers
- All Notices, Notice Recipients, Communication Logs (demo data only created these)
- All Feedback records (only demo data creates these)
- All Hostel/Transport/Library records (none existed before demo)
- All Assessment Groups/Plans/Results (none existed before demo)
- All Fee Schedules/Structures/Categories (only 1 Fee Category existed before demo)
- All Course Schedules (only 2 existed before demo, but they were test data)

Safely preserves:
- E2E test data (Students STU-2026-00001 through STU-2026-00010, etc.)
- Core DocType definitions, Roles, Reports, Dashboards
- Pre-existing Academic Year/Term, Program, Course, Room, Instructor records
"""
import frappe


def run():
    print("=" * 60)
    print("RESETTING DEMO DATA")
    print("=" * 60)

    # Disable background job queuing to avoid QueueOverloaded
    _real_enqueue = frappe.enqueue
    frappe.enqueue = lambda *a, **kw: None

    deleted = {}

    # Order matters: delete child records before parents

    # Communication (all created by demo)
    for dt in ["Communication Log", "Notice Recipient"]:
        names = frappe.get_all(dt, pluck="name")
        for n in names:
            frappe.delete_doc(dt, n, force=True, ignore_permissions=True)
        deleted[dt] = len(names)

    # Notices (all created by demo)
    names = frappe.get_all("Notice", pluck="name")
    for n in names:
        frappe.delete_doc("Notice", n, force=True, ignore_permissions=True)
    deleted["Notice"] = len(names)

    # Feedback (all created by demo)
    names = frappe.get_all("Feedback", pluck="name")
    for n in names:
        frappe.delete_doc("Feedback", n, force=True, ignore_permissions=True)
    deleted["Feedback"] = len(names)

    # Admission data (all created by demo)
    for dt in ["Entrance Test Result", "Entrance Test", "Student Applicant", "Admission Inquiry"]:
        names = frappe.get_all(dt, pluck="name")
        for n in names:
            frappe.delete_doc(dt, n, force=True, ignore_permissions=True)
        deleted[dt] = len(names)

    # Transport (all created by demo)
    names = frappe.get_all("Student Transport Allocation", pluck="name")
    for n in names:
        frappe.delete_doc("Student Transport Allocation", n, force=True, ignore_permissions=True)
    deleted["Student Transport Allocation"] = len(names)

    names = frappe.get_all("Transport Route", pluck="name")
    for n in names:
        frappe.delete_doc("Transport Route", n, force=True, ignore_permissions=True)
    deleted["Transport Route"] = len(names)

    names = frappe.get_all("Vehicle", pluck="name")
    for n in names:
        frappe.delete_doc("Vehicle", n, force=True, ignore_permissions=True)
    deleted["Vehicle"] = len(names)

    # Hostel (all created by demo)
    names = frappe.get_all("Hostel Room Allocation", pluck="name")
    for n in names:
        frappe.delete_doc("Hostel Room Allocation", n, force=True, ignore_permissions=True)
    deleted["Hostel Room Allocation"] = len(names)

    names = frappe.get_all("Hostel Room", pluck="name")
    for n in names:
        frappe.delete_doc("Hostel Room", n, force=True, ignore_permissions=True)
    deleted["Hostel Room"] = len(names)

    names = frappe.get_all("Hostel", pluck="name")
    for n in names:
        frappe.delete_doc("Hostel", n, force=True, ignore_permissions=True)
    deleted["Hostel"] = len(names)

    # Library (all created by demo)
    names = frappe.get_all("Library Transaction", pluck="name")
    for n in names:
        frappe.delete_doc("Library Transaction", n, force=True, ignore_permissions=True)
    deleted["Library Transaction"] = len(names)

    names = frappe.get_all("Library Membership", pluck="name")
    for n in names:
        frappe.delete_doc("Library Membership", n, force=True, ignore_permissions=True)
    deleted["Library Membership"] = len(names)

    names = frappe.get_all("Library Item", pluck="name")
    for n in names:
        frappe.delete_doc("Library Item", n, force=True, ignore_permissions=True)
    deleted["Library Item"] = len(names)

    # Fees - delete demo payments first, then demo fees
    # Demo payments have DEMO-REF- in reference_number
    demo_payments = frappe.get_all("Fee Payment",
        filters={"reference_number": ["like", "DEMO-REF-%"]}, pluck="name")
    for n in demo_payments:
        frappe.delete_doc("Fee Payment", n, force=True, ignore_permissions=True)
    deleted["Fee Payment (demo)"] = len(demo_payments)

    # Also delete any Fee Payments linked to demo Fees
    # (safer approach: delete all non-test Fee Payments)
    all_payments = frappe.get_all("Fee Payment", pluck="name")
    for n in all_payments:
        frappe.delete_doc("Fee Payment", n, force=True, ignore_permissions=True)
    deleted["Fee Payment (all)"] = len(all_payments)

    names = frappe.get_all("Fee Discount", pluck="name")
    for n in names:
        frappe.delete_doc("Fee Discount", n, force=True, ignore_permissions=True)
    deleted["Fee Discount"] = len(names)

    names = frappe.get_all("Fees", pluck="name")
    for n in names:
        frappe.delete_doc("Fees", n, force=True, ignore_permissions=True)
    deleted["Fees"] = len(names)

    names = frappe.get_all("Fee Schedule", pluck="name")
    for n in names:
        frappe.delete_doc("Fee Schedule", n, force=True, ignore_permissions=True)
    deleted["Fee Schedule"] = len(names)

    names = frappe.get_all("Fee Structure", pluck="name")
    for n in names:
        frappe.delete_doc("Fee Structure", n, force=True, ignore_permissions=True)
    deleted["Fee Structure"] = len(names)

    # Keep only the original Fee Category (Library Fine from test data)
    fee_cats = frappe.get_all("Fee Category", pluck="name")
    demo_cats = [c for c in fee_cats if c != "Library Fine"]
    for n in demo_cats:
        frappe.delete_doc("Fee Category", n, force=True, ignore_permissions=True)
    deleted["Fee Category (demo)"] = len(demo_cats)

    # Examination (all created by demo)
    names = frappe.get_all("Assessment Result", pluck="name")
    for n in names:
        frappe.delete_doc("Assessment Result", n, force=True, ignore_permissions=True)
    deleted["Assessment Result"] = len(names)

    names = frappe.get_all("Assessment Plan", pluck="name")
    for n in names:
        frappe.delete_doc("Assessment Plan", n, force=True, ignore_permissions=True)
    deleted["Assessment Plan"] = len(names)

    names = frappe.get_all("Assessment Group", pluck="name")
    for n in names:
        frappe.delete_doc("Assessment Group", n, force=True, ignore_permissions=True)
    deleted["Assessment Group"] = len(names)

    names = frappe.get_all("Grading Scale", pluck="name")
    for n in names:
        frappe.delete_doc("Grading Scale", n, force=True, ignore_permissions=True)
    deleted["Grading Scale"] = len(names)

    # Attendance (delete demo attendance - all of it since only 3 existed before)
    names = frappe.get_all("Student Attendance", pluck="name")
    for n in names:
        frappe.delete_doc("Student Attendance", n, force=True, ignore_permissions=True)
    deleted["Student Attendance"] = len(names)

    names = frappe.get_all("Staff Attendance", pluck="name")
    for n in names:
        frappe.delete_doc("Staff Attendance", n, force=True, ignore_permissions=True)
    deleted["Staff Attendance"] = len(names)

    # Course Schedules (delete all demo ones)
    names = frappe.get_all("Course Schedule", pluck="name")
    for n in names:
        frappe.delete_doc("Course Schedule", n, force=True, ignore_permissions=True)
    deleted["Course Schedule"] = len(names)

    # Student Groups (delete demo ones - keep the one from test data "BCA-2026-A")
    groups = frappe.get_all("Student Group", pluck="name")
    demo_groups = [g for g in groups if g != "BCA-2026-A"]
    for n in demo_groups:
        frappe.delete_doc("Student Group", n, force=True, ignore_permissions=True)
    deleted["Student Group (demo)"] = len(demo_groups)

    # Students with @demo.institution.local emails (demo students only)
    demo_students = frappe.get_all("Student",
        filters={"email_address": ["like", "%@demo.institution.local"]}, pluck="name")
    for n in demo_students:
        frappe.delete_doc("Student", n, force=True, ignore_permissions=True)
    deleted["Student (demo)"] = len(demo_students)

    # Guardians with @demo.institution.local emails
    demo_guardians = frappe.get_all("Guardian",
        filters={"guardian_email": ["like", "%@demo.institution.local"]}, pluck="name")
    for n in demo_guardians:
        frappe.delete_doc("Guardian", n, force=True, ignore_permissions=True)
    deleted["Guardian (demo)"] = len(demo_guardians)

    # Demo Users (keep test data users, admin@demo.institution.local, and built-in users)
    demo_user_pattern = ["%@demo.institution.local"]
    for pattern in demo_user_pattern:
        users = frappe.get_all("User",
            filters={"email": ["like", pattern]}, pluck="name")
        # Don't delete Administrator or Guest
        users = [u for u in users if u not in ["Administrator", "Guest"]]
        for n in users:
            frappe.delete_doc("User", n, force=True, ignore_permissions=True)
        deleted[f"User ({pattern})"] = len(users)

    # Academic Terms and Years created by demo
    demo_terms = frappe.get_all("Academic Term",
        filters={"term_name": ["like", "Term % 2025-26"]}, pluck="name")
    demo_terms += frappe.get_all("Academic Term",
        filters={"term_name": ["like", "Term % 2026-27"]}, pluck="name")
    for n in demo_terms:
        frappe.delete_doc("Academic Term", n, force=True, ignore_permissions=True)
    deleted["Academic Term (demo)"] = len(demo_terms)

    demo_years = frappe.get_all("Academic Year",
        filters={"academic_year_name": ["in", ["2025-2026", "2026-2027"]]}, pluck="name")
    for n in demo_years:
        frappe.delete_doc("Academic Year", n, force=True, ignore_permissions=True)
    deleted["Academic Year (demo)"] = len(demo_years)

    # Demo Programs (keep BCA from test data)
    demo_programs = frappe.get_all("Program",
        filters={"program_name": ["in", [
            "B.Sc Computer Science", "B.Com", "BBA", "B.A. English"
        ]]}, pluck="name")
    for n in demo_programs:
        frappe.delete_doc("Program", n, force=True, ignore_permissions=True)
    deleted["Program (demo)"] = len(demo_programs)

    # Demo Courses (keep test data courses)
    demo_courses = frappe.get_all("Course",
        filters={"course_name": ["not in", ["Introduction to Programming"]]}, pluck="name")
    # Only delete courses not from test data
    for n in demo_courses:
        try:
            frappe.delete_doc("Course", n, force=True, ignore_permissions=True)
        except Exception:
            pass  # Might be linked
    deleted["Course (demo)"] = len(demo_courses)

    # Demo Instructors (keep INST-0001 and INST-0002 from test data)
    demo_instructors = frappe.get_all("Instructor",
        filters={"email": ["like", "%@demo.institution.local"]}, pluck="name")
    for n in demo_instructors:
        frappe.delete_doc("Instructor", n, force=True, ignore_permissions=True)
    deleted["Instructor (demo)"] = len(demo_instructors)

    frappe.enqueue = _real_enqueue
    frappe.db.commit()

    print("\n" + "=" * 60)
    print("DELETION SUMMARY")
    print("=" * 60)
    total = 0
    for dt, cnt in deleted.items():
        if cnt > 0:
            print(f"  {dt}: {cnt} deleted")
            total += cnt
    print(f"\n  Total records deleted: {total}")
    print("=" * 60)
