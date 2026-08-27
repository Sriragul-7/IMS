# Copyright (c) 2026, Institution ERP and contributors
# License: MIT. See LICENSE

import frappe
from frappe.model.document import Document


class EntranceTestResult(Document):
	def validate(self):
		self.calculate_result()

	def calculate_result(self):
		"""Auto-calculate Pass/Fail based on entrance test passing marks."""
		if self.entrance_test and self.marks_obtained is not None:
			test = frappe.get_doc("Entrance Test", self.entrance_test)
			if self.marks_obtained >= test.passing_marks:
				self.result = "Pass"
			else:
				self.result = "Fail"
