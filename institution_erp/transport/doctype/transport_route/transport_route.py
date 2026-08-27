import frappe
from frappe.model.document import Document


class TransportRoute(Document):
    def validate(self):
        if self.stops:
            orders = [s.stop_order for s in self.stops if s.stop_order]
            if len(orders) != len(set(orders)):
                frappe.throw("Duplicate Stop Order values found in stops.")
