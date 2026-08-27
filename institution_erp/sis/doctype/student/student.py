# Copyright (c) 2026, Institution ERP and contributors
# License: MIT. See LICENSE

import frappe
from frappe.model.document import Document


class Student(Document):
	def validate(self):
		self.validate_guardian()

	def validate_guardian(self):
		if self.guardian:
			if not frappe.db.exists("Guardian", self.guardian):
				frappe.throw(
					f"Guardian '{self.guardian}' does not exist. "
					"Please create the Guardian record first."
				)
