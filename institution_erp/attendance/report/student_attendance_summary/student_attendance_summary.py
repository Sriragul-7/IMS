# Copyright (c) 2026, Institution ERP and contributors
# License: MIT. See LICENSE

import frappe
from frappe import _


def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_columns()
	data = get_data(filters)
	chart = get_chart_data(data, filters)

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
			"fieldname": "total_days",
			"fieldtype": "Int",
			"label": _("Total Days"),
			"width": 100,
		},
		{
			"fieldname": "present",
			"fieldtype": "Int",
			"label": _("Present"),
			"width": 100,
		},
		{
			"fieldname": "absent",
			"fieldtype": "Int",
			"label": _("Absent"),
			"width": 100,
		},
		{
			"fieldname": "late",
			"fieldtype": "Int",
			"label": _("Late"),
			"width": 100,
		},
		{
			"fieldname": "excused",
			"fieldtype": "Int",
			"label": _("Excused"),
			"width": 100,
		},
		{
			"fieldname": "attendance_percentage",
			"fieldtype": "Percent",
			"label": _("Attendance %"),
			"width": 120,
		},
	]


def get_data(filters):
	student_group = filters.get("student_group")
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	if not student_group:
		return []

	# Get all students in the group
	members = frappe.get_all(
		"Student Group Member",
		filters={"parent": student_group},
		fields=["student"],
	pluck="student",
	)

	if not members:
		return []

	# Build attendance query using raw SQL for proper date range handling
	conditions = ["student_group = %s"]
	values = [student_group]

	if members:
		placeholders = ", ".join(["%s"] * len(members))
		conditions.append(f"student IN ({placeholders})")
		values.extend(members)

	if from_date and to_date:
		conditions.append("attendance_date BETWEEN %s AND %s")
		values.extend([from_date, to_date])
	elif from_date:
		conditions.append("attendance_date >= %s")
		values.append(from_date)
	elif to_date:
		conditions.append("attendance_date <= %s")
		values.append(to_date)

	sql = f"SELECT student, status FROM `tabStudent Attendance` WHERE {' AND '.join(conditions)}"
	attendance_records = frappe.db.sql(sql, values, as_dict=True)

	# Aggregate by student
	student_stats = {}
	for record in attendance_records:
		student = record.student
		status = record.status
		if student not in student_stats:
			student_stats[student] = {
				"student": student,
				"total_days": 0,
				"present": 0,
				"absent": 0,
				"late": 0,
				"excused": 0,
			}
		student_stats[student]["total_days"] += 1
		status_lower = status.lower()
		if status_lower in student_stats[student]:
			student_stats[student][status_lower] += 1

	# Get student names
	data = []
	for student_name in members:
		stats = student_stats.get(student_name, {
			"student": student_name,
			"total_days": 0,
			"present": 0,
			"absent": 0,
			"late": 0,
			"excused": 0,
		})

		# Fetch student name
		student_doc = frappe.get_doc("Student", student_name)
		stats["student_name"] = f"{student_doc.first_name} {student_doc.last_name or ''}".strip()

		# Calculate attendance percentage
		if stats["total_days"] > 0:
			stats["attendance_percentage"] = round(
				(stats["present"] + stats["late"]) / stats["total_days"] * 100, 1
			)
		else:
			stats["attendance_percentage"] = 0

		data.append(stats)

	return data


def get_chart_data(data, filters):
	if not data:
		return None

	present_total = sum(d.get("present", 0) for d in data)
	absent_total = sum(d.get("absent", 0) for d in data)
	late_total = sum(d.get("late", 0) for d in data)
	excused_total = sum(d.get("excused", 0) for d in data)

	return {
		"data": {
			"labels": ["Present", "Absent", "Late", "Excused"],
			"datasets": [
				{
					"values": [present_total, absent_total, late_total, excused_total],
				}
			],
		},
		"type": "donut",
		"colors": ["#28a745", "#dc3545", "#ffc107", "#17a2b8"],
	}
