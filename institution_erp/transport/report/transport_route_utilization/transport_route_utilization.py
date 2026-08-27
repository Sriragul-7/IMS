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
        {"fieldname": "route_name", "fieldtype": "Data", "label": _("Route"),
         "width": 200},
        {"fieldname": "vehicle_number", "fieldtype": "Data", "label": _("Vehicle"),
         "width": 130},
        {"fieldname": "capacity", "fieldtype": "Int", "label": _("Vehicle Capacity"),
         "width": 140},
        {"fieldname": "allocated", "fieldtype": "Int", "label": _("Allocated Students"),
         "width": 150},
        {"fieldname": "remaining", "fieldtype": "Int", "label": _("Remaining"),
         "width": 100},
        {"fieldname": "utilization_pct", "fieldtype": "Percent", "label": _("Utilization %"),
         "width": 120},
        {"fieldname": "fee_amount", "fieldtype": "Currency", "label": _("Fee"),
         "width": 120},
    ]


def get_data(filters):
    conditions = ["1=1"]
    values = []
    if filters.get("transport_route"):
        conditions.append("tr.name = %s")
        values.append(filters.get("transport_route"))

    where_clause = " AND ".join(conditions)

    routes = frappe.db.sql(
        f"""
            SELECT tr.name, tr.route_name, tr.vehicle, tr.fee_amount
            FROM `tabTransport Route` tr
            WHERE {where_clause}
            ORDER BY tr.route_name
        """,
        values,
        as_dict=True,
    )

    data = []
    for route in routes:
        vehicle = frappe.get_doc("Vehicle", route.vehicle)
        allocated = frappe.db.count(
            "Student Transport Allocation",
            {"transport_route": route.name, "status": "Active"},
        )
        capacity = vehicle.capacity or 0
        remaining = max(capacity - allocated, 0)
        utilization_pct = round((allocated / capacity) * 100, 1) if capacity > 0 else 0

        data.append({
            "route_name": route.route_name,
            "vehicle_number": vehicle.vehicle_number,
            "capacity": capacity,
            "allocated": allocated,
            "remaining": remaining,
            "utilization_pct": utilization_pct,
            "fee_amount": route.fee_amount,
        })

    return data


def get_chart_data(data):
    labels = [d["route_name"] for d in data]
    allocated = [d["allocated"] for d in data]
    remaining = [d["remaining"] for d in data]
    return {
        "data": {
            "labels": labels,
            "datasets": [
                {"values": allocated, "title": "Allocated"},
                {"values": remaining, "title": "Remaining"},
            ],
        },
        "type": "donut",
        "colors": ["#007bff", "#6c757d"],
    }
