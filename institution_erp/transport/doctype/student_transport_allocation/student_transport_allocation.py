import frappe
from frappe.model.document import Document


class StudentTransportAllocation(Document):
    def validate(self):
        if self.status == "Active":
            self.validate_vehicle_capacity()
            self.validate_duplicate_active()

    def before_insert(self):
        if not self.status:
            self.status = "Active"

    def validate_vehicle_capacity(self):
        route = frappe.get_doc("Transport Route", self.transport_route)
        vehicle = frappe.get_doc("Vehicle", route.vehicle)
        active_count = frappe.db.count(
            "Student Transport Allocation",
            {
                "transport_route": self.transport_route,
                "status": "Active",
                "name": ("!=", self.name or ""),
            },
        )
        if active_count >= vehicle.capacity:
            frappe.throw(
                f"Vehicle '{vehicle.vehicle_number}' on route '{route.route_name}' "
                f"has no remaining capacity. Capacity: {vehicle.capacity}, "
                f"Currently allocated: {active_count}."
            )

    def validate_duplicate_active(self):
        existing = frappe.db.exists(
            "Student Transport Allocation",
            {
                "student": self.student,
                "transport_route": self.transport_route,
                "status": "Active",
                "name": ("!=", self.name or ""),
            },
        )
        if existing:
            frappe.throw(
                f"Student '{self.student}' is already allocated to route "
                f"'{self.transport_route}' (Active)."
            )
