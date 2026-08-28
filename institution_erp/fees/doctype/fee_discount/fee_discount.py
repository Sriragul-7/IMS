import frappe
from frappe.model.document import Document


class FeeDiscount(Document):
    def validate(self):
        self.validate_discount_value()

    def validate_discount_value(self):
        if self.discount_type == "Percentage" and self.discount_value:
            if self.discount_value <= 0 or self.discount_value > 100:
                frappe.throw("Percentage discount must be between 0 and 100.")

    def on_update(self):
        """When status changes to Approved, apply discount to linked Fees record."""
        if self.status != "Approved" or not self.fees:
            return

        fees_doc = frappe.get_doc("Fees", self.fees)

        # Calculate discount amount
        if self.discount_type == "Percentage":
            discount_amount = (fees_doc.total_amount * self.discount_value) / 100
        else:
            discount_amount = self.discount_value

        # Recompute outstanding with the new discount
        fees_doc.discount_amount = discount_amount
        fees_doc.recompute_paid_and_status()

        frappe.db.set_value("Fees", self.fees, {
            "discount_amount": fees_doc.discount_amount,
            "paid_amount": fees_doc.paid_amount,
            "outstanding_amount": fees_doc.outstanding_amount,
            "status": fees_doc.status,
        })
        frappe.db.commit()
