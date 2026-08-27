import frappe

def execute():
    workflow_name = "Admission Approval"
    
    # Delete existing workflow if it exists
    if frappe.db.exists("Workflow", workflow_name):
        frappe.delete_doc("Workflow", workflow_name, ignore_permissions=True)
        print(f"Deleted existing workflow: {workflow_name}")

    # Create the workflow
    workflow = frappe.get_doc({
        "doctype": "Workflow",
        "workflow_name": workflow_name,
        "document_type": "Student Applicant",
        "is_active": 1,
        "workflow_state_field": "workflow_state",
        "states": [
            {
                "state": "Draft",
                "doc_status": 0,
                "update_field": "status",
                "update_value": "Draft",
                "allow_edit": "Admissions Officer"
            },
            {
                "state": "Applied",
                "doc_status": 0,
                "update_field": "status",
                "update_value": "Applied",
                "allow_edit": "Admissions Officer"
            },
            {
                "state": "Under Review",
                "doc_status": 0,
                "update_field": "status",
                "update_value": "Under Review",
                "allow_edit": "Academic Head"
            },
            {
                "state": "Approved",
                "doc_status": 1,
                "update_field": "status",
                "update_value": "Approved",
                "allow_edit": "Academic Head"
            },
            {
                "state": "Rejected",
                "doc_status": 2,
                "update_field": "status",
                "update_value": "Rejected",
                "allow_edit": "Academic Head"
            },
            {
                "state": "Waitlisted",
                "doc_status": 0,
                "update_field": "status",
                "update_value": "Waitlisted",
                "allow_edit": "Academic Head"
            }
        ],
        "transitions": [
            {
                "state": "Draft",
                "action": "Apply",
                "next_state": "Applied",
                "allowed": "Admissions Officer"
            },
            {
                "state": "Applied",
                "action": "Review",
                "next_state": "Under Review",
                "allowed": "Admissions Officer"
            },
            {
                "state": "Under Review",
                "action": "Approve",
                "next_state": "Approved",
                "allowed": "Academic Head"
            },
            {
                "state": "Under Review",
                "action": "Reject",
                "next_state": "Rejected",
                "allowed": "Academic Head"
            },
            {
                "state": "Under Review",
                "action": "Waitlist",
                "next_state": "Waitlisted",
                "allowed": "Academic Head"
            }
        ]
    })
    
    workflow.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"\nWorkflow '{workflow_name}' created successfully!")
    print(f"  Document Type: Student Applicant")
    print(f"  States: Draft -> Applied -> Under Review -> Approved/Rejected/Waitlisted")
    print(f"  Workflow State Field: workflow_state")
