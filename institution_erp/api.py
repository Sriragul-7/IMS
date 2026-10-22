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
		return f"`tabStudent`.name = {frappe.db.escape(student)}"

	guardian_students = _get_portal_guardian_students(user)
	if guardian_students:
		students_str = ", ".join([frappe.db.escape(s) for s in guardian_students])
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
		return f"`tabFees`.student = {frappe.db.escape(student)}"

	guardian_students = _get_portal_guardian_students(user)
	if guardian_students:
		students_str = ", ".join([frappe.db.escape(s) for s in guardian_students])
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
		return f"`tabFee Payment`.student = {frappe.db.escape(student)}"

	guardian_students = _get_portal_guardian_students(user)
	if guardian_students:
		students_str = ", ".join([frappe.db.escape(s) for s in guardian_students])
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
		return f"`tabStudent Attendance`.student = {frappe.db.escape(student)}"

	guardian_students = _get_portal_guardian_students(user)
	if guardian_students:
		students_str = ", ".join([frappe.db.escape(s) for s in guardian_students])
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
		groups_str = ", ".join([frappe.db.escape(g) for g in groups])
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
		students_str = ", ".join([frappe.db.escape(s) for s in all_portal_students])
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
		plans_str = ", ".join([frappe.db.escape(p) for p in plans])
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
		students_str = ", ".join([frappe.db.escape(s) for s in all_portal_students])
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
		students_str = ", ".join([frappe.db.escape(s) for s in all_portal_students])
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
		students_str = ", ".join([frappe.db.escape(s) for s in all_portal_students])
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
		return f"`tabLibrary Transaction`.student = {frappe.db.escape(student)}"

	guardian_students = _get_portal_guardian_students(user)
	if guardian_students:
		students_str = ", ".join([frappe.db.escape(s) for s in guardian_students])
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
		return f"`tabLibrary Membership`.student = {frappe.db.escape(student)}"

	guardian_students = _get_portal_guardian_students(user)
	if guardian_students:
		students_str = ", ".join([frappe.db.escape(s) for s in guardian_students])
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
		students_str = ", ".join([frappe.db.escape(s) for s in all_portal_students])
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


# ---------------------------------------------------------------------------
# PORTAL APIs (Stage 3: Student/Guardian Portal)
# ---------------------------------------------------------------------------

def _portal_user_type():
	"""Return ('student', student_name) or ('guardian', guardian_name) or (None, None)."""
	user = frappe.session.user
	roles = frappe.get_roles(user)
	if "Student" in roles:
		perm = frappe.db.get_value("User Permission",
			{"user": user, "allow": "Student"}, "for_value")
		if perm:
			return "student", perm
	if "Guardian" in roles:
		perm = frappe.db.get_value("User Permission",
			{"user": user, "allow": "Guardian"}, "for_value")
		if perm:
			return "guardian", perm
	return None, None


def _guardian_children(guardian_name):
	"""Return list of student names linked to a Guardian via Student.guardian."""
	return [s.name for s in frappe.get_all("Student",
		filters={"guardian": guardian_name}, fields=["name"])]


def _validate_guardian_student(guardian_name, student):
	"""Ensure student belongs to this guardian."""
	children = _guardian_children(guardian_name)
	if student not in children:
		frappe.throw("Not your child", frappe.PermissionError)


@frappe.whitelist()
def portal_get_profile():
	"""Return current user's profile data (Student or Guardian)."""
	user_type, record_name = _portal_user_type()
	if not user_type:
		frappe.throw("Not a portal user", frappe.PermissionError)

	if user_type == "student":
		s = frappe.get_doc("Student", record_name)
		guardian_info = None
		if s.guardian:
			g = frappe.get_doc("Guardian", s.guardian)
			guardian_info = {
				"guardian": g.name,
				"guardian_name": g.guardian_name,
				"relation": g.relation_to_student,
			}
		full_name = " ".join(filter(None, [s.first_name, s.middle_name, s.last_name]))
		return {
			"type": "student",
			"name": s.name,
			"student_name": full_name,
			"email": s.email_address,
			"gender": s.gender,
			"date_of_birth": str(s.date_of_birth) if s.date_of_birth else "",
			"blood_group": s.blood_group or "",
			"student_category": s.category,
			"program": s.program,
			"academic_year": s.academic_year,
			"admission_number": s.admission_number,
			"status": s.status,
			"guardians": [guardian_info] if guardian_info else [],
		}
	else:
		g = frappe.get_doc("Guardian", record_name)
		children_names = _guardian_children(g.name)
		children = []
		for cname in children_names:
			st = frappe.get_doc("Student", cname)
			full_name = " ".join(filter(None, [st.first_name, st.middle_name, st.last_name]))
			children.append({
				"student": st.name,
				"student_name": full_name,
				"program": st.program,
				"status": st.status,
			})
		return {
			"type": "guardian",
			"name": g.name,
			"guardian_name": g.guardian_name,
			"email": g.guardian_email,
			"mobile_phone": g.phone_number,
			"children": children,
		}


@frappe.whitelist()
def portal_get_attendance(student=None):
	"""Return attendance records for a student (current user or specified)."""
	user_type, record_name = _portal_user_type()
	if not user_type:
		frappe.throw("Not a portal user", frappe.PermissionError)

	if user_type == "student":
		student = record_name
	elif user_type == "guardian":
		if not student:
			frappe.throw("Student parameter required for guardian", frappe.ValidationError)
		_validate_guardian_student(record_name, student)

	records = frappe.get_all(
		"Student Attendance",
		filters={"student": student},
		fields=["name", "student_group", "attendance_date", "status", "course_schedule"],
		order_by="attendance_date desc",
		page_length=100,
	)

	summary = {"Present": 0, "Absent": 0, "Late": 0, "Excused": 0}
	for r in records:
		summary[r.status] = summary.get(r.status, 0) + 1
	total = sum(summary.values())
	percentage = round((summary["Present"] / total * 100), 1) if total else 0

	return {
		"student": student,
		"records": records,
		"summary": summary,
		"total": total,
		"percentage": percentage,
	}


@frappe.whitelist()
def portal_get_results(student=None):
	"""Return assessment results for a student."""
	user_type, record_name = _portal_user_type()
	if not user_type:
		frappe.throw("Not a portal user", frappe.PermissionError)

	if user_type == "student":
		student = record_name
	elif user_type == "guardian":
		if not student:
			frappe.throw("Student parameter required for guardian", frappe.ValidationError)
		_validate_guardian_student(record_name, student)

	records = frappe.get_all(
		"Assessment Result",
		filters={"student": student},
		fields=["name", "assessment_plan", "marks_obtained", "percentage", "grade", "status", "remarks"],
		order_by="creation desc",
		page_length=100,
	)

	for r in records:
		if r.assessment_plan:
			plan = frappe.get_all(
				"Assessment Plan",
				filters={"name": r.assessment_plan},
				fields=["course", "max_marks", "passing_marks", "grading_scale", "exam_date"],
			)
			if plan:
				r.update(plan[0])

	return {"student": student, "records": records}


@frappe.whitelist()
def portal_get_fees(student=None):
	"""Return fee records for a student."""
	user_type, record_name = _portal_user_type()
	if not user_type:
		frappe.throw("Not a portal user", frappe.PermissionError)

	if user_type == "student":
		student = record_name
	elif user_type == "guardian":
		if not student:
			frappe.throw("Student parameter required for guardian", frappe.ValidationError)
		_validate_guardian_student(record_name, student)

	records = frappe.get_all(
		"Fees",
		filters={"student": student},
		fields=["name", "fee_schedule", "academic_year", "due_date", "total_amount", "discount_amount", "paid_amount", "outstanding_amount", "status"],
		order_by="creation desc",
		page_length=100,
	)

	payments = frappe.get_all(
		"Fee Payment",
		filters={"student": student},
		fields=["name", "fees", "amount", "payment_mode", "reference_number", "payment_date"],
		order_by="payment_date desc",
		page_length=100,
	)

	return {"student": student, "fees": records, "payments": payments}


@frappe.whitelist()
def portal_get_notices():
	"""Return notices visible to the current portal user."""
	user_type, record_name = _portal_user_type()
	if not user_type:
		frappe.throw("Not a portal user", frappe.PermissionError)

	filters = {"status": "Published"}

	records = frappe.get_all(
		"Notice",
		filters=filters,
		fields=["name", "title", "body", "publish_date", "audience_type", "status"],
		order_by="publish_date desc",
		page_length=50,
	)
	return {"notices": records}


@frappe.whitelist()
def portal_get_library(student=None):
	"""Return library transactions for a student."""
	user_type, record_name = _portal_user_type()
	if not user_type:
		frappe.throw("Not a portal user", frappe.PermissionError)

	if user_type == "student":
		student = record_name
	elif user_type == "guardian":
		if not student:
			frappe.throw("Student parameter required for guardian", frappe.ValidationError)
		_validate_guardian_student(record_name, student)

	active = frappe.get_all(
		"Library Transaction",
		filters={"student": student, "status": "Issued"},
		fields=["name", "library_item", "transaction_date", "due_date", "status", "fine_amount"],
		order_by="transaction_date desc",
		page_length=50,
	)

	all_txns = frappe.get_all(
		"Library Transaction",
		filters={"student": student},
		fields=["name", "library_item", "transaction_date", "due_date", "return_date", "status", "fine_amount"],
		order_by="transaction_date desc",
		page_length=100,
	)

	return {"student": student, "active_items": active, "transactions": all_txns}


@frappe.whitelist()
def portal_get_feedback(student=None):
	"""Return feedback submitted by or for a student."""
	user_type, record_name = _portal_user_type()
	if not user_type:
		frappe.throw("Not a portal user", frappe.PermissionError)

	if user_type == "student":
		student = record_name
	elif user_type == "guardian":
		if not student:
			frappe.throw("Student parameter required for guardian", frappe.ValidationError)
		_validate_guardian_student(record_name, student)

	records = frappe.get_all(
		"Feedback",
		filters={"student": student},
		fields=["name", "student", "category", "subject", "description", "raised_date", "status"],
		order_by="raised_date desc",
		page_length=50,
	)

	return {"student": student, "feedback": records}


@frappe.whitelist()
def portal_submit_feedback(student, feedback_type, subject, message):
	"""Submit feedback on behalf of a student."""
	user_type, record_name = _portal_user_type()
	if not user_type:
		frappe.throw("Not a portal user", frappe.PermissionError)

	if user_type == "guardian":
		_validate_guardian_student(record_name, student)

	feedback = frappe.get_doc({
		"doctype": "Feedback",
		"student": student,
		"category": feedback_type,
		"subject": subject,
		"description": message,
		"raised_date": frappe.utils.today(),
	})
	feedback.insert(ignore_permissions=True)
	return {"success": True, "name": feedback.name}


# ---------------------------------------------------------------------------
# STAFF PORTAL APIs (Phase 3: Staff Cockpit)
# ---------------------------------------------------------------------------

STAFF_ROLE_DOCTYPE_MAP = {
	"Instructor": "Instructor",
	"Fee Manager": "Fee Manager",
	"Facility Manager": "Facility Manager",
	"Communication Officer": "Communication Officer",
	"Admissions Officer": "Admissions Officer",
	"Academic Head": "Academic Head",
}


def _staff_user_info():
	"""Return (role, full_name) for a staff user, or (None, None)."""
	user = frappe.session.user
	roles = frappe.get_roles(user)
	for role in STAFF_ROLE_DOCTYPE_MAP:
		if role in roles:
			full_name = frappe.db.get_value("User", user, "full_name") or user
			return role, full_name
	if "System Manager" in roles:
		full_name = frappe.db.get_value("User", user, "full_name") or user
		return "System Manager", full_name
	return None, None


@frappe.whitelist()
def portal_get_staff_profile():
	"""Return staff user profile data."""
	role, full_name = _staff_user_info()
	if not role:
		frappe.throw("Not a staff user", frappe.PermissionError)
	user = frappe.session.user
	return {
		"type": "staff",
		"name": user,
		"role": role,
		"full_name": full_name,
		"email": user,
	}


@frappe.whitelist()
def portal_get_attendance_summary():
	"""Instructor: students count, groups count, today's classes, attendance marked today."""
	role, _ = _staff_user_info()
	if role not in ("Instructor", "Academic Head"):
		frappe.throw("Not authorized", frappe.PermissionError)

	total_students = frappe.db.count("Student", {"status": "Active"})
	total_groups = frappe.db.count("Student Group")

	today = frappe.utils.today()
	today_classes = []
	try:
		# Resolve User email -> Instructor name (Link field)
		instructor_name = frappe.db.get_value(
			"Instructor", {"email": frappe.session.user}, "name")
		schedules = []
		if instructor_name:
			schedules = frappe.get_all("Course Schedule",
				filters={"instructor": instructor_name},
				fields=["name", "course", "student_group", "from_time", "to_time", "day_of_week"])
		for s in schedules:
			time_slot = ""
			if s.from_time and s.to_time:
				time_slot = f"{s.from_time.strftime('%H:%M')}-{s.to_time.strftime('%H:%M')}"
			today_classes.append({
				"name": s.name,
				"course": s.course,
				"course_code": s.student_group or "",
				"time_slot": time_slot,
				"day": s.day_of_week or "",
				"status": "Upcoming",
			})
	except Exception:
		pass

	attendance_marked = frappe.db.count("Student Attendance", {
		"attendance_date": today,
	})

	return {
		"total_students": total_students,
		"total_groups": total_groups,
		"today_classes": today_classes,
		"marked_today": attendance_marked,
	}


@frappe.whitelist()
def portal_get_pending_assessments():
	"""Instructor: assessment plans that need marks entry."""
	role, _ = _staff_user_info()
	if role not in ("Instructor", "Academic Head"):
		frappe.throw("Not authorized", frappe.PermissionError)

	try:
		# Resolve User email -> Instructor name (Link field)
		instructor_name = frappe.db.get_value(
			"Instructor", {"email": frappe.session.user}, "name")
		filters = {}
		if instructor_name:
			filters["instructor"] = instructor_name
		plans = frappe.get_all("Assessment Plan",
			filters=filters,
			fields=["name", "assessment_group", "exam_date", "student_group"],
			order_by="exam_date desc",
			limit_page_length=20)
		result = []
		for p in plans:
			result.append({
				"name": p.name,
				"assessment_name": p.assessment_group or p.name,
				"due_date": str(p.exam_date) if p.exam_date else "",
			})
		return result
	except Exception:
		return []


@frappe.whitelist()
def portal_get_all_fees():
	"""Fee Manager: all fee records with student names."""
	role, _ = _staff_user_info()
	if role not in ("Fee Manager", "Academic Head", "System Manager"):
		frappe.throw("Not authorized", frappe.PermissionError)

	rows = frappe.db.sql("""
		SELECT f.name, f.student, f.fee_schedule, f.academic_year,
			   f.total_amount, f.paid_amount, f.outstanding_amount, f.status,
			   COALESCE(s.first_name, '') AS s_first,
			   COALESCE(s.middle_name, '') AS s_mid,
			   COALESCE(s.last_name, '') AS s_last
		FROM `tabFees` f
		LEFT JOIN `tabStudent` s ON s.name = f.student
		ORDER BY f.creation DESC
		LIMIT 200
	""", as_dict=True)

	for f in rows:
		f.student_name = " ".join(filter(None, [f.s_first, f.s_mid, f.s_last])) or f.student or ""
		del f.s_first
		del f.s_mid
		del f.s_last

	return {"fees": rows}


@frappe.whitelist()
def portal_get_pending_discounts():
	"""Fee Manager: fees pending discount approval."""
	role, _ = _staff_user_info()
	if role not in ("Fee Manager", "System Manager"):
		frappe.throw("Not authorized", frappe.PermissionError)

	try:
		rows = frappe.db.sql("""
			SELECT f.name, f.student, f.total_amount, f.paid_amount, f.outstanding_amount,
				   COALESCE(s.first_name, '') AS s_first,
				   COALESCE(s.middle_name, '') AS s_mid,
				   COALESCE(s.last_name, '') AS s_last
			FROM `tabFees` f
			LEFT JOIN `tabStudent` s ON s.name = f.student
			WHERE f.status = 'Partial'
			ORDER BY f.creation DESC
			LIMIT 50
		""", as_dict=True)
		for f in rows:
			f.student_name = " ".join(filter(None, [f.s_first, f.s_mid, f.s_last])) or f.student or ""
			del f.s_first
			del f.s_mid
			del f.s_last
		return rows
	except Exception:
		return []


@frappe.whitelist()
def portal_get_library_all():
	"""Facility Manager: all library data."""
	role, _ = _staff_user_info()
	if role not in ("Facility Manager", "Academic Head", "System Manager"):
		frappe.throw("Not authorized", frappe.PermissionError)

	rows = frappe.db.sql("""
		SELECT lt.name, lt.library_item, lt.student, lt.transaction_date,
			   lt.due_date, lt.status,
			   li.title AS item_title,
			   COALESCE(s.first_name, '') AS s_first,
			   COALESCE(s.middle_name, '') AS s_mid,
			   COALESCE(s.last_name, '') AS s_last
		FROM `tabLibrary Transaction` lt
		LEFT JOIN `tabLibrary Item` li ON li.name = lt.library_item
		LEFT JOIN `tabStudent` s ON s.name = lt.student
		WHERE lt.status = 'Issued'
		ORDER BY lt.due_date ASC
		LIMIT 100
	""", as_dict=True)

	for t in rows:
		t.title = t.item_title or t.library_item or ""
		t.member_name = " ".join(filter(None, [t.s_first, t.s_mid, t.s_last])) or t.student or ""
		t.member = t.student or ""
		del t.item_title
		del t.s_first
		del t.s_mid
		del t.s_last

	overdue = [t for t in rows if t.due_date and str(t.due_date) < frappe.utils.today()]

	return {"active_items": rows, "overdue_items": overdue}


@frappe.whitelist()
def portal_get_hostel_overview():
	"""Facility Manager: hostel occupancy stats."""
	role, _ = _staff_user_info()
	if role not in ("Facility Manager", "Academic Head", "System Manager"):
		frappe.throw("Not authorized", frappe.PermissionError)

	try:
		hostels = frappe.get_all("Hostel", fields=["name", "total_capacity"])
		result = []
		for h in hostels:
			rooms = frappe.get_all("Hostel Room", filters={"hostel": h.name}, fields=["name"])
			room_names = [r.name for r in rooms]
			allocated = 0
			if room_names:
				allocated = frappe.db.count("Hostel Room Allocation",
					{"hostel_room": ["in", room_names], "status": "Active"})
			total = h.total_capacity or 0
			pct = round(allocated / total * 100) if total > 0 else 0
			result.append({
				"name": h.name,
				"total": total,
				"occupied": allocated,
				"pct": pct,
			})
		return result
	except Exception:
		return []


@frappe.whitelist()
def portal_get_feedback_queue():
	"""Communication Officer: open feedback records."""
	role, _ = _staff_user_info()
	if role not in ("Communication Officer", "Academic Head", "System Manager"):
		frappe.throw("Not authorized", frappe.PermissionError)

	try:
		feedback = frappe.get_all("Feedback",
			filters={"status": ["in", ["Open", "Pending"]]},
			fields=["name", "category", "student", "subject", "status", "creation"],
			order_by="creation desc",
			limit_page_length=50)
		for f in feedback:
			f.feedback_type = f.category or "General"
		return feedback
	except Exception:
		return []


@frappe.whitelist()
def portal_get_admission_inquiries():
	"""Admissions Officer: recent student records."""
	role, _ = _staff_user_info()
	if role not in ("Admissions Officer", "Academic Head", "System Manager"):
		frappe.throw("Not authorized", frappe.PermissionError)

	try:
		rows = frappe.db.sql("""
			SELECT name, first_name, middle_name, last_name, status, creation
			FROM `tabStudent`
			ORDER BY creation DESC
			LIMIT 50
		""", as_dict=True)
		for s in rows:
			s.inquiry_name = " ".join(filter(None, [s.first_name, s.middle_name, s.last_name])) or s.name
		return rows
	except Exception:
		return []


@frappe.whitelist()
def portal_get_admission_pipeline():
	"""Admissions Officer: pipeline stats by workflow state."""
	role, _ = _staff_user_info()
	if role not in ("Admissions Officer", "Academic Head", "System Manager"):
		frappe.throw("Not authorized", frappe.PermissionError)

	try:
		rows = frappe.db.sql("""
			SELECT workflow_state, COUNT(name) AS cnt
			FROM `tabStudent Applicant`
			GROUP BY workflow_state
		""", as_dict=True)
		pipeline = {"open": 0, "applied": 0, "review": 0, "approved": 0, "rejected": 0}
		for s in rows:
			status = (s.workflow_state or "").lower()
			if "draft" in status or "open" in status:
				pipeline["open"] += s.cnt
			elif "applied" in status:
				pipeline["applied"] += s.cnt
			elif "review" in status:
				pipeline["review"] += s.cnt
			elif "approved" in status:
				pipeline["approved"] += s.cnt
			elif "rejected" in status:
				pipeline["rejected"] += s.cnt
		return pipeline
	except Exception:
		return {}


@frappe.whitelist()
def portal_get_academic_overview():
	"""Academic Head: programs, students, courses, avg attendance."""
	role, _ = _staff_user_info()
	if role not in ("Academic Head", "System Manager"):
		frappe.throw("Not authorized", frappe.PermissionError)

	programs = frappe.db.count("Program")
	students = frappe.db.count("Student", {"status": "Active"})
	courses = frappe.db.count("Course")

	today = frappe.utils.today()
	week_ago = frappe.utils.add_days(today, -7)
	try:
		total = frappe.db.count("Student Attendance", {"attendance_date": ["between", [week_ago, today]]})
		present = frappe.db.count("Student Attendance", {"attendance_date": ["between", [week_ago, today]], "status": "Present"})
		avg_att = round(present / total * 100) if total > 0 else 0
	except Exception:
		avg_att = 0

	return {
		"programs": programs,
		"students": students,
		"courses": courses,
		"avg_attendance": avg_att,
	}


@frappe.whitelist()
def portal_get_attendance_overview():
	"""Academic Head: attendance breakdown by student group."""
	role, _ = _staff_user_info()
	if role not in ("Academic Head", "System Manager"):
		frappe.throw("Not authorized", frappe.PermissionError)

	today = frappe.utils.today()
	week_ago = frappe.utils.add_days(today, -7)
	try:
		groups = frappe.get_all("Student Group", fields=["name", "group_name"])
		result = []
		for g in groups:
			total = frappe.db.count("Student Attendance", {
				"student_group": g.name,
				"attendance_date": ["between", [week_ago, today]]
			})
			present = frappe.db.count("Student Attendance", {
				"student_group": g.name,
				"attendance_date": ["between", [week_ago, today]],
				"status": "Present"
			})
			pct = round(present / total * 100) if total > 0 else 0
			result.append({
				"group": g.group_name or g.name,
				"total": total,
				"marked": present,
				"pct": pct,
			})
		return result
	except Exception:
		return []


@frappe.whitelist()
def portal_get_exam_performance():
	"""Academic Head: exam results submission status."""
	role, _ = _staff_user_info()
	if role not in ("Academic Head", "System Manager"):
		frappe.throw("Not authorized", frappe.PermissionError)

	try:
		plans = frappe.get_all("Assessment Plan",
			fields=["name", "assessment_group", "student_group"],
			order_by="exam_date desc",
			limit_page_length=20)
		result = []
		for p in plans:
			total = frappe.db.count("Assessment Result", {"assessment_plan": p.name})
			# Count non-empty grades (handles both NULL and empty string)
			submitted = frappe.db.count("Assessment Result", {
				"assessment_plan": p.name,
				"grade": ["!=", ""],
			})
			status = "Complete" if total > 0 and submitted >= total else "Pending"
			result.append({
				"assessment": p.assessment_group or p.name,
				"total": total,
				"submitted": submitted,
				"status": status,
			})
		return result
	except Exception:
		return []


@frappe.whitelist()
def portal_get_admin_overview():
	"""System Manager: institution-wide aggregate stats."""
	role, _ = _staff_user_info()
	if role != "System Manager":
		frappe.throw("Not authorized", frappe.PermissionError)

	total_students = frappe.db.count("Student", {"status": "Active"})
	total_staff = frappe.db.count("Instructor")
	total_programs = frappe.db.count("Program")
	total_courses = frappe.db.count("Course")

	# Outstanding fees
	fee_rows = frappe.db.sql("""
		SELECT COALESCE(SUM(outstanding_amount), 0) AS total_outstanding
		FROM `tabFees` WHERE status != 'Paid'
	""", as_dict=True)
	total_outstanding = fee_rows[0].total_outstanding if fee_rows else 0

	# Average attendance (last 7 days)
	today = frappe.utils.today()
	week_ago = frappe.utils.add_days(today, -7)
	try:
		total_att = frappe.db.count("Student Attendance", {"attendance_date": ["between", [week_ago, today]]})
		present_att = frappe.db.count("Student Attendance", {"attendance_date": ["between", [week_ago, today]], "status": "Present"})
		avg_att = round(present_att / total_att * 100) if total_att > 0 else 0
	except Exception:
		avg_att = 0

	# Open feedback
	open_feedback = frappe.db.count("Feedback", {"status": ["in", ["Open", "Pending"]]})

	# Library active issues
	library_active = frappe.db.count("Library Transaction", {"status": "Issued"})

	# Pipeline
	try:
		pipeline_rows = frappe.db.sql("""
			SELECT status, COUNT(name) AS cnt FROM `tabStudent` GROUP BY status
		""", as_dict=True)
		pipeline = {"active": 0, "inactive": 0}
		for pr in pipeline_rows:
			s = (pr.status or "").lower()
			if "active" in s:
				pipeline["active"] += pr.cnt
			elif "inactive" in s:
				pipeline["inactive"] += pr.cnt
	except Exception:
		pipeline = {"active": 0, "inactive": 0}

	# System stats
	total_doctypes = frappe.db.count("DocType", {"issingle": 0})
	active_users = frappe.db.count("User", {"enabled": 1, "user_type": ["!=", "Guest"]})

	return {
		"stats": {
			"total_students": total_students,
			"total_staff": total_staff,
			"avg_attendance": avg_att,
			"total_outstanding": total_outstanding,
			"total_programs": total_programs,
			"total_courses": total_courses,
			"open_feedback": open_feedback,
			"library_active": library_active,
			"total_doctypes": total_doctypes,
			"active_users": active_users,
		},
		"pipeline": pipeline,
	}
