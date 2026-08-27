# Copyright (c) 2026, Institution ERP and contributors
# License: MIT. See LICENSE

import frappe
from frappe.model.document import Document


class StudentAttendance(Document):
	def validate(self):
		self.validate_no_duplicate()

	def validate_no_duplicate(self):
		"""Prevent duplicate attendance for same student + same date + same course_schedule."""
		if not self.student or not self.attendance_date:
			return

		# Build conditions manually to handle NULL course_schedule properly
		conditions = [
			"student = %s",
			"attendance_date = %s",
			"name != %s",
		]
		values = [self.student, self.attendance_date, self.name or ""]

		if self.course_schedule:
			conditions.append("course_schedule = %s")
			values.append(self.course_schedule)
		else:
			conditions.append("(course_schedule IS NULL OR course_schedule = '')")

		existing = frappe.db.sql(
			f"SELECT name FROM `tabStudent Attendance` WHERE {' AND '.join(conditions)}",
			values,
		pluck="name",
		)

		if existing:
			frappe.throw(
				f"Attendance already recorded for Student '{self.student}' on "
				f"{self.attendance_date}"
				f"{f' for Course Schedule {self.course_schedule}' if self.course_schedule else ' (daily attendance)'}. "
				f"Please edit the existing record instead."
			)
