"""
Stage 3 prep: Apply workspace role restrictions + fix FEE-2026-0071.

Workspace visibility is controlled by the `Has Role` child table on Workspace.
is_permitted() in frappe/desk/desktop.py checks if the user has at least one matching role.
If no roles set = visible to all. System Manager sees all via Workspace Manager bypass.

Also sets default_workspace on each staff user so they land on their role's workspace.

Run: bench --site institution.localhost execute institution_erp.apply_workspace_roles.run
"""
import frappe


WORKSPACE_ROLES = {
    "Admissions": ["Admissions Officer", "Academic Head", "System Manager"],
    "Academics": ["Academic Head", "System Manager"],
    "My Classes": ["Instructor"],
    "Fees & Accounts": ["Fee Manager", "System Manager"],
    "Facilities": ["Facility Manager", "System Manager"],
    "Communication": ["Communication Officer", "System Manager"],
}

DEFAULT_WORKSPACES = {
    "admissions@demo.institution.local": "Admissions",
    "academichead@demo.institution.local": "Academics",
    "instructor1@demo.institution.local": "My Classes",
    "instructor2@demo.institution.local": "My Classes",
    "feemanager@demo.institution.local": "Fees & Accounts",
    "facilitymanager@demo.institution.local": "Facilities",
    "comms.officer@demo.institution.local": "Communication",
}


def run():
    frappe.set_user("Administrator")

    print("=" * 60)
    print("APPLYING WORKSPACE ROLE RESTRICTIONS")
    print("=" * 60)

    # 1. Apply Has Role child records to each workspace via SQL to avoid validation issues
    for ws_name, roles in WORKSPACE_ROLES.items():
        # Clear existing roles
        frappe.db.sql("DELETE FROM `tabHas Role` WHERE parent=%s AND parenttype='Workspace'", ws_name)
        for i, role in enumerate(roles):
            frappe.db.sql("""
                INSERT INTO `tabHas Role` (name, parent, parenttype, parentfield, role, idx)
                VALUES (%s, %s, 'Workspace', 'roles', %s, %s)
            """, (frappe.generate_hash(), ws_name, role, i + 1))
        print(f"  {ws_name}: roles = {roles}")

    # 2. Set default_workspace on each staff user (via SQL to avoid on_update hooks)
    print("\nSetting default_workspace per user...")
    for email, ws_name in DEFAULT_WORKSPACES.items():
        frappe.db.set_value("User", email, "default_workspace", ws_name)
        print(f"  {email} -> {ws_name}")

    frappe.db.commit()
    print("\nDone.")

    # 3. Fix FEE-2026-0071
    print("\n" + "=" * 60)
    print("FIXING FEE-2026-0071")
    print("=" * 60)
    fee_name = "FEE-2026-0071"
    if frappe.db.exists("Fees", fee_name):
        fee = frappe.get_doc("Fees", fee_name)
        print(f"  Before: total={fee.total_amount}, discount={fee.discount_amount}, paid={fee.paid_amount}, outstanding={fee.outstanding_amount}, status={fee.status}")

        # The discount (1000) exceeds total (15). Cap discount to total.
        if fee.discount_amount > fee.total_amount:
            frappe.db.set_value("Fees", fee_name, "discount_amount", fee.total_amount)
            fee.reload()
            fee.recompute_paid_and_status()
            frappe.db.set_value("Fees", fee_name, {
                "discount_amount": fee.total_amount,
                "paid_amount": fee.paid_amount,
                "outstanding_amount": fee.outstanding_amount,
                "status": fee.status,
            })
            frappe.db.commit()
            fee.reload()
            print(f"  After: total={fee.total_amount}, discount={fee.discount_amount}, paid={fee.paid_amount}, outstanding={fee.outstanding_amount}, status={fee.status}")
            print("  FIXED")
        else:
            print("  Already OK")
    else:
        print(f"  {fee_name} not found")

    frappe.db.commit()
    print("\nAll TASK 0 items complete.")
