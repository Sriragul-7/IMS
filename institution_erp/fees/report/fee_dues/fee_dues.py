# Copyright (c) 2026, Institution ERP and contributors
# License: MIT. See LICENSE

import frappe
from frappe import _
from frappe.utils import today, date_diff


def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_columns()
	data = get_data(filters)
	chart = get_chart_data(data)

	return columns, data, None, chart


def get_columns():
	return [
		{
			"fieldname": "student",
			"fieldtype": "Link",
			"label": _("Student"),
			"options": "Student",
			"width": 200,
		},
		{
			"fieldname": "student_name",
			"fieldtype": "Data",
			"label": _("Student Name"),
			"width": 200,
		},
		{
			"fieldname": "program",
			"fieldtype": "Data",
			"label": _("Program"),
			"width": 150,
		},
		{
			"fieldname": "total_amount",
			"fieldtype": "Currency",
			"label": _("Total Amount"),
			"width": 120,
		},
		{
			"fieldname": "paid_amount",
			"fieldtype": "Currency",
			"label": _("Paid Amount"),
			"width": 120,
		},
		{
			"fieldname": "outstanding_amount",
			"fieldtype": "Currency",
			"label": _("Outstanding Amount"),
			"width": 140,
		},
		{
			"fieldname": "due_date",
			"fieldtype": "Date",
			"label": _("Due Date"),
			"width": 120,
		},
		{
			"fieldname": "status",
			"fieldtype": "Data",
			"label": _("Status"),
			"width": 120,
		},
		{
			"fieldname": "days_overdue",
			"fieldtype": "Int",
			"label": _("Days Overdue"),
			"width": 110,
		},
	]


def get_data(filters):
	academic_year = filters.get("academic_year")
	program = filters.get("program")
	status = filters.get("status")

	conditions = ["1=1"]
	values = []

	if academic_year:
		conditions.append("f.academic_year = %s")
		values.append(academic_year)

	if program:
		# Join with Student to filter by program
		conditions.append("s.program = %s")
		values.append(program)

	if status:
		conditions.append("f.status = %s")
		values.append(status)

	where_clause = " AND ".join(conditions)

	sql = f"""
		SELECT
			f.student,
			f.total_amount,
			f.discount_amount,
			f.paid_amount,
			f.outstanding_amount,
			f.due_date,
			f.status,
			s.program
		FROM `tabFees` f
		LEFT JOIN `tabStudent` s ON f.student = s.name
		WHERE {where_clause}
		ORDER BY f.due_date ASC
	"""

	results = frappe.db.sql(sql, values, as_dict=True)

	data = []
	today_date = today()

	for row in results:
		# Fetch student name
		student_name = frappe.db.get_value(
			"Student", row.student, ["first_name", "last_name"], as_dict=True
		)
		full_name = ""
		if student_name:
			full_name = f"{student_name.first_name} {student_name.last_name or ''}".strip()

		# Calculate days overdue
		days_overdue = 0
		if row.status == "Overdue" and row.due_date:
			days_overdue = abs(date_diff(today_date, row.due_date))

		data.append({
			"student": row.student,
			"student_name": full_name,
			"program": row.program,
			"total_amount": row.total_amount,
			"paid_amount": row.paid_amount,
			"outstanding_amount": row.outstanding_amount,
			"due_date": row.due_date,
			"status": row.status,
			"days_overdue": days_overdue,
		})

	return data


def get_chart_data(data):
	if not data:
		return None

	total_outstanding = sum(d.get("outstanding_amount", 0) for d in data)
	total_paid = sum(d.get("paid_amount", 0) for d in data)

	return {
		"data": {
			"labels": ["Paid", "Outstanding"],
			"datasets": [
				{
					"values": [total_paid, total_outstanding],
				}
			],
		},
		"type": "donut",
		"colors": ["#28a745", "#dc3545"],
	}
