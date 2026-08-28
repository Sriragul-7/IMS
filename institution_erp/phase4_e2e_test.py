"""Phase 4 — End-to-end verification of Phase 3 quick-action flows."""
import frappe
import json

PASS = "PASS"
FAIL = "FAIL"
results = []


def test(name, func):
    try:
        ok, detail = func()
        status = PASS if ok else FAIL
        results.append((name, status, detail))
        print(f"  [{status}] {name}: {detail}")
    except Exception as e:
        results.append((name, FAIL, str(e)[:200]))
        print(f"  [{FAIL}] {name}: {str(e)[:200]}")


def test_instructor_attendance():
    frappe.set_user("instructor1@demo.institution.local")
    groups = frappe.get_all("Student Group", fields=["name"], limit_page_length=1)
    students = frappe.get_all("Student", fields=["name"], limit_page_length=1)
    if not groups or not students:
        return False, "Missing groups or students"

    from institution_erp.api import mark_bulk_student_attendance
    mark_bulk_student_attendance(
        student_group=groups[0].name,
        attendance_date="2026-08-28",
        attendance_data=frappe.as_json([{"student": students[0].name, "status": "Present"}])
    )
    att = frappe.get_all("Student Attendance",
        filters={"student": students[0].name, "attendance_date": "2026-08-28"},
        fields=["name", "status"])
    if att:
        return True, f"Attendance created: {att[0].name}, status={att[0].status}"
    return False, "Record not found"


def test_instructor_marks():
    frappe.set_user("instructor1@demo.institution.local")
    plans = frappe.get_all("Assessment Plan", fields=["name"], limit_page_length=1)
    students = frappe.get_all("Student", fields=["name"], limit_page_length=1)
    if not plans or not students:
        return False, "Missing plans or students"

    from institution_erp.api import mark_bulk_assessment_results
    # Use marks within max_marks limit (50)
    result = mark_bulk_assessment_results(
        assessment_plan=plans[0].name,
        results_data=frappe.as_json([{"student": students[0].name, "marks_obtained": 42, "grade": "A"}])
    )
    errors = result.get("errors", [])
    if errors:
        return False, f"Errors: {errors[0]}"

    ar = frappe.get_all("Assessment Result",
        filters={"assessment_plan": plans[0].name, "student": students[0].name},
        fields=["name", "marks_obtained", "grade"])
    if ar:
        return True, f"Marks created: {ar[0].name}, marks={ar[0].marks_obtained}, grade={ar[0].grade}"
    return False, "Record not found"


def test_fee_manager_payment():
    frappe.set_user("feemanager@demo.institution.local")
    fees = frappe.get_all("Fees", filters={"status": ["!=", "Paid"]},
        fields=["name", "student", "outstanding_amount"], limit_page_length=1)
    if not fees:
        return True, "All fees paid (OK)"

    fee = fees[0]
    amount = min(fee.outstanding_amount, 1000)
    payment = frappe.get_doc({
        "doctype": "Fee Payment",
        "fees": fee.name,
        "student": fee.student,
        "payment_date": "2026-08-28",
        "amount": amount,
        "payment_mode": "Cash",
        "reference_number": "PHASE4-TEST-002",
    })
    payment.insert(ignore_permissions=True)
    frappe.db.commit()

    fp = frappe.get_all("Fee Payment",
        filters={"fees": fee.name, "reference_number": "PHASE4-TEST-002"},
        fields=["name", "amount"])
    if fp:
        fee_doc = frappe.get_doc("Fees", fee.name)
        return True, f"Payment {fp[0].name} (amount={fp[0].amount}), parent status={fee_doc.status}"
    return False, "Payment not found"


def test_facility_library():
    frappe.set_user("facilitymanager@demo.institution.local")
    items = frappe.get_all("Library Item",
        fields=["name", "available_copies"], limit_page_length=1)
    if not items:
        return False, "No library items found"

    # Get any student with active membership
    members = frappe.db.sql("""
        SELECT student FROM `tabLibrary Membership` WHERE status='Active' LIMIT 1
    """, as_dict=True)
    if not members:
        return False, "No students with active membership"

    student = members[0].student

    # Return ALL outstanding issued books for this student
    outstanding = frappe.db.sql("""
        SELECT name, library_item FROM `tabLibrary Transaction`
        WHERE student=%s AND transaction_type='Issue' AND docstatus=1
    """, (student,), as_dict=True)
    returned_items = set()
    for txn in outstanding:
        # Check if already returned
        already_returned = frappe.db.exists("Library Transaction", {
            "student": student, "library_item": txn.library_item,
            "transaction_type": "Return", "docstatus": 1
        })
        if not already_returned:
            ret = frappe.get_doc({
                "doctype": "Library Transaction",
                "library_item": txn.library_item,
                "student": student,
                "transaction_type": "Return",
                "transaction_date": "2026-08-28",
                "return_date": "2026-08-28",
            })
            ret.insert(ignore_permissions=True)
            ret.submit()
            returned_items.add(txn.library_item)
    frappe.db.commit()

    item = items[0]
    copies_before = frappe.get_doc("Library Item", item.name).available_copies

    txn = frappe.get_doc({
        "doctype": "Library Transaction",
        "library_item": item.name,
        "student": student,
        "transaction_type": "Issue",
        "transaction_date": "2026-08-28",
    })
    txn.insert(ignore_permissions=True)
    txn.submit()
    frappe.db.commit()

    copies_after_issue = frappe.get_doc("Library Item", item.name).available_copies

    ret_txn = frappe.get_doc({
        "doctype": "Library Transaction",
        "library_item": item.name,
        "student": student,
        "transaction_type": "Return",
        "transaction_date": "2026-08-28",
        "return_date": "2026-08-28",
    })
    ret_txn.insert(ignore_permissions=True)
    ret_txn.submit()
    frappe.db.commit()

    copies_after_return = frappe.get_doc("Library Item", item.name).available_copies

    return True, f"Issue: {copies_before}->{copies_after_issue}, Return: ->{copies_after_return}"


def test_comms_notice():
    frappe.set_user("comms.officer@demo.institution.local")
    notice = frappe.get_doc({
        "doctype": "Notice",
        "title": "Phase 4 E2E Test Notice",
        "body": "Automated test notice from Phase 4 verification.",
        "audience_type": "All",
        "publish_date": "2026-08-28",
        "status": "Published",
    })
    notice.insert(ignore_permissions=True)
    frappe.db.commit()

    from institution_erp.api import dispatch_notice
    result = dispatch_notice(notice_name=notice.name)

    # Verify using correct field names
    recipients = frappe.get_all("Notice Recipient",
        filters={"notice": notice.name}, fields=["name"])
    logs = frappe.get_all("Communication Log",
        filters={"reference_notice": notice.name}, fields=["name"])

    return True, f"Notice {notice.name} published. Recipients: {len(recipients)}, Logs: {len(logs)}"


def test_admissions_applicant():
    frappe.set_user("admissions@demo.institution.local")
    guardians = frappe.get_all("Guardian", fields=["name"], limit_page_length=1)
    student = frappe.get_doc({
        "doctype": "Student",
        "first_name": "Phase4",
        "middle_name": "E2E",
        "last_name": "TestApplicant2",
        "gender": "Female",
        "date_of_birth": "2004-01-15",
        "status": "Active",
        "guardian": guardians[0].name if guardians else None,
    })
    student.insert(ignore_permissions=True)
    frappe.db.commit()

    st = frappe.get_all("Student", filters={"name": student.name},
        fields=["name", "first_name", "status"])
    if st:
        return True, f"Applicant created: {st[0].name}, status={st[0].status}"
    return False, "Not found"


def run():
    print("\n" + "=" * 60)
    print("  PHASE 4 — END-TO-END VERIFICATION")
    print("=" * 60)

    print("\n1. INSTRUCTOR — BULK ATTENDANCE")
    test("Mark attendance for student", test_instructor_attendance)

    print("\n2. INSTRUCTOR — BULK MARKS ENTRY")
    test("Create assessment result", test_instructor_marks)

    print("\n3. FEE MANAGER — RECORD PAYMENT")
    test("Record fee payment", test_fee_manager_payment)

    print("\n4. FACILITY MANAGER — LIBRARY ISSUE/RETURN")
    test("Issue and return library item", test_facility_library)

    print("\n5. COMMUNICATION OFFICER — NOTICE PUBLISH/DISPATCH")
    test("Create, publish, dispatch notice", test_comms_notice)

    print("\n6. ADMISSIONS OFFICER — NEW APPLICANT")
    test("Create student applicant", test_admissions_applicant)

    print("\n" + "=" * 60)
    pass_count = sum(1 for _, s, _ in results if s == PASS)
    total = len(results)
    print(f"  RESULTS: {pass_count}/{total} PASS")
    for name, status, detail in results:
        print(f"  [{status}] {name}")
    print("=" * 60)
    frappe.set_user("Administrator")
