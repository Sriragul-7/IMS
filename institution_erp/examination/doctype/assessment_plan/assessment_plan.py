import frappe
from frappe.model.document import Document


class AssessmentPlan(Document):
    def validate(self):
        self.validate_marks()

    def validate_marks(self):
        if self.passing_marks and self.max_marks:
            if self.passing_marks >= self.max_marks:
                frappe.throw(
                    f"Passing Marks ({self.passing_marks}) must be less than "
                    f"Max Marks ({self.max_marks})."
                )
