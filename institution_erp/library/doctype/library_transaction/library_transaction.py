import frappe
from frappe.model.document import Document
from frappe.utils import today, getdate, add_days

FINE_PER_DAY = 5


class LibraryTransaction(Document):
    def validate(self):
        if self.transaction_type == "Issue":
            self.validate_issue()
            self.set_due_date()
            self.status = "Issued"
        elif self.transaction_type == "Return":
            self.validate_return()
            self.status = "Returned"

    def before_insert(self):
        if self.transaction_type == "Issue":
            self.status = "Issued"
        elif self.transaction_type == "Return":
            self.status = "Returned"

    def set_due_date(self):
        if not self.due_date and self.transaction_date:
            self.due_date = add_days(getdate(self.transaction_date), 14)

    def validate_issue(self):
        item = frappe.get_doc("Library Item", self.library_item)
        if item.available_copies < 1:
            frappe.throw(
                f"No copies available for '{item.title}'. "
                f"Available: {item.available_copies}, Total: {item.total_copies}."
            )

        membership = frappe.db.get_value(
            "Library Membership",
            {"student": self.student, "status": "Active"},
            ["name", "max_books_allowed", "valid_upto"],
            as_dict=True,
        )
        if not membership:
            frappe.throw(
                f"Student '{self.student}' does not have an Active Library Membership."
            )
        if membership.valid_upto and getdate(membership.valid_upto) < getdate(today()):
            frappe.throw(
                f"Library Membership '{membership.name}' has expired "
                f"(valid up to {membership.valid_upto})."
            )

        currently_issued = frappe.db.sql(
            "SELECT COUNT(*) FROM `tabLibrary Transaction` "
            "WHERE student = %s AND library_item = %s AND transaction_type = 'Issue' "
            "AND docstatus = 1",
            [self.student, self.library_item],
        )[0][0]

        currently_returned = frappe.db.sql(
            "SELECT COUNT(*) FROM `tabLibrary Transaction` "
            "WHERE student = %s AND library_item = %s AND transaction_type = 'Return' "
            "AND docstatus = 1",
            [self.student, self.library_item],
        )[0][0]

        if currently_issued > currently_returned:
            frappe.throw(
                f"Student '{self.student}' already has an unreturned copy of '{self.library_item}'."
            )

        unreturned_items = frappe.db.sql(
            "SELECT DISTINCT lt.library_item FROM `tabLibrary Transaction` lt "
            "WHERE lt.student = %s AND lt.transaction_type = 'Issue' AND lt.docstatus = 1 "
            "AND lt.library_item NOT IN ("
            "  SELECT DISTINCT lt2.library_item FROM `tabLibrary Transaction` lt2 "
            "  WHERE lt2.transaction_type = 'Return' AND lt2.docstatus = 1 "
            "  AND lt2.student = lt.student"
            ")",
            [self.student],
        )

        unreturned = len(unreturned_items)

        if unreturned >= membership.max_books_allowed:
            frappe.throw(
                f"Student '{self.student}' already has {unreturned} unreturned book(s). "
                f"Maximum allowed: {membership.max_books_allowed}."
            )

    def validate_return(self):
        item = frappe.get_doc("Library Item", self.library_item)
        issue_txn = frappe.db.get_value(
            "Library Transaction",
            {
                "student": self.student,
                "library_item": self.library_item,
                "transaction_type": "Issue",
                "docstatus": 1,
            },
            ["name", "due_date"],
            as_dict=True,
        )
        if not issue_txn:
            frappe.throw(
                f"No open Issue transaction found for Student '{self.student}' "
                f"and Library Item '{self.library_item}'."
            )

        self.return_date = self.return_date or getdate(today())

        if issue_txn.due_date and getdate(self.return_date) > getdate(issue_txn.due_date):
            days_overdue = (getdate(self.return_date) - getdate(issue_txn.due_date)).days
            self.fine_amount = days_overdue * FINE_PER_DAY

    def on_submit(self):
        if self.transaction_type == "Issue":
            frappe.db.set_value(
                "Library Item",
                self.library_item,
                "available_copies",
                frappe.db.get_value("Library Item", self.library_item, "available_copies") - 1,
            )
            frappe.db.commit()
        elif self.transaction_type == "Return":
            frappe.db.set_value(
                "Library Item",
                self.library_item,
                "available_copies",
                frappe.db.get_value("Library Item", self.library_item, "available_copies") + 1,
            )
            if self.fine_amount and self.fine_amount > 0:
                self.create_fine_record()
            frappe.db.commit()

    def create_fine_record(self):
        fee_cat = frappe.db.get_value("Fee Category", {"category_name": "Library Fine"}, "name")
        if not fee_cat:
            fee_cat_doc = frappe.get_doc({
                "doctype": "Fee Category",
                "category_name": "Library Fine",
            })
            fee_cat_doc.insert(ignore_permissions=True)
            fee_cat = fee_cat_doc.name

        fees_doc = frappe.get_doc({
            "doctype": "Fees",
            "student": self.student,
            "academic_year": frappe.db.get_value("Academic Year", {}, "name") or "2026-2027",
            "due_date": today(),
            "components": [{
                "fee_category": fee_cat,
                "amount": self.fine_amount,
            }],
        })
        fees_doc.insert(ignore_permissions=True)
        fees_doc.submit()
        frappe.db.commit()
