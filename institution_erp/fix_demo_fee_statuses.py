"""
One-off patch: recompute paid_amount/outstanding_amount/status on all demo Fees records.
The demo data generator bypassed Fee Payment.on_submit via SQL, so these fields were
never recomputed through the real recompute_paid_and_status() logic.

Run: bench --site institution.localhost execute institution_erp.fix_demo_fee_statuses.run
"""
import frappe


def run():
    print("=" * 60)
    print("FIXING DEMO FEE STATUSES")
    print("=" * 60)

    frappe.set_user("Administrator")

    # Find all demo Fees (linked to demo students with @demo.institution.local emails)
    demo_fees = frappe.db.sql("""
        SELECT f.name
        FROM `tabFees` f
        JOIN `tabStudent` s ON f.student = s.name
        WHERE s.email_address LIKE %s
    """, ("%@demo.institution.local",), as_dict=True)

    print(f"\nFound {len(demo_fees)} demo Fees records to recompute")

    fixed = 0
    errors = 0
    for fee_row in demo_fees:
        try:
            fees_doc = frappe.get_doc("Fees", fee_row.name)
            old_paid = fees_doc.paid_amount
            old_outstanding = fees_doc.outstanding_amount
            old_status = fees_doc.status

            fees_doc.recompute_paid_and_status()

            # Only update if something changed
            if (fees_doc.paid_amount != old_paid or
                fees_doc.outstanding_amount != old_outstanding or
                fees_doc.status != old_status):
                frappe.db.set_value("Fees", fee_row.name, {
                    "paid_amount": fees_doc.paid_amount,
                    "outstanding_amount": fees_doc.outstanding_amount,
                    "status": fees_doc.status,
                })
                fixed += 1
                if fixed <= 5:
                    print(f"  Fixed {fee_row.name}: paid {old_paid}->{fees_doc.paid_amount}, "
                          f"outstanding {old_outstanding}->{fees_doc.outstanding_amount}, "
                          f"status {old_status}->{fees_doc.status}")
            else:
                # Still correct - but count as verified
                pass
        except Exception as e:
            errors += 1
            print(f"  ERROR on {fee_row.name}: {e}")

    frappe.db.commit()

    print(f"\nResults: {fixed} fixed, {errors} errors, {len(demo_fees) - fixed - errors} already correct")
    print("=" * 60)
