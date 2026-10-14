#!/usr/bin/env python3
"""
Generate placeholder images for UI screenshots (25 placeholders).
Each is a clean gray box with figure number and title.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pathlib import Path

IMAGES_DIR = Path(__file__).parent.parent / "images"
IMAGES_DIR.mkdir(exist_ok=True)

GRAY = '#94a3b8'
GRAY_LIGHT = '#f1f5f9'
DARK = '#1e293b'
BIT_BLUE = '#1e40af'

placeholders = [
    ("fig5_1_admissions_cockpit", "Figure 5.1 — Admissions Cockpit\n/institution-portal/admissions\n[Replace with screenshot]"),
    ("fig5_2_applicant_workflow", "Figure 5.2 — Student Applicant Workflow in Desk\nDesk → Student Applicant list → workflow states\n[Replace with screenshot]"),
    ("fig5_3_student_master", "Figure 5.3 — Student Master Form\nDesk → Student form (STU-.YYYY.-.#####)\n[Replace with screenshot]"),
    ("fig5_4_schedule_conflict", "Figure 5.4 — Course Schedule Conflict Validation\nDesk → Course Schedule → attempt double-book\n[Replace with screenshot]"),
    ("fig5_5_instructor_cockpit", "Figure 5.5 — Instructor Cockpit: Attendance\n/institution-portal/instructor\n[Replace with screenshot]"),
    ("fig5_6_bulk_attendance_api", "Figure 5.6 — Bulk Attendance API Response\nPostman/console showing API response\n[Replace with screenshot]"),
    ("fig5_7_grading_scale", "Figure 5.7 — Grading Scale Intervals\nDesk → Grading Scale form with intervals\n[Replace with screenshot]"),
    ("fig5_8_results_gate", "Figure 5.8 — Results Page: Published vs Unpublished\n/institution-portal/#/results — blue banner for unpublished\n[Replace with screenshot]"),
    ("fig5_9_fee_cockpit", "Figure 5.9 — Fee Manager Cockpit\n/institution-portal/fees-manager\n[Replace with screenshot]"),
    ("fig5_10_fee_dues_report", "Figure 5.10 — Fee Dues Report\nDesk → Fee Dues Report with filters\n[Replace with screenshot]"),
    ("fig5_11_library_flow", "Figure 5.11 — Library Transaction Flow\nDesk → Library Transaction Issue/Return\n[Replace with screenshot]"),
    ("fig5_12_hostel_occupancy", "Figure 5.12 — Hostel Occupancy View\n/institution-portal/facility-manager → Hostel\n[Replace with screenshot]"),
    ("fig5_13_transport_route", "Figure 5.13 — Transport Route Map\nDesk → Transport Route with stops\n[Replace with screenshot]"),
    ("fig5_14_comm_cockpit", "Figure 5.14 — Communication Cockpit\n/institution-portal/communication\n[Replace with screenshot]"),
    ("fig5_15_inst_dashboard", "Figure 5.15 — Institution Overview Dashboard\nDesk → Institution Overview Dashboard (5 cards + 2 charts)\n[Replace with screenshot]"),
    ("fig5_17_student_dashboard", "Figure 5.17 — Student Dashboard\n/institution-portal/#/dashboard\n[Replace with screenshot]"),
    ("fig5_18_guardian_switcher", "Figure 5.18 — Guardian Child Switcher\nSidebar dropdown showing 2 children\n[Replace with screenshot]"),
    ("fig5_19_admin_cockpit", "Figure 5.19 — Admin Cockpit\n/institution-portal/admin\n[Replace with screenshot]"),
    ("fig5_20_rebranded_desk", "Figure 5.20 — Rebranded Desk: BIT Theme\nDesk list view showing Inter font + blue primary\n[Replace with screenshot]"),
    ("fig6_1_responsive", "Figure 6.1 — Responsive Breakpoints\nBrowser dev tools device toolbar at 4 widths\n[Replace with screenshot]"),
    ("fig7_1_adm_pipeline", "Figure 7.1 — Admissions Pipeline\nCockpit pipeline funnel + Desk workflow\n[Replace with screenshot]"),
    ("fig7_2_results_gate", "Figure 7.2 — Student Results: Published Gate\nResults page with banner + published cards\n[Replace with screenshot]"),
    ("fig7_3_fee_outstanding", "Figure 7.3 — Fee Manager Outstanding View\nCockpit outstanding list + Desk fee list\n[Replace with screenshot]"),
    ("fig7_4_inst_dashboard", "Figure 7.4 — Institution Overview Dashboard\nDashboard with 5 Number Cards + 2 Charts\n[Replace with screenshot]"),
    ("fig7_5_guardian_switch", "Figure 7.5 — Guardian Portal Child Switcher\nDashboard switch → data updates\n[Replace with screenshot]"),
    ("fig7_6_rebranded_desk", "Figure 7.6 — Rebranded Desk: BIT Theme\nFull Desk view showing theming\n[Replace with screenshot]"),
]

def save_fig(fig, name, dpi=200):
    path = IMAGES_DIR / f"{name}.png"
    fig.savefig(path, dpi=dpi, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"Generated: {path}")

for name, text in placeholders:
    fig, ax = plt.subplots(figsize=(16, 9))  # 16:9 aspect ratio
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')
    
    # Outer border
    outer = Rectangle((0.5, 0.5), 15, 8, facecolor=GRAY_LIGHT, edgecolor=GRAY, linewidth=2)
    ax.add_patch(outer)
    
    # Inner content area
    inner = Rectangle((1.5, 1.5), 13, 6, facecolor='white', edgecolor=GRAY, linewidth=1)
    ax.add_patch(inner)
    
    # Placeholder icon (camera)
    ax.text(8, 5.5, "📷", ha='center', va='center', fontsize=60)
    
    # Figure label
    ax.text(8, 4.0, "PLACEHOLDER", ha='center', va='center', fontsize=18, fontweight='bold', color=BIT_BLUE)
    
    # Figure details
    ax.text(8, 3.2, text, ha='center', va='center', fontsize=11, color=DARK, 
            wrap=True, family='DejaVu Sans', linespacing=1.5)
    
    # Instruction
    ax.text(8, 1.8, "Right-click → Change Picture to replace\nSize: 16:9 • Resolution: 1920×1080 recommended", 
            ha='center', va='center', fontsize=9, color=GRAY, style='italic')
    
    save_fig(fig, name)

print(f"\n=== Generated {len(placeholders)} placeholder images ===")