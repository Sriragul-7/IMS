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
        {"fieldname": "hostel_name", "fieldtype": "Data", "label": _("Hostel"),
         "width": 200},
        {"fieldname": "hostel_type", "fieldtype": "Data", "label": _("Type"),
         "width": 100},
        {"fieldname": "total_capacity", "fieldtype": "Int", "label": _("Total Capacity"),
         "width": 130},
        {"fieldname": "occupied", "fieldtype": "Int", "label": _("Occupied"),
         "width": 100},
        {"fieldname": "vacant", "fieldtype": "Int", "label": _("Vacant"),
         "width": 100},
        {"fieldname": "occupancy_pct", "fieldtype": "Percent", "label": _("Occupancy %"),
         "width": 120},
    ]


def get_data(filters):
    conditions = ["1=1"]
    values = []
    if filters.get("hostel"):
        conditions.append("h.name = %s")
        values.append(filters.get("hostel"))

    where_clause = " AND ".join(conditions)

    hostels = frappe.db.sql(
        f"""
            SELECT h.name, h.hostel_name, h.hostel_type, h.total_capacity
            FROM `tabHostel` h
            WHERE {where_clause}
            ORDER BY h.hostel_name
        """,
        values,
        as_dict=True,
    )

    data = []
    for hostel in hostels:
        occupied = frappe.db.count(
            "Hostel Room Allocation",
            {"status": "Active"},
        )
        occupied = frappe.db.sql(
            """
                SELECT COUNT(*) FROM `tabHostel Room Allocation`hra
                JOIN `tabHostel Room` hr ON hra.hostel_room = hr.name
                WHERE hr.hostel = %s AND hra.status = 'Active'
            """,
            [hostel.name],
        )[0][0]

        capacity = hostel.total_capacity or 0
        vacant = max(capacity - occupied, 0)
        occupancy_pct = round((occupied / capacity) * 100, 1) if capacity > 0 else 0

        data.append({
            "hostel_name": hostel.hostel_name,
            "hostel_type": hostel.hostel_type,
            "total_capacity": capacity,
            "occupied": occupied,
            "vacant": vacant,
            "occupancy_pct": occupancy_pct,
        })

    return data


def get_chart_data(data):
    labels = [d["hostel_name"] for d in data]
    occupied = [d["occupied"] for d in data]
    vacant = [d["vacant"] for d in data]
    return {
        "data": {
            "labels": labels,
            "datasets": [
                {"values": occupied, "title": "Occupied"},
                {"values": vacant, "title": "Vacant"},
            ],
        },
        "type": "donut",
        "colors": ["#dc3545", "#28a745"],
    }
