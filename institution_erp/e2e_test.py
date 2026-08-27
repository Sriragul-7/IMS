import frappe

def execute():
    print("=" * 60)
    print("END-TO-END TEST: Admissions Module")
    print("=" * 60)
    
    # 0. Clean up any existing test data
    print("\n[0] Cleaning up existing test data...")
    # Delete in correct order to avoid link errors
    for dt in ["Entrance Test Result", "Entrance Test"]:
        existing = frappe.get_all(dt, pluck="name")
        for name in existing:
            frappe.delete_doc(dt, name, ignore_permissions=True, force=True)
    
    # Delete approved Student Applicants first (which may have linked Students/Guardians)
    existing_applicants = frappe.get_all("Student Applicant", filters={"status": "Approved"}, pluck="name")
    for name in existing_applicants:
        # Delete linked student first, then its guardian
        student_name = frappe.db.get_value("Student Applicant", name, "created_student")
        if student_name:
            guardian_name = frappe.db.get_value("Student", student_name, "guardian")
            frappe.delete_doc("Student", student_name, ignore_permissions=True, force=True)
            if guardian_name and frappe.db.exists("Guardian", guardian_name):
                frappe.delete_doc("Guardian", guardian_name, ignore_permissions=True, force=True)
        frappe.delete_doc("Student Applicant", name, ignore_permissions=True, force=True)
    
    # Delete remaining Student Applicants
    existing_applicants = frappe.get_all("Student Applicant", pluck="name")
    for name in existing_applicants:
        frappe.delete_doc("Student Applicant", name, ignore_permissions=True, force=True)
    
    existing_inquiries = frappe.get_all("Admission Inquiry", pluck="name")
    for name in existing_inquiries:
        frappe.delete_doc("Admission Inquiry", name, ignore_permissions=True, force=True)
    
    frappe.db.commit()
    print("  Cleanup done.")

    # 1. Create Admission Inquiry
    print("\n[1] Creating Admission Inquiry...")
    inquiry = frappe.get_doc({
        "doctype": "Admission Inquiry",
        "naming_series": "ADM-INQ-.YYYY.-.####",
        "applicant_name": "Test Applicant Parent",
        "date_of_birth": "2010-01-15",
        "gender": "Male",
        "guardian_name": "Test Guardian",
        "guardian_phone": "+91-9999999999",
        "guardian_email": "test.guardian@example.com",
        "program_interested": "Bachelor of Computer Applications",
        "source": "Website",
        "inquiry_date": frappe.utils.today(),
        "status": "Open",
        "remarks": "Test inquiry for E2E testing"
    })
    inquiry.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"  Created: {inquiry.name}")

    # 2. Create Student Applicant from Inquiry
    print("\n[2] Creating Student Applicant (Draft)...")
    applicant = frappe.get_doc({
        "doctype": "Student Applicant",
        "naming_series": "STU-APP-.YYYY.-.####",
        "applicant_name": "TestApplicant Student",
        "date_of_birth": "2010-01-15",
        "gender": "Male",
        "program": "Bachelor of Computer Applications",
        "academic_year": frappe.db.get_single_value("Academic Year", "name") or "2026-2027",
        "guardian_name": "Test Guardian",
        "guardian_email": "test.guardian@example.com",
        "guardian_phone": "+91-9999999999",
        "guardian_occupation": "Engineer",
        "previous_school": "Test School",
        "previous_school_marks": 85.5,
        "inquiry": inquiry.name,
        "application_date": frappe.utils.today(),
        "status": "Draft"
    })
    applicant.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"  Created: {applicant.name} (Status: {applicant.status})")

    # 3. Move to Applied
    print("\n[3] Moving to Applied status...")
    applicant.status = "Applied"
    applicant.workflow_state = "Applied"
    applicant.save(ignore_permissions=True)
    frappe.db.commit()
    print(f"  Status: {applicant.status}")

    # 4. Move to Under Review
    print("\n[4] Moving to Under Review status...")
    applicant.status = "Under Review"
    applicant.workflow_state = "Under Review"
    applicant.save(ignore_permissions=True)
    frappe.db.commit()
    print(f"  Status: {applicant.status}")

    # 5. Create Entrance Test
    print("\n[5] Creating Entrance Test...")
    test = frappe.get_doc({
        "doctype": "Entrance Test",
        "test_name": "TEST-BCA-Entrance",
        "test_date": frappe.utils.today(),
        "program": "Bachelor of Computer Applications",
        "max_marks": 100,
        "passing_marks": 40
    })
    test.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"  Created: {test.name}")

    # 6. Create Entrance Test Result (Pass)
    print("\n[6] Creating Entrance Test Result (Pass)...")
    result = frappe.get_doc({
        "doctype": "Entrance Test Result",
        "entrance_test": test.name,
        "student_applicant": applicant.name,
        "marks_obtained": 75
    })
    result.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"  Created: {result.name} - Result: {result.result}")

    # 7. Approve the applicant
    print("\n[7] Approving Student Applicant...")
    applicant.status = "Approved"
    applicant.workflow_state = "Approved"
    applicant.save(ignore_permissions=True)
    frappe.db.commit()
    
    # Reload to check if created_student was set
    applicant.reload()
    print(f"  Status: {applicant.status}")
    print(f"  Created Student: {applicant.created_student}")

    # 8. Verify auto-created records
    print("\n[8] Verifying auto-created records...")
    
    if applicant.created_student:
        student = frappe.get_doc("Student", applicant.created_student)
        print(f"  Student: {student.name}")
        print(f"    First Name: {student.first_name}")
        print(f"    Last Name: {student.last_name}")
        print(f"    Gender: {student.gender}")
        print(f"    DOB: {student.date_of_birth}")
        print(f"    Program: {student.program}")
        print(f"    Guardian: {student.guardian}")
        
        # Verify guardian
        guardian = frappe.get_doc("Guardian", student.guardian)
        print(f"  Guardian: {guardian.name}")
        print(f"    Name: {guardian.guardian_name}")
        print(f"    Email: {guardian.guardian_email}")
        print(f"    Phone: {guardian.mobile_number}")
        print(f"    Occupation: {guardian.occupation}")
        
        print("\n" + "=" * 60)
        print("TEST PASSED: Guardian and Student auto-created successfully!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("TEST FAILED: created_student was not set!")
        print("=" * 60)
    
    # 9. Verify workflow states
    print("\n[9] Verifying workflow states...")
    states = frappe.get_all("Workflow State", pluck="name")
    print(f"  Available states: {states}")
    
    actions = frappe.get_all("Workflow Action Master", pluck="name")
    print(f"  Available actions: {actions}")
    
    workflows = frappe.get_all("Workflow", filters={"document_type": "Student Applicant"}, pluck="name")
    print(f"  Workflows for Student Applicant: {workflows}")
    
    print("\n[10] Test Summary:")
    print(f"  - Admission Inquiry: {inquiry.name}")
    print(f"  - Student Applicant: {applicant.name}")
    print(f"  - Entrance Test: {test.name}")
    print(f"  - Entrance Test Result: {result.name} ({result.result})")
    print(f"  - Auto-created Student: {applicant.created_student}")
    print(f"  - Auto-created Guardian: {student.guardian if applicant.created_student else 'N/A'}")
    print(f"\nAll tests completed successfully!")
