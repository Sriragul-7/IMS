# Copyright (c) 2026, Institution ERP and contributors
# License: MIT. See LICENSE

"""
Stage 5 E2E Test: Fees Module
Run: bench --site institution.localhost execute institution_erp.e2e_test_stage5.execute
"""

import frappe
from frappe import _


def execute():
    print("=" * 60)
    print("STAGE 5 E2E TEST: Fees Module")
    print("=" * 60)

    results = {
        "fee_categories": "FAIL",
        "fee_structure_total": "FAIL",
        "fee_schedule_generation": "FAIL",
        "duplicate_generation_skip": "FAIL",
        "discount_pending_no_effect": "FAIL",
        "discount_approval_effect": "FAIL",
        "partial_payment": "FAIL",
        "full_payment": "FAIL",
        "overpayment_rejection": "FAIL",
        "fee_dues_report": "FAIL",
    }

    # ------------------------------------------------------------------
    # STEP 0: Cleanup
    # ------------------------------------------------------------------
    print("\n[0] Cleaning up existing test data...")
    cleanup_test_data()
    frappe.db.commit()
    print("  Cleanup done.")

    # ------------------------------------------------------------------
    # STEP 1: Ensure prerequisite records exist
    # ------------------------------------------------------------------
    print("\n[1] Ensuring prerequisite records...")

    # Academic Year
    if not frappe.db.exists("Academic Year", "2026-2027"):
        frappe.get_doc({
            "doctype": "Academic Year",
            "academic_year_name": "2026-2027",
        }).insert(ignore_permissions=True)
        print("  Created Academic Year: 2026-2027")

    # Program
    if not frappe.db.exists("Program", {"program_name": "BCA"}):
        frappe.get_doc({
            "doctype": "Program",
            "program_name": "BCA",
        }).insert(ignore_permissions=True)
        print("  Created Program: BCA")

    program = frappe.db.get_value("Program", {"program_name": "BCA"}, "name")

    # Students (create 3 test students)
    students = []

    # Create a guardian for the students
    if not frappe.db.exists("Guardian", {"guardian_name": "Test Guardian"}):
        frappe.get_doc({
            "doctype": "Guardian",
            "guardian_name": "Test Guardian",
            "relation_to_student": "Father",
        }).insert(ignore_permissions=True)
    guardian = frappe.db.get_value("Guardian", {"guardian_name": "Test Guardian"}, "name")

    for i in range(1, 4):
        student_label = f"FeeTest{i:03d}"
        existing = frappe.db.get_value("Student", {"first_name": student_label}, "name")
        if existing:
            students.append(existing)
        else:
            doc = frappe.get_doc({
                "doctype": "Student",
                "first_name": student_label,
                "gender": "Male",
                "date_of_birth": "2000-01-01",
                "guardian": guardian,
            })
            doc.insert(ignore_permissions=True)
            students.append(doc.name)
    frappe.db.commit()
    print(f"  Students ready: {students}")

    # Student Group
    if not frappe.db.exists("Student Group", "FEE-TEST-GROUP"):
        group = frappe.get_doc({
            "doctype": "Student Group",
            "group_name": "FEE-TEST-GROUP",
            "program": program,
            "academic_year": "2026-2027",
            "members": [{"student": s} for s in students],
        })
        group.insert(ignore_permissions=True)
        frappe.db.commit()
        print("  Created Student Group: FEE-TEST-GROUP")

    student_group = frappe.db.get_value("Student Group", {"group_name": "FEE-TEST-GROUP"}, "name")

    # ------------------------------------------------------------------
    # STEP 2: Create Fee Categories
    # ------------------------------------------------------------------
    print("\n[2] Creating Fee Categories...")
    categories = []
    for cat_name in ["Tuition", "Lab Fee", "Library"]:
        if not frappe.db.exists("Fee Category", cat_name):
            frappe.get_doc({
                "doctype": "Fee Category",
                "category_name": cat_name,
                "description": f"Test {cat_name}",
            }).insert(ignore_permissions=True)
        categories.append(cat_name)
    frappe.db.commit()
    print(f"  Created Fee Categories: {categories}")
    results["fee_categories"] = "PASS"

    # ------------------------------------------------------------------
    # STEP 3: Create Fee Structure and verify total_amount
    # ------------------------------------------------------------------
    print("\n[3] Creating Fee Structure with components...")
    fee_structure = frappe.get_doc({
        "doctype": "Fee Structure",
        "structure_name": "Test Fee Structure 2026",
        "program": program,
        "academic_year": "2026-2027",
        "components": [
            {"fee_category": "Tuition", "amount": 50000},
            {"fee_category": "Lab Fee", "amount": 10000},
            {"fee_category": "Library", "amount": 5000},
        ],
    })
    fee_structure.insert(ignore_permissions=True)
    frappe.db.commit()

    # Verify total_amount = 50000 + 10000 + 5000 = 65000
    if fee_structure.total_amount == 65000:
        print(f"  Fee Structure created: {fee_structure.name}, total_amount = {fee_structure.total_amount} (CORRECT)")
        results["fee_structure_total"] = "PASS"
    else:
        print(f"  ERROR: total_amount = {fee_structure.total_amount}, expected 65000")

    # ------------------------------------------------------------------
    # STEP 4: Create Fee Schedule and generate Fees
    # ------------------------------------------------------------------
    print("\n[4] Creating Fee Schedule and generating Fees...")
    fee_schedule = frappe.get_doc({
        "doctype": "Fee Schedule",
        "fee_structure": fee_structure.name,
        "student_group": student_group,
        "due_date": "2026-09-30",
        "applicable_students": [
            {"student": students[0], "included": 1},
            {"student": students[1], "included": 1},
            {"student": students[2], "included": 1},
        ],
    })
    fee_schedule.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"  Fee Schedule created: {fee_schedule.name}")

    # Generate fees
    from institution_erp.api import generate_fees_from_schedule
    gen_result = generate_fees_from_schedule(fee_schedule.name)
    print(f"  Generation result: created={gen_result['created']}, skipped={gen_result['skipped']}, errors={gen_result['errors']}")

    if gen_result["created"] == 3 and gen_result["errors"] == 0:
        results["fee_schedule_generation"] = "PASS"
    else:
        print(f"  ERROR: Expected 3 created, got {gen_result['created']}")
        if gen_result["error_details"]:
            for err in gen_result["error_details"]:
                print(f"    {err}")

    # ------------------------------------------------------------------
    # STEP 5: Re-run generation — should skip all (no duplicates)
    # ------------------------------------------------------------------
    print("\n[5] Re-running generation (duplicate skip test)...")
    gen_result2 = generate_fees_from_schedule(fee_schedule.name)
    print(f"  Re-run result: created={gen_result2['created']}, skipped={gen_result2['skipped']}, errors={gen_result2['errors']}")

    if gen_result2["skipped"] == 3 and gen_result2["created"] == 0:
        results["duplicate_generation_skip"] = "PASS"
    else:
        print(f"  ERROR: Expected 3 skipped, 0 created")

    # Get the first student's Fees record for discount/payment tests
    fees_name = frappe.db.get_value(
        "Fees", {"fee_schedule": fee_schedule.name, "student": students[0]}, "name"
    )
    fees_doc = frappe.get_doc("Fees", fees_name)
    print(f"  Student {students[0]} Fees: {fees_name}, total={fees_doc.total_amount}, outstanding={fees_doc.outstanding_amount}, status={fees_doc.status}")

    # ------------------------------------------------------------------
    # STEP 6: Create Fee Discount (Pending) — should NOT affect total
    # ------------------------------------------------------------------
    print("\n[6] Creating Fee Discount (Pending status)...")
    discount = frappe.get_doc({
        "doctype": "Fee Discount",
        "student": students[0],
        "fees": fees_name,
        "discount_type": "Fixed Amount",
        "discount_value": 5000,
        "reason": "Test scholarship",
        "status": "Pending",
    })
    discount.insert(ignore_permissions=True)
    frappe.db.commit()

    # Reload fees and check total unchanged
    fees_doc.reload()
    if fees_doc.total_amount == 65000:
        print(f"  Discount Pending: total_amount still {fees_doc.total_amount} (CORRECT — no effect)")
        results["discount_pending_no_effect"] = "PASS"
    else:
        print(f"  ERROR: total_amount changed to {fees_doc.total_amount} while discount is Pending")

    # ------------------------------------------------------------------
    # STEP 7: Approve discount — should reduce total
    # ------------------------------------------------------------------
    print("\n[7] Approving Fee Discount...")
    discount.status = "Approved"
    discount.approved_by = "Administrator"
    discount.save(ignore_permissions=True)
    frappe.db.commit()

    fees_doc.reload()
    expected_discount = 5000
    expected_net = 65000 - expected_discount  # 60000
    if fees_doc.discount_amount == expected_discount:
        print(f"  Discount Approved: discount_amount = {fees_doc.discount_amount} (CORRECT)")
        results["discount_approval_effect"] = "PASS"
    else:
        print(f"  ERROR: discount_amount = {fees_doc.discount_amount}, expected {expected_discount}")

    # Recompute paid/status
    fees_doc.recompute_paid_and_status()
    print(f"  After discount: outstanding={fees_doc.outstanding_amount}, status={fees_doc.status}")

    # ------------------------------------------------------------------
    # STEP 8: Partial Payment
    # ------------------------------------------------------------------
    print("\n[8] Recording partial payment...")
    payment1 = frappe.get_doc({
        "doctype": "Fee Payment",
        "fees": fees_name,
        "student": students[0],
        "payment_date": "2026-08-27",
        "amount": 30000,
        "payment_mode": "Bank Transfer",
        "reference_number": "TXN-001",
        "remarks": "Partial payment test",
    })
    payment1.insert(ignore_permissions=True)
    frappe.set_user("Administrator")
    payment1.submit()
    frappe.db.commit()

    fees_doc.reload()
    fees_doc.recompute_paid_and_status()
    print(f"  After partial payment: paid={fees_doc.paid_amount}, outstanding={fees_doc.outstanding_amount}, status={fees_doc.status}")

    if fees_doc.paid_amount == 30000 and fees_doc.status == "Partially Paid":
        results["partial_payment"] = "PASS"
    else:
        print(f"  ERROR: paid_amount={fees_doc.paid_amount}, status={fees_doc.status}")

    # ------------------------------------------------------------------
    # STEP 9: Full Payment (settle remaining)
    # ------------------------------------------------------------------
    print("\n[9] Recording final payment to settle balance...")
    remaining = fees_doc.outstanding_amount  # Should be 30000
    payment2 = frappe.get_doc({
        "doctype": "Fee Payment",
        "fees": fees_name,
        "student": students[0],
        "payment_date": "2026-08-27",
        "amount": remaining,
        "payment_mode": "Cash",
        "remarks": "Final payment test",
    })
    payment2.insert(ignore_permissions=True)
    payment2.submit()
    frappe.db.commit()

    fees_doc.reload()
    fees_doc.recompute_paid_and_status()
    print(f"  After final payment: paid={fees_doc.paid_amount}, outstanding={fees_doc.outstanding_amount}, status={fees_doc.status}")

    if fees_doc.paid_amount == 60000 and fees_doc.outstanding_amount == 0 and fees_doc.status == "Paid":
        results["full_payment"] = "PASS"
    else:
        print(f"  ERROR: paid={fees_doc.paid_amount}, outstanding={fees_doc.outstanding_amount}, status={fees_doc.status}")

    # ------------------------------------------------------------------
    # STEP 10: Attempt overpayment — should be rejected
    # ------------------------------------------------------------------
    print("\n[10] Attempting overpayment (should be rejected)...")
    try:
        overpay = frappe.get_doc({
            "doctype": "Fee Payment",
            "fees": fees_name,
            "student": students[0],
            "payment_date": "2026-08-27",
            "amount": 5000,
            "payment_mode": "Card",
            "remarks": "Overpayment test",
        })
        overpay.insert(ignore_permissions=True)
        print("  ERROR: Overpayment was NOT rejected!")
    except frappe.exceptions.ValidationError as e:
        print(f"  Overpayment REJECTED: {str(e)[:100]}")
        results["overpayment_rejection"] = "PASS"

    # ------------------------------------------------------------------
    # STEP 11: Run Fee Dues Report
    # ------------------------------------------------------------------
    print("\n[11] Running Fee Dues Report...")
    from institution_erp.fees.report.fee_dues.fee_dues import execute as report_execute

    report_filters = {"academic_year": "2026-2027"}
    columns, data, message, chart = report_execute(report_filters)
    print(f"  Report returned {len(data)} rows")

    # Should have 3 rows (one per student)
    if len(data) == 3:
        for row in data:
            print(f"    {row['student']}: total={row['total_amount']}, paid={row['paid_amount']}, outstanding={row['outstanding_amount']}, status={row['status']}")
        results["fee_dues_report"] = "PASS"
    else:
        print(f"  WARNING: Expected 3 rows, got {len(data)}")

    # ------------------------------------------------------------------
    # CLEANUP
    # ------------------------------------------------------------------
    print("\n[Cleanup] Removing test data...")
    cleanup_test_data()
    frappe.db.commit()
    print("  Cleanup done.")

    # ------------------------------------------------------------------
    # SUMMARY
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("STAGE 5 E2E TEST SUMMARY")
    print("=" * 60)
    for test_name, status in results.items():
        marker = "PASS" if status == "PASS" else "FAIL"
        print(f"  {test_name}: {marker}")

    all_pass = all(v == "PASS" for v in results.values())
    print("\n" + "=" * 60)
    if all_pass:
        print("ALL TESTS PASSED!")
    else:
        failed = [k for k, v in results.items() if v != "PASS"]
        print(f"SOME TESTS FAILED: {', '.join(failed)}")
    print("=" * 60)


def cleanup_test_data():
    """Delete test data in reverse dependency order."""
    # Fee Payments
    for name in frappe.get_all("Fee Payment", pluck="name"):
        frappe.delete_doc("Fee Payment", name, ignore_permissions=True, force=True)

    # Fee Discounts
    for name in frappe.get_all("Fee Discount", pluck="name"):
        frappe.delete_doc("Fee Discount", name, ignore_permissions=True, force=True)

    # Fees
    for name in frappe.get_all("Fees", pluck="name"):
        frappe.delete_doc("Fees", name, ignore_permissions=True, force=True)

    # Fee Schedules
    for name in frappe.get_all("Fee Schedule", pluck="name"):
        frappe.delete_doc("Fee Schedule", name, ignore_permissions=True, force=True)

    # Fee Structures
    for name in frappe.get_all("Fee Structure", pluck="name"):
        frappe.delete_doc("Fee Structure", name, ignore_permissions=True, force=True)

    # Fee Categories
    for name in frappe.get_all("Fee Category", pluck="name"):
        frappe.delete_doc("Fee Category", name, ignore_permissions=True, force=True)

    # Student Groups (test only)
    for name in frappe.get_all("Student Group", filters={"group_name": ["like", "FEE-TEST-GROUP"]}, pluck="name"):
        frappe.delete_doc("Student Group", name, ignore_permissions=True, force=True)

    # Students (test only) - find by first_name prefix
    for name in frappe.get_all("Student", filters={"first_name": ["like", "FeeTest%"]}, pluck="name"):
        frappe.delete_doc("Student", name, ignore_permissions=True, force=True)

    # Guardian (test only)
    for name in frappe.get_all("Guardian", filters={"guardian_name": "Test Guardian"}, pluck="name"):
        frappe.delete_doc("Guardian", name, ignore_permissions=True, force=True)
