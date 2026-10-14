#!/usr/bin/env python3
"""
Generate additional diagrams: Design Tokens table (Fig 4.14) and Cockpit Wireframe (Fig 4.15)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pathlib import Path

IMAGES_DIR = Path(__file__).parent.parent / "images"
IMAGES_DIR.mkdir(exist_ok=True)

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

# ============================================================
# Figure 4.14: Design System Token Reference
# ============================================================
fig, ax = plt.subplots(figsize=(11, 6))
ax.set_xlim(0, 11)
ax.set_ylim(0, 6)
ax.axis('off')

tokens = {
    "Colors": [
        ("--color-primary", BIT_BLUE, "Primary brand color (BIT Blue)"),
        ("--color-success", GREEN, "Success states, positive actions"),
        ("--color-warning", AMBER, "Warning states, pending items"),
        ("--color-danger", RED, "Error states, destructive actions"),
        ("--color-info", "#0ea5e9", "Informational states"),
        ("--color-bg", "#f8fafc", "Page background"),
        ("--color-surface", WHITE, "Card/surface background"),
        ("--color-border", "#e2e8f0", "Border/divider color"),
    ],
    "Typography": [
        ("--text-xs", "0.75rem (12px)", "Small labels, captions"),
        ("--text-sm", "0.875rem (14px)", "Body text, form inputs"),
        ("--text-base", "1rem (16px)", "Default body text"),
        ("--text-lg", "1.125rem (18px)", "Subheadings"),
        ("--text-xl", "1.25rem (20px)", "Section headings"),
        ("--text-2xl", "1.5rem (24px)", "Page titles"),
        ("--text-3xl", "1.875rem (30px)", "Dashboard hero numbers"),
        ("--leading-relaxed", "1.6", "Relaxed line height for readability"),
    ],
    "Spacing": [
        ("--space-1", "4px", "Tight spacing"),
        ("--space-2", "8px", "Default gap"),
        ("--space-3", "12px", "Medium gap"),
        ("--space-4", "16px", "Standard padding"),
        ("--space-5", "20px", "Large padding"),
        ("--space-6", "24px", "Section gap"),
        ("--space-8", "32px", "Major section gap"),
    ],
    "Radii": [
        ("--radius-sm", "6px", "Buttons, inputs, badges"),
        ("--radius-md", "10px", "Cards, modals, dropdowns"),
        ("--radius-lg", "14px", "Large cards, sheets"),
        ("--radius-xl", "20px", "Hero sections, overlays"),
    ],
    "Shadows": [
        ("--shadow-sm", "0 1px 2px rgba(0,0,0,0.05)", "Subtle elevation"),
        ("--shadow-md", "0 4px 6px rgba(0,0,0,0.07)", "Card elevation"),
        ("--shadow-lg", "0 10px 15px rgba(0,0,0,0.1)", "Modal/dropdown elevation"),
    ],
    "Transitions": [
        ("--transition-fast", "150ms", "Hover, focus states"),
        ("--transition-base", "200ms", "Standard transitions"),
    ],
}

# Column positions
col_x = [0.2, 2.5, 5.5, 9.5]
col_w = [2.2, 2.8, 3.8, 1.5]
headers = ["Token", "Value", "Usage", "Visual"]

# Header row
y = 5.5
for i, (h, x, w) in enumerate(zip(headers, col_x, col_w)):
    rect = Rectangle((x, y), w, 0.4, facecolor=BIT_BLUE, edgecolor=BIT_BLUE)
    ax.add_patch(rect)
    ax.text(x + w/2, y + 0.2, h, ha='center', va='center', fontsize=10, fontweight='bold', color='white')

y -= 0.4
for category, items in tokens.items():
    # Category header
    rect = Rectangle((0.2, y), 10.6, 0.35, facecolor=GRAY_LIGHT, edgecolor=GRAY)
    ax.add_patch(rect)
    ax.text(0.5, y + 0.175, category, ha='left', va='center', fontsize=9, fontweight='bold', color=DARK)
    y -= 0.35
    
    for token, value, usage in items:
        row_color = WHITE if items.index((token, value, usage)) % 2 == 0 else GRAY_LIGHT
        # Token
        rect = Rectangle((col_x[0], y), col_w[0], 0.3, facecolor=row_color, edgecolor=GRAY_LIGHT)
        ax.add_patch(rect)
        ax.text(col_x[0] + 0.1, y + 0.15, token, ha='left', va='center', fontsize=8, fontfamily='monospace')
        
        # Value
        rect = Rectangle((col_x[1], y), col_w[1], 0.3, facecolor=row_color, edgecolor=GRAY_LIGHT)
        ax.add_patch(rect)
        # Color swatch for colors
        if category == "Colors" and token.startswith("--color-"):
            swatch = Rectangle((col_x[1] + 0.1, y + 0.05), 0.4, 0.2, facecolor=value, edgecolor=GRAY)
            ax.add_patch(swatch)
            ax.text(col_x[1] + 0.6, y + 0.15, value, ha='left', va='center', fontsize=8, fontfamily='monospace')
        else:
            ax.text(col_x[1] + 0.1, y + 0.15, value, ha='left', va='center', fontsize=8, fontfamily='monospace')
        
        # Usage
        rect = Rectangle((col_x[2], y), col_w[2], 0.3, facecolor=row_color, edgecolor=GRAY_LIGHT)
        ax.add_patch(rect)
        ax.text(col_x[2] + 0.1, y + 0.15, usage, ha='left', va='center', fontsize=8)
        
        # Visual indicator
        rect = Rectangle((col_x[3], y), col_w[3], 0.3, facecolor=row_color, edgecolor=GRAY_LIGHT)
        ax.add_patch(rect)
        if category == "Colors":
            swatch = Rectangle((col_x[3] + 0.3, y + 0.05), 0.8, 0.2, facecolor=value, edgecolor=GRAY)
            ax.add_patch(swatch)
        elif category == "Radii":
            from matplotlib.patches import FancyBboxPatch
            box = FancyBboxPatch((col_x[3] + 0.3, y + 0.05), 1.0, 0.2, 
                                  boxstyle=f"round,pad=0.02", facecolor=BIT_LIGHT, edgecolor=BIT_BLUE)
            ax.add_patch(box)
        elif category == "Shadows":
            # Simple shadow representation
            rect = Rectangle((col_x[3] + 0.3, y + 0.05), 1.0, 0.2, facecolor=BIT_LIGHT, edgecolor=GRAY)
            ax.add_patch(rect)
            # Shadow effect with text
            ax.text(col_x[3] + 0.8, y + 0.15, "▼", ha='center', va='center', fontsize=8, color=GRAY)
        else:
            ax.text(col_x[3] + 0.5, y + 0.15, "●", ha='center', va='center', fontsize=8, color=BIT_BLUE)
        
        y -= 0.3
    
    y -= 0.1  # gap between categories

ax.set_title("Figure 4.14 — Design System Token Reference (Portal & Cockpit)", fontsize=13, fontweight='bold', pad=15)
save_fig(fig, "fig4_14_design_tokens")

# ============================================================
# Figure 4.15: Cockpit Wireframe (Instructor Cockpit)
# ============================================================
fig, ax = plt.subplots(figsize=(11, 7))
ax.set_xlim(0, 11)
ax.set_ylim(0, 7)
ax.axis('off')

# Browser chrome
chrome = Rectangle((0.5, 0.5), 10, 6, facecolor='#f1f5f9', edgecolor='#cbd5e1', linewidth=2)
ax.add_patch(chrome)

# Address bar
addr = Rectangle((1, 6.0), 9, 0.4, facecolor=WHITE, edgecolor='#e2e8f0')
ax.add_patch(addr)
ax.text(1.2, 6.2, "http://localhost:8000/institution-portal/instructor  🔒", ha='left', va='center', fontsize=8, color=GRAY, fontfamily='monospace')

# Header bar
header = Rectangle((1, 5.5), 9, 0.7, facecolor=BIT_BLUE, edgecolor=BIT_BLUE)
ax.add_patch(header)
ax.text(1.5, 5.85, "Instructor Cockpit", ha='left', va='center', fontsize=14, fontweight='bold', color='white')
ax.text(9.5, 5.85, "Dr. Rajesh Kumar  ▼", ha='right', va='center', fontsize=10, color='white')
ax.text(9.5, 5.55, "Open Full Desk →", ha='right', va='center', fontsize=9, color=BIT_LIGHT)

# Stats row (4 StatCards)
stat_data = [
    ("My Students", "42", "👥", GREEN),
    ("Assigned Groups", "3", "📚", BIT_BLUE),
    ("Attendance Today", "78%", "✅", AMBER),
    ("Pending Marks", "5", "✏️", RED),
]
for i, (label, value, icon, color) in enumerate(stat_data):
    x = 1.2 + i * 2.4
    card = Rectangle((x, 4.5), 2.1, 0.9, facecolor=WHITE, edgecolor='#e2e8f0', linewidth=1)
    ax.add_patch(card)
    # Color bar top
    bar = Rectangle((x, 5.3), 2.1, 0.08, facecolor=color)
    ax.add_patch(bar)
    ax.text(x + 1.05, 5.15, value, ha='center', va='center', fontsize=20, fontweight='bold', color=DARK)
    ax.text(x + 1.05, 4.7, label, ha='center', va='center', fontsize=9, color=GRAY)
    ax.text(x + 0.15, 5.2, icon, ha='left', va='center', fontsize=14)

# Today's Classes section
section_y = 4.2
ax.text(1.2, section_y, "Today's Classes", ha='left', va='bottom', fontsize=12, fontweight='bold', color=DARK)
section_y -= 0.35

classes = [
    ("09:00–10:00", "CS101 - Programming", "Group A", "Room 101", "Ongoing", GREEN),
    ("10:15–11:15", "CS201 - Data Structures", "Group B", "Room 102", "Upcoming", BIT_BLUE),
    ("11:30–12:30", "CS301 - Algorithms", "Group A", "Room 103", "Upcoming", BIT_BLUE),
    ("14:00–15:00", "CS101 - Lab", "Group C", "Lab 2", "Upcoming", BIT_BLUE),
]

for time, course, group, room, status, color in classes:
    card = Rectangle((1.2, section_y), 8.6, 0.55, facecolor=WHITE, edgecolor='#e2e8f0', linewidth=1)
    ax.add_patch(card)
    ax.text(1.4, section_y + 0.275, time, ha='left', va='center', fontsize=9, fontweight='bold', fontfamily='monospace', color=DARK)
    ax.text(2.8, section_y + 0.275, course, ha='left', va='center', fontsize=9, color=DARK)
    ax.text(5.5, section_y + 0.275, group, ha='left', va='center', fontsize=9, color=GRAY)
    ax.text(7.0, section_y + 0.275, room, ha='left', va='center', fontsize=9, color=GRAY)
    # Status badge
    badge = Rectangle((8.8, section_y + 0.125), 0.8, 0.3, facecolor=color, edgecolor=color)
    ax.add_patch(badge)
    ax.text(9.2, section_y + 0.275, status, ha='center', va='center', fontsize=8, fontweight='bold', color='white')
    section_y -= 0.6

# Quick Actions
qa_y = section_y - 0.2
ax.text(1.2, qa_y, "Quick Actions", ha='left', va='bottom', fontsize=12, fontweight='bold', color=DARK)
qa_y -= 0.35

actions = [
    ("Mark Attendance", "📋", BIT_BLUE),
    ("Enter Marks", "✏️", GREEN),
    ("Assessment Plans", "📝", PURPLE),
    ("My Schedule", "📅", AMBER),
]

for i, (label, icon, color) in enumerate(actions):
    x = 1.2 + i * 2.3
    btn = Rectangle((x, qa_y), 2.0, 0.55, facecolor=WHITE, edgecolor=color, linewidth=1.5)
    ax.add_patch(btn)
    ax.text(x + 0.2, qa_y + 0.275, icon, ha='left', va='center', fontsize=16)
    ax.text(x + 1.0, qa_y + 0.275, label, ha='center', va='center', fontsize=10, fontweight='bold', color=DARK)

# Pending Marks Entry
pm_y = qa_y - 0.7
ax.text(1.2, pm_y, "Pending Marks Entry", ha='left', va='bottom', fontsize=12, fontweight='bold', color=DARK)
pm_y -= 0.35

pending = [
    ("CS101 - Midterm", "Group A", "2026-01-15", "Enter", GREEN),
    ("CS201 - Quiz 2", "Group B", "2026-01-18", "Enter", AMBER),
]

for course, group, due, btn_text, color in pending:
    card = Rectangle((1.2, pm_y), 8.6, 0.45, facecolor=WHITE, edgecolor='#e2e8f0', linewidth=1)
    ax.add_patch(card)
    ax.text(1.4, pm_y + 0.225, course, ha='left', va='center', fontsize=9, fontweight='bold', color=DARK)
    ax.text(4.5, pm_y + 0.225, group, ha='left', va='center', fontsize=9, color=GRAY)
    ax.text(6.5, pm_y + 0.225, f"Due: {due}", ha='left', va='center', fontsize=9, color=GRAY)
    btn = Rectangle((8.8, pm_y + 0.075), 0.8, 0.3, facecolor=color, edgecolor=color)
    ax.add_patch(btn)
    ax.text(9.2, pm_y + 0.225, btn_text, ha='center', va='center', fontsize=8, fontweight='bold', color='white')
    pm_y -= 0.5

ax.set_title("Figure 4.15 — Instructor Cockpit Wireframe (Vue 3 SPA)", fontsize=13, fontweight='bold', pad=15)
save_fig(fig, "fig4_15_cockpit_wireframe")

print("\n=== Extra diagrams generated ===")