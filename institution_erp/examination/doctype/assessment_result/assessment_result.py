import frappe
from frappe.model.document import Document


class AssessmentResult(Document):
    def validate(self):
        self.validate_marks()
        self.validate_no_duplicate()
        self.calculate_grade()
        self.calculate_status()

    def validate_marks(self):
        if not self.assessment_plan or self.marks_obtained is None:
            return

        plan = frappe.get_doc("Assessment Plan", self.assessment_plan)
        if self.marks_obtained > plan.max_marks:
            frappe.throw(
                f"Marks Obtained ({self.marks_obtained}) cannot exceed "
                f"Max Marks ({plan.max_marks}) for Assessment Plan '{self.assessment_plan}'."
            )

    def validate_no_duplicate(self):
        if not self.student or not self.assessment_plan:
            return

        conditions = [
            "student = %s",
            "assessment_plan = %s",
            "name != %s",
        ]
        values = [self.student, self.assessment_plan, self.name or ""]

        existing = frappe.db.sql(
            f"SELECT name FROM `tabAssessment Result` WHERE {' AND '.join(conditions)}",
            values,
            pluck="name",
        )

        if existing:
            frappe.throw(
                f"Assessment Result already exists for Student '{self.student}' "
                f"on Assessment Plan '{self.assessment_plan}'. "
                f"Please edit the existing record instead."
            )

    def calculate_grade(self):
        if not self.assessment_plan or self.marks_obtained is None:
            return

        plan = frappe.get_doc("Assessment Plan", self.assessment_plan)
        if not plan.grading_scale:
            return

        scale = frappe.get_doc("Grading Scale", plan.grading_scale)
        if not scale.intervals:
            return

        percentage = (self.marks_obtained / plan.max_marks) * 100 if plan.max_marks else 0
        self.percentage = round(percentage, 2)

        sorted_intervals = sorted(
            scale.intervals, key=lambda x: x.threshold_percent or 0, reverse=True
        )

        self.grade = ""
        for interval in sorted_intervals:
            if percentage >= (interval.threshold_percent or 0):
                self.grade = interval.grade_code
                break

        if not self.grade and sorted_intervals:
            self.grade = sorted_intervals[-1].grade_code

    def calculate_status(self):
        if not self.assessment_plan or self.marks_obtained is None:
            return

        plan = frappe.get_doc("Assessment Plan", self.assessment_plan)
        self.status = "Pass" if self.marks_obtained >= plan.passing_marks else "Fail"
