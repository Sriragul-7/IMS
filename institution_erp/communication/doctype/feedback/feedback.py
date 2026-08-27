import frappe
from frappe.model.document import Document


class Feedback(Document):
    def validate(self):
        if not self.student and not self.guardian:
            frappe.throw("At least one of Student or Guardian must be provided.")
        if self.status in ("Resolved", "Closed") and not self.resolution_notes:
            frappe.throw("Resolution Notes are required when status is Resolved or Closed.")
