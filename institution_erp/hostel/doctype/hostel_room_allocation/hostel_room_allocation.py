import frappe
from frappe.model.document import Document
from frappe.utils import today


class HostelRoomAllocation(Document):
    def validate(self):
        if self.status == "Active":
            self.validate_capacity()
            self.validate_no_duplicate_active()

    def before_insert(self):
        if not self.status:
            self.status = "Active"

    def on_update(self):
        self.recompute_occupied_count()

    def on_trash(self):
        self.recompute_occupied_count()

    def validate_capacity(self):
        room = frappe.get_doc("Hostel Room", self.hostel_room)
        occupied = room.occupied_count or 0
        if occupied >= room.capacity:
            frappe.throw(
                f"Room '{room.room_number}' in Hostel '{room.hostel}' is full. "
                f"Capacity: {room.capacity}, Currently Occupied: {occupied}."
            )

    def validate_no_duplicate_active(self):
        existing = frappe.db.exists(
            "Hostel Room Allocation",
            {
                "student": self.student,
                "status": "Active",
                "name": ("!=", self.name or ""),
            },
        )
        if existing:
            frappe.throw(
                f"Student '{self.student}' already has an Active allocation "
                f"({existing}). A student cannot have two simultaneous Active allocations."
            )

    def recompute_occupied_count(self):
        room_name = self.hostel_room
        if not room_name:
            return
        count = frappe.db.count(
            "Hostel Room Allocation",
            {"hostel_room": room_name, "status": "Active"},
        )
        frappe.db.set_value("Hostel Room", room_name, "occupied_count", count)
        frappe.db.commit()
