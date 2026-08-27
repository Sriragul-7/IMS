import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today


class Notice(Document):
    def validate(self):
        if self.expiry_date and self.publish_date:
            if getdate(self.expiry_date) < getdate(self.publish_date):
                frappe.throw("Expiry Date cannot be before Publish Date.")

    def on_update(self):
        if self.status == "Published" and self.has_value_changed("status"):
            self.resolve_audience_and_create_recipients()

    def resolve_audience_and_create_recipients(self):
        """Resolve audience into concrete list of Students and create Notice Recipient records."""
        recipients = self._get_recipient_students()

        existing = frappe.get_all(
            "Notice Recipient",
            filters={"notice": self.name},
            pluck="name",
        )
        existing_count = len(existing)

        if len(recipients) == existing_count:
            return

        for student_name in recipients:
            if not frappe.db.exists(
                "Notice Recipient",
                {"notice": self.name, "student": student_name},
            ):
                frappe.get_doc({
                    "doctype": "Notice Recipient",
                    "notice": self.name,
                    "student": student_name,
                    "recipient_type": "Student",
                }).insert(ignore_permissions=True)

        frappe.db.commit()

    def _get_recipient_students(self):
        """Return list of Student names based on audience_type."""
        if self.audience_type == "All":
            return frappe.get_all("Student", pluck="name")

        elif self.audience_type == "Program-wise":
            if not self.target_program:
                frappe.throw("Target Program is required for Program-wise audience.")
            return frappe.get_all(
                "Student",
                filters={"program": self.target_program},
                pluck="name",
            )

        elif self.audience_type == "Student Group-wise":
            if not self.target_student_group:
                frappe.throw("Target Student Group is required.")
            members = frappe.get_all(
                "Student Group Member",
                filters={"parent": self.target_student_group},
                pluck="student",
            )
            return members

        elif self.audience_type == "Role-wise":
            if not self.target_role:
                frappe.throw("Target Role is required for Role-wise audience.")
            users = frappe.get_all(
                "Has Role",
                filters={"role": self.target_role, "parenttype": "User"},
                pluck="parent",
            )
            students = []
            for user in users:
                student = frappe.db.get_value("Student", {"email_address": user}, "name")
                if student:
                    students.append(student)
            return students

        elif self.audience_type == "Individual Student":
            if not self.target_student:
                frappe.throw("Target Student is required for Individual Student audience.")
            return [self.target_student]

        return []
