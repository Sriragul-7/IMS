# Copyright (c) 2026, Institution ERP and contributors
# License: MIT. See LICENSE

import frappe
from frappe.model.document import Document


class StaffAttendance(Document):
	def validate(self):
		self.validate_no_duplicate()

	def validate_no_duplicate(self):
		"""Prevent duplicate attendance for same instructor + same date."""
		if not self.instructor or not self.attendance_date:
			return

		if frappe.db.exists(
			"Staff Attendance",
			{
				"instructor": self.instructor,
				"attendance_date": self.attendance_date,
				"name": ["!=", self.name],
			},
		):
			frappe.throw(
				f"Attendance already recorded for Instructor '{self.instructor}' on "
				f"{self.attendance_date}. Please edit the existing record instead."
			)
