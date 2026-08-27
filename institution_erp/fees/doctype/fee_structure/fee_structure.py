import frappe
from frappe.model.document import Document


class FeeStructure(Document):
    def validate(self):
        self.validate_components()
        self.calculate_total_amount()

    def validate_components(self):
        if not self.components:
            frappe.throw("At least one Fee Component is required.")

    def calculate_total_amount(self):
        self.total_amount = sum(component.amount or 0 for component in self.components)
