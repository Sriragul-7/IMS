# Copyright (c) 2026, Institution ERP and contributors
# License: MIT. See LICENSE

import frappe
from frappe.model.document import Document


class CourseSchedule(Document):
	def validate(self):
		self.validate_no_double_booking()

	def validate_no_double_booking(self):
		"""Prevent double-booking for the same room or instructor on the same day and overlapping time."""
		if not self.day_of_week or not self.from_time or not self.to_time:
			return

		filters = {
			"day_of_week": self.day_of_week,
			"from_time": ["<", self.to_time],
			"to_time": [">", self.from_time],
			"name": ["!=", self.name],
		}

		# Check room double-booking
		if self.room:
			room_conflict = frappe.db.exists(
				"Course Schedule",
				{**filters, "room": self.room},
			)
			if room_conflict:
				conflict_doc = frappe.get_doc("Course Schedule", room_conflict)
				frappe.throw(
					f"Room '{self.room}' is already booked on {self.day_of_week} "
					f"from {conflict_doc.from_time} to {conflict_doc.to_time} "
					f"(Course Schedule: {conflict_doc.name}). "
					f"Cannot create overlapping schedule from {self.from_time} to {self.to_time}."
				)

		# Check instructor double-booking
		if self.instructor:
			instructor_conflict = frappe.db.exists(
				"Course Schedule",
				{**filters, "instructor": self.instructor},
			)
			if instructor_conflict:
				conflict_doc = frappe.get_doc("Course Schedule", instructor_conflict)
				frappe.throw(
					f"Instructor '{self.instructor}' is already scheduled on {self.day_of_week} "
					f"from {conflict_doc.from_time} to {conflict_doc.to_time} "
					f"(Course Schedule: {conflict_doc.name}). "
					f"Cannot create overlapping schedule from {self.from_time} to {self.to_time}."
				)
