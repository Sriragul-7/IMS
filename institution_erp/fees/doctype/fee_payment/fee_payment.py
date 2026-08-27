import frappe
from frappe.model.document import Document


class FeePayment(Document):
    def validate(self):
        self.validate_payment_amount()
        self.validate_student()

    def validate_student(self):
        """Auto-fetch student from linked Fees if not set."""
        if not self.student and self.fees:
            self.student = frappe.db.get_value("Fees", self.fees, "student")

    def validate_payment_amount(self):
        if not self.fees or not self.amount:
            return

        fees_doc = frappe.get_doc("Fees", self.fees)
        # Recompute paid_amount to get current outstanding
        fees_doc.recompute_paid_and_status()

        if self.amount > fees_doc.outstanding_amount:
            frappe.throw(
                f"Payment amount ({self.amount}) cannot exceed outstanding amount "
                f"({fees_doc.outstanding_amount}) for Fees '{self.fees}'."
            )

    def on_submit(self):
        """Update parent Fees record's paid_amount and status after payment."""
        if not self.fees:
            return

        fees_doc = frappe.get_doc("Fees", self.fees)
        fees_doc.recompute_paid_and_status()
        fees_doc.save(ignore_permissions=True)
        frappe.db.commit()
