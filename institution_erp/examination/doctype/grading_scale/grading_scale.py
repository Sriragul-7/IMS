import frappe
from frappe.model.document import Document


class GradingScale(Document):
    def validate(self):
        self.validate_intervals()
        self.validate_no_overlap()

    def validate_intervals(self):
        if not self.intervals:
            frappe.throw("At least one Grading Interval is required.")

    def validate_no_overlap(self):
        if not self.intervals or len(self.intervals) < 2:
            return

        sorted_intervals = sorted(self.intervals, key=lambda x: x.threshold_percent or 0, reverse=True)

        for i in range(len(sorted_intervals) - 1):
            higher = sorted_intervals[i]
            lower = sorted_intervals[i + 1]
            if higher.threshold_percent == lower.threshold_percent:
                frappe.throw(
                    f"Grading Intervals '{higher.grade_code}' and '{lower.grade_code}' "
                    f"both have the same threshold ({higher.threshold_percent}%). "
                    f"Thresholds must be unique."
                )
