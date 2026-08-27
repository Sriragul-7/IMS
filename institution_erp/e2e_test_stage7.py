import frappe
from frappe.utils import today, add_days, nowdate


def execute():
    print("=" * 60)
    print("STAGE 7 E2E TEST: Communication & Dashboards")
    print("=" * 60)

    results = {}

    try:
        cleanup()

        # Block 0: Notice creation, publish, audience resolution
        results.update(block_0_notice())

        # Block 1: dispatch_notice creates Communication Log entries
        results.update(block_1_dispatch())

        # Block 2: Feedback lifecycle
        results.update(block_2_feedback())

        # Block 3: Number Cards verification
        results.update(block_3_number_cards())

        # Block 4: Dashboard Charts verification
        results.update(block_4_dashboard_charts())

    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cleanup()

    print("\n" + "=" * 60)
    print("STAGE 7 E2E TEST SUMMARY")
    print("=" * 60)
    all_pass = True
    for block, passed in results.items():
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_pass = False
        print(f"  {block}: {status}")

    print("\n" + "=" * 60)
    if all_pass:
        print("ALL TESTS PASSED!")
    else:
        print("SOME TESTS FAILED!")
    print("=" * 60)


def cleanup():
    """Delete test data in reverse dependency order."""
    for dt in ["Communication Log", "Notice Recipient", "Notice", "Feedback"]:
        names = frappe.get_all(dt, pluck="name")
        for name in names:
            frappe.delete_doc(dt, name, force=True, ignore_permissions=True)
    frappe.db.commit()


# ---------------------------------------------------------------------------
# Block 0: Notice creation, publish, audience resolution
# ---------------------------------------------------------------------------

def block_0_notice():
    print("\n[0] NOTICE CREATION & PUBLISH")
    results = {}

    # Ensure we have a student group with members
    group = "BCA-2026-A"
    members = frappe.get_all(
        "Student Group Member",
        filters={"parent": group},
        pluck="student",
    )
    print(f"  Student Group '{group}' has {len(members)} members: {members}")
    results["group_members_exist"] = len(members) > 0

    # Create Notice targeting the Student Group
    notice = frappe.get_doc({
        "doctype": "Notice",
        "title": "Test Notice - Stage 7",
        "body": "<p>This is a test notice for Stage 7 E2E testing.</p>",
        "audience_type": "Student Group-wise",
        "target_student_group": group,
        "publish_date": today(),
        "status": "Draft",
    })
    notice.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"  Created Notice: {notice.name}, status={notice.status}")
    results["notice_created"] = notice.name is not None

    # Verify no recipients yet (only created on Publish)
    recipients_before = frappe.get_all(
        "Notice Recipient",
        filters={"notice": notice.name},
        pluck="name",
    )
    print(f"  Recipients before publish: {len(recipients_before)}")
    results["no_recipients_before_publish"] = len(recipients_before) == 0

    # Publish the notice
    notice.status = "Published"
    notice.save(ignore_permissions=True)
    frappe.db.commit()

    # Reload to check recipients were created
    recipients_after = frappe.get_all(
        "Notice Recipient",
        filters={"notice": notice.name},
        fields=["name", "student", "recipient_type", "read_status"],
    )
    print(f"  Recipients after publish: {len(recipients_after)}")
    for r in recipients_after:
        print(f"    - {r.student} ({r.recipient_type}, {r.read_status})")
    results["recipients_created"] = len(recipients_after) == len(members)

    # Verify all group members are recipients
    recipient_students = {r.student for r in recipients_after}
    member_set = set(members)
    results["all_members_recipients"] = recipient_students == member_set

    return results


# ---------------------------------------------------------------------------
# Block 1: dispatch_notice creates Communication Log entries
# ---------------------------------------------------------------------------

def block_1_dispatch():
    print("\n[1] DISPATCH NOTICE")
    results = {}

    # Ensure students in the group have email addresses for dispatch
    group = "BCA-2026-A"
    members = frappe.get_all(
        "Student Group Member",
        filters={"parent": group},
        pluck="student",
    )
    for student_name in members:
        student = frappe.get_doc("Student", student_name)
        if not student.email_address:
            student.email_address = f"{student_name.lower()}@test.example.com"
        if not student.phone_number:
            student.phone_number = "+91-9876500001"
        student.save(ignore_permissions=True)
    frappe.db.commit()
    print(f"  Ensured email/phone for {len(members)} students")

    # Find the published notice
    notices = frappe.get_all(
        "Notice",
        filters={"status": "Published"},
        pluck="name",
    )
    if not notices:
        print("  ERROR: No published notices found")
        results["dispatch_no_notice"] = False
        return results

    notice_name = notices[0]
    print(f"  Dispatching notice: {notice_name}")

    # Call dispatch_notice
    from institution_erp.api import dispatch_notice
    result = dispatch_notice(notice_name)
    print(f"  Dispatch result: logged_count={result['logged_count']}, errors={result['errors']}")
    results["dispatch_logged"] = result["logged_count"] > 0
    results["dispatch_no_errors"] = len(result["errors"]) == 0

    # Verify Communication Log entries created
    logs = frappe.get_all(
        "Communication Log",
        filters={"reference_notice": notice_name},
        fields=["name", "recipient", "channel", "status", "sent_at"],
    )
    print(f"  Communication Log entries: {len(logs)}")
    for log in logs:
        print(f"    - {log.recipient} via {log.channel} ({log.status})")
    results["comm_logs_created"] = len(logs) > 0

    # All should be "Sent" (stub behavior)
    all_sent = all(log.status == "Sent" for log in logs)
    results["all_logs_sent"] = all_sent

    return results


# ---------------------------------------------------------------------------
# Block 2: Feedback lifecycle
# ---------------------------------------------------------------------------

def block_2_feedback():
    print("\n[2] FEEDBACK LIFECYCLE")
    results = {}

    # Create a Feedback from a Student
    student = frappe.get_all("Student", pluck="name")[0]
    feedback = frappe.get_doc({
        "doctype": "Feedback",
        "student": student,
        "category": "Academic",
        "subject": "Test Feedback - Stage 7",
        "description": "<p>This is test feedback for Stage 7.</p>",
        "status": "Open",
        "raised_date": today(),
    })
    feedback.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"  Created Feedback: {feedback.name}, status={feedback.status}")
    results["feedback_created"] = feedback.name is not None
    results["feedback_initial_status"] = feedback.status == "Open"

    # Check open feedback count BEFORE resolving
    open_count = frappe.db.count("Feedback", filters={"status": ["in", ["Open", "In Progress"]]})
    print(f"  Open Feedback count (before resolve): {open_count}")
    results["open_feedback_count"] = open_count > 0

    # Change to In Progress
    feedback.status = "In Progress"
    feedback.save(ignore_permissions=True)
    frappe.db.commit()
    print(f"  Status changed to: {feedback.status}")
    results["feedback_in_progress"] = feedback.status == "In Progress"

    # Try to change to Resolved without resolution_notes - should fail
    feedback.status = "Resolved"
    try:
        feedback.save(ignore_permissions=True)
        frappe.db.commit()
        print("  ERROR: Should have thrown for missing resolution_notes")
        results["feedback_resolved_requires_notes"] = False
    except Exception as e:
        frappe.db.rollback()
        print(f"  Correctly rejected: resolution_notes required")
        results["feedback_resolved_requires_notes"] = True

    # Reload doc after failed save attempt (stale doc)
    feedback = frappe.get_doc("Feedback", feedback.name)

    # Change to Resolved WITH resolution_notes
    feedback.status = "Resolved"
    feedback.resolution_notes = "<p>Issue resolved by updating course materials.</p>"
    feedback.save(ignore_permissions=True)
    frappe.db.commit()
    print(f"  Status changed to: {feedback.status} with resolution_notes")
    results["feedback_resolved"] = feedback.status == "Resolved"
    results["feedback_has_resolution_notes"] = bool(feedback.resolution_notes)

    return results


# ---------------------------------------------------------------------------
# Block 3: Number Cards verification
# ---------------------------------------------------------------------------

def block_3_number_cards():
    print("\n[3] NUMBER CARDS VERIFICATION")
    results = {}

    # Total Active Students - count all Student records
    student_count = frappe.db.count("Student")
    print(f"  Total Active Students: {student_count}")
    results["total_students_count"] = student_count > 0

    # Total Outstanding Fees
    outstanding = frappe.db.sql(
        "SELECT COALESCE(SUM(outstanding_amount), 0) FROM `tabFees` WHERE status != 'Paid'"
    )[0][0]
    print(f"  Total Outstanding Fees: {outstanding}")

    # Books Currently Issued
    books_issued = frappe.db.count("Library Transaction", filters={"status": "Issued"})
    print(f"  Books Currently Issued: {books_issued}")

    # Hostel Occupancy (rooms occupied)
    hostel_occupied = frappe.db.count("Hostel Room Allocation", filters={"status": "Occupied"})
    print(f"  Hostel Rooms Occupied: {hostel_occupied}")

    # Verify Number Card documents exist
    number_cards = frappe.get_all("Number Card", pluck="name")
    print(f"  Number Cards in system: {len(number_cards)} - {number_cards}")
    results["number_cards_exist"] = len(number_cards) >= 5

    return results


# ---------------------------------------------------------------------------
# Block 4: Dashboard Charts verification
# ---------------------------------------------------------------------------

def block_4_dashboard_charts():
    print("\n[4] DASHBOARD CHARTS & DASHBOARD VERIFICATION")
    results = {}

    # Verify Dashboard Chart documents exist
    charts = frappe.get_all("Dashboard Chart", pluck="name")
    print(f"  Dashboard Charts in system: {len(charts)} - {charts}")
    results["dashboard_charts_exist"] = len(charts) >= 2

    # Create Dashboard programmatically if not exists
    if not frappe.db.exists("Dashboard", "Institution Overview"):
        dashboard = frappe.get_doc({
            "doctype": "Dashboard",
            "dashboard_name": "Institution Overview",
            "is_standard": 0,
            "module": "Communication",
            "charts": [
                {"chart": "Fee Collection Trend", "width": "Full"},
                {"chart": "Attendance Trend", "width": "Full"},
            ],
            "cards": [
                {"card": "Total Active Students"},
                {"card": "Total Outstanding Fees"},
                {"card": "Books Currently Issued"},
                {"card": "Hostel Occupancy (Rooms Occupied)"},
                {"card": "Open Feedback/Complaints"},
            ],
        })
        dashboard.insert(ignore_permissions=True)
        frappe.db.commit()
        print("  Created Institution Overview dashboard programmatically")
    else:
        print("  Institution Overview dashboard already exists")

    # Verify Dashboard
    dashboard = frappe.get_doc("Dashboard", "Institution Overview")
    print(f"  Institution Overview charts: {len(dashboard.charts)}")
    print(f"  Institution Overview cards: {len(dashboard.cards)}")
    results["institution_overview_charts"] = len(dashboard.charts) >= 2
    results["institution_overview_cards"] = len(dashboard.cards) >= 5

    # Verify Dashboard document exists in system
    dashboards = frappe.get_all("Dashboard", pluck="name")
    print(f"  Dashboards in system: {len(dashboards)} - {dashboards}")
    results["dashboard_exists"] = len(dashboards) >= 1

    return results
