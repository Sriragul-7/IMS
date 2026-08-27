import frappe

def execute():
    # Create Admissions Officer role
    if not frappe.db.exists("Role", "Admissions Officer"):
        role = frappe.get_doc({
            "doctype": "Role",
            "role_name": "Admissions Officer",
            "desk_access": 1,
            "is_custom": 1
        })
        role.insert(ignore_permissions=True)
        print("Created role: Admissions Officer")
    else:
        print("Role 'Admissions Officer' already exists")

    # Create Academic Head role
    if not frappe.db.exists("Role", "Academic Head"):
        role = frappe.get_doc({
            "doctype": "Role",
            "role_name": "Academic Head",
            "desk_access": 1,
            "is_custom": 1
        })
        role.insert(ignore_permissions=True)
        print("Created role: Academic Head")
    else:
        print("Role 'Academic Head' already exists")

    # Create Instructor role
    if not frappe.db.exists("Role", "Instructor"):
        role = frappe.get_doc({
            "doctype": "Role",
            "role_name": "Instructor",
            "desk_access": 1,
            "is_custom": 1
        })
        role.insert(ignore_permissions=True)
        print("Created role: Instructor")
    else:
        print("Role 'Instructor' already exists")

    # Create Fee Manager role
    if not frappe.db.exists("Role", "Fee Manager"):
        role = frappe.get_doc({
            "doctype": "Role",
            "role_name": "Fee Manager",
            "desk_access": 1,
            "is_custom": 1
        })
        role.insert(ignore_permissions=True)
        print("Created role: Fee Manager")
    else:
        print("Role 'Fee Manager' already exists")

    # Create Facility Manager role
    if not frappe.db.exists("Role", "Facility Manager"):
        role = frappe.get_doc({
            "doctype": "Role",
            "role_name": "Facility Manager",
            "desk_access": 1,
            "is_custom": 1
        })
        role.insert(ignore_permissions=True)
        print("Created role: Facility Manager")
    else:
        print("Role 'Facility Manager' already exists")

    # Create Communication Officer role
    if not frappe.db.exists("Role", "Communication Officer"):
        role = frappe.get_doc({
            "doctype": "Role",
            "role_name": "Communication Officer",
            "desk_access": 1,
            "is_custom": 1
        })
        role.insert(ignore_permissions=True)
        print("Created role: Communication Officer")
    else:
        print("Role 'Communication Officer' already exists")

    # Create Student role (portal role, no desk access)
    if not frappe.db.exists("Role", "Student"):
        role = frappe.get_doc({
            "doctype": "Role",
            "role_name": "Student",
            "desk_access": 0,
            "is_custom": 1
        })
        role.insert(ignore_permissions=True)
        print("Created role: Student")
    else:
        print("Role 'Student' already exists")

    # Create Guardian role (portal role, no desk access)
    if not frappe.db.exists("Role", "Guardian"):
        role = frappe.get_doc({
            "doctype": "Role",
            "role_name": "Guardian",
            "desk_access": 0,
            "is_custom": 1
        })
        role.insert(ignore_permissions=True)
        print("Created role: Guardian")
    else:
        print("Role 'Guardian' already exists")

    frappe.db.commit()
    print("\nRoles created successfully!")
