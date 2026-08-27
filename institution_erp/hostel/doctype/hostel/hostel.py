import frappe
from frappe.model.document import Document


class Hostel(Document):
    def validate(self):
        self.recompute_total_capacity()

    def recompute_total_capacity(self):
        total = 0
        for room in frappe.get_all(
            "Hostel Room",
            filters={"hostel": self.name},
            fields=["capacity"],
        ):
            total += room.capacity or 0
        self.total_capacity = total
