# Copyright (c) 2026, Institution ERP and contributors
# License: MIT. See LICENSE

import frappe
from frappe.model.document import Document


class StudentApplicant(Document):
	def on_update(self):
		"""Auto-create Guardian and Student when status changes to Approved."""
		if self.status == "Approved" and not self.created_student:
			self.create_guardian_and_student()

	def create_guardian_and_student(self):
		"""Create Guardian and Student records from applicant data."""
		try:
			# Check if guardian already exists by email
			guardian_name = None
			if self.guardian_email:
				existing = frappe.db.get_value(
					"Guardian",
					{"guardian_email": self.guardian_email},
					"name"
				)
				if existing:
					guardian_name = existing

			# Create Guardian if not exists
			if not guardian_name:
				guardian = frappe.get_doc({
					"doctype": "Guardian",
					"guardian_name": self.guardian_name,
					"guardian_email": self.guardian_email,
					"mobile_number": self.guardian_phone,
					"occupation": self.guardian_occupation,
					"relation_to_student": "Guardian"
				})
				guardian.insert(ignore_permissions=True)
				guardian_name = guardian.name

			# Split applicant name into first and last name
			name_parts = (self.applicant_name or "").strip().split(" ", 1)
			first_name = name_parts[0] if name_parts else ""
			last_name = name_parts[1] if len(name_parts) > 1 else ""

			# Create Student
			student = frappe.get_doc({
				"doctype": "Student",
				"first_name": first_name,
				"last_name": last_name,
				"gender": self.gender,
				"date_of_birth": self.date_of_birth,
				"program": self.program,
				"academic_year": self.academic_year,
				"guardian": guardian_name,
				"previous_school": self.previous_school
			})
			student.insert(ignore_permissions=True)

			# Link back to applicant
			frappe.db.set_value("Student Applicant", self.name, "created_student", student.name)
			frappe.msgprint(
				f"Student {student.name} and Guardian {guardian_name} created successfully.",
				alert=True
			)

		except Exception as e:
			frappe.log_error(
				message=f"Failed to create Guardian/Student for {self.name}: {str(e)}",
				title="Admission Approval Error"
			)
			frappe.throw(
				f"Error creating records: {str(e)}. Please check the applicant data."
			)
