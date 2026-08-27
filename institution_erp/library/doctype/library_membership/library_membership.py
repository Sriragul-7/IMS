import frappe
from frappe.model.document import Document
from frappe.utils import today


class LibraryMembership(Document):
    def validate(self):
        if self.valid_upto and self.issue_date and self.valid_upto < self.issue_date:
            frappe.throw("Valid Upto date cannot be before Issue Date.")
        if self.max_books_allowed and self.max_books_allowed < 1:
            frappe.throw("Max Books Allowed must be at least 1.")

    def before_insert(self):
        if not self.status:
            self.status = "Active"
