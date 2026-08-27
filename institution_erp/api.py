# Copyright (c) 2026, Institution ERP and contributors
# License: MIT. See LICENSE

import frappe
from frappe import _


def get_permission_query_conditions_staff_attendance(user):
	"""
	Restrict Instructor role to only see/edit their own staff attendance.
	"""
	if "System Manager" in frappe.get_roles(user):
		return ""

	if "Academic Head" in frappe.get_roles(user):
		return ""

	if "Instructor" in frappe.get_roles(user):
		instructor = frappe.db.get_value("Instructor", {"email": frappe.db.get_value("User", user, "email")}, "name")
		if not instructor:
			return "1=0"
		return f"`tabStaff Attendance`.instructor = '{instructor}'"

	return "1=0"


@frappe.whitelist()
def get_students_in_group(student_group):
	"""Fetch all students in a given Student Group."""
	if not frappe.db.exists("Student Group", student_group):
		frappe.throw(_("Student Group '{0}' does not exist.").format(student_group))

	members = frappe.get_all(
		"Student Group Member",
		filters={"parent": student_group},
		fields=["student"],
	pluck="student",
	)

	if not members:
		frappe.throw(
			_("No students found in Student Group '{0}'. "
			"Please add members to the group first.").format(student_group)
		)

	students = []
	for student_name in members:
		student = frappe.get_doc("Student", student_name)
		students.append({
			"student": student.name,
			"student_name": f"{student.first_name} {student.last_name or ''}".strip(),
			"status": "Present",  # default status
		})

	return students


@frappe.whitelist()
def mark_bulk_student_attendance(student_group, attendance_date, attendance_data, course_schedule=None):
	"""
	Bulk-create Student Attendance records.

	Args:
	    student_group: Name of the Student Group
	    attendance_date: Date string (YYYY-MM-DD)
	    attendance_data: JSON string or list of dicts [{"student": "STU-...", "status": "Present"}, ...]
	    course_schedule: Optional Course Schedule name
	"""
	if isinstance(attendance_data, str):
		import json
		attendance_data = json.loads(attendance_data)

	if not attendance_data:
		frappe.throw(_("No attendance data provided."))

	if not frappe.db.exists("Student Group", student_group):
		frappe.throw(_("Student Group '{0}' does not exist.").format(student_group))

	created = []
	errors = []

	for record in attendance_data:
		student = record.get("student")
		status = record.get("status")

		if not student or not status:
			errors.append(f"Invalid record: {record}")
			continue

		if status not in ("Present", "Absent", "Late", "Excused"):
			errors.append(f"Invalid status '{status}' for student {student}")
			continue

		# Check for existing attendance using raw SQL for proper NULL handling
		if course_schedule:
			existing = frappe.db.sql(
				"SELECT name FROM `tabStudent Attendance` "
				"WHERE student = %s AND attendance_date = %s AND course_schedule = %s",
				(student, attendance_date, course_schedule),
			pluck="name",
			)
		else:
			existing = frappe.db.sql(
				"SELECT name FROM `tabStudent Attendance` "
				"WHERE student = %s AND attendance_date = %s "
				"AND (course_schedule IS NULL OR course_schedule = '')",
				(student, attendance_date),
			pluck="name",
			)

		if existing:
			errors.append(
				f"Attendance already exists for {student} on {attendance_date}"
				f"{f' (Schedule: {course_schedule})' if course_schedule else ''}"
			)
			continue

		try:
			att = frappe.get_doc({
				"doctype": "Student Attendance",
				"student": student,
				"student_group": student_group,
				"course_schedule": course_schedule or None,
				"attendance_date": attendance_date,
				"status": status,
			})
			att.insert(ignore_permissions=True)
			created.append(att.name)
		except Exception as e:
			errors.append(f"Error creating attendance for {student}: {str(e)}")

	if created:
		frappe.db.commit()

	return {
		"created": len(created),
		"records": created,
		"errors": errors,
	}


@frappe.whitelist()
def mark_bulk_staff_attendance(attendance_date, attendance_data):
	"""
	Bulk-create Staff Attendance records.

	Args:
	    attendance_date: Date string (YYYY-MM-DD)
	    attendance_data: JSON string or list of dicts [{"instructor": "INST-...", "status": "Present"}, ...]
	"""
	if isinstance(attendance_data, str):
		import json
		attendance_data = json.loads(attendance_data)

	if not attendance_data:
		frappe.throw(_("No attendance data provided."))

	created = []
	errors = []

	for record in attendance_data:
		instructor = record.get("instructor")
		status = record.get("status")

		if not instructor or not status:
			errors.append(f"Invalid record: {record}")
			continue

		if status not in ("Present", "Absent", "Half Day", "On Leave"):
			errors.append(f"Invalid status '{status}' for instructor {instructor}")
			continue

		if frappe.db.exists(
			"Staff Attendance",
			{"instructor": instructor, "attendance_date": attendance_date},
		):
			errors.append(f"Attendance already exists for {instructor} on {attendance_date}")
			continue

		try:
			att = frappe.get_doc({
				"doctype": "Staff Attendance",
				"instructor": instructor,
				"attendance_date": attendance_date,
				"status": status,
			})
			att.insert(ignore_permissions=True)
			created.append(att.name)
		except Exception as e:
			errors.append(f"Error creating attendance for {instructor}: {str(e)}")

	if created:
		frappe.db.commit()

	return {
		"created": len(created),
		"records": created,
		"errors": errors,
	}


# ---------------------------------------------------------------------------
# Examination: Permission Query Conditions
# ---------------------------------------------------------------------------

def get_permission_query_conditions_assessment_plan(user):
	"""
	Restrict Instructor role to only see Assessment Plans where they
	are the assigned instructor.
	"""
	if "System Manager" in frappe.get_roles(user):
		return ""

	if "Academic Head" in frappe.get_roles(user):
		return ""

	if "Instructor" in frappe.get_roles(user):
		instructor = frappe.db.get_value(
			"Instructor",
			{"email": frappe.db.get_value("User", user, "email")},
			"name",
		)
		if not instructor:
			return "1=0"

		return f"`tabAssessment Plan`.instructor = '{instructor}'"

	return "1=0"


# ---------------------------------------------------------------------------
# Examination: Bulk Marks Entry
# ---------------------------------------------------------------------------

@frappe.whitelist()
def mark_bulk_assessment_results(assessment_plan, results_data):
	"""
	Bulk-create or update Assessment Result records for a given Assessment Plan.

	Args:
	    assessment_plan: Name of the Assessment Plan
	    results_data: JSON string or list of dicts
	                 [{"student": "STU-...", "marks_obtained": 85}, ...]
	"""
	if isinstance(results_data, str):
		import json
		results_data = json.loads(results_data)

	if not results_data:
		frappe.throw(_("No results data provided."))

	if not frappe.db.exists("Assessment Plan", assessment_plan):
		frappe.throw(_("Assessment Plan '{0}' does not exist.").format(assessment_plan))

	plan = frappe.get_doc("Assessment Plan", assessment_plan)

	created = []
	updated = []
	errors = []

	for record in results_data:
		student = record.get("student")
		marks = record.get("marks_obtained")

		if not student or marks is None:
			errors.append(f"Invalid record: {record}")
			continue

		try:
			marks = int(marks)
		except (ValueError, TypeError):
			errors.append(f"Invalid marks value '{marks}' for student {student}")
			continue

		if marks < 0:
			errors.append(f"Marks cannot be negative for student {student}")
			continue

		if marks > plan.max_marks:
			errors.append(
				f"Marks ({marks}) exceed max_marks ({plan.max_marks}) for student {student}"
			)
			continue

		existing = frappe.db.get_value(
			"Assessment Result",
			{"assessment_plan": assessment_plan, "student": student},
			"name",
		)

		try:
			if existing:
				result_doc = frappe.get_doc("Assessment Result", existing)
				result_doc.marks_obtained = marks
				result_doc.save(ignore_permissions=True)
				updated.append(existing)
			else:
				result_doc = frappe.get_doc({
					"doctype": "Assessment Result",
					"assessment_plan": assessment_plan,
					"student": student,
					"marks_obtained": marks,
				})
				result_doc.insert(ignore_permissions=True)
				created.append(result_doc.name)
		except Exception as e:
			errors.append(f"Error processing student {student}: {str(e)}")

	if created or updated:
		frappe.db.commit()

	return {
		"created": len(created),
		"updated": len(updated),
		"records": created + updated,
		"errors": errors,
	}


# ---------------------------------------------------------------------------
# Fees: Permission Query Conditions
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Fees: Generate Fees from Fee Schedule
# ---------------------------------------------------------------------------

@frappe.whitelist()
def generate_fees_from_schedule(fee_schedule_name):
	"""
	Generate Fees (invoice) records from a Fee Schedule.

	For each included student in the schedule, creates one consolidated Fees record
	with all components from the linked Fee Structure. Skips students who already
	a Fees record for this exact fee_schedule (no duplicates on re-run).

	Approach: One consolidated Fees record per student (not one per component)
	because it's simpler to manage payments against a single invoice and aligns
	with how fee structures are defined (one structure = one billing event).

	Returns:
	    dict with created, skipped, errors counts and details
	"""
	if not frappe.db.exists("Fee Schedule", fee_schedule_name):
		frappe.throw(_("Fee Schedule '{0}' does not exist.").format(fee_schedule_name))

	schedule = frappe.get_doc("Fee Schedule", fee_schedule_name)
	fee_structure = frappe.get_doc("Fee Structure", schedule.fee_structure)

	if not fee_structure.components:
		frappe.throw(_("Fee Structure '{0}' has no components.").format(fee_structure.name))

	created = []
	skipped = []
	errors = []

	for student_row in schedule.applicable_students:
		if not student_row.included:
			continue

		student = student_row.student

		# Check for existing Fees for this exact schedule + student combination
		existing_fees = frappe.db.get_value(
			"Fees",
			{"fee_schedule": fee_schedule_name, "student": student},
			"name",
		)

		if existing_fees:
			skipped.append({"student": student, "fees": existing_fees})
			continue

		try:
			# Build components from the fee structure
			components = []
			for comp in fee_structure.components:
				components.append({
					"fee_category": comp.fee_category,
					"amount": comp.amount,
				})

			fees_doc = frappe.get_doc({
				"doctype": "Fees",
				"student": student,
				"fee_schedule": fee_schedule_name,
				"academic_year": fee_structure.academic_year,
				"due_date": schedule.due_date,
				"components": components,
			})
			fees_doc.insert(ignore_permissions=True)
			created.append(fees_doc.name)
		except Exception as e:
			errors.append(f"Error creating fees for student {student}: {str(e)}")

	if created:
		frappe.db.commit()

	return {
		"created": len(created),
		"skipped": len(skipped),
		"errors": len(errors),
		"records": created,
		"skipped_details": skipped,
		"error_details": errors,
	}


# ---------------------------------------------------------------------------
# Library: Permission Query Conditions
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Hostel: Permission Query Conditions
# ---------------------------------------------------------------------------

def get_permission_query_conditions_hostel(user):
	if "System Manager" in frappe.get_roles(user):
		return ""

	if "Facility Manager" in frappe.get_roles(user):
		return ""

	if "Academic Head" in frappe.get_roles(user):
		return ""

	return "1=0"


# ---------------------------------------------------------------------------
# Transport: Permission Query Conditions
# ---------------------------------------------------------------------------

def get_permission_query_conditions_transport(user):
	if "System Manager" in frappe.get_roles(user):
		return ""

	if "Facility Manager" in frappe.get_roles(user):
		return ""

	if "Academic Head" in frappe.get_roles(user):
		return ""

	return "1=0"


# ---------------------------------------------------------------------------
# Communication: Dispatch Notice (stub — no real gateway)
# ---------------------------------------------------------------------------

@frappe.whitelist()
def dispatch_notice(notice_name):
	"""
	Stub dispatch: for each recipient of a Published Notice, creates a
	Communication Log entry per available channel (Email if email exists,
	SMS if phone exists). No actual gateway is called — status is set to
	"Sent" immediately to simulate successful dispatch.

	Returns:
	    dict with logged_count and errors
	"""
	if not frappe.db.exists("Notice", notice_name):
		frappe.throw(_("Notice '{0}' does not exist.").format(notice_name))

	notice = frappe.get_doc("Notice", notice_name)
	if notice.status != "Published":
		frappe.throw(_("Notice must be Published before dispatching."))

	recipients = frappe.get_all(
		"Notice Recipient",
		filters={"notice": notice_name},
		fields=["name", "student", "recipient_type"],
	)

	logged_count = 0
	errors = []

	for rec in recipients:
		student_doc = frappe.get_doc("Student", rec.student)
		channels_logged = []

		# Email channel
		if student_doc.email_address:
			try:
				frappe.get_doc({
					"doctype": "Communication Log",
					"reference_notice": notice_name,
					"recipient_type": rec.recipient_type,
					"recipient": student_doc.email_address,
					"channel": "Email",
					"message_summary": notice.title,
					"status": "Sent",
				}).insert(ignore_permissions=True)
				channels_logged.append("Email")
			except Exception as e:
				errors.append(f"Email to {rec.student}: {str(e)}")

		# SMS channel (stub — log what WOULD be sent)
		if student_doc.phone_number:
			try:
				frappe.get_doc({
					"doctype": "Communication Log",
					"reference_notice": notice_name,
					"recipient_type": rec.recipient_type,
					"recipient": student_doc.phone_number,
					"channel": "SMS",
					"message_summary": notice.title,
					"status": "Sent",
				}).insert(ignore_permissions=True)
				channels_logged.append("SMS")
			except Exception as e:
				errors.append(f"SMS to {rec.student}: {str(e)}")

		if channels_logged:
			logged_count += 1

	if logged_count > 0:
		frappe.db.commit()

	return {
		"logged_count": logged_count,
		"errors": errors,
	}


# ---------------------------------------------------------------------------
# Portal: Helper to resolve current user to Student or Guardian
# ---------------------------------------------------------------------------

def _get_portal_student(user):
	"""Return Student name for a Student-role user, or None."""
	if "Student" not in frappe.get_roles(user):
		return None
	email = frappe.db.get_value("User", user, "email")
	return frappe.db.get_value("Student", {"email_address": email}, "name")


def _get_portal_guardian_students(user):
	"""Return list of Student names linked to a Guardian-role user."""
	if "Guardian" not in frappe.get_roles(user):
		return []
	email = frappe.db.get_value("User", user, "email")
	guardian = frappe.db.get_value("Guardian", {"guardian_email": email}, "name")
	if not guardian:
		return []
	return frappe.get_all("Student", filters={"guardian": guardian}, pluck="name")


# ---------------------------------------------------------------------------
# Portal: Permission Query Conditions for Student/Guardian roles
# ---------------------------------------------------------------------------

def get_permission_query_conditions_student(user):
	"""Students see only their own record; Guardians see their children."""
	if "System Manager" in frappe.get_roles(user):
		return ""
	if "Academic Head" in frappe.get_roles(user):
		return ""
	if "Admissions Officer" in frappe.get_roles(user):
		return ""

	student = _get_portal_student(user)
	if student:
		return f"`tabStudent`.name = '{student}'"

	guardian_students = _get_portal_guardian_students(user)
	if guardian_students:
		students_str = ", ".join([f"'{s}'" for s in guardian_students])
		return f"`tabStudent`.name in ({students_str})"

	return "1=0"


def get_permission_query_conditions_fees(user):
	"""Students/Guardians see only their own fees; staff roles see all."""
	if "System Manager" in frappe.get_roles(user):
		return ""
	if "Fee Manager" in frappe.get_roles(user):
		return ""
	if "Academic Head" in frappe.get_roles(user):
		return ""

	student = _get_portal_student(user)
	if student:
		return f"`tabFees`.student = '{student}'"

	guardian_students = _get_portal_guardian_students(user)
	if guardian_students:
		students_str = ", ".join([f"'{s}'" for s in guardian_students])
		return f"`tabFees`.student in ({students_str})"

	return "1=0"


def get_permission_query_conditions_fee_payment(user):
	"""Students/Guardians see only their own payments; staff roles see all."""
	if "System Manager" in frappe.get_roles(user):
		return ""
	if "Fee Manager" in frappe.get_roles(user):
		return ""
	if "Academic Head" in frappe.get_roles(user):
		return ""

	student = _get_portal_student(user)
	if student:
		return f"`tabFee Payment`.student = '{student}'"

	guardian_students = _get_portal_guardian_students(user)
	if guardian_students:
		students_str = ", ".join([f"'{s}'" for s in guardian_students])
		return f"`tabFee Payment`.student in ({students_str})"

	return "1=0"


def get_permission_query_conditions_student_attendance(user):
	"""Students/Guardians see only their own attendance; Instructors see their groups."""
	if "System Manager" in frappe.get_roles(user):
		return ""
	if "Academic Head" in frappe.get_roles(user):
		return ""

	student = _get_portal_student(user)
	if student:
		return f"`tabStudent Attendance`.student = '{student}'"

	guardian_students = _get_portal_guardian_students(user)
	if guardian_students:
		students_str = ", ".join([f"'{s}'" for s in guardian_students])
		return f"`tabStudent Attendance`.student in ({students_str})"

	if "Instructor" in frappe.get_roles(user):
		instructor = frappe.db.get_value(
			"Instructor",
			{"email": frappe.db.get_value("User", user, "email")},
			"name",
		)
		if not instructor:
			return "1=0"
		groups = frappe.get_all(
			"Course Schedule",
			filters={"instructor": instructor},
			pluck="student_group",
		)
		if not groups:
			return "1=0"
		groups_str = ", ".join([f"'{g}'" for g in groups])
		return f"`tabStudent Attendance`.student_group in ({groups_str})"

	return "1=0"


def get_permission_query_conditions_assessment_result(user):
	"""Students/Guardians see only their own results where results_published=1."""
	if "System Manager" in frappe.get_roles(user):
		return ""
	if "Academic Head" in frappe.get_roles(user):
		return ""

	student = _get_portal_student(user)
	guardian_students = _get_portal_guardian_students(user)
	all_portal_students = []
	if student:
		all_portal_students.append(student)
	if guardian_students:
		all_portal_students.extend(guardian_students)

	if all_portal_students:
		students_str = ", ".join([f"'{s}'" for s in all_portal_students])
		return (
			f"`tabAssessment Result`.student in ({students_str}) "
			f"AND `tabAssessment Result`.assessment_plan IN ("
			f"SELECT name FROM `tabAssessment Plan` WHERE assessment_group IN ("
			f"SELECT name FROM `tabAssessment Group` WHERE results_published = 1))"
		)

	if "Instructor" in frappe.get_roles(user):
		instructor = frappe.db.get_value(
			"Instructor",
			{"email": frappe.db.get_value("User", user, "email")},
			"name",
		)
		if not instructor:
			return "1=0"
		plans = frappe.get_all(
			"Assessment Plan",
			filters={"instructor": instructor},
			pluck="name",
		)
		if not plans:
			return "1=0"
		plans_str = ", ".join([f"'{p}'" for p in plans])
		return f"`tabAssessment Result`.assessment_plan in ({plans_str})"

	return "1=0"


def get_permission_query_conditions_notice(user):
	"""Students/Guardians see notices where they are a resolved recipient."""
	if "System Manager" in frappe.get_roles(user):
		return ""
	if "Communication Officer" in frappe.get_roles(user):
		return ""
	if "Academic Head" in frappe.get_roles(user):
		return ""

	student = _get_portal_student(user)
	guardian_students = _get_portal_guardian_students(user)
	all_portal_students = []
	if student:
		all_portal_students.append(student)
	if guardian_students:
		all_portal_students.extend(guardian_students)

	if all_portal_students:
		students_str = ", ".join([f"'{s}'" for s in all_portal_students])
		return (
			f"`tabNotice`.name IN ("
			f"SELECT notice FROM `tabNotice Recipient` "
			f"WHERE student in ({students_str}))"
		)

	return "1=0"


def get_permission_query_conditions_notice_recipient(user):
	"""Students/Guardians see only their own Notice Recipient records."""
	if "System Manager" in frappe.get_roles(user):
		return ""
	if "Communication Officer" in frappe.get_roles(user):
		return ""
	if "Academic Head" in frappe.get_roles(user):
		return ""

	student = _get_portal_student(user)
	guardian_students = _get_portal_guardian_students(user)
	all_portal_students = []
	if student:
		all_portal_students.append(student)
	if guardian_students:
		all_portal_students.extend(guardian_students)

	if all_portal_students:
		students_str = ", ".join([f"'{s}'" for s in all_portal_students])
		return f"`tabNotice Recipient`.student in ({students_str})"

	return "1=0"


def get_permission_query_conditions_feedback(user):
	"""Students/Guardians see only their own feedback; staff roles see all."""
	if "System Manager" in frappe.get_roles(user):
		return ""
	if "Communication Officer" in frappe.get_roles(user):
		return ""
	if "Academic Head" in frappe.get_roles(user):
		return ""
	if "Instructor" in frappe.get_roles(user):
		return ""

	student = _get_portal_student(user)
	guardian_students = _get_portal_guardian_students(user)
	all_portal_students = []
	if student:
		all_portal_students.append(student)
	if guardian_students:
		all_portal_students.extend(guardian_students)

	if all_portal_students:
		students_str = ", ".join([f"'{s}'" for s in all_portal_students])
		return f"`tabFeedback`.student in ({students_str})"

	return "1=0"


def get_permission_query_conditions_library_transaction(user):
	"""Students/Guardians see only their own library transactions."""
	if "System Manager" in frappe.get_roles(user):
		return ""
	if "Facility Manager" in frappe.get_roles(user):
		return ""
	if "Academic Head" in frappe.get_roles(user):
		return ""

	student = _get_portal_student(user)
	if student:
		return f"`tabLibrary Transaction`.student = '{student}'"

	guardian_students = _get_portal_guardian_students(user)
	if guardian_students:
		students_str = ", ".join([f"'{s}'" for s in guardian_students])
		return f"`tabLibrary Transaction`.student in ({students_str})"

	return "1=0"


def get_permission_query_conditions_library_item(user):
	if "System Manager" in frappe.get_roles(user):
		return ""
	if "Facility Manager" in frappe.get_roles(user):
		return ""
	if "Academic Head" in frappe.get_roles(user):
		return ""
	if "Student" in frappe.get_roles(user) or "Guardian" in frappe.get_roles(user):
		return ""  # Read-only access for portal users
	return "1=0"


def get_permission_query_conditions_library_membership(user):
	if "System Manager" in frappe.get_roles(user):
		return ""
	if "Facility Manager" in frappe.get_roles(user):
		return ""
	if "Academic Head" in frappe.get_roles(user):
		return ""

	student = _get_portal_student(user)
	if student:
		return f"`tabLibrary Membership`.student = '{student}'"

	guardian_students = _get_portal_guardian_students(user)
	if guardian_students:
		students_str = ", ".join([f"'{s}'" for s in guardian_students])
		return f"`tabLibrary Membership`.student in ({students_str})"

	return "1=0"


def get_permission_query_conditions_communication_log(user):
	"""Students/Guardians see only logs addressed to them."""
	if "System Manager" in frappe.get_roles(user):
		return ""
	if "Communication Officer" in frappe.get_roles(user):
		return ""
	if "Academic Head" in frappe.get_roles(user):
		return ""

	student = _get_portal_student(user)
	guardian_students = _get_portal_guardian_students(user)
	all_portal_students = []
	if student:
		all_portal_students.append(student)
	if guardian_students:
		all_portal_students.extend(guardian_students)

	if all_portal_students:
		students_str = ", ".join([f"'{s}'" for s in all_portal_students])
		return (
			f"`tabCommunication Log`.reference_notice IN ("
			f"SELECT notice FROM `tabNotice Recipient` "
			f"WHERE student in ({students_str}))"
		)

	return "1=0"


# ---------------------------------------------------------------------------
# Portal: User creation and User Permission setup
# ---------------------------------------------------------------------------

@frappe.whitelist()
def ensure_guardian_user(guardian_name):
	"""Create a Frappe User for a Guardian if one doesn't exist."""
	guardian = frappe.get_doc("Guardian", guardian_name)
	if not guardian.guardian_email:
		return {"created": False, "reason": "No email on Guardian record"}

	email = guardian.guardian_email
	if frappe.db.exists("User", email):
		return {"created": False, "reason": "User already exists", "user": email}

	user = frappe.get_doc({
		"doctype": "User",
		"email": email,
		"first_name": guardian.guardian_name,
		"user_type": "Website User",
		"send_welcome_email": 0,
	})
	user.append("roles", {"role": "Guardian"})
	user.insert(ignore_permissions=True)

	# Add User Permission: can read own Guardian record
	frappe.get_doc({
		"doctype": "User Permission",
		"user": email,
		"allow": "Guardian",
		"for_value": guardian_name,
	}).insert(ignore_permissions=True)

	# Add User Permissions for each linked Student
	students = frappe.get_all("Student", filters={"guardian": guardian_name}, pluck="name")
	for student_name in students:
		frappe.get_doc({
			"doctype": "User Permission",
			"user": email,
			"allow": "Student",
			"for_value": student_name,
		}).insert(ignore_permissions=True)

	frappe.db.commit()
	return {"created": True, "user": email, "students_linked": students}


@frappe.whitelist()
def ensure_all_guardian_users():
	"""Bulk-create Users for all Guardians that have email addresses."""
	guardians = frappe.get_all("Guardian", fields=["name", "guardian_email"])
	results = {"created": 0, "skipped": 0, "errors": []}
	for g in guardians:
		if not g.guardian_email:
			results["skipped"] += 1
			continue
		try:
			res = ensure_guardian_user(g.name)
			if res.get("created"):
				results["created"] += 1
		except Exception as e:
			results["errors"].append(f"{g.name}: {str(e)}")
	return results


@frappe.whitelist()
def ensure_student_user(student_name):
	"""Create a Frappe User for a Student if one doesn't exist and has email."""
	student = frappe.get_doc("Student", student_name)
	if not student.email_address:
		return {"created": False, "reason": "No email on Student record"}

	email = student.email_address
	if frappe.db.exists("User", email):
		return {"created": False, "reason": "User already exists", "user": email}

	user = frappe.get_doc({
		"doctype": "User",
		"email": email,
		"first_name": student.first_name,
		"last_name": student.last_name or "",
		"user_type": "Website User",
		"send_welcome_email": 0,
	})
	user.append("roles", {"role": "Student"})
	user.insert(ignore_permissions=True)

	# Add User Permission: can read own Student record
	frappe.get_doc({
		"doctype": "User Permission",
		"user": email,
		"allow": "Student",
		"for_value": student_name,
	}).insert(ignore_permissions=True)

	frappe.db.commit()
	return {"created": True, "user": email}


@frappe.whitelist()
def ensure_all_student_users():
	"""Bulk-create Users for all Students that have email addresses."""
	students = frappe.get_all("Student", fields=["name", "email_address"])
	results = {"created": 0, "skipped": 0, "errors": []}
	for s in students:
		if not s.email_address:
			results["skipped"] += 1
			continue
		try:
			res = ensure_student_user(s.name)
			if res.get("created"):
				results["created"] += 1
		except Exception as e:
			results["errors"].append(f"{s.name}: {str(e)}")
	return results


@frappe.whitelist()
def backfill_student_status():
	"""Set status=Active for all existing Student records missing a status."""
	frappe.db.sql(
		"UPDATE `tabStudent` SET status = 'Active' WHERE status IS NULL OR status = ''"
	)
	frappe.db.commit()
	updated = frappe.db.sql(
		"SELECT COUNT(*) FROM `tabStudent` WHERE status = 'Active'"
	)[0][0]
	return {"backfilled": updated}
