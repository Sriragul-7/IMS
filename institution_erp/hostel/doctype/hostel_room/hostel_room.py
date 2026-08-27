import frappe
from frappe.model.document import Document


class HostelRoom(Document):
    def before_insert(self):
        if not self.occupied_count:
            self.occupied_count = 0

    def validate(self):
        if self.capacity and self.capacity < 1:
            frappe.throw("Capacity must be at least 1.")
