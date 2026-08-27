import frappe
from frappe.utils import today


def execute():
    print("=" * 60)
    print("STAGE 8 E2E TEST: Portal Access & Student Status")
    print("=" * 60)

    results = {}

    try:
        # Block 0: Student status field and backfill
        results.update(block_0_student_status())

        # Block 1: Guardian portal user creation
        results.update(block_1_guardian_user())

        # Block 2: Student portal user creation
        results.update(block_2_student_user())

        # Block 3: Permission scoping verification
        results.update(block_3_permission_scoping())

        # Block 4: Staff role permissions spot-check
        results.update(block_4_staff_permissions())

    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print("STAGE 8 E2E TEST SUMMARY")
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


# ---------------------------------------------------------------------------
# Block 0: Student status field and backfill
# ---------------------------------------------------------------------------

def block_0_student_status():
    print("\n[0] STUDENT STATUS FIELD & BACKFILL")
    results = {}

    # Verify status field exists on Student
    meta = frappe.get_meta("Student")
    status_field = meta.get_field("status")
    results["status_field_exists"] = status_field is not None
    print(f"  Status field exists: {results['status_field_exists']}")
    if status_field:
        print(f"  Default: {status_field.default}, Options: {status_field.options}")

    # Run backfill
    from institution_erp.api import backfill_student_status
    result = backfill_student_status()
    print(f"  Backfill result: {result}")
    results["backfill_completed"] = result["backfilled"] > 0

    # Verify all students have status=Active
    all_active = frappe.db.sql(
        "SELECT COUNT(*) FROM `tabStudent` WHERE status = 'Active'"
    )[0][0]
    total_students = frappe.db.count("Student")
    print(f"  Students with status=Active: {all_active}/{total_students}")
    results["all_students_active"] = all_active == total_students

    # Test setting individual status - pick a student with a valid guardian link
    candidates = frappe.get_all("Student", fields=["name", "guardian"])
    student = None
    for c in candidates:
        if c.guardian and frappe.db.exists("Guardian", c.guardian):
            student = c.name
            break
    if not student:
        student = candidates[0].name
    doc = frappe.get_doc("Student", student)
    doc.status = "Alumni"
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print(f"  Set {student} status to Alumni")

    # Verify it stuck
    doc = frappe.get_doc("Student", student)
    results["status_update_works"] = doc.status == "Alumni"
    print(f"  Verified status: {doc.status}")

    # Restore to Active
    doc.status = "Active"
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print(f"  Restored {student} status to Active")

    return results


# ---------------------------------------------------------------------------
# Block 1: Guardian portal user creation
# ---------------------------------------------------------------------------

def block_1_guardian_user():
    print("\n[1] GUARDIAN PORTAL USER CREATION")
    results = {}

    # Find a Guardian with email
    guardian = frappe.get_all("Guardian", fields=["name", "guardian_email", "guardian_name"])[0]
    print(f"  Using Guardian: {guardian.name} ({guardian.guardian_email})")

    from institution_erp.api import ensure_guardian_user

    # Create user
    result = ensure_guardian_user(guardian.name)
    print(f"  ensure_guardian_user result: {result}")
    results["guardian_user_created"] = result.get("created") == True or result.get("reason") == "User already exists"

    # Verify User exists
    user_exists = frappe.db.exists("User", guardian.guardian_email)
    results["guardian_user_exists"] = user_exists is not None
    print(f"  User exists: {user_exists}")

    # Verify User has Guardian role
    if user_exists:
        roles = frappe.get_roles(guardian.guardian_email)
        results["guardian_role_assigned"] = "Guardian" in roles
        print(f"  Guardian role assigned: {'Guardian' in roles}")

        # Verify User Permissions for linked students
        linked_students = frappe.get_all("Student", filters={"guardian": guardian.name}, pluck="name")
        print(f"  Linked students: {linked_students}")
        results["linked_students_exist"] = len(linked_students) > 0

        # Check User Permissions
        user_perms = frappe.get_all(
            "User Permission",
            filters={"user": guardian.guardian_email, "allow": "Student"},
            pluck="for_value",
        )
        print(f"  User Permissions (Student): {user_perms}")
        results["user_permissions_created"] = set(linked_students).issubset(set(user_perms))

    # Test bulk creation
    from institution_erp.api import ensure_all_guardian_users
    bulk_result = ensure_all_guardian_users()
    print(f"  Bulk result: {bulk_result}")
    results["bulk_guardian_users"] = len(bulk_result["errors"]) == 0

    return results


# ---------------------------------------------------------------------------
# Block 2: Student portal user creation
# ---------------------------------------------------------------------------

def block_2_student_user():
    print("\n[2] STUDENT PORTAL USER CREATION")
    results = {}

    # Find a student with email
    students_with_email = frappe.get_all(
        "Student",
        filters={"email_address": ["is", "set"]},
        fields=["name", "email_address", "first_name"],
    )
    if not students_with_email:
        print("  No students with email found - setting email on first student")
        student_doc = frappe.get_all("Student", pluck="name")[0]
        doc = frappe.get_doc("Student", student_doc)
        doc.email_address = f"{student_doc.lower()}@test.example.com"
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        students_with_email = frappe.get_all(
            "Student",
            filters={"email_address": ["is", "set"]},
            fields=["name", "email_address", "first_name"],
        )

    student = students_with_email[0]
    print(f"  Using Student: {student.name} ({student.email_address})")

    from institution_erp.api import ensure_student_user

    # Create user
    result = ensure_student_user(student.name)
    print(f"  ensure_student_user result: {result}")
    results["student_user_created"] = result.get("created") == True or result.get("reason") == "User already exists"

    # Verify User exists
    user_exists = frappe.db.exists("User", student.email_address)
    results["student_user_exists"] = user_exists is not None
    print(f"  User exists: {user_exists}")

    # Verify User has Student role
    if user_exists:
        roles = frappe.get_roles(student.email_address)
        results["student_role_assigned"] = "Student" in roles
        print(f"  Student role assigned: {'Student' in roles}")

        # Verify User Permission
        user_perms = frappe.get_all(
            "User Permission",
            filters={"user": student.email_address, "allow": "Student"},
            pluck="for_value",
        )
        print(f"  User Permissions (Student): {user_perms}")
        results["user_permission_created"] = student.name in user_perms

    # Test bulk creation
    from institution_erp.api import ensure_all_student_users
    bulk_result = ensure_all_student_users()
    print(f"  Bulk result: {bulk_result}")
    results["bulk_student_users"] = len(bulk_result["errors"]) == 0

    return results


# ---------------------------------------------------------------------------
# Block 3: Permission scoping verification
# ---------------------------------------------------------------------------

def block_3_permission_scoping():
    print("\n[3] PERMISSION SCOPING VERIFICATION")
    results = {}

    from institution_erp.api import (
        _get_portal_student,
        _get_portal_guardian_students,
        get_permission_query_conditions_student,
        get_permission_query_conditions_fees,
        get_permission_query_conditions_student_attendance,
    )

    # Test Student portal resolution
    students_with_email = frappe.get_all(
        "Student",
        filters={"email_address": ["is", "set"]},
        fields=["name", "email_address"],
    )

    if students_with_email:
        student = students_with_email[0]
        # Check if there's a User with this email that has Student role
        user = frappe.db.exists("User", student.email_address)
        if user:
            roles = frappe.get_roles(student.email_address)
            if "Student" in roles:
                resolved = _get_portal_student(student.email_address)
                print(f"  Student portal resolution: {student.email_address} -> {resolved}")
                results["student_resolution"] = resolved == student.name

                # Test permission condition
                cond = get_permission_query_conditions_student(student.email_address)
                print(f"  Student permission condition: {cond}")
                results["student_condition_valid"] = student.name in cond

                # Test fees condition
                cond_fees = get_permission_query_conditions_fees(student.email_address)
                print(f"  Fees permission condition: {cond_fees}")
                results["fees_condition_valid"] = student.name in cond_fees

    # Test Guardian portal resolution
    guardians = frappe.get_all("Guardian", fields=["name", "guardian_email"])
    for g in guardians:
        if g.guardian_email:
            user = frappe.db.exists("User", g.guardian_email)
            if user:
                roles = frappe.get_roles(g.guardian_email)
                if "Guardian" in roles:
                    guardian_students = _get_portal_guardian_students(g.guardian_email)
                    print(f"  Guardian portal resolution: {g.guardian_email} -> {guardian_students}")
                    if guardian_students:
                        results["guardian_resolution"] = len(guardian_students) > 0

                        # Test permission condition
                        cond = get_permission_query_conditions_student(g.guardian_email)
                        print(f"  Guardian permission condition: {cond}")
                        results["guardian_condition_valid"] = all(
                            s in cond for s in guardian_students
                        )
                        break

    return results


# ---------------------------------------------------------------------------
# Block 4: Staff role permissions spot-check
# ---------------------------------------------------------------------------

def block_4_staff_permissions():
    print("\n[4] STAFF ROLE PERMISSIONS SPOT-CHECK")
    results = {}

    # Verify custom roles exist
    custom_roles = frappe.get_all("Role", filters={"is_custom": 1}, pluck="name")
    print(f"  Custom roles: {custom_roles}")
    expected_roles = {"Student", "Guardian", "Communication Officer", "Facility Manager"}
    results["custom_roles_exist"] = expected_roles.issubset(set(custom_roles))

    # Verify portal roles have desk_access=0
    for role_name in ["Student", "Guardian"]:
        role = frappe.get_doc("Role", role_name)
        print(f"  {role_name} desk_access: {role.desk_access}")
        results[f"{role_name.lower()}_no_desk"] = role.desk_access == 0

    # Verify Staff roles have desk_access=1
    for role_name in ["Admissions Officer", "Academic Head", "Instructor", "Fee Manager", "Facility Manager", "Communication Officer"]:
        role = frappe.get_doc("Role", role_name)
        print(f"  {role_name} desk_access: {role.desk_access}")
        results[f"{role_name.lower().replace(' ', '_')}_has_desk"] = role.desk_access == 1

    # Spot-check: Fee Manager should only see fee DocTypes
    fee_manager_perms = frappe.get_all(
        "DocPerm",
        filters={"role": "Fee Manager"},
        fields=["parent"],
    )
    fee_manager_dtypes = {p.parent for p in fee_manager_perms}
    print(f"  Fee Manager DocTypes: {fee_manager_dtypes}")
    expected_fee_dtypes = {"Fees", "Fee Payment", "Fee Category", "Fee Discount", "Fee Schedule", "Fee Structure"}
    results["fee_manager_scoped"] = fee_manager_dtypes == expected_fee_dtypes

    # Spot-check: Facility Manager should only see Library/Hostel/Transport
    fm_perms = frappe.get_all(
        "DocPerm",
        filters={"role": "Facility Manager"},
        fields=["parent"],
    )
    fm_dtypes = {p.parent for p in fm_perms}
    print(f"  Facility Manager DocTypes: {fm_dtypes}")
    expected_fm_dtypes = {
        "Hostel", "Hostel Room", "Hostel Room Allocation",
        "Vehicle", "Transport Route", "Student Transport Allocation",
        "Library Item", "Book Category", "Library Membership", "Library Transaction",
    }
    results["facility_manager_scoped"] = fm_dtypes == expected_fm_dtypes

    return results
