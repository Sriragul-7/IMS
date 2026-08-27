import frappe
from frappe.model.document import Document


class LibraryItem(Document):
    def validate(self):
        if self.available_copies is None:
            self.available_copies = self.total_copies
        if self.available_copies < 0:
            frappe.throw("Available Copies cannot be negative.")
        if self.total_copies < 0:
            frappe.throw("Total Copies cannot be negative.")
        if self.available_copies > self.total_copies:
            frappe.throw(
                f"Available Copies ({self.available_copies}) cannot exceed "
                f"Total Copies ({self.total_copies})."
            )

    def before_insert(self):
        self.available_copies = self.total_copies
