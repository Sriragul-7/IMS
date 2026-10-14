#!/usr/bin/env python3
"""
Generate real diagrams using matplotlib and PIL.
No system graphviz required.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
import numpy as np
from pathlib import Path
import os

IMAGES_DIR = Path(__file__).parent.parent / "images"
IMAGES_DIR.mkdir(exist_ok=True)

# Color palette
BIT_BLUE = '#1e40af'
BIT_LIGHT = '#dbeafe'
GREEN = '#10b981'
GREEN_LIGHT = '#dcfce7'
AMBER = '#f59e0b'
AMBER_LIGHT = '#fef3c7'
RED = '#ef4444'
RED_LIGHT = '#fee2e2'
PURPLE = '#8b5cf6'
PURPLE_LIGHT = '#ede9fe'
GRAY = '#64748b'
GRAY_LIGHT = '#f0f4f8'
WHITE = '#ffffff'
DARK = '#1e293b'

def save_fig(fig, name, dpi=300):
    path = IMAGES_DIR / f"{name}.png"
    fig.savefig(path, dpi=dpi, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"Generated: {path}")
    return path

def add_box(ax, x, y, w, h, text, fc=WHITE, ec=GRAY, fs=9, bold=False, round_pad=0.05, shape='round'):
    """Add a rectangle with text. shape: 'round', 'rect', 'cylinder'"""
    if shape == 'cylinder':
        # Draw cylinder as ellipse top + rectangle + ellipse bottom
        # Top ellipse
        from matplotlib.patches import Ellipse
        top = Ellipse((x + w/2, y + h), w, h * 0.15, facecolor=fc, edgecolor=ec, linewidth=1.5)
        ax.add_patch(top)
        # Body
        body = Rectangle((x, y + h * 0.075), w, h * 0.85, facecolor=fc, edgecolor=ec, linewidth=1.5, fill=True)
        ax.add_patch(body)
        # Bottom ellipse (just edge)
        bottom = Ellipse((x + w/2, y), w, h * 0.15, facecolor='none', edgecolor=ec, linewidth=1.5)
        ax.add_patch(bottom)
        # Text centered in body
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=fs, 
                fontweight='bold' if bold else 'normal', wrap=True, family='DejaVu Sans')
    else:
        box = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad={round_pad}", 
                              facecolor=fc, edgecolor=ec, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=fs, 
                fontweight='bold' if bold else 'normal', wrap=True, family='DejaVu Sans')
    return (x, y, w, h)

def add_arrow(ax, x1, y1, x2, y2, label="", fs=8, color=GRAY, dir='forward', style='solid'):
    """Add an arrow with optional label. dir: 'forward', 'both'. style: 'solid', 'dashed'"""
    conn_style = "arc3,rad=0.0"
    if style == 'dashed':
        arrow = FancyArrowPatch((x1, y1), (x2, y2), 
                                arrowstyle='->', mutation_scale=15,
                                linewidth=1.2, color=color,
                                connectionstyle=conn_style, linestyle='dashed')
        ax.add_patch(arrow)
        if dir == 'both':
            arrow2 = FancyArrowPatch((x2, y2), (x1, y1), 
                                    arrowstyle='->', mutation_scale=15,
                                    linewidth=1.2, color=color,
                                    connectionstyle=conn_style, linestyle='dashed')
            ax.add_patch(arrow2)
    else:
        if dir == 'both':
            arrow1 = FancyArrowPatch((x1, y1), (x2, y2), 
                                    arrowstyle='->', mutation_scale=15,
                                    linewidth=1.2, color=color,
                                    connectionstyle=conn_style)
            arrow2 = FancyArrowPatch((x2, y2), (x1, y1), 
                                    arrowstyle='->', mutation_scale=15,
                                    linewidth=1.2, color=color,
                                    connectionstyle=conn_style)
            ax.add_patch(arrow1)
            ax.add_patch(arrow2)
        else:
            arrow = FancyArrowPatch((x1, y1), (x2, y2), 
                                    arrowstyle='->', mutation_scale=15,
                                    linewidth=1.2, color=color,
                                    connectionstyle=conn_style)
            ax.add_patch(arrow)
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my + 0.02, label, ha='center', va='bottom', fontsize=fs, color=color, family='DejaVu Sans')

# ============================================================
# Figure 3.1: Technology Stack Diagram
# ============================================================
fig, ax = plt.subplots(figsize=(11, 8.5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Layer labels
layers = [
    (0.5, 9.2, "Presentation Layer", BIT_LIGHT),
    (0.5, 6.8, "API Layer", GREEN_LIGHT),
    (0.5, 4.4, "Business Logic Layer", PURPLE_LIGHT),
    (0.5, 1.8, "Data Layer", AMBER_LIGHT),
]

for x, y, label, fc in layers:
    box = FancyBboxPatch((x, y), 9, 0.4, boxstyle="round,pad=0.03", facecolor=fc, edgecolor=GRAY, linewidth=1)
    ax.add_patch(box)
    ax.text(x + 0.3, y + 0.2, label, ha='left', va='center', fontsize=11, fontweight='bold', color=DARK)

# Presentation Layer components
pres_items = [
    (1, 8.3, "Vue 3 SPA\n(Student/Guardian Portal)", BIT_LIGHT),
    (4, 8.3, "Vue 3 Cockpits\n(7 Staff Roles)", BIT_LIGHT),
    (7, 8.3, "Frappe Desk\n(Rebranded: Inter + BIT Blue)", AMBER_LIGHT),
]
for x, y, text, fc in pres_items:
    add_box(ax, x, y, 2.5, 1.2, text, fc=fc, ec=BIT_BLUE, fs=9)

# API Layer
api_items = [
    (2, 5.9, "11 Whitelisted Methods\n(frappe.call / REST)", GREEN_LIGHT),
    (6, 5.9, "Frappe REST API\n(DocType CRUD)", GREEN_LIGHT),
]
for x, y, text, fc in api_items:
    add_box(ax, x, y, 3, 1.2, text, fc=fc, ec=GREEN, fs=9)

# Business Logic Layer
logic_items = [
    (0.8, 3.5, "DocType Controllers\n(22 files, validation)", PURPLE_LIGHT),
    (3.3, 3.5, "Hooks & Events\n(on_update, on_submit)", PURPLE_LIGHT),
    (5.8, 3.5, "16 permission_query_conditions\n(Row-level Security)", PURPLE_LIGHT),
    (8.3, 3.5, "Workflow Engine\n(Student Applicant, Fee Discount)", PURPLE_LIGHT),
]
for x, y, text, fc in logic_items:
    add_box(ax, x, y, 2.2, 1.2, text, fc=fc, ec=PURPLE, fs=8)

# Data Layer
data_items = [
    (2, 0.9, "MariaDB 10.6+\n(48 DocTypes, 8 Child Tables)", AMBER_LIGHT),
    (6, 0.9, "Redis 7+\n(Caching, Sessions, Queues)", AMBER_LIGHT),
]
for x, y, text, fc in data_items:
    add_box(ax, x, y, 3, 1.2, text, fc=fc, ec=AMBER, fs=9)

# Arrows between layers
# Pres -> API
add_arrow(ax, 2.25, 8.3, 3.5, 7.1, "")
add_arrow(ax, 5.25, 8.3, 6.5, 7.1, "")
add_arrow(ax, 8.25, 8.3, 7.5, 7.1, "")

# API -> Logic
add_arrow(ax, 3.5, 5.9, 2.4, 4.7, "")
add_arrow(ax, 7.5, 5.9, 6.9, 4.7, "")

# Logic -> Data
add_arrow(ax, 1.9, 3.5, 3.5, 2.1, "")
add_arrow(ax, 4.4, 3.5, 3.5, 2.1, "")
add_arrow(ax, 6.9, 3.5, 5.5, 2.1, "")
add_arrow(ax, 9.4, 3.5, 7.5, 2.1, "")

ax.set_title("Figure 3.1 — Technology Stack Diagram", fontsize=13, fontweight='bold', pad=15)
save_fig(fig, "fig3_1_tech_stack")

# ============================================================
# Figure 4.1: System Architecture Diagram (Layered)
# ============================================================
fig, ax = plt.subplots(figsize=(11, 8.5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Users (left)
users = [
    (0.3, 8.8, "Student", BIT_LIGHT),
    (0.3, 7.8, "Guardian", BIT_LIGHT),
    (0.3, 6.8, "Instructor", AMBER_LIGHT),
    (0.3, 5.8, "Admissions", AMBER_LIGHT),
    (0.3, 4.8, "Fee Manager", AMBER_LIGHT),
    (0.3, 3.8, "Facility Mgr", AMBER_LIGHT),
    (0.3, 2.8, "Comm Officer", AMBER_LIGHT),
    (0.3, 1.8, "Academic Head", AMBER_LIGHT),
    (0.3, 0.8, "System Mgr", PURPLE_LIGHT),
]
for x, y, text, fc in users:
    add_box(ax, x, y, 1.8, 0.7, text, fc=fc, ec=GRAY, fs=9, bold=True)

# Frontend (center-left)
fe_items = [
    (2.8, 5.5, "Vue 3 Portal SPA\n/institution-portal", BIT_LIGHT),
    (2.8, 3.5, "Vue 3 Staff Cockpits\n/institution-portal/<role>", AMBER_LIGHT),
    (2.8, 1.5, "Frappe Desk (Rebranded)\n/app", PURPLE_LIGHT),
]
for x, y, text, fc in fe_items:
    add_box(ax, x, y, 2.5, 1.2, text, fc=fc, ec=GRAY, fs=9)

# Backend (center-right)
be_items = [
    (6.5, 7.5, "Authentication\nJWT + Session", PURPLE_LIGHT),
    (6.5, 5.5, "Whitelisted API\n(11 methods)", GREEN_LIGHT),
    (6.5, 3.5, "DocType Controllers\n(Validation, Hooks)", PURPLE_LIGHT),
    (6.5, 1.5, "permission_query_conditions\n(16 functions)", PURPLE_LIGHT),
]
for x, y, text, fc in be_items:
    add_box(ax, x, y, 2.5, 1.2, text, fc=fc, ec=GRAY, fs=9)

# Database (right)
db_items = [
    (9.5, 5.5, "MariaDB\n48 DocTypes", AMBER_LIGHT),
    (9.5, 2.5, "Redis\nCache/Queue/Session", AMBER_LIGHT),
]
for x, y, text, fc in db_items:
    add_box(ax, x, y, 2.5, 1.2, text, fc=fc, ec=AMBER, fs=9, shape='cylinder')

# Arrows
# Users -> Frontend
for _, y, _, _ in users[:2]:  # Student, Guardian
    add_arrow(ax, 2.1, y + 0.35, 2.8, 6.1, "")
for _, y, _, _ in users[2:]:  # Staff
    add_arrow(ax, 2.1, y + 0.35, 2.8, 4.1, "")

# Cockpit -> Desk (dashed)
add_arrow(ax, 4.1, 4.1, 4.1, 2.1, "Open Full Desk", color=GRAY)

# Frontend -> Auth
add_arrow(ax, 4.1, 5.5, 5.3, 7.5, "")
add_arrow(ax, 4.1, 4.1, 5.3, 5.5, "")
add_arrow(ax, 4.1, 2.1, 5.3, 3.5, "")

# Frontend -> API
add_arrow(ax, 5.3, 5.5, 6.5, 5.5, "")
add_arrow(ax, 5.3, 4.1, 6.5, 5.5, "")
add_arrow(ax, 5.3, 2.1, 6.5, 3.5, "REST/Desk API")

# Backend internal
add_arrow(ax, 7.8, 7.5, 7.8, 6.1, "")
add_arrow(ax, 7.8, 5.5, 7.8, 4.1, "")
add_arrow(ax, 7.8, 3.5, 7.8, 2.1, "")

# Backend -> DB
add_arrow(ax, 9.0, 7.5, 9.5, 6.1, "")
add_arrow(ax, 9.0, 5.5, 9.5, 6.1, "")
add_arrow(ax, 9.0, 3.5, 9.5, 6.1, "")
add_arrow(ax, 9.0, 1.5, 9.5, 3.1, "")
add_arrow(ax, 9.0, 3.5, 9.5, 3.1, "")

ax.set_title("Figure 4.1 — System Architecture Diagram", fontsize=13, fontweight='bold', pad=15)
save_fig(fig, "fig4_1_sys_arch")

# ============================================================
# Figure 4.2: Module Dependency Graph
# ============================================================
fig, ax = plt.subplots(figsize=(11, 6))
ax.set_xlim(0, 11)
ax.set_ylim(0, 6)
ax.axis('off')

modules = {
    "Academics\n(10)": (2, 4.5, BIT_LIGHT, BIT_BLUE),
    "SIS\n(2)": (5, 4.5, GREEN_LIGHT, GREEN),
    "Admissions\n(5)": (8, 4.5, AMBER_LIGHT, AMBER),
    "Attendance\n(2)": (2, 2.5, PURPLE_LIGHT, PURPLE),
    "Examination\n(5)": (5, 2.5, PURPLE_LIGHT, PURPLE),
    "Fees\n(9)": (8, 2.5, RED_LIGHT, RED),
    "Library\n(4)": (2, 0.5, GREEN_LIGHT, GREEN),
    "Hostel\n(3)": (5, 0.5, AMBER_LIGHT, AMBER),
    "Transport\n(4)": (8, 0.5, PURPLE_LIGHT, PURPLE),
    "Communication\n(4)": (10.5, 2.5, PURPLE_LIGHT, PURPLE),
}

boxes = {}
for name, (x, y, fc, ec) in modules.items():
    add_box(ax, x, y, 2.2, 1.5, name, fc=fc, ec=ec, fs=9)
    boxes[name.split('\n')[0]] = (x + 1.1, y + 0.75)

# Dependencies (arrows)
deps = [
    ("SIS", "Academics", "Student Group Member"),
    ("Admissions", "Academics", "Program, Academic Year"),
    ("Admissions", "SIS", "Creates Student+Guardian"),
    ("Attendance", "Academics", "Course Schedule, Group"),
    ("Attendance", "SIS", "Student, Instructor"),
    ("Examination", "Academics", "Course, Group, Grading Scale"),
    ("Fees", "SIS", "Student"),
    ("Fees", "Academics", "Acad Year, Student Group"),
    ("Library", "SIS", "Student"),
    ("Hostel", "SIS", "Student"),
    ("Transport", "SIS", "Student"),
    ("Communication", "SIS", "Student, Guardian"),
    ("Communication", "Academics", "Student Group, Program"),
]

for src, dst, label in deps:
    if src in boxes and dst in boxes:
        x1, y1 = boxes[src]
        x2, y2 = boxes[dst]
        # Determine direction
        if x1 < x2:
            add_arrow(ax, x1 + 1.1, y1, x2 - 1.1, y2, label, fs=7)
        elif x1 > x2:
            add_arrow(ax, x1 - 1.1, y1, x2 + 1.1, y2, label, fs=7)
        else:
            add_arrow(ax, x1, y1 - 0.75, x2, y2 + 0.75, label, fs=7)

ax.set_title("Figure 4.2 — Module Dependency Graph", fontsize=13, fontweight='bold', pad=15)
save_fig(fig, "fig4_2_module_dep")

# ============================================================
# Figure 4.3: Role-Permission Matrix (simplified table visualization)
# ============================================================
fig, ax = plt.subplots(figsize=(12, 5))
ax.set_xlim(0, 12)
ax.set_ylim(0, 5)
ax.axis('off')

roles = ["Student", "Guardian", "Admissions", "Academic\nHead", "Instructor", "Fee Mgr", "Facility", "Comm", "Sys Mgr"]
entities = ["Student", "Guardian", "Admissions", "Academics", "Exam", "Fees", "Facilities", "Comm"]

# Colors
FULL = GREEN_LIGHT
READ = AMBER_LIGHT
NONE = RED_LIGHT
HEADER = BIT_BLUE

# Header row
for j, role in enumerate(roles):
    x = 1.5 + j * 1.05
    add_box(ax, x, 4.2, 1.0, 0.5, role, fc=HEADER, ec=HEADER, fs=8, bold=True)
    # White text for header
    for patch in ax.patches:
        if isinstance(patch, FancyBboxPatch) and patch.get_facecolor()[:3] == tuple(int(HEADER.lstrip('#')[i:i+2], 16)/255 for i in (0,2,4)):
            pass  # handled by text color

# Entity rows
matrix = {
    "Student":      [FULL, NONE, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
    "Guardian":     [FULL, FULL, NONE, NONE, NONE, NONE, NONE, NONE, NONE],
    "Admissions":   [NONE, NONE, FULL, READ, NONE, NONE, NONE, NONE, FULL],
    "Academic\nHead": [READ, READ, READ, FULL, FULL, READ, READ, READ, FULL],
    "Instructor":   [NONE, NONE, NONE, READ, FULL, NONE, NONE, NONE, FULL],
    "Fee Mgr":      [NONE, NONE, NONE, NONE, NONE, FULL, NONE, NONE, FULL],
    "Facility":     [NONE, NONE, NONE, NONE, NONE, NONE, FULL, FULL, FULL],
    "Comm":         [NONE, NONE, NONE, NONE, NONE, NONE, NONE, FULL, FULL],
}

for i, (entity, row) in enumerate(matrix.items()):
    y = 3.5 - i * 0.4
    # Entity name
    add_box(ax, 0.3, y, 1.1, 0.35, entity, fc=GRAY_LIGHT, ec=GRAY, fs=8, bold=True)
    for j, color in enumerate(row):
        x = 1.5 + j * 1.05
        txt = "Full" if color == FULL else ("Read" if color == READ else "—")
        add_box(ax, x, y, 1.0, 0.35, txt, fc=color, ec=GRAY, fs=7, bold=(color==FULL))

# Legend
add_box(ax, 0.3, 0.2, 1.5, 0.3, "Full / Own / Linked", fc=FULL, ec=GRAY, fs=8)
add_box(ax, 2.0, 0.2, 1.5, 0.3, "Read Only", fc=READ, ec=GRAY, fs=8)
add_box(ax, 3.7, 0.2, 1.5, 0.3, "No Access", fc=NONE, ec=GRAY, fs=8)

ax.set_title("Figure 4.3 — Role-Permission Matrix (Write Access)", fontsize=13, fontweight='bold', pad=15)
save_fig(fig, "fig4_3_role_matrix")

# ============================================================
# Figure 4.4: ER Diagram (simplified key entities)
# ============================================================
fig, ax = plt.subplots(figsize=(14, 9))
ax.set_xlim(0, 14)
ax.set_ylim(0, 9)
ax.axis('off')

# Define entities with positions
entities_er = {
    # Core
    "Student": (1, 7, BIT_LIGHT, BIT_BLUE, "Student\nSTU-.YYYY.-.#####\nfirst_name, last_name\nprogram, guardian\nemail, status"),
    "Guardian": (1, 5, BIT_LIGHT, BIT_BLUE, "Guardian\n{name}-{###}\nguardian_name, email\nrelation, phone"),
    "Program": (4, 8, GREEN_LIGHT, GREEN, "Program\nfield:program_name\nprogram_code, dept"),
    "Course": (6, 8, GREEN_LIGHT, GREEN, "Course\nfield:course_name\ncourse_code, credits\ncourse_type"),
    "Academic Year": (8, 8, GREEN_LIGHT, GREEN, "Academic Year\nfield:academic_year_name\nyear_start, year_end"),
    "Academic Term": (10, 8, GREEN_LIGHT, GREEN, "Academic Term\nfield:term_name\nacademic_year, dates"),
    "Student Group": (12, 7, GREEN_LIGHT, GREEN, "Student Group\nfield:group_name\nprogram, acad_year\ncourse, max_strength"),
    "Course Schedule": (12, 5, AMBER_LIGHT, AMBER, "Course Schedule\nhash\ncourse, group, instructor\nroom, day, time"),
    "Instructor": (10, 5, AMBER_LIGHT, AMBER, "Instructor\nINST-.####\nname, employee_id\ndept, email, status"),
    "Room": (8, 5, AMBER_LIGHT, AMBER, "Room\nfield:room_name\nbuilding, floor\ncapacity, type"),
    # Admissions
    "Adm Inquiry": (1, 2.5, PURPLE_LIGHT, PURPLE, "Admission Inquiry\nADM-INQ-.YYYY.-.####\nname, program, status"),
    "Stu Applicant": (3.5, 2.5, PURPLE_LIGHT, PURPLE, "Student Applicant\nSTU-APP-.YYYY.-.####\nworkflow_state\ncreated_student"),
    "Entrance Test": (6, 2.5, PURPLE_LIGHT, PURPLE, "Entrance Test\nfield:test_name\ndate, max/passing"),
    "Test Result": (8.5, 2.5, PURPLE_LIGHT, PURPLE, "Test Result\nhash\ntest, applicant\nmarks, result"),
    # Examination
    "Grading Scale": (1, 0.5, RED_LIGHT, RED, "Grading Scale\nfield:scale_name\nintervals"),
    "Assess Group": (3.5, 0.5, RED_LIGHT, RED, "Assessment Group\nfield:group_name\nacad_term, published\nweightage"),
    "Assess Plan": (6, 0.5, RED_LIGHT, RED, "Assessment Plan\nhash\ngroup, course, group\nmax, passing, scale"),
    "Assess Result": (8.5, 0.5, RED_LIGHT, RED, "Assessment Result\nhash\nplan, student\nmarks, grade, %"),
}

boxes_er = {}
for name, (x, y, fc, ec, text) in entities_er.items():
    add_box(ax, x, y, 2.2, 1.4, text, fc=fc, ec=ec, fs=7)
    boxes_er[name] = (x + 1.1, y + 0.7)

# Key relationships
relationships = [
    ("Student", "Guardian", "guardian"),
    ("Student", "Program", "program"),
    ("Program", "Course", "courses"),
    ("Academic Year", "Academic Term", "terms"),
    ("Academic Year", "Student Group", "groups"),
    ("Program", "Student Group", "program"),
    ("Course", "Student Group", "course"),
    ("Course Schedule", "Course", "course"),
    ("Course Schedule", "Student Group", "student_group"),
    ("Course Schedule", "Instructor", "instructor"),
    ("Course Schedule", "Room", "room"),
    ("Student Group", "Student", "members"),
    ("Adm Inquiry", "Stu Applicant", "converts"),
    ("Stu Applicant", "Student", "creates on approve"),
    ("Stu Applicant", "Guardian", "creates on approve"),
    ("Stu Applicant", "Entrance Test", "takes"),
    ("Entrance Test", "Test Result", "results"),
    ("Stu Applicant", "Test Result", "applicant"),
    ("Grading Scale", "Assess Group", "used by"),
    ("Assess Group", "Assess Plan", "plans"),
    ("Course", "Assess Plan", "course"),
    ("Student Group", "Assess Plan", "group"),
    ("Assess Plan", "Assess Result", "results"),
    ("Student", "Assess Result", "student"),
]

for src, dst, label in relationships:
    if src in boxes_er and dst in boxes_er:
        x1, y1 = boxes_er[src]
        x2, y2 = boxes_er[dst]
        add_arrow(ax, x1, y1, x2, y2, label, fs=6, color=GRAY)

ax.set_title("Figure 4.4 — Entity-Relationship Diagram (Key Entities)", fontsize=13, fontweight='bold', pad=15)
save_fig(fig, "fig4_4_er_diagram")

# ============================================================
# Figure 4.5: DFD Level 0
# ============================================================
fig, ax = plt.subplots(figsize=(11, 7))
ax.set_xlim(0, 11)
ax.set_ylim(0, 7)
ax.axis('off')

# External entities (left)
ext_left = [
    (0.5, 6.0, "Student", BIT_LIGHT),
    (0.5, 5.0, "Guardian", BIT_LIGHT),
    (0.5, 4.0, "Instructor", AMBER_LIGHT),
    (0.5, 3.0, "Admissions", AMBER_LIGHT),
    (0.5, 2.0, "Fee Manager", AMBER_LIGHT),
    (0.5, 1.0, "Facility Mgr", AMBER_LIGHT),
]
for x, y, text, fc in ext_left:
    add_box(ax, x, y, 1.8, 0.6, text, fc=fc, ec=GRAY, fs=9, shape='oval')

ext_right = [
    (8.7, 3.5, "Comm Officer", AMBER_LIGHT),
    (8.7, 2.5, "Academic Head", AMBER_LIGHT),
    (8.7, 1.5, "Sys Manager", PURPLE_LIGHT),
]
for x, y, text, fc in ext_right:
    add_box(ax, x, y, 1.8, 0.6, text, fc=fc, ec=GRAY, fs=9, shape='oval')

# Central process
add_box(ax, 3.5, 2.5, 4, 3, "Institution ERP\n(Process 0)", fc=BIT_BLUE, ec=BIT_BLUE, fs=14, bold=True)

# Database
add_box(ax, 3.5, 0.2, 4, 1, "MariaDB\n(48 DocTypes)", fc=AMBER_LIGHT, ec=AMBER, fs=11, shape='cylinder')

# Flows
for _, y, _, _ in ext_left:
    add_arrow(ax, 2.3, y + 0.3, 3.5, 4.0, "", color=BIT_BLUE)
for _, y, _, _ in ext_right:
    add_arrow(ax, 7.7, y + 0.3, 7.5, 4.0, "", color=BIT_BLUE)

add_arrow(ax, 5.5, 2.5, 5.5, 1.2, "", color=AMBER, dir='both')

ax.set_title("Figure 4.5 — DFD Level 0 (Context Diagram)", fontsize=13, fontweight='bold', pad=15)
save_fig(fig, "fig4_5_dfd_l0")

# ============================================================
# Figure 4.6: DFD Level 1
# ============================================================
fig, ax = plt.subplots(figsize=(13, 8))
ax.set_xlim(0, 13)
ax.set_ylim(0, 8)
ax.axis('off')

# External
ext = {
    "Student": (0.5, 6.5, BIT_LIGHT),
    "Guardian": (0.5, 5.5, BIT_LIGHT),
    "Staff": (0.5, 4.5, AMBER_LIGHT),
}

for name, (x, y, fc) in ext.items():
    add_box(ax, x, y, 1.5, 0.6, name, fc=fc, ec=GRAY, fs=9, shape='oval')

# Processes
processes = {
    "1. Admissions": (2.5, 6.5, PURPLE_LIGHT, PURPLE),
    "2. Academics": (2.5, 5.0, BIT_LIGHT, BIT_BLUE),
    "3. Fees": (2.5, 3.5, RED_LIGHT, RED),
    "4. Facilities": (2.5, 2.0, GREEN_LIGHT, GREEN),
    "5. Communication": (2.5, 0.5, PURPLE_LIGHT, PURPLE),
    "6. Examination": (6.5, 6.5, AMBER_LIGHT, AMBER),
    "7. Attendance": (6.5, 5.0, AMBER_LIGHT, AMBER),
    "8. Portal Access": (6.5, 3.5, BIT_LIGHT, BIT_BLUE),
}

proc_pos = {}
for name, (x, y, fc, ec) in processes.items():
    add_box(ax, x, y, 3, 1.0, name, fc=fc, ec=ec, fs=8)
    proc_pos[name] = (x + 1.5, y + 0.5)

# Data stores
datastores = {
    "D1: Student &\nGuardian Master": (10.5, 6.5),
    "D2: Academic\nStructure": (10.5, 5.5),
    "D3: Fees &\nPayments": (10.5, 4.5),
    "D4: Assessment\n& Results": (10.5, 3.5),
    "D5: Attendance\nRecords": (10.5, 2.5),
    "D6: Facilities\n(Lib/Hostel/Trans)": (10.5, 1.5),
    "D7: Communication\n(Notices/Feedback)": (10.5, 0.5),
    "D8: Admissions\nPipeline": (6.5, 0.5),
}

for name, (x, y) in datastores.items():
    add_box(ax, x, y, 2.2, 0.7, name, fc=AMBER_LIGHT, ec=AMBER, fs=7, shape='cylinder')

# Flows (simplified - just key ones)
flows = [
    ("Student", "1. Admissions", ""),
    ("Staff", "1. Admissions", ""),
    ("1. Admissions", "D8: Admissions\nPipeline", ""),
    ("1. Admissions", "D1: Student &\nGuardian Master", "creates"),
    ("Staff", "2. Academics", ""),
    ("2. Academics", "D2: Academic\nStructure", ""),
    ("Staff", "3. Fees", ""),
    ("Student", "3. Fees", ""),
    ("3. Fees", "D3: Fees &\nPayments", ""),
    ("3. Fees", "D1: Student &\nGuardian Master", ""),
    ("Staff", "4. Facilities", ""),
    ("Student", "4. Facilities", ""),
    ("4. Facilities", "D6: Facilities\n(Lib/Hostel/Trans)", ""),
    ("Staff", "5. Communication", ""),
    ("Student", "5. Communication", ""),
    ("Guardian", "5. Communication", ""),
    ("5. Communication", "D7: Communication\n(Notices/Feedback)", ""),
    ("Staff", "6. Examination", ""),
    ("Student", "6. Examination", "view if published"),
    ("6. Examination", "D4: Assessment\n& Results", ""),
    ("Staff", "7. Attendance", ""),
    ("Student", "7. Attendance", ""),
    ("7. Attendance", "D5: Attendance\nRecords", ""),
    ("Student", "8. Portal Access", ""),
    ("Guardian", "8. Portal Access", ""),
    ("8. Portal Access", "D1: Student &\nGuardian Master", "own/linked"),
    ("8. Portal Access", "D3: Fees &\nPayments", "own"),
    ("8. Portal Access", "D4: Assessment\n& Results", "published"),
]

for src, dst, label in flows:
    src_pos = ext.get(src) or proc_pos.get(src) or datastores.get(src)
    dst_pos = ext.get(dst) or proc_pos.get(dst) or datastores.get(dst)
    if src_pos and dst_pos:
        add_arrow(ax, src_pos[0] + 0.75, src_pos[1], dst_pos[0], dst_pos[1] + 0.35, label, fs=6)

ax.set_title("Figure 4.6 — DFD Level 1", fontsize=13, fontweight='bold', pad=15)
save_fig(fig, "fig4_6_dfd_l1")

# ============================================================
# Figure 4.7: Use Case Diagram
# ============================================================
fig, ax = plt.subplots(figsize=(13, 7))
ax.set_xlim(0, 13)
ax.set_ylim(0, 7)
ax.axis('off')

# Actors
actors = {
    "Student": (0.5, 5.5, BIT_LIGHT),
    "Guardian": (0.5, 4.5, BIT_LIGHT),
    "Instructor": (0.5, 3.5, AMBER_LIGHT),
    "Admissions": (0.5, 2.5, AMBER_LIGHT),
    "Fee Mgr": (0.5, 1.5, AMBER_LIGHT),
    "Facility": (0.5, 0.5, AMBER_LIGHT),
}

for name, (x, y, fc) in actors.items():
    # Draw stick figure
    head = Circle((x + 0.3, y + 0.5), 0.15, fill=False, edgecolor=DARK, linewidth=1.5)
    ax.add_patch(head)
    body = plt.Line2D([x+0.3, x+0.3], [y+0.35, y+0.1], color=DARK, linewidth=1.5)
    ax.add_line(body)
    arm = plt.Line2D([x+0.1, x+0.5], [y+0.3, y+0.2], color=DARK, linewidth=1.5)
    ax.add_line(arm)
    leg1 = plt.Line2D([x+0.3, x+0.2], [y+0.1, y], color=DARK, linewidth=1.5)
    ax.add_line(leg1)
    leg2 = plt.Line2D([x+0.3, x+0.4], [y+0.1, y], color=DARK, linewidth=1.5)
    ax.add_line(leg2)
    ax.text(x + 0.5, y + 0.25, name, ha='left', va='center', fontsize=9, fontweight='bold')

# Use case groups
# Portal
portal_ucs = ["View Dashboard", "View Attendance", "View Results", "View Fees & Payments", 
              "View Library", "View Notices", "Submit Feedback", "Switch Child"]
for i, uc in enumerate(portal_ucs):
    y = 5.5 - i * 0.4
    add_box(ax, 2.5, y, 2.5, 0.35, uc, fc=BIT_LIGHT, ec=BIT_BLUE, fs=7, shape='ellipse')

# Cockpit
cockpit_ucs = ["View Role Dashboard", "Quick Actions"]
for i, uc in enumerate(cockpit_ucs):
    y = 3.5 - i * 0.4
    add_box(ax, 2.5, y, 2.5, 0.35, uc, fc=AMBER_LIGHT, ec=AMBER, fs=7, shape='ellipse')

# Desk
desk_ucs = ["Manage Admissions", "Manage Academics", "Mark Attendance", "Enter Marks",
            "Manage Fees", "Manage Facilities", "Dispatch Notices", "Manage Feedback",
            "View Reports", "Administer System"]
for i, uc in enumerate(desk_ucs):
    y = 5.5 - i * 0.4
    add_box(ax, 6.5, y, 2.8, 0.35, uc, fc=PURPLE_LIGHT, ec=PURPLE, fs=7, shape='ellipse')

# Group labels
ax.text(3.75, 6.0, "Student/Guardian Portal", ha='center', fontsize=11, fontweight='bold', color=BIT_BLUE)
ax.text(3.75, 3.5, "Staff Cockpits", ha='center', fontsize=11, fontweight='bold', color=AMBER)
ax.text(7.9, 6.0, "Frappe Desk (Full CRUD)", ha='center', fontsize=11, fontweight='bold', color=PURPLE)

# Connections (simplified)
# Student/Guardian -> Portal UCs
for i in range(len(portal_ucs)):
    y = 5.5 - i * 0.4 + 0.175
    add_arrow(ax, 0.8, 5.5, 2.5, y, "", color=BIT_BLUE)
    add_arrow(ax, 0.8, 4.5, 2.5, y, "", color=BIT_BLUE)

# Staff -> Cockpit
for name, (x, y, _) in list(actors.items())[2:]:
    add_arrow(ax, 0.8, y + 0.25, 2.5, 3.7, "", color=AMBER)

# Cockpit -> Desk (include)
add_arrow(ax, 5.0, 3.5, 6.5, 5.5, "<<include>>", color=PURPLE)

# System Manager -> All Desk
add_arrow(ax, 0.8, 0.5, 6.5, 2.5, "", color=PURPLE)

ax.set_title("Figure 4.7 — Use Case Diagram", fontsize=13, fontweight='bold', pad=15)
save_fig(fig, "fig4_7_use_case")

# ============================================================
# Figure 4.8: Sequence — Admission Approval
# ============================================================
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Lifelines
lifelines = {
    "Admissions Officer": 1,
    "Institution ERP": 5,
    "MariaDB": 9,
}

for name, x in lifelines.items():
    # Header
    add_box(ax, x - 0.7, 9.2, 1.4, 0.5, name, fc=BIT_BLUE if "ERP" in name else (AMBER_LIGHT if "Officer" in name else AMBER_LIGHT), ec=DARK, fs=10, bold=True)
    # Lifeline
    line = plt.Line2D([x, x], [9.0, 0.5], color=GRAY, linewidth=1.5, linestyle='--')
    ax.add_line(line)

# Messages
msgs = [
    (1, "Admissions Officer", 5, "Institution ERP", "1. Review Applicant\n(Workflow: Under Review)", 8.5),
    (5, "Institution ERP", 9, "MariaDB", "2. READ Student Applicant", 7.8),
    (1, "Admissions Officer", 5, "Institution ERP", "3. Approve Applicant\n(Workflow: Approved)", 7.1),
    (5, "Institution ERP", 5, "Institution ERP", "4. on_update Trigger\n(Student Applicant)", 6.4),
    (5, "Institution ERP", 9, "MariaDB", "5. CREATE Guardian DocType", 5.7),
    (5, "Institution ERP", 9, "MariaDB", "6. CREATE Student DocType\n(STU-.YYYY.-.#####)", 5.0),
    (5, "Institution ERP", 9, "MariaDB", "7. LINK Guardian→Student\n(guardian field)", 4.3),
    (5, "Institution ERP", 9, "MariaDB", "8. SET created_student\n= Student Name", 3.6),
    (5, "Institution ERP", 1, "Admissions Officer", "9. Return Success\n(Student + Guardian created)", 2.9),
]

for x1, src, x2, dst, label, y in msgs:
    # Arrow
    arrow = FancyArrowPatch((x1, y + 0.15), (x2, y + 0.15), 
                            arrowstyle='->', mutation_scale=15,
                            linewidth=1.5, color=BIT_BLUE)
    ax.add_patch(arrow)
    # Label box
    mx = (x1 + x2) / 2
    add_box(ax, mx - 1.5, y - 0.3, 3, 0.6, label, fc=WHITE, ec=BIT_BLUE, fs=8)

# Note
note_text = "Auto-creation happens in on_update hook\nwhen workflow_state='Approved'\n→ create Guardian\n→ create Student\n→ link both"
ax.text(7, 1.5, note_text, ha='left', va='center', fontsize=8, 
        bbox=dict(boxstyle="round,pad=0.3", facecolor=AMBER_LIGHT, edgecolor=AMBER, linewidth=1))

ax.set_title("Figure 4.8 — Sequence Diagram: Admission Approval → Auto Student/Guardian Creation", fontsize=13, fontweight='bold', pad=15)
save_fig(fig, "fig4_8_seq_admission")

# ============================================================
# Figure 4.9: Sequence — Fee Payment
# ============================================================
fig, ax = plt.subplots(figsize=(10, 7))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

lifelines = {
    "Fee Manager": 1,
    "Institution ERP": 5,
    "MariaDB": 9,
}

for name, x in lifelines.items():
    add_box(ax, x - 0.7, 9.2, 1.4, 0.5, name, fc=AMBER_LIGHT if "Manager" in name else BIT_BLUE, ec=DARK, fs=10, bold=True)
    line = plt.Line2D([x, x], [9.0, 0.5], color=GRAY, linewidth=1.5, linestyle='--')
    ax.add_line(line)

msgs = [
    (1, "Fee Manager", 5, "Institution ERP", "1. Create Fee Payment\n(amount, mode, ref)", 8.5),
    (5, "Institution ERP", 9, "MariaDB", "2. VALIDATE payment ≤ outstanding", 7.8),
    (5, "Institution ERP", 9, "MariaDB", "3. INSERT Fee Payment\n(docstatus=1 on submit)", 7.1),
    (5, "Institution ERP", 5, "Institution ERP", "4. on_submit Hook\n(recompute_paid_and_status)", 6.4),
    (5, "Institution ERP", 9, "MariaDB", "5. READ all Fee Payments\nfor this Fees", 5.7),
    (5, "Institution ERP", 5, "Institution ERP", "6. CALCULATE paid = Σ payments\ndiscount = discount_amount\noutstanding = total - paid - discount", 5.0),
    (5, "Institution ERP", 9, "MariaDB", "7. UPDATE Fees\npaid, outstanding, status", 4.3),
    (5, "Institution ERP", 1, "Fee Manager", "8. Return Updated\nFees + Payment", 3.6),
]

for x1, src, x2, dst, label, y in msgs:
    arrow = FancyArrowPatch((x1, y + 0.15), (x2, y + 0.15), 
                            arrowstyle='->', mutation_scale=15,
                            linewidth=1.5, color=AMBER)
    ax.add_patch(arrow)
    mx = (x1 + x2) / 2
    add_box(ax, mx - 1.5, y - 0.3, 3, 0.6, label, fc=WHITE, ec=AMBER, fs=8)

ax.set_title("Figure 4.9 — Sequence Diagram: Fee Payment → Recompute Outstanding", fontsize=13, fontweight='bold', pad=15)
save_fig(fig, "fig4_9_seq_fee")

# ============================================================
# Figure 4.10: Sequence — Assessment Result
# ============================================================
fig, ax = plt.subplots(figsize=(10, 9))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

lifelines = {
    "Instructor": 1,
    "Institution ERP": 4,
    "MariaDB": 7,
    "Student Portal": 10,
}

for name, x in lifelines.items():
    add_box(ax, x - 0.8, 9.2, 1.6, 0.5, name, 
            fc=AMBER_LIGHT if "Instructor" in name else (BIT_BLUE if "ERP" in name else (AMBER_LIGHT if "MariaDB" in name else BIT_LIGHT)), 
            ec=DARK, fs=9, bold=True)
    line = plt.Line2D([x, x], [9.0, 0.5], color=GRAY, linewidth=1.5, linestyle='--')
    ax.add_line(line)

msgs = [
    (1, "Instructor", 4, "Institution ERP", "1. mark_bulk_assessment_results\n(assessment_plan, results_data)", 8.5),
    (4, "Institution ERP", 7, "MariaDB", "2. VALIDATE marks ≤ max_marks", 7.8),
    (4, "Institution ERP", 7, "MariaDB", "3. READ Grading Scale intervals", 7.1),
    (4, "Institution ERP", 4, "Institution ERP", "4. FOR each result:\n   % = marks/max*100\n   grade = matching interval\n   status = Pass/Fail", 6.4),
    (4, "Institution ERP", 7, "MariaDB", "5. UPSERT Assessment Result\n(prevents duplicate)", 5.7),
    (4, "Institution ERP", 1, "Instructor", "6. Return Created Results", 5.0),
    (1, "Instructor", 4, "Institution ERP", "7. Set Assessment Group\nresults_published = 1", 4.3),
    (4, "Institution ERP", 7, "MariaDB", "8. UPDATE Assessment Group", 3.6),
    (10, "Student Portal", 4, "Institution ERP", "9. portal_get_results\n(student, assessment_plan)", 2.9),
    (4, "Institution ERP", 4, "Institution ERP", "10. CHECK results_published = 1?", 2.2),
    (4, "Institution ERP", 7, "MariaDB", "11. IF yes: READ Results\nELSE: 'Not Published'", 1.5),
    (4, "Institution ERP", 10, "Student Portal", "12. Return Results OR\n'Not Published' banner", 0.8),
]

for x1, src, x2, dst, label, y in msgs:
    arrow = FancyArrowPatch((x1, y + 0.15), (x2, y + 0.15), 
                            arrowstyle='->', mutation_scale=15,
                            linewidth=1.5, color=PURPLE)
    ax.add_patch(arrow)
    mx = (x1 + x2) / 2
    add_box(ax, mx - 1.5, y - 0.3, 3, 0.6, label, fc=WHITE, ec=PURPLE, fs=7)

ax.set_title("Figure 4.10 — Sequence Diagram: Assessment Result Entry → Results Published Gate", fontsize=13, fontweight='bold', pad=15)
save_fig(fig, "fig4_10_seq_assessment")

# ============================================================
# Figure 4.11: Sequence — Library Fine
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

lifelines = {
    "Facility Manager": 1,
    "Institution ERP": 5,
    "MariaDB": 9,
}

for name, x in lifelines.items():
    add_box(ax, x - 0.7, 9.2, 1.4, 0.5, name, fc=AMBER_LIGHT if "Manager" in name else BIT_BLUE, ec=DARK, fs=10, bold=True)
    line = plt.Line2D([x, x], [9.0, 0.5], color=GRAY, linewidth=1.5, linestyle='--')
    ax.add_line(line)

msgs = [
    (1, "Facility Manager", 5, "Institution ERP", "1. Submit Library Transaction\n(type=Return, return_date)", 8.5),
    (5, "Institution ERP", 9, "MariaDB", "2. VALIDATE open Issue exists", 7.8),
    (5, "Institution ERP", 5, "Institution ERP", "3. CALCULATE fine = days_overdue × ₹5", 7.1),
    (5, "Institution ERP", 9, "MariaDB", "4. UPDATE Transaction\nfine_amount, status=Returned\navailable_copies++", 6.4),
    (5, "Institution ERP", 5, "Institution ERP", "5. IF fine > 0:\n   CREATE Fees Record\n   (category=Library Fine)", 5.7),
    (5, "Institution ERP", 9, "MariaDB", "6. INSERT Fees\n(outstanding = fine)", 5.0),
    (5, "Institution ERP", 1, "Facility Manager", "7. Return Transaction\n+ Fine Fee Created", 4.3),
]

for x1, src, x2, dst, label, y in msgs:
    arrow = FancyArrowPatch((x1, y + 0.15), (x2, y + 0.15), 
                            arrowstyle='->', mutation_scale=15,
                            linewidth=1.5, color=GREEN)
    ax.add_patch(arrow)
    mx = (x1 + x2) / 2
    add_box(ax, mx - 1.5, y - 0.3, 3, 0.6, label, fc=WHITE, ec=GREEN, fs=8)

# Limitation note
ax.text(7, 2.5, "LIMITATION: Fine creates Fee immediately\nwithout Fee Manager approval workflow", ha='left', va='center', fontsize=8,
        bbox=dict(boxstyle="round,pad=0.3", facecolor=RED_LIGHT, edgecolor=RED, linewidth=1))

ax.set_title("Figure 4.11 — Sequence Diagram: Library Return → Fine Calculation → Fee Creation", fontsize=13, fontweight='bold', pad=15)
save_fig(fig, "fig4_11_seq_library")

# ============================================================
# Figure 4.12: Activity — Student Portal
# ============================================================
fig, ax = plt.subplots(figsize=(9, 9))
ax.set_xlim(0, 9)
ax.set_ylim(0, 9)
ax.axis('off')

# Nodes
nodes = {
    "Start": (4.5, 8.3, "circle"),
    "Login": (4.5, 7.3, "box"),
    "Auth": (4.5, 6.3, "box"),
    "RoleCheck": (4.5, 5.3, "diamond"),
    "Dashboard": (4.5, 4.3, "box"),
    "NavMenu": (4.5, 3.3, "box"),
    "Attendance": (1.5, 2.0, "box"),
    "Results": (3.5, 2.0, "box"),
    "Fees": (5.5, 2.0, "box"),
    "Library": (7.5, 2.0, "box"),
    "Notices": (1.5, 0.7, "box"),
    "Feedback": (3.5, 0.7, "box"),
    "Profile": (5.5, 0.7, "box"),
    "Logout": (4.5, -0.5, "box"),
    "End": (4.5, -1.3, "circle"),
}

# Adjust y to fit
y_offset = 1.5
for name, (x, y, shape) in nodes.items():
    nodes[name] = (x, y + y_offset, shape)

for name, (x, y, shape) in nodes.items():
    if shape == "circle":
        circ = Circle((x, y), 0.25, fill=True, facecolor=BIT_BLUE, edgecolor=BIT_BLUE)
        ax.add_patch(circ)
        ax.text(x, y, "●", ha='center', va='center', fontsize=14, color='white')
        ax.text(x, y - 0.5, name, ha='center', va='top', fontsize=9, fontweight='bold')
    elif shape == "diamond":
        diamond = mpatches.Polygon([[x, y+0.25], [x+0.35, y], [x, y-0.25], [x-0.35, y]], 
                                    fill=True, facecolor=AMBER_LIGHT, edgecolor=AMBER)
        ax.add_patch(diamond)
        ax.text(x, y, name, ha='center', va='center', fontsize=8, fontweight='bold')
    else:
        fc = BIT_LIGHT if name not in ["Logout", "End"] else RED_LIGHT
        add_box(ax, x - 1.2, y - 0.2, 2.4, 0.5, name, fc=fc, ec=BIT_BLUE, fs=8)

# Edges
edges = [
    ("Start", "Login"), ("Login", "Auth"), ("Auth", "RoleCheck"),
    ("RoleCheck", "Dashboard"), ("Dashboard", "NavMenu"),
    ("NavMenu", "Attendance"), ("NavMenu", "Results"), ("NavMenu", "Fees"),
    ("NavMenu", "Library"), ("NavMenu", "Notices"), ("NavMenu", "Feedback"),
    ("NavMenu", "Profile"),
]
for src, dst in edges:
    x1, y1, _ = nodes[src]
    x2, y2, _ = nodes[dst]
    add_arrow(ax, x1, y1 - 0.25, x2, y2 + 0.25, "", color=BIT_BLUE)

# Return edges from pages to NavMenu
for page in ["Attendance", "Results", "Fees", "Library", "Notices", "Feedback", "Profile"]:
    x1, y1, _ = nodes[page]
    x2, y2, _ = nodes["NavMenu"]
    add_arrow(ax, x1, y1 - 0.25, x2, y2 + 0.25, "", color=BIT_BLUE, style='dashed')

add_arrow(ax, 4.5, 0.5, 4.5, 0, "Logout", color=RED)

# Yes/No labels
ax.text(4.9, 5.3, "Yes", fontsize=8, color=GREEN)
ax.text(4.0, 5.0, "No", fontsize=8, color=RED)

ax.set_title("Figure 4.12 — Activity Diagram: Student Portal Flow", fontsize=13, fontweight='bold', pad=15)
save_fig(fig, "fig4_12_act_student")

# ============================================================
# Figure 4.13: Activity — Staff Hybrid Flow
# ============================================================
fig, ax = plt.subplots(figsize=(9, 8))
ax.set_xlim(0, 9)
ax.set_ylim(0, 8)
ax.axis('off')

nodes = {
    "Start": (4.5, 7.3, "circle"),
    "Login": (4.5, 6.3, "box"),
    "RoleDetect": (4.5, 5.3, "box"),
    "Redirect": (4.5, 4.3, "box"),
    "Cockpit": (4.5, 3.3, "box"),
    "QuickAction": (4.5, 2.3, "box"),
    "OpenDesk": (4.5, 1.3, "box"),
    "DeskWork": (4.5, 0.3, "box"),
    "Return": (4.5, -0.5, "box"),
    "Logout": (4.5, -1.5, "box"),
    "End": (4.5, -2.3, "circle"),
}

y_offset = 2.5
for name, (x, y, shape) in nodes.items():
    nodes[name] = (x, y + y_offset, shape)

for name, (x, y, shape) in nodes.items():
    if shape == "circle":
        circ = Circle((x, y), 0.25, fill=True, facecolor=BIT_BLUE, edgecolor=BIT_BLUE)
        ax.add_patch(circ)
        ax.text(x, y - 0.5, name, ha='center', va='top', fontsize=9, fontweight='bold')
    else:
        fc = AMBER_LIGHT if name not in ["OpenDesk", "DeskWork", "Logout", "End"] else (PURPLE_LIGHT if name in ["OpenDesk", "DeskWork"] else RED_LIGHT)
        add_box(ax, x - 1.5, y - 0.25, 3, 0.5, name, fc=fc, ec=AMBER if "Desk" not in name else PURPLE, fs=9)

edges = [
    ("Start", "Login"), ("Login", "RoleDetect"), ("RoleDetect", "Redirect"),
    ("Redirect", "Cockpit"), ("Cockpit", "QuickAction"), ("QuickAction", "OpenDesk"),
    ("OpenDesk", "DeskWork"), ("DeskWork", "Return"), ("Return", "Cockpit"),
    ("Cockpit", "Logout"), ("Logout", "End"),
]
for src, dst in edges:
    x1, y1, _ = nodes[src]
    x2, y2, _ = nodes[dst]
    add_arrow(ax, x1, y1 - 0.25, x2, y2 + 0.25, "", color=AMBER)

# Loop indicator
ax.text(7.5, 2.5, "Loop:\nDesk Work →\nRefresh Cockpit", ha='left', fontsize=9, 
        bbox=dict(boxstyle="round,pad=0.3", facecolor=GRAY_LIGHT, edgecolor=GRAY))

ax.set_title("Figure 4.13 — Activity Diagram: Staff Hybrid Flow (Cockpit → Desk)", fontsize=13, fontweight='bold', pad=15)
save_fig(fig, "fig4_13_act_staff")

# ============================================================
# Figure 5.16: Workflow — Student Applicant
# ============================================================
fig, ax = plt.subplots(figsize=(11, 3.5))
ax.set_xlim(0, 11)
ax.set_ylim(0, 3.5)
ax.axis('off')

states = [
    (0.5, 1.5, "Draft", AMBER_LIGHT),
    (2.5, 1.5, "Applied", BIT_LIGHT),
    (5.0, 1.5, "Under Review", AMBER_LIGHT),
    (7.5, 1.5, "Approved", GREEN_LIGHT),
    (9.5, 1.5, "Rejected", RED_LIGHT),
]

for x, y, name, fc in states:
    add_box(ax, x, y, 1.8, 0.8, name, fc=fc, ec=DARK if name == "Approved" else GRAY, fs=10, bold=(name=="Approved"))

transitions = [
    (0, 1, "Submit Application"),
    (1, 2, "Officer Reviews"),
    (2, 3, "Approve\n→ Creates Student+Guardian"),
    (2, 4, "Reject"),
    (3, 4, "Reopen (if needed)"),
    (4, 1, "Re-apply"),
]

for i, j, label in transitions:
    x1, y1, _, _ = states[i]
    x2, y2, _, _ = states[j]
    x1 += 1.8
    add_arrow(ax, x1, y1 + 0.4, x2, y2 + 0.4, label, fs=8, color=BIT_BLUE)

# Note
ax.text(8, 0.2, "on_update hook: workflow_state='Approved'\n→ create Guardian → create Student → link both", 
        ha='left', fontsize=8, bbox=dict(boxstyle="round,pad=0.3", facecolor=AMBER_LIGHT, edgecolor=AMBER))

ax.set_title("Figure 5.16 — Student Applicant Workflow (Draft → Approved → Auto-Creation)", fontsize=13, fontweight='bold', pad=15)
save_fig(fig, "fig5_16_wf_applicant")

print("\n=== All diagrams generated successfully ===")
print(f"Images saved to: {IMAGES_DIR}")
print(f"Total files: {len(list(IMAGES_DIR.glob('*.png')))}")