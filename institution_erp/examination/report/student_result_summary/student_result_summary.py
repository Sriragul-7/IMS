# Copyright (c) 2026, Institution ERP and contributors
# License: MIT. See LICENSE

import frappe
from frappe import _


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
			"fieldname": "assessment_plan",
			"fieldtype": "Link",
			"label": _("Assessment Plan"),
			"options": "Assessment Plan",
			"width": 180,
		},
		{
			"fieldname": "course",
			"fieldtype": "Data",
			"label": _("Course"),
			"width": 180,
		},
		{
			"fieldname": "max_marks",
			"fieldtype": "Int",
			"label": _("Max Marks"),
			"width": 100,
		},
		{
			"fieldname": "marks_obtained",
			"fieldtype": "Int",
			"label": _("Marks Obtained"),
			"width": 130,
		},
		{
			"fieldname": "percentage",
			"fieldtype": "Percent",
			"label": _("Percentage"),
			"width": 110,
		},
		{
			"fieldname": "grade",
			"fieldtype": "Data",
			"label": _("Grade"),
			"width": 80,
		},
		{
			"fieldname": "status",
			"fieldtype": "Data",
			"label": _("Status"),
			"width": 80,
		},
	]


def get_data(filters):
	student = filters.get("student")
	student_group = filters.get("student_group")
	assessment_group = filters.get("assessment_group")

	if not student and not student_group:
		return []

	conditions = []
	values = []

	if student:
		conditions.append("ar.student = %s")
		values.append(student)

	if student_group:
		conditions.append("ap.student_group = %s")
		values.append(student_group)

	if assessment_group:
		conditions.append("ap.assessment_group = %s")
		values.append(assessment_group)

	if not conditions:
		return []

	where_clause = " AND ".join(conditions)

	sql = f"""
		SELECT
			ar.student,
			ar.assessment_plan,
			ar.marks_obtained,
			ar.percentage,
			ar.grade,
			ar.status,
			ap.max_marks,
			ap.course,
			ap.assessment_group
		FROM `tabAssessment Result` ar
		JOIN `tabAssessment Plan` ap ON ar.assessment_plan = ap.name
		WHERE {where_clause}
		ORDER BY ar.student, ap.exam_date
	"""
	results = frappe.db.sql(sql, values, as_dict=True)

	# Fetch student names
	student_names = {}
	student_list = list(set(r.student for r in results))
	if student_list:
		placeholders = ", ".join(["%s"] * len(student_list))
		name_rows = frappe.db.sql(
			f"SELECT name, first_name, last_name FROM `tabStudent` WHERE name IN ({placeholders})",
			student_list,
			as_dict=True,
		)
		for row in name_rows:
			student_names[row.name] = f"{row.first_name} {row.last_name or ''}".strip()

	# Fetch course names
	course_names = {}
	course_list = list(set(r.course for r in results if r.course))
	if course_list:
		placeholders = ", ".join(["%s"] * len(course_list))
		course_rows = frappe.db.sql(
			f"SELECT name, course_name FROM `tabCourse` WHERE name IN ({placeholders})",
			course_list,
			as_dict=True,
		)
		for row in course_rows:
			course_names[row.name] = row.course_name

	data = []
	for r in results:
		data.append({
			"student": r.student,
			"student_name": student_names.get(r.student, ""),
			"assessment_plan": r.assessment_plan,
			"course": course_names.get(r.course, r.course),
			"max_marks": r.max_marks,
			"marks_obtained": r.marks_obtained,
			"percentage": r.percentage,
			"grade": r.grade,
			"status": r.status,
			"bold": 0,
		})

	# Add summary row
	if data:
		total_marks = sum(d.get("marks_obtained", 0) for d in data)
		total_max = sum(d.get("max_marks", 0) for d in data)
		avg_pct = round(total_marks / total_max * 100, 2) if total_max else 0

		# Determine overall grade from first result's grading scale
		overall_grade = ""
		if data and results:
			first_plan = frappe.db.get_value(
				"Assessment Plan", results[0].assessment_plan, "grading_scale"
			)
			if first_plan:
				scale = frappe.get_doc("Grading Scale", first_plan)
				sorted_intervals = sorted(
					scale.intervals,
					key=lambda x: x.threshold_percent or 0,
					reverse=True,
				)
				for interval in sorted_intervals:
					if avg_pct >= (interval.threshold_percent or 0):
						overall_grade = interval.grade_code
						break

		data.append({
			"student": "",
			"student_name": "OVERALL AVERAGE",
			"assessment_plan": "",
			"course": "",
			"max_marks": total_max,
			"marks_obtained": total_marks,
			"percentage": avg_pct,
			"grade": overall_grade,
			"status": "",
			"bold": 1,
		})

	return data


def get_chart_data(data):
	if not data or len(data) <= 1:
		return None

	student_grades = {}
	for d in data:
		if d.get("bold"):
			continue
		student = d.get("student")
		if student not in student_grades:
			student_grades[student] = {"total_marks": 0, "total_max": 0}
		student_grades[student]["total_marks"] += d.get("marks_obtained", 0)
		student_grades[student]["total_max"] += d.get("max_marks", 0)

	present_count = 0
	fail_count = 0
	for sg in student_grades.values():
		pct = (sg["total_marks"] / sg["total_max"] * 100) if sg["total_max"] else 0
		if pct >= 50:
			present_count += 1
		else:
			fail_count += 1

	return {
		"data": {
			"labels": ["Pass", "Fail"],
			"datasets": [{"values": [present_count, fail_count]}],
		},
		"type": "donut",
		"colors": ["#28a745", "#dc3545"],
	}
