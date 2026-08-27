import frappe
from frappe.model.document import Document
from frappe.utils import today, getdate


class Fees(Document):
    def validate(self):
        self.calculate_total_amount()
        self.recompute_paid_and_status()

    def calculate_total_amount(self):
        self.total_amount = sum(component.amount or 0 for component in self.components)

    def get_net_amount(self):
        """Total amount minus discount."""
        return self.total_amount - (self.discount_amount or 0)

    def recompute_paid_and_status(self):
        """Recompute paid_amount from linked Fee Payments and determine status."""
        if not self.name:
            return

        paid = frappe.db.sql(
            "SELECT COALESCE(SUM(amount), 0) FROM `tabFee Payment` WHERE fees = %s AND docstatus = 1",
            self.name,
        )[0][0]

        self.paid_amount = paid
        net_amount = self.get_net_amount()
        self.outstanding_amount = net_amount - self.paid_amount

        if self.outstanding_amount <= 0:
            self.status = "Paid"
        elif self.paid_amount > 0:
            self.status = "Partially Paid"
        else:
            self.status = "Unpaid"

        # Check for overdue
        if self.outstanding_amount > 0 and self.due_date:
            if getdate(self.due_date) < getdate(today()):
                self.status = "Overdue"
