import frappe
from frappe.model.document import Document


class Vehicle(Document):
    def validate(self):
        if self.capacity and self.capacity < 1:
            frappe.throw("Capacity must be at least 1.")
