"""
Generate 6 role-based Frappe Desk Workspaces for institution_erp.
Each workspace is a JSON file synced via bench migrate.

Run: bench --site institution.localhost execute institution_erp.create_workspaces.run
"""
import json
import os
import frappe

WORKSPACES_DIR = os.path.join(
    os.path.dirname(__file__), "..", "institution_erp"
)

def _id():
    import random, string
    return "".join(random.choices(string.ascii_letters, k=10))

def _link(label, link_to, link_type="DocType", type="Link", **kwargs):
    return {
        "type": type,
        "hidden": 0,
        "is_query_report": 0,
        "label": label,
        "link_count": 0,
        "link_to": link_to,
        "link_type": link_type,
        "onboard": 0,
        **kwargs,
    }

def _card_break(label):
    return {"type": "Card Break", "label": label, "hidden": 0, "link_count": 0, "link_type": "", "onboard": 0}

def _shortcut(label, link_to, link_type="DocType", doc_view="List", color="Grey"):
    return {
        "color": color,
        "doc_view": doc_view,
        "label": label,
        "link_to": link_to,
        "stats_filter": "[]",
        "type": link_type,
    }

def _number_card(name):
    return {"number_card_name": name, "width": "Half"}

def _chart(name):
    return {"chart_name": name, "width": "Half"}

def _content_block(block_id, btype, data):
    return {"id": block_id, "type": btype, "data": data}

def _write_workspace(name, label, module, icon, links, shortcuts=None, number_cards=None, charts=None, roles=None):
    shortcuts = shortcuts or []
    number_cards = number_cards or []
    charts = charts or []
    roles = roles or []

    # Build content JSON (layout)
    content_items = []
    for sc in shortcuts:
        content_items.append(_content_block(_id(), "shortcut", {"shortcut_name": sc["label"], "col": 3}))
    content_items.append(_content_block(_id(), "spacer", {"col": 12}))

    card_groups = {}
    for link in links:
        if link["type"] == "Card Break":
            card_groups[link["label"]] = []
        else:
            last_break = None
            for l in links:
                if l["type"] == "Card Break":
                    last_break = l["label"]
                elif l == link and last_break:
                    card_groups[last_break].append(link)
                    break

    for card_name in card_groups:
        content_items.append(_content_block(_id(), "card", {"card_name": card_name, "col": 4}))

    ws = {
        "app": "institution_erp",
        "charts": charts,
        "content": json.dumps(content_items),
        "custom_blocks": [],
        "docstatus": 0,
        "doctype": "Workspace",
        "for_user": "",
        "hide_custom": 0,
        "icon": icon,
        "idx": 1,
        "is_hidden": 0,
        "label": label,
        "links": links,
        "modified": "2026-08-27 00:00:00.000000",
        "modified_by": "Administrator",
        "module": module,
        "name": name,
        "number_cards": number_cards,
        "owner": "Administrator",
        "parent_page": "",
        "public": 1,
        "quick_lists": [],
        "restrict_to_domain": "",
        "roles": roles,
        "sequence_id": 1.0,
        "shortcuts": shortcuts,
        "title": label,
        "type": "Workspace",
    }

    # Write to module directory
    ws_dir = os.path.join(WORKSPACES_DIR, module.lower().replace(" ", "_").replace("&", ""), "workspace", name.lower().replace(" ", "_").replace("&", ""))
    os.makedirs(ws_dir, exist_ok=True)
    ws_path = os.path.join(ws_dir, f"{name.lower().replace(' ', '_').replace('&', '')}.json")

    with open(ws_path, "w") as f:
        json.dump(ws, f, indent=1)

    print(f"  Created workspace: {label} -> {ws_path}")
    return ws_path


def run():
    print("=" * 60)
    print("CREATING ROLE-BASED WORKSPACES")
    print("=" * 60)

    # ─── a) Admissions workspace ─────────────────────────────────────
    print("\n[1/6] Admissions workspace...")
    _write_workspace(
        name="Admissions",
        label="Admissions",
        module="Admissions",
        icon="admissions",
        shortcuts=[
            _shortcut("Admission Inquiry", "Admission Inquiry"),
            _shortcut("Student Applicant", "Student Applicant"),
            _shortcut("New Admission Inquiry", "Admission Inquiry", doc_view="Form", color="Green"),
        ],
        number_cards=[
            _number_card("Total Active Students"),
        ],
        links=[
            _card_break("Admissions"),
            _link("Admission Inquiry", "Admission Inquiry"),
            _link("Student Applicant", "Student Applicant"),
            _link("Entrance Test", "Entrance Test"),
            _link("Entrance Test Result", "Entrance Test Result"),
            _card_break("Students"),
            _link("Student", "Student"),
            _link("Student Group", "Student Group"),
        ],
        roles=[{"role": "Admissions Officer"}, {"role": "Academic Head"}],
    )

    # ─── b) Academics workspace ──────────────────────────────────────
    print("[2/6] Academics workspace...")
    _write_workspace(
        name="Academics",
        label="Academics",
        module="Academics",
        icon="academic-cap",
        shortcuts=[
            _shortcut("Program", "Program"),
            _shortcut("Course", "Course"),
            _shortcut("Student Group", "Student Group"),
            _shortcut("Instructor", "Instructor"),
        ],
        number_cards=[
            _number_card("Total Active Students"),
        ],
        links=[
            _card_break("Academic Setup"),
            _link("Academic Year", "Academic Year"),
            _link("Academic Term", "Academic Term"),
            _link("Program", "Program"),
            _link("Course", "Course"),
            _card_break("Scheduling"),
            _link("Student Group", "Student Group"),
            _link("Course Schedule", "Course Schedule"),
            _link("Instructor", "Instructor"),
            _link("Room", "Room"),
            _card_break("Attendance & Examination"),
            _link("Student Attendance", "Student Attendance"),
            _link("Staff Attendance", "Staff Attendance"),
            _link("Assessment Plan", "Assessment Plan"),
            _link("Assessment Result", "Assessment Result"),
            _link("Grading Scale", "Grading Scale"),
        ],
        roles=[{"role": "Academic Head"}, {"role": "System Manager"}],
    )

    # ─── c) My Classes workspace (Instructor) ────────────────────────
    print("[3/6] My Classes workspace...")
    _write_workspace(
        name="My Classes",
        label="My Classes",
        module="Academics",
        icon="education",
        shortcuts=[
            _shortcut("Course Schedule", "Course Schedule"),
            _shortcut("Student Attendance", "Student Attendance"),
            _shortcut("Assessment Plan", "Assessment Plan"),
        ],
        number_cards=[],
        links=[
            _card_break("My Teaching"),
            _link("Course Schedule", "Course Schedule"),
            _link("Student Group", "Student Group"),
            _link("Student Attendance", "Student Attendance"),
            _card_break("Assessment"),
            _link("Assessment Plan", "Assessment Plan"),
            _link("Assessment Result", "Assessment Result"),
            _link("Grading Scale", "Grading Scale"),
        ],
        roles=[{"role": "Instructor"}],
    )

    # ─── d) Fees & Accounts workspace ────────────────────────────────
    print("[4/6] Fees & Accounts workspace...")
    _write_workspace(
        name="Fees & Accounts",
        label="Fees & Accounts",
        module="Fees",
        icon="currency",
        shortcuts=[
            _shortcut("Fees", "Fees"),
            _shortcut("Fee Payment", "Fee Payment"),
            _shortcut("Fee Structure", "Fee Structure"),
            _shortcut("Fee Schedule", "Fee Schedule"),
        ],
        number_cards=[
            _number_card("Total Outstanding Fees"),
        ],
        charts=[
            _chart("Fee Collection Trend"),
        ],
        links=[
            _card_break("Fee Setup"),
            _link("Fee Category", "Fee Category"),
            _link("Fee Structure", "Fee Structure"),
            _link("Fee Schedule", "Fee Schedule"),
            _card_break("Transactions"),
            _link("Fees", "Fees"),
            _link("Fee Payment", "Fee Payment"),
            _link("Fee Discount", "Fee Discount"),
            _card_break("Reports"),
            _link("Fee Dues Report", "Fee Dues Report", link_type="Report"),
        ],
        roles=[{"role": "Fee Manager"}, {"role": "System Manager"}],
    )

    # ─── e) Facilities workspace ─────────────────────────────────────
    print("[5/6] Facilities workspace...")
    _write_workspace(
        name="Facilities",
        label="Facilities",
        module="Library",
        icon="settings",
        shortcuts=[
            _shortcut("Library Item", "Library Item"),
            _shortcut("Library Transaction", "Library Transaction"),
            _shortcut("Hostel Room", "Hostel Room"),
            _shortcut("Transport Route", "Transport Route"),
        ],
        number_cards=[
            _number_card("Books Currently Issued"),
            _number_card("Hostel Occupancy (Rooms Occupied)"),
        ],
        links=[
            _card_break("Library"),
            _link("Book Category", "Book Category"),
            _link("Library Item", "Library Item"),
            _link("Library Membership", "Library Membership"),
            _link("Library Transaction", "Library Transaction"),
            _card_break("Hostel"),
            _link("Hostel", "Hostel"),
            _link("Hostel Room", "Hostel Room"),
            _link("Hostel Room Allocation", "Hostel Room Allocation"),
            _card_break("Transport"),
            _link("Vehicle", "Vehicle"),
            _link("Transport Route", "Transport Route"),
            _link("Student Transport Allocation", "Student Transport Allocation"),
            _card_break("Reports"),
            _link("Library Circulation Report", "Library Circulation Report", link_type="Report"),
            _link("Hostel Occupancy Report", "Hostel Occupancy Report", link_type="Report"),
            _link("Transport Route Utilization", "Transport Route Utilization", link_type="Report"),
        ],
        roles=[{"role": "Facility Manager"}, {"role": "System Manager"}],
    )

    # ─── f) Communication workspace ──────────────────────────────────
    print("[6/6] Communication workspace...")
    _write_workspace(
        name="Communication",
        label="Communication",
        module="Communication",
        icon="chat",
        shortcuts=[
            _shortcut("Notice", "Notice"),
            _shortcut("Feedback", "Feedback"),
            _shortcut("New Notice", "Notice", doc_view="Form", color="Green"),
        ],
        number_cards=[
            _number_card("Open Feedback/Complaints"),
        ],
        links=[
            _card_break("Communication"),
            _link("Notice", "Notice"),
            _link("Notice Recipient", "Notice Recipient"),
            _link("Feedback", "Feedback"),
            _link("Communication Log", "Communication Log"),
        ],
        roles=[{"role": "Communication Officer"}, {"role": "System Manager"}],
    )

    print(f"\nAll 6 workspaces created.")
    print("=" * 60)
