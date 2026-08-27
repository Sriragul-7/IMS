import frappe

def execute():
    web_form_name = "Student Application"
    
    # Delete existing web form if it exists
    if frappe.db.exists("Web Form", web_form_name):
        frappe.delete_doc("Web Form", web_form_name, ignore_permissions=True)
        print(f"Deleted existing web form: {web_form_name}")

    # Work around Web Form validate issue by setting flags
    frappe.flags.in_fixtures = True
    
    try:
        web_form = frappe.new_doc("Web Form")
        web_form.title = "Student Application"
        web_form.route = "student-application"
        web_form.doc_type = "Student Applicant"
        web_form.module = "Admissions"
        web_form.is_standard = 0
        web_form.published = 1
        web_form.login_required = 0
        web_form.allow_multiple = 1
        web_form.allow_edit = 0
        web_form.allow_delete = 0
        web_form.button_label = "Submit Application"
        web_form.success_title = "Application Submitted"
        web_form.success_message = "Your application has been submitted successfully. We will review it and get back to you soon."
        web_form.introduction_text = "<h2>Student Application Form</h2><p>Please fill in the details below to apply for admission.</p>"
        
        # Add fields
        fields = [
            {"fieldname": "applicant_name", "fieldtype": "Data", "label": "Full Name", "reqd": 1},
            {"fieldname": "date_of_birth", "fieldtype": "Date", "label": "Date of Birth", "reqd": 1},
            {"fieldname": "gender", "fieldtype": "Select", "label": "Gender", "options": "\nMale\nFemale\nOther", "reqd": 1},
            {"fieldname": "section_personal", "fieldtype": "Section Break", "label": "Personal Details"},
            {"fieldname": "previous_school", "fieldtype": "Data", "label": "Previous School"},
            {"fieldname": "previous_school_marks", "fieldtype": "Float", "label": "Previous School Marks (%)"},
            {"fieldname": "column_break_personal", "fieldtype": "Column Break"},
            {"fieldname": "program", "fieldtype": "Link", "label": "Program", "options": "Program", "reqd": 1},
            {"fieldname": "academic_year", "fieldtype": "Link", "label": "Academic Year", "options": "Academic Year", "reqd": 1},
            {"fieldname": "section_guardian", "fieldtype": "Section Break", "label": "Guardian Details"},
            {"fieldname": "guardian_name", "fieldtype": "Data", "label": "Guardian Name", "reqd": 1},
            {"fieldname": "guardian_email", "fieldtype": "Data", "label": "Guardian Email", "options": "Email"},
            {"fieldname": "column_break_guardian", "fieldtype": "Column Break"},
            {"fieldname": "guardian_phone", "fieldtype": "Phone", "label": "Guardian Phone"},
            {"fieldname": "guardian_occupation", "fieldtype": "Data", "label": "Guardian Occupation"},
        ]
        
        for f in fields:
            web_form.append("web_form_fields", f)
        
        web_form.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"\nWeb Form '{web_form_name}' created successfully!")
        print(f"  Route: /student-application")
        print(f"  DocType: Student Applicant")
        print(f"  Published: Yes")
    finally:
        frappe.flags.in_fixtures = False
