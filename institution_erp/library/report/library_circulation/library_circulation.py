import frappe
from frappe import _
from frappe.utils import today, getdate


def execute(filters=None):
    if not filters:
        filters = {}
    columns = get_columns()
    data = get_data(filters)
    return columns, data, None, None


def get_columns():
    return [
        {"fieldname": "student", "fieldtype": "Link", "label": _("Student"),
         "options": "Student", "width": 150},
        {"fieldname": "student_name", "fieldtype": "Data", "label": _("Student Name"),
         "width": 180},
        {"fieldname": "library_item", "fieldtype": "Link", "label": _("Book"),
         "options": "Library Item", "width": 200},
        {"fieldname": "book_title", "fieldtype": "Data", "label": _("Book Title"),
         "width": 200},
        {"fieldname": "transaction_date", "fieldtype": "Date", "label": _("Issue Date"),
         "width": 120},
        {"fieldname": "due_date", "fieldtype": "Date", "label": _("Due Date"),
         "width": 120},
        {"fieldname": "return_date", "fieldtype": "Date", "label": _("Return Date"),
         "width": 120},
        {"fieldname": "days_overdue", "fieldtype": "Int", "label": _("Days Overdue"),
         "width": 120},
        {"fieldname": "fine_amount", "fieldtype": "Currency", "label": _("Fine"),
         "width": 120},
        {"fieldname": "status", "fieldtype": "Data", "label": _("Status"),
         "width": 100},
    ]


def get_data(filters):
    conditions = ["lt.transaction_type = 'Issue'"]
    values = []

    if filters.get("status"):
        conditions.append("lt.status = %s")
        values.append(filters.get("status"))
    if filters.get("student"):
        conditions.append("lt.student = %s")
        values.append(filters.get("student"))

    where_clause = " AND ".join(conditions)

    sql = f"""
        SELECT
            lt.student,
            lt.library_item,
            lt.transaction_date,
            lt.due_date,
            lt.return_date,
            lt.fine_amount,
            lt.status
        FROM `tabLibrary Transaction` lt
        WHERE {where_clause}
        ORDER BY lt.transaction_date DESC
    """
    rows = frappe.db.sql(sql, values, as_dict=True)

    data = []
    for row in rows:
        student_name = frappe.db.get_value("Student", row.student, "first_name") or ""
        student_last = frappe.db.get_value("Student", row.student, "last_name") or ""
        if student_last:
            student_name = f"{student_name} {student_last}".strip()
        book_title = frappe.db.get_value("Library Item", row.library_item, "title") or ""
        days_overdue = 0
        if row.return_date and row.due_date:
            delta = getdate(row.return_date) - getdate(row.due_date)
            if delta.days > 0:
                days_overdue = delta.days
        elif row.status == "Issued" and row.due_date:
            delta = getdate(today()) - getdate(row.due_date)
            if delta.days > 0:
                days_overdue = delta.days

        data.append({
            "student": row.student,
            "student_name": student_name,
            "library_item": row.library_item,
            "book_title": book_title,
            "transaction_date": row.transaction_date,
            "due_date": row.due_date,
            "return_date": row.return_date,
            "days_overdue": days_overdue,
            "fine_amount": row.fine_amount,
            "status": row.status,
        })

    return data
