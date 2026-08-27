import frappe

def execute():
    # Create Workflow States first
    states = ["Draft", "Applied", "Under Review", "Approved", "Rejected", "Waitlisted"]
    for state_name in states:
        if not frappe.db.exists("Workflow State", state_name):
            ws = frappe.get_doc({
                "doctype": "Workflow State",
                "workflow_state_name": state_name
            })
            ws.insert(ignore_permissions=True)
            print(f"Created Workflow State: {state_name}")
        else:
            print(f"Workflow State '{state_name}' already exists")

    # Create Workflow Actions
    actions = ["Apply", "Review", "Approve", "Reject", "Waitlist"]
    for action_name in actions:
        if not frappe.db.exists("Workflow Action Master", action_name):
            wa = frappe.get_doc({
                "doctype": "Workflow Action Master",
                "workflow_action_name": action_name
            })
            wa.insert(ignore_permissions=True)
            print(f"Created Workflow Action: {action_name}")
        else:
            print(f"Workflow Action '{action_name}' already exists")

    frappe.db.commit()
    print("\nWorkflow states and actions created!")
