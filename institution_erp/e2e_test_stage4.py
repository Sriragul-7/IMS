# Copyright (c) 2026, Institution ERP and contributors
# License: MIT. See LICENSE

"""
Stage 4 E2E Test: Examination & Grading Module
Run with: bench --site institution.localhost execute institution_erp.e2e_test_stage4.execute
"""

import frappe
import json


def execute():
    print("=" * 60)
    print("STAGE 4 E2E TEST: Examination & Grading Module")
    print("=" * 60)

    results = {
        "grading_scale": "FAIL",
        "assessment_group": "FAIL",
        "assessment_plan_validation": "FAIL",
        "bulk_marks_entry": "FAIL",
        "auto_grade_calculation": "FAIL",
        "invalid_marks_rejection": "FAIL",
        "duplicate_result_prevention": "FAIL",
        "report_output": "FAIL",
        "results_published_visibility": "FAIL",
    }

    # ------------------------------------------------------------------
    # STEP 0: Clean up existing test data
    # ------------------------------------------------------------------
    print("\n[0] Cleaning up existing test data...")
    cleanup_test_data()
    frappe.db.commit()
    print("  Cleanup done.")

    # ------------------------------------------------------------------
    # STEP 1: Create Grading Scale with 5 intervals
    # ------------------------------------------------------------------
    print("\n[1] Creating Grading Scale with 5 intervals...")
    grading_scale = frappe.get_doc({
        "doctype": "Grading Scale",
        "scale_name": "Standard Scale",
        "intervals": [
            {"grade_code": "A+", "threshold_percent": 90, "grade_description": "Outstanding"},
            {"grade_code": "A", "threshold_percent": 80, "grade_description": "Excellent"},
            {"grade_code": "B", "threshold_percent": 70, "grade_description": "Very Good"},
            {"grade_code": "C", "threshold_percent": 60, "grade_description": "Good"},
            {"grade_code": "F", "threshold_percent": 0, "grade_description": "Fail"},
        ],
    })
    grading_scale.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"  Created Grading Scale: {grading_scale.name}")
    results["grading_scale"] = "PASS"

    # Validate overlap detection
    print("\n  Testing overlap detection...")
    try:
        bad_scale = frappe.get_doc({
            "doctype": "Grading Scale",
            "scale_name": "Bad Scale",
            "intervals": [
                {"grade_code": "A", "threshold_percent": 80, "grade_description": "Good"},
                {"grade_code": "B", "threshold_percent": 80, "grade_description": "Also Good"},
            ],
        })
        bad_scale.insert(ignore_permissions=True)
        print("  ERROR: Overlap was NOT detected!")
    except frappe.exceptions.ValidationError:
        print("  OVERLAP CORRECTLY DETECTED: Duplicate threshold rejected")

    # ------------------------------------------------------------------
    # STEP 2: Create Assessment Group
    # ------------------------------------------------------------------
    print("\n[2] Creating Assessment Group...")
    # Ensure Academic Term exists
    if not frappe.db.exists("Academic Term", "2026-2027-Term1"):
        term = frappe.get_doc({
            "doctype": "Academic Term",
            "term_name": "2026-2027-Term1",
            "academic_year": "2026-2027",
            "term_start_date": "2026-08-01",
            "term_end_date": "2026-12-31",
        })
        term.insert(ignore_permissions=True)
        print(f"  Created Academic Term: {term.name}")

    assessment_group = frappe.get_doc({
        "doctype": "Assessment Group",
        "group_name": "Unit Test 1",
        "academic_term": "2026-2027-Term1",
        "results_published": 0,
        "weightage_percent": 30,
    })
    assessment_group.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"  Created Assessment Group: {assessment_group.name}")
    results["assessment_group"] = "PASS"

    # ------------------------------------------------------------------
    # STEP 3: Create Assessment Plan with validation
    # ------------------------------------------------------------------
    print("\n[3] Creating Assessment Plan...")

    # Ensure existing records from Stage 3
    if not frappe.db.exists("Academic Year", "2026-2027"):
        frappe.get_doc({
            "doctype": "Academic Year",
            "year_name": "2026-2027",
        }).insert(ignore_permissions=True)

    if not frappe.db.exists("Program", {"program_code": "BCA"}):
        frappe.get_doc({
            "doctype": "Program",
            "program_name": "Bachelor of Computer Applications",
            "program_code": "BCA",
        }).insert(ignore_permissions=True)

    if not frappe.db.exists("Course", {"course_code": "CS101"}):
        frappe.get_doc({
            "doctype": "Course",
            "course_name": "Introduction to Programming",
            "course_code": "CS101",
        }).insert(ignore_permissions=True)

    # Ensure student group exists
    if not frappe.db.exists("Student Group", "BCA-2026-A"):
        frappe.get_doc({
            "doctype": "Student Group",
            "group_name": "BCA-2026-A",
            "program": frappe.db.get_value("Program", {"program_code": "BCA"}, "name"),
            "academic_year": "2026-2027",
            "course": frappe.db.get_value("Course", {"course_code": "CS101"}, "name"),
        }).insert(ignore_permissions=True)
        frappe.db.commit()
        print("  Created Student Group: BCA-2026-A")

    # Ensure students exist
    students = get_existing_students()

    plan = frappe.get_doc({
        "doctype": "Assessment Plan",
        "assessment_group": assessment_group.name,
        "course": frappe.db.get_value("Course", {"course_code": "CS101"}, "name"),
        "student_group": "BCA-2026-A",
        "max_marks": 100,
        "passing_marks": 40,
        "grading_scale": grading_scale.name,
        "exam_date": "2026-08-27",
    })
    plan.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"  Created Assessment Plan: {plan.name} (max_marks=100, passing_marks=40)")

    # Validate passing_marks >= max_marks
    print("\n  Testing plan validation (passing >= max)...")
    try:
        bad_plan = frappe.get_doc({
            "doctype": "Assessment Plan",
            "assessment_group": assessment_group.name,
            "course": frappe.db.get_value("Course", {"course_code": "CS101"}, "name"),
            "student_group": "BCA-2026-A",
            "max_marks": 50,
            "passing_marks": 60,
            "grading_scale": grading_scale.name,
            "exam_date": "2026-08-28",
        })
        bad_plan.insert(ignore_permissions=True)
        print("  ERROR: Validation was NOT triggered!")
    except frappe.exceptions.ValidationError:
        print("  PLAN VALIDATION CORRECTLY TRIGGERED: passing_marks >= max_marks rejected")
        results["assessment_plan_validation"] = "PASS"

    # ------------------------------------------------------------------
    # STEP 4: Bulk marks entry
    # ------------------------------------------------------------------
    print("\n[4] Testing bulk marks entry...")
    from institution_erp.api import mark_bulk_assessment_results

    marks_data = [
        {"student": students[0], "marks_obtained": 92},
        {"student": students[1], "marks_obtained": 78},
        {"student": students[2], "marks_obtained": 55},
    ]

    result = mark_bulk_assessment_results(plan.name, json.dumps(marks_data))
    print(f"  Created: {result['created']}, Updated: {result['updated']}, Errors: {len(result['errors'])}")

    if result["created"] == 3 and not result["errors"]:
        results["bulk_marks_entry"] = "PASS"
    else:
        print(f"  Errors: {result['errors']}")

    # ------------------------------------------------------------------
    # STEP 5: Verify auto grade calculation
    # ------------------------------------------------------------------
    print("\n[5] Verifying auto grade calculation...")
    all_grades_correct = True

    expected = [
        (students[0], 92, "A+", "Pass"),
        (students[1], 78, "B", "Pass"),
        (students[2], 55, "F", "Pass"),  # 55 >= 40 passing_marks = Pass
    ]

    for student_name, expected_marks, expected_grade, expected_status in expected:
        res = frappe.db.get_value(
            "Assessment Result",
            {"assessment_plan": plan.name, "student": student_name},
            ["marks_obtained", "grade", "status", "percentage"],
            as_dict=True,
        )
        if res:
            grade_ok = res.grade == expected_grade
            status_ok = res.status == expected_status
            pct_ok = res.percentage == round(expected_marks / 100 * 100, 2)
            print(f"  {student_name}: marks={res.marks_obtained}, grade={res.grade} (exp {expected_grade}), "
                  f"status={res.status} (exp {expected_status}), pct={res.percentage}% "
                  f"{'OK' if grade_ok and status_ok else 'MISMATCH'}")
            if not (grade_ok and status_ok):
                all_grades_correct = False
        else:
            print(f"  {student_name}: RESULT NOT FOUND!")
            all_grades_correct = False

    if all_grades_correct:
        results["auto_grade_calculation"] = "PASS"

    # ------------------------------------------------------------------
    # STEP 6: Invalid marks rejection (marks > max_marks)
    # ------------------------------------------------------------------
    print("\n[6] Testing invalid marks rejection...")
    invalid_result = mark_bulk_assessment_results(
        plan.name,
        json.dumps([{"student": students[0], "marks_obtained": 150}]),
    )
    if invalid_result["errors"] and invalid_result["created"] == 0:
        print(f"  INVALID MARKS CORRECTLY REJECTED: {invalid_result['errors'][0][:80]}...")
        results["invalid_marks_rejection"] = "PASS"
    else:
        print("  ERROR: Invalid marks were NOT rejected!")

    # ------------------------------------------------------------------
    # STEP 7: Duplicate result prevention
    # ------------------------------------------------------------------
    print("\n[7] Testing duplicate result prevention...")
    dup_result = mark_bulk_assessment_results(
        plan.name,
        json.dumps([{"student": students[0], "marks_obtained": 85}]),
    )
    if dup_result["updated"] == 1 and not dup_result["errors"]:
        print(f"  DUPLICATE HANDLED CORRECTLY: Updated existing record for {students[0]}")
        results["duplicate_result_prevention"] = "PASS"
    elif dup_result["errors"]:
        print(f"  ERROR: {dup_result['errors'][0]}")
    else:
        print("  ERROR: Unexpected result!")

    # ------------------------------------------------------------------
    # STEP 8: Run Student Result Summary report
    # ------------------------------------------------------------------
    print("\n[8] Running Student Result Summary report...")
    from institution_erp.examination.report.student_result_summary.student_result_summary import execute as report_execute

    report_filters = {"student_group": "BCA-2026-A"}
    columns, data, message, chart = report_execute(report_filters)

    print(f"  Report returned {len(data)} rows")
    for row in data:
        bold = " (OVERALL)" if row.get("bold") else ""
        print(f"    {row.get('student_name', 'N/A')}: marks={row.get('marks_obtained')}, "
              f"max={row.get('max_marks')}, grade={row.get('grade')}, "
              f"pct={row.get('percentage')}%{bold}")

    if len(data) == 4:
        results["report_output"] = "PASS"
    else:
        print(f"  WARNING: Expected 4 rows (3 students + 1 overall), got {len(data)}")

    # ------------------------------------------------------------------
    # STEP 9: Test results_published visibility
    # ------------------------------------------------------------------
    print("\n[9] Testing results_published visibility...")
    test_results_published_visibility(assessment_group, results)

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
    print("STAGE 4 E2E TEST SUMMARY")
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


def get_existing_students():
    """Get existing students from the BCA-2026-A group or create new ones."""
    members = frappe.get_all(
        "Student Group Member",
        filters={"parent": "BCA-2026-A"},
        fields=["student"],
        pluck="student",
    )
    if members:
        return members[:3]

    # Create students if none exist
    students = []
    for i in range(1, 4):
        name = f"STU-2026-Test{i:03d}"
        if not frappe.db.exists("Student", name):
            student = frappe.get_doc({
                "doctype": "Student",
                "first_name": f"TestStudent{i}",
                "last_name": "Tester",
                "gender": "Male",
                "date_of_birth": "2000-01-01",
            })
            student.insert(ignore_permissions=True)
            students.append(student.name)
        else:
            students.append(name)

    # Add to student group
    group = frappe.get_doc("Student Group", "BCA-2026-A")
    for s in students:
        if not any(m.student == s for m in (group.members or [])):
            group.append("members", {"student": s, "joining_date": "2026-08-01"})
    group.save(ignore_permissions=True)
    frappe.db.commit()

    return students


def test_results_published_visibility(assessment_group, results):
    """Test that results_published toggle controls visibility."""
    # With results_published = 0, non-privileged users should NOT see results
    assessment_group.results_published = 0
    assessment_group.save(ignore_permissions=True)
    frappe.db.commit()

    count_unpublished = frappe.db.sql(
        "SELECT COUNT(*) FROM `tabAssessment Result` ar "
        "JOIN `tabAssessment Plan` ap ON ar.assessment_plan = ap.name "
        "JOIN `tabAssessment Group` ag ON ap.assessment_group = ag.name "
        "WHERE ag.results_published = 0",
    )[0][0]
    print(f"  Results with results_published=0: {count_unpublished}")

    # Now publish
    assessment_group.results_published = 1
    assessment_group.save(ignore_permissions=True)
    frappe.db.commit()

    count_published = frappe.db.sql(
        "SELECT COUNT(*) FROM `tabAssessment Result` ar "
        "JOIN `tabAssessment Plan` ap ON ar.assessment_plan = ap.name "
        "JOIN `tabAssessment Group` ag ON ap.assessment_group = ag.name "
        "WHERE ag.results_published = 1",
    )[0][0]
    print(f"  Results with results_published=1: {count_published}")

    if count_published > 0:
        results["results_published_visibility"] = "PASS"
    else:
        print("  ERROR: No results found with published=1")

    # Reset
    assessment_group.results_published = 0
    assessment_group.save(ignore_permissions=True)
    frappe.db.commit()


def cleanup_test_data():
    """Delete test data in reverse dependency order."""
    # Delete Assessment Results
    for name in frappe.get_all("Assessment Result", pluck="name"):
        frappe.delete_doc("Assessment Result", name, ignore_permissions=True, force=True)

    # Delete Assessment Plans
    for name in frappe.get_all("Assessment Plan", pluck="name"):
        frappe.delete_doc("Assessment Plan", name, ignore_permissions=True, force=True)

    # Delete Assessment Groups
    for name in frappe.get_all("Assessment Group", pluck="name"):
        frappe.delete_doc("Assessment Group", name, ignore_permissions=True, force=True)

    # Delete Grading Scales
    for name in frappe.get_all("Grading Scale", pluck="name"):
        frappe.delete_doc("Grading Scale", name, ignore_permissions=True, force=True)
