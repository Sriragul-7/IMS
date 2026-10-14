#!/usr/bin/env python3
"""
Generate Project_Report.docx mirroring the OLD report's exact structure/layout,
swapping in THIS project's content:
 - Same front matter pages (Cover, Bonafide=i, Declaration=ii, Acknowledgement=iii, Abstract=iv, TOC=v-viii, LOF=ix, LOT=x)
 - Same chapter style: "CHAPTER I INTRODUCTION" (Roman numerals), sections "1.1 BACKGROUND" immediately followed by body text
 - Same figure/table caption format and position
 - ALL 16 pictures kept untouched (embedded as-is)
 - Table structure kept, only words replaced with this project's content
 - NO empty spaces between heading and body
Output: report/final_report/Project_Report.docx
"""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

APP_ROOT = "/home/sriragul/frappe-bench/apps/institution_erp"
FINAL_DIR = os.path.join(APP_ROOT, "report", "final_report")
IMAGES_DIR = os.path.join(FINAL_DIR, "images")
OUT_DOCX = os.path.join(FINAL_DIR, "Project_Report.docx")
os.makedirs(FINAL_DIR, exist_ok=True)

BODY_FONT = "Times New Roman"
HEAD_FONT = "Times New Roman"
BODY_SIZE = Pt(13)
HEAD_SIZE = Pt(14)
CAP_SIZE = Pt(13)
BLACK = RGBColor(0, 0, 0)
GRAY_FILL = "D9D9D9"

doc = Document()

# ---------- Base style: TNR 13 justified 1.5, no empty space ----------
normal = doc.styles["Normal"]
normal.font.name = BODY_FONT
normal.font.size = BODY_SIZE
normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
normal.paragraph_format.line_spacing = 1.5
normal.paragraph_format.space_before = Pt(0)
normal.paragraph_format.space_after = Pt(6)
normal.paragraph_format.first_line_indent = Cm(0)
rPr = normal.element.get_or_add_rPr()
rFonts = rPr.find(qn("w:rFonts"))
if rFonts is None:
    rFonts = OxmlElement("w:rFonts"); rPr.append(rFonts)
for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
    rFonts.set(qn(attr), BODY_FONT)

# ---------- Heading 1: Chapter - centered, caps, NO page break before, tight ----------
h1 = doc.styles["Heading 1"]
h1.font.name = HEAD_FONT
h1.font.size = HEAD_SIZE
h1.font.bold = True
h1.font.italic = False
h1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
h1.paragraph_format.line_spacing = 1.5
h1.paragraph_format.space_before = Pt(0)
h1.paragraph_format.space_after = Pt(4)
h1.paragraph_format.page_break_before = False
rPr = h1.element.get_or_add_rPr()
rFonts = rPr.find(qn("w:rFonts"))
if rFonts is None:
    rFonts = OxmlElement("w:rFonts"); rPr.append(rFonts)
for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
    rFonts.set(qn(attr), HEAD_FONT)
caps = OxmlElement("w:caps"); caps.set(qn("w:val"), "true"); rPr.append(caps)

# ---------- Heading 2: Section - left, caps, tight ----------
h2 = doc.styles["Heading 2"]
h2.font.name = HEAD_FONT
h2.font.size = HEAD_SIZE
h2.font.bold = True
h2.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
h2.paragraph_format.line_spacing = 1.5
h2.paragraph_format.space_before = Pt(0)
h2.paragraph_format.space_after = Pt(4)
rPr = h2.element.get_or_add_rPr()
rFonts = rPr.find(qn("w:rFonts"))
if rFonts is None:
    rFonts = OxmlElement("w:rFonts"); rPr.append(rFonts)
for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
    rFonts.set(qn(attr), HEAD_FONT)
caps = OxmlElement("w:caps"); caps.set(qn("w:val"), "true"); rPr.append(caps)

# ---------- Heading 3: Subsection - left, sentence case, tight ----------
h3 = doc.styles["Heading 3"]
h3.font.name = HEAD_FONT
h3.font.size = HEAD_SIZE
h3.font.bold = True
h3.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
h3.paragraph_format.line_spacing = 1.5
h3.paragraph_format.space_before = Pt(0)
h3.paragraph_format.space_after = Pt(4)
rPr = h3.element.get_or_add_rPr()
rFonts = rPr.find(qn("w:rFonts"))
if rFonts is None:
    rFonts = OxmlElement("w:rFonts"); rPr.append(rFonts)
for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
    rFonts.set(qn(attr), HEAD_FONT)

# ---------- Section: A4 portrait ----------
sec = doc.sections[0]
sec.page_width = Cm(21.0); sec.page_height = Cm(29.7)
sec.orientation = WD_ORIENT.PORTRAIT
sec.top_margin = Cm(2.54); sec.bottom_margin = Cm(2.54)
sec.left_margin = Cm(3.175); sec.right_margin = Cm(2.54)
sec.header_distance = Cm(1.27); sec.footer_distance = Cm(1.27)

# ---------- Helpers ----------
def set_cell_shading(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)

def set_cell_margins(cell, top=60, bottom=60, left=110, right=110):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for tag, val in (("top", top), ("bottom", bottom), ("start", left), ("end", right), ("left", left), ("right", right)):
        node = OxmlElement(f"w:{tag}"); node.set(qn("w:w"), str(val)); node.set(qn("w:type"), "dxa"); tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, sz=4, color="000000"):
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}"); el.set(qn("w:val"), "single"); el.set(qn("w:sz"), str(sz)); el.set(qn("w:space"), "0"); el.set(qn("w:color"), color); borders.append(el)
    tblPr.append(borders)

def set_repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    th = OxmlElement("w:tblHeader"); th.set(qn("w:val"), "true"); trPr.append(th)

def run_font(run, size=BODY_SIZE, bold=False, italic=False, font=BODY_FONT, color=BLACK, caps=False):
    run.font.name = font; run.font.size = size; run.font.bold = bold; run.font.italic = italic
    run.font.color.rgb = color
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts"); rPr.append(rFonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(attr), font)
    if caps:
        ce = OxmlElement("w:caps"); ce.set(qn("w:val"), "true"); rPr.append(ce)
    return run

def add_field_instr(paragraph, instr):
    f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = instr
    f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "separate")
    t = OxmlElement("w:t"); t.text = "Update field to populate."
    f3 = OxmlElement("w:fldChar"); f3.set(qn("w:fldCharType"), "end")
    r = paragraph.add_run(); r._r.append(f1); r._r.append(it); r._r.append(f2)
    r2 = paragraph.add_run(); r2._r.append(t)
    r3 = paragraph.add_run(); r3._r.append(f3)
    for rr in (r, r2, r3):
        run_font(rr, size=Pt(12), font=BODY_FONT)

def add_page_field(paragraph):
    f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = " PAGE "
    f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "separate")
    t = OxmlElement("w:t"); t.text = "1"
    f3 = OxmlElement("w:fldChar"); f3.set(qn("w:fldCharType"), "end")
    r = paragraph.add_run(); r._r.append(f1); r._r.append(it); r._r.append(f2)
    r2 = paragraph.add_run(); r2._r.append(t)
    r3 = paragraph.add_run(); r3._r.append(f3)
    for rr in (r, r2, r3):
        run_font(rr, size=Pt(12), font=BODY_FONT)

def body(text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=BODY_SIZE, bold=False, italic=False,
         space_after=6, space_before=0, font=BODY_FONT):
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.line_spacing = 1.5; pf.space_before = Pt(space_before); pf.space_after = Pt(space_after); pf.first_line_indent = Cm(0)
    run = p.add_run(text)
    run_font(run, size=size, bold=bold, italic=italic, font=font)
    return p

def heading(text, level):
    p = doc.add_paragraph(style=f"Heading {level}")
    run = p.add_run(text)
    run_font(run, size=HEAD_SIZE, bold=True, font=HEAD_FONT)
    return p

def caption(label, num, title):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(6); p.paragraph_format.line_spacing = 1.0
    rl = p.add_run(f"{label} {num}. ")
    run_font(rl, size=CAP_SIZE, bold=True, font=HEAD_FONT)
    rt = p.add_run(title)
    run_font(rt, size=CAP_SIZE, bold=False, font=HEAD_FONT)
    return p

def table_caption(num, title):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4); p.paragraph_format.space_after = Pt(4); p.paragraph_format.line_spacing = 1.0
    rl = p.add_run(f"Table {num}. ")
    run_font(rl, size=CAP_SIZE, bold=True, font=HEAD_FONT)
    rt = p.add_run(title)
    run_font(rt, size=CAP_SIZE, bold=False, font=HEAD_FONT)
    return p

def insert_image(path, width_cm=13.0, fig_num=None, title=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4); p.paragraph_format.space_after = Pt(2)
    run = p.add_run()
    run.add_picture(path, width=Cm(width_cm))
    if fig_num and title:
        caption("Figure", fig_num, title)
    return p

def make_table(headers, rows, widths_cm=None, font_size=Pt(10)):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table)
    hdr = table.rows[0]
    set_repeat_header(hdr)
    for i, h in enumerate(headers):
        cell = hdr.cells[i]
        set_cell_margins(cell)
        set_cell_shading(cell, GRAY_FILL)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        cp = cell.paragraphs[0]
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.space_after = Pt(0); cp.paragraph_format.space_before = Pt(0)
        run = cp.add_run(h); run_font(run, size=font_size, bold=True, font=HEAD_FONT)
    for row in rows:
        cells = table.add_row().cells
        for i, val in enumerate(row):
            cell = cells[i]
            set_cell_margins(cell)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            cp = cell.paragraphs[0]
            cp.alignment = WD_ALIGN_PARAGRAPH.LEFT if i == 0 else WD_ALIGN_PARAGRAPH.CENTER
            cp.paragraph_format.space_after = Pt(0); cp.paragraph_format.space_before = Pt(0)
            run = cp.add_run(str(val)); run_font(run, size=font_size, font=BODY_FONT)
    if widths_cm:
        for i, w in enumerate(widths_cm):
            for row in table.rows:
                row.cells[i].width = Cm(w)
    return table

def new_section(fmt, start=1):
    s = doc.add_section(WD_SECTION.NEW_PAGE)
    s.page_width = Cm(21.0); s.page_height = Cm(29.7)
    s.orientation = WD_ORIENT.PORTRAIT
    s.top_margin = Cm(2.54); s.bottom_margin = Cm(2.54)
    s.left_margin = Cm(3.175); s.right_margin = Cm(2.54)
    s.header_distance = Cm(1.27); s.footer_distance = Cm(1.27)
    sectPr = s._sectPr
    for old in sectPr.findall(qn("w:pgNumType")):
        sectPr.remove(old)
    pg = OxmlElement("w:pgNumType"); pg.set(qn("w:fmt"), fmt); pg.set(qn("w:start"), str(start)); sectPr.append(pg)
    f = s.footer; f.is_linked_to_previous = False
    fp = f.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_page_field(fp)
    return s

print("Framework ready.")

# ===========================================================================
# FRONT MATTER (exact copy of old report structure)
# ===========================================================================

def cover_block():
    """Cover page - unnumbered, matches old report layout exactly."""
    for _ in range(4):
        body("", space_after=16)
    p = body("TITLE OF PROJECT REPORT", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(18), bold=True,
             space_after=18, space_before=0)
    run_font(p.runs[0], size=Pt(18), bold=True, font=BODY_FONT, caps=True)
    body("PROJECT REPORT", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), space_after=14)
    body("Submitted by", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), italic=True, space_after=14)
    body("[STUDENT NAME]", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(16), space_after=10)
    body("[REGISTER NO]", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), space_after=18)
    body("In partial fulfilment for the award of the degree of", align=WD_ALIGN_PARAGRAPH.CENTER,
         size=Pt(14), italic=True, space_after=0)
    body("BACHELOR OF ENGINEERING", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(16), space_after=0)
    body("in", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), italic=True, space_after=0)
    body("ELECTRONICS AND COMMUNICATION ENGINEERING", align=WD_ALIGN_PARAGRAPH.CENTER,
         size=Pt(14), space_after=18)
    body("BANNARI AMMAN INSTITUTE OF TECHNOLOGY", align=WD_ALIGN_PARAGRAPH.CENTER,
         size=Pt(16), bold=True, space_after=0)
    body("(An Autonomous Institution Affiliated to Anna University, Chennai)", align=WD_ALIGN_PARAGRAPH.CENTER,
         size=Pt(14), space_after=0)
    body("SATHYAMANGALAM-638401", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), space_after=0)
    body("ANNA UNIVERSITY: CHENNAI 600 025", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), space_after=14)
    body("OCTOBER 2026", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(16), space_after=0)

# COVER (unnumbered)
cover_block()

# ---- BONAFIDE CERTIFICATE (i, Roman) ----
s_roman = new_section("lowerRoman", 1)
body("BONAFIDE CERTIFICATE", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(16), bold=True,
     space_before=26, space_after=18)
body("Certified that this project report \u201cInstitution ERP \u2014 Student Information System and "
     "Institution Management Platform\u201d is the bonafide work of \u201c[STUDENT NAME] ([REGISTER NO])\u201d "
     "who carried out the project work under my supervision.", size=Pt(14), space_after=22)
body("", space_after=10)
body("<<Signature of the Head of Department>>                              <<Signature of the Supervisor>>",
     align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), space_after=6)
body("SIGNATURE                                                         SIGNATURE",
     align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), space_after=12)
body("[HOD NAME]                                                     [GUIDE NAME]",
     align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), space_after=6)
body("HEAD OF THE DEPARTMENT                                       SUPERVISOR",
     align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), space_after=6)
body("Department of Electronics and Communication Engineering      Department of Electronics and Communication Engineering",
     align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), space_after=6)
body("Bannari Amman Institute of Technology                         Bannari Amman Institute of Technology",
     align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), space_after=6)
body("<<Full address of the Department & College >>                 <<Full address of the Department & College >>",
     align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), space_after=16)
body("Submitted for Project Viva Voce examination held on \u2026\u2026\u2026\u2026 [VIVA DATE]",
     align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), space_after=0)
body("", space_after=10)
body("Internal Examiner I                                             Internal Examiner II",
     align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), space_after=0)
body("[EXAMINER 1]                                                    [EXAMINER 2]",
     align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), space_after=0)

# ---- DECLARATION (ii) ----
doc.add_page_break()
body("DECLARATION", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(16), bold=True,
     space_before=26, space_after=18)
body("We affirm that the project work titled \u201cInstitution ERP \u2014 Student Information System and "
     "Institution Management Platform\u201d being submitted in partial fulfilment for the award of the degree "
     "of Bachelor of Engineering in Electronics and Communication Engineering is the record of original work "
     "done by us under the guidance of [GUIDE NAME], [GUIDE DESIGNATION], Department of [DEPT NAME]. It has "
     "not formed a part of any other project work(s) submitted for the award of any degree or diploma, either "
     "in this or any other University.", size=Pt(14), space_after=26)
body("", space_after=8)
body("[STUDENT NAME]", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), space_after=0)
body("([REGISTER NO])", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), space_after=22)
body("", space_after=8)
body("(Signature of the Guide)", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), space_after=0)
body("[GUIDE NAME]", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), space_after=0)
body("[GUIDE DESIGNATION], [DEPT NAME]", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), space_after=0)
body("Bannari Amman Institute of Technology", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), space_after=0)
body("I certify that the declaration made above by the candidate is true.", align=WD_ALIGN_PARAGRAPH.CENTER,
     size=Pt(14), space_before=16, space_after=0)

# ---- ACKNOWLEDGEMENT (iii) ----
doc.add_page_break()
body("ACKNOWLEDGEMENT", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(16), bold=True,
     space_before=26, space_after=18)
body("We would like to express our heartfelt thanks to our esteemed Chairman [CHAIRMAN NAME] and the "
     "respected Principal [PRINCIPAL NAME], for providing excellent facilities and support during the course "
     "of study in this institute.", size=Pt(13), space_after=12)
body("We are grateful to [HOD NAME], Head of the Department, Department of Electronics and Communication "
     "Engineering, for his valuable suggestions that helped us carry out the project work successfully.",
     size=Pt(13), space_after=12)
body("We wish to express our sincere thanks to our Faculty guide [GUIDE NAME], [GUIDE DESIGNATION], "
     "Department of Electronics and Communication Engineering, for his constructive ideas, inspiration, "
     "encouragement, excellent guidance, and technical support that made it possible to complete this "
     "project work.", size=Pt(13), space_after=12)
body("We would like to thank our friends, faculty, and non-teaching staff who contributed directly and "
     "indirectly to the success of this project.", size=Pt(13), space_after=22)
body("", space_after=6)
body("[STUDENT NAME]", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), space_after=0)
body("([REGISTER NO])", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), space_after=0)

# ---- ABSTRACT (iv) ----
doc.add_page_break()
body("ABSTRACT", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), bold=True,
     space_before=14, space_after=10)
body("This project presents Institution ERP, a Student Information System and institution management "
     "platform built on Frappe v16 for Bannari Amman Institute of Technology. Institutional administration "
     "today depends on fragmented, manual processes that create data silos and increase the compliance "
     "burden. The aim of this work was to design and implement a unified system covering the full student "
     "lifecycle \u2014 from admissions inquiry through graduation \u2014 across academics, attendance, "
     "examinations, fees, library, hostel, transport, and institutional communication. The methodology "
     "adopts a hybrid architecture: a Vue 3 portal for students and guardians, role-specific Vue cockpits "
     "for staff, and a rebranded Frappe Desk for full CRUD operations. Row-level security is enforced "
     "through User Permissions and permission_query_conditions, with results publication gating controlling "
     "mark visibility. The implemented system comprises 48 DocTypes across 10 modules, 8 custom roles, "
     "11 whitelisted API methods, and 16 row-level permission conditions, deployed at zero infrastructure "
     "cost on an open-source stack. Results demonstrate secure role-scoped access, automated student and "
     "guardian creation on admission approval, automatic grade calculation, fee recomputation, and library "
     "fine handling.", size=Pt(13), space_after=8)
body("Keywords: Institution ERP, Student Information System, Frappe v16, Role-Based Access Control, "
     "permission_query_conditions, Vue 3.", align=WD_ALIGN_PARAGRAPH.LEFT, size=Pt(13), space_after=0)

# ---- TABLE OF CONTENTS (v-viii) ----
doc.add_page_break()
body("TABLE OF CONTENTS", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), bold=True,
     space_before=14, space_after=10)
toc_p = doc.add_paragraph(); toc_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
add_field_instr(toc_p, ' TOC \\o "1-3" \\h \\z \\u ')

# ---- LIST OF FIGURES (ix) ----
doc.add_page_break()
body("LIST OF FIGURES", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), bold=True,
     space_before=14, space_after=10)
lof_p = doc.add_paragraph()
add_field_instr(lof_p, ' TOC \\c "Figure" \\h \\z \\u ')

# ---- LIST OF TABLES (x) ----
doc.add_page_break()
body("LIST OF TABLES", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), bold=True,
     space_before=14, space_after=10)
lot_p = doc.add_paragraph()
add_field_instr(lot_p, ' TOC \\c "Table" \\h \\z \\u ')

# ---- ABBREVIATIONS (xi) ----
doc.add_page_break()
body("ABBREVIATIONS AND NOMENCLATURE", align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(14), bold=True,
     space_before=14, space_after=10)
abbr_rows = [
    ("ERP", "Enterprise Resource Planning"),
    ("SIS", "Student Information System"),
    ("DocType", "Document Type (Frappe data model entity)"),
    ("API", "Application Programming Interface"),
    ("UI", "User Interface"),
    ("CRUD", "Create, Read, Update, Delete"),
    ("RBAC", "Role-Based Access Control"),
    ("SPA", "Single-Page Application"),
    ("LMS", "Learning Management System"),
    ("JWT", "JSON Web Token"),
]
make_table(["Abbreviation", "Expansion / Meaning"], abbr_rows, widths_cm=[4.0, 12.5],
           font_size=Pt(11))

print("Front matter ready.")

# ===========================================================================
# MAIN BODY: Arabic page numbering from Chapter 1
# ===========================================================================
s_arabic = new_section("decimal", 1)

ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]

# ===========================================================================
# CHAPTER I: INTRODUCTION
# ===========================================================================
doc.add_page_break()
heading(f"CHAPTER {ROMAN[0]}", 1)
heading("INTRODUCTION", 1)

body("Higher education administration in India depends heavily on manual, paper-based, and fragmented "
     "digital systems. Admissions, academics, attendance, examinations, fees, library, hostel, transport, "
     "and institutional communication are often maintained through separate spreadsheets, registers, and "
     "standalone applications that do not share data. This fragmentation creates data silos, duplicates "
     "effort, slows decision-making, and increases the compliance burden on institutions. There is a clear "
     "need for an integrated Enterprise Resource Planning (ERP) system that unifies the entire student "
     "lifecycle \u2014 from first enquiry through graduation \u2014 within a single, secure, role-scoped "
     "platform.", space_after=10)

body("Bannari Amman Institute of Technology (BIT), the demo brand for this project, administers multiple "
     "programs, courses, student groups, instructors, and thousands of academic and financial records each "
     "year. Managing these records across disconnected systems leads to inconsistent student data, "
     "difficulty in producing consolidated reports, and limited visibility for students and guardians into "
     "attendance, results, and fees. Existing institutional software is often either too generic to reflect "
     "Indian academic workflows (entrance tests, fee structures, results publication gating) or too "
     "expensive and rigid to deploy at scale. A purpose-built Student Information System (SIS) on an "
     "open-source, extensible platform addresses these gaps.", space_after=10)

body("In the Indian higher-education context, the problem is compounded by regulatory and accreditation "
     "requirements. Institutions must submit data to statutory bodies, maintain attendance percentages for "
     "university compliance, track fee collections for financial audits, and produce examination result "
     "sheets for degree certification. Manual processes make these reporting obligations error-prone and "
     "time-consuming. Staff spend disproportionate effort on data entry and reconciliation rather than on "
     "student-facing academic work. A unified ERP reduces this administrative overhead, improves data "
     "accuracy, and gives leadership real-time visibility into institutional operations.", space_after=10)
body("Furthermore, students and guardians currently have no self-service access to their records. A student "
     "must visit the office to check attendance, results, or fee dues. A guardian with multiple children "
     "must maintain separate logins or rely on the student to relay information. This lack of transparency "
     "erodes trust and increases administrative queries. A student and guardian portal with row-level "
     "scoping addresses this directly, giving each stakeholder secure, immediate access to their own data.",
     space_after=10)

heading("1.1 BACKGROUND", 2)
body("Educational institutions operate as complex organizations with interdependent functions. The "
     "admissions function manages inquiries, applications, entrance tests, and approvals. The academics "
     "function manages programs, courses, schedules, instructors, and student groups. The attendance "
     "function records student and staff presence. The examination function manages grading scales, "
     "assessment plans, marks entry, and result publication. The fees function manages fee structures, "
     "schedules, invoices, payments, and discounts. The library function manages books, memberships, "
     "issues, returns, and fines. The hostel function manages rooms and allocations. The transport "
     "function manages vehicles, routes, and student allocations. The communication function manages "
     "notices, feedback, and institutional dashboards.", space_after=10)
body("When these functions run on disconnected systems, a student's record may exist in multiple places "
     "with conflicting values. A change of address or program in one system does not propagate to others. "
     "Generating a consolidated view of a student \u2014 attendance, results, fees, and library status \u2014 "
     "requires manual reconciliation across registers and spreadsheets. This inefficiency motivates a "
     "unified platform where every module shares a single source of truth.", space_after=10)

heading("1.2 PROBLEM STATEMENT", 2)
body("Existing institution management solutions \u2014 including ERPNext Education, openSIS, Fedena, and "
     "Moodle-based setups \u2014 are either overly heavy and tightly coupled, lack Indian academic workflows, "
     "or provide only a learning-management perspective without comprehensive administration, finance, "
     "hostel, and transport modules. ERPNext Education is tightly coupled to the broader ERPNext ecosystem, "
     "making customisation for Indian academic workflows complex. openSIS is open source but has a dated "
     "user interface and limited extensibility. Fedena is a commercial Ruby on Rails school ERP whose "
     "licensing restricts deployment for budget-constrained institutions. Moodle-based setups provide a "
     "strong learning-management foundation but cover administration, fees, hostel, and transport only "
     "weakly when extended beyond course delivery.", space_after=10)
body("None of these offers a hybrid staff interface that combines focused role-specific cockpits with full "
     "CRUD access through a rebranded Frappe Desk, together with a student and guardian portal that "
     "enforces row-level data scoping at the database level. Table 1.1 compares these existing solutions "
     "against the requirements of a modern institution ERP.", space_after=6)
table_caption("1.1", "Comparison of Existing ERP Solutions")
make_table(
    ["Solution", "Core Strength", "Key Limitation", "Relevance to This Project"],
    [
        ["ERPNext Education", "Comprehensive ERP with education domain", "Tight coupling; complex to customise", "Reference for modular ERP structure"],
        ["openSIS", "Open-source student information system", "Dated UI; limited extensibility", "Reference for SIS data model"],
        ["Fedena", "Ruby on Rails; commercial school ERP", "Commercial licensing; limited customisation", "Reference for role-based access"],
        ["Moodle-based SIS", "Strong LMS foundation", "Weak administration, fees, hostel, transport coverage", "Reference for student portal UI"],
        ["Institution ERP (Proposed)", "Frappe v16 metadata-driven; hybrid UI; row-level security", "New implementation; future scope documented", "This project"],
    ],
    widths_cm=[3.0, 3.6, 3.8, 4.1], font_size=Pt(10))

heading("1.3 OBJECTIVES", 2)
body("The objectives of this project are:", space_after=6)
for obj in [
    "To design and implement a unified Student Information System covering the complete student lifecycle "
    "from admission inquiry to graduation.",
    "To implement role-based access control with row-level security so that students, guardians, and staff "
    "see only the data they are authorised to view.",
    "To deliver a hybrid staff interface combining role-specific Vue 3 cockpits for high-frequency actions "
    "with a rebranded Frappe Desk for full CRUD operations.",
    "To provide Student and Guardian portals with data scoping through permission_query_conditions and "
    "results publication gating for examination marks.",
    "To deploy the system at zero infrastructure cost using an entirely open-source stack (Frappe v16, "
    "Python, MariaDB, Redis, Vue 3, Nginx).",
]:
    p = doc.add_paragraph(style="List Bullet")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.left_indent = Cm(0.75)
    run = p.add_run(obj); run_font(run, size=BODY_SIZE, font=BODY_FONT)

heading("1.4 SCOPE", 2)
body("The system scope comprises 10 modules \u2014 Admissions, Student Information System (SIS), Academics, "
     "Attendance, Examination, Fees, Library, Hostel, Transport, and Communication \u2014 implemented "
     "through 48 DocTypes, 8 custom roles (6 staff roles and 2 portal roles), 6 script reports, 11 "
     "whitelisted API methods, and 16 permission_query_conditions covering 19 DocTypes. The demo brand is "
     "Bannari Amman Institute of Technology, deployed on site institution.localhost.", space_after=10)

heading("1.5 MOTIVATION", 2)
body("The motivation for this project is twofold. Institutionally, BIT requires a branded, integrated "
     "system to replace fragmented record-keeping across departments. Academically, the work satisfies the "
     "capstone project requirement for the Bachelor of Engineering degree, providing practical experience "
     "in full-stack development, database design, access control, and software testing on a live Frappe v16 "
     "site. The project demonstrates that a complete institution management system can be built and "
     "deployed at zero infrastructure cost using an open-source frontend and backend stack.", space_after=10)

heading("1.6 REPORT ORGANISATION", 2)
body("The remainder of this report is organised as follows. Chapter 2 presents the literature survey and "
     "identifies the research gap. Chapter 3 defines the system requirements, including functional and "
     "non-functional requirements, hardware and software requirements, and the tools and technologies used. "
     "Chapter 4 covers system analysis and design, including architecture, module design, role-based access "
     "model, database design, data flow, use case, sequence, and activity diagrams. Chapter 5 details the "
     "implementation, module by module, together with the permission model, workflow engine, automation, "
     "the student/guardian portal, staff cockpits, and the staged build method. Chapter 6 presents the "
     "testing strategy, test cases, security testing, and results. Chapter 7 discusses the results, "
     "screenshots, and limitations observed. Chapter 8 states the conclusion and future enhancements. "
     "References and appendices follow the main chapters.", space_after=10)

heading("1.7 SIGNIFICANCE OF THE STUDY", 2)
body("This study is significant because it addresses a widespread problem in Indian higher education: the "
     "absence of an affordable, integrated, and role-secured student information system. Most institutions "
     "rely on manual registers or expensive commercial ERPs that are difficult to customise. Institution "
     "ERP demonstrates that a complete system can be built on entirely open-source software at zero "
     "infrastructure cost, making it accessible to institutions of all sizes.", space_after=10)
body("The study contributes a working model of row-level security implemented at the database level through "
     "permission_query_conditions, a hybrid staff interface combining role-specific cockpits with a "
     "rebranded Frappe Desk, and a results publication gating mechanism for examination marks. These "
     "contributions can be reused by other institutions building similar systems on Frappe v16.", space_after=10)
body("Practically, the system reduces administrative overhead by eliminating duplicate data entry across "
     "departments, improves data accuracy through a single source of truth, and gives students and "
     "guardians self-service access to attendance, results, fees, and library records. For the institution, "
     "it provides real-time visibility into academic and financial operations through dashboards and "
     "reports.", space_after=10)

heading("1.8 LIMITATIONS AND DELIMITATIONS", 2)
body("The study is delimited to the Bannari Amman Institute of Technology as the demo brand and to the "
     "Frappe v16 platform. It does not cover integration with external systems such as payment gateways, "
     "SMS/email gateways, or biometric attendance devices, as these are outside the scope of the capstone "
     "project. The system is evaluated using demo data rather than live institutional data, so performance "
     "under large-scale concurrent load has not been tested. These limitations are documented in Chapter 7 "
     "and are proposed for future enhancement.", space_after=10)

print("Chapter I ready.")


# ===========================================================================
# CHAPTER II: LITERATURE SURVEY
# ===========================================================================
doc.add_page_break()
heading(f"CHAPTER {ROMAN[1]}", 1)
heading("LITERATURE SURVEY", 1)

body("This chapter surveys existing institution management and student information systems relevant to the "
     "proposed problem statement. Each source is cited using the author-year format. The chapter concludes "
     "with constructive criticism, gap identification, and a summary of the proposed solution.", space_after=10)

heading("2.2 EXISTING WORKS", 2)
body("ERPNext Education provides a comprehensive ERP with an education domain module covering students, "
     "courses, assessments, and fees. It is tightly coupled to the broader ERPNext ecosystem, which makes "
     "customisation for Indian academic workflows complex and time-consuming [2]. openSIS is an open-source "
     "student information system that maintains student records, grades, and attendance, but its user "
     "interface is dated and extensibility is limited [3]. Fedena, built on Ruby on Rails, is a commercial "
     "school ERP with role-based access, but commercial licensing restricts deployment for "
     "budget-constrained institutions [4]. Moodle-based setups provide a strong learning-management "
     "foundation but cover administration, fees, hostel, and transport only weakly when extended beyond "
     "course delivery [5].", space_after=10)
body("Frappe Framework, the platform selected for this project, provides a metadata-driven DocType model, "
     "a built-in permission system, and a web desk that accelerates development of data-intensive "
     "applications [1]. Role-based access control (RBAC) is an established model for educational systems, "
     "where permissions are assigned to roles rather than individual users [6]. Hybrid UI patterns, "
     "combining focused dashboards with full-featured administrative interfaces, improve usability in "
     "enterprise applications [7].", space_after=10)

table_caption("2.1", "Literature Comparison Matrix")
make_table(
    ["System", "Licensing", "Architecture", "Student Portal", "Fee/Finance", "Hostel/Transport", "Extensibility", "Indian Academic Workflow"],
    [
        ["ERPNext Education", "Open source", "Frappe/ERPNext", "Limited", "Partial", "Partial", "High", "Partial"],
        ["openSIS", "Open source", "PHP/MySQL", "Basic", "No", "No", "Medium", "No"],
        ["Fedena", "Commercial", "Ruby on Rails", "Yes", "Yes", "Partial", "Medium", "No"],
        ["Moodle-based SIS", "Open source", "PHP/MySQL", "Yes", "No", "No", "High", "No"],
        ["Institution ERP (Proposed)", "MIT (open source)", "Frappe v16 + Vue 3", "Yes (scoped)", "Yes", "Yes", "High", "Yes"],
    ],
    widths_cm=[2.4, 1.8, 2.1, 1.9, 1.7, 2.0, 1.9, 2.2], font_size=Pt(9))

heading("2.3 GAP IDENTIFICATION", 2)
body("No existing system combines all of the following: (a) Frappe's metadata-driven agility and DocType "
     "data model; (b) Indian academic workflows such as entrance tests, fee structures, schedules, and "
     "results publication gating; (c) a hybrid staff interface of role-specific Vue cockpits plus a "
     "rebranded Frappe Desk; (d) student and guardian portals with row-level data scoping enforced at the "
     "database level through permission_query_conditions; and (e) zero-cost deployment on an open-source "
     "stack. This research gap motivates the proposed Institution ERP.", space_after=10)
body("The gap is significant because each missing capability addresses a real administrative pain point. "
     "Without metadata-driven agility, adding a new academic entity (for example, a new assessment type or "
     "a new fee component) requires schema changes and developer intervention. Without Indian academic "
     "workflows, institutions must maintain parallel manual processes for entrance tests and result "
     "publication. Without row-level data scoping at the database level, a determined user could bypass UI "
     "restrictions and access another student's records through direct API calls. Without zero-cost "
     "deployment, many institutions cannot afford the solution at all. Institution ERP closes every one of "
     "these gaps.", space_after=10)

heading("2.4 PROPOSED SOLUTION SUMMARY", 2)
body("Institution ERP addresses the identified gaps through a staged build method, a hybrid UI architecture, "
     "dual permission mechanisms (User Permissions plus permission_query_conditions), results publication "
     "gating, and automated student/guardian creation on admission approval. The design and implementation "
     "of these features are detailed in Chapters 4 and 5.", space_after=10)

print("Chapter II ready.")

# ===========================================================================
# CHAPTER III: SYSTEM REQUIREMENTS
# ===========================================================================
doc.add_page_break()
heading(f"CHAPTER {ROMAN[2]}", 1)
heading("SYSTEM REQUIREMENTS", 1)

body("This chapter defines the functional and non-functional requirements of Institution ERP, together "
     "with hardware and software requirements and the tools and technologies used. All version numbers "
     "were verified against the live project documentation and site.", space_after=10)

heading("3.2 FUNCTIONAL REQUIREMENTS", 2)
body("The following functional requirements (FR) were derived from the literature survey and the problem "
     "statement. Each requirement is mapped to a priority and the module responsible for its implementation.",
     space_after=6)
table_caption("3.1", "Functional Requirements List")
make_table(
    ["FR-ID", "Requirement", "Priority", "Module"],
    [
        ["FR-01", "Admission inquiry \u2192 applicant \u2192 entrance test \u2192 approval workflow", "High", "Admissions"],
        ["FR-02", "Auto-create Student and Guardian records on applicant approval", "High", "Admissions/SIS"],
        ["FR-03", "Student and Guardian master records with unique naming", "High", "SIS"],
        ["FR-04", "Program, course, academic year/term, room, instructor, student group management", "High", "Academics"],
        ["FR-05", "Course scheduling with double-booking prevention", "High", "Academics"],
        ["FR-06", "Student and staff attendance marking with duplicate prevention", "High", "Attendance"],
        ["FR-07", "Grading scales, assessment plans, bulk marks entry, auto grade calculation", "High", "Examination"],
        ["FR-08", "Results publication gating (results_published flag)", "High", "Examination"],
        ["FR-09", "Fee structures, schedules, invoices, payments, discounts, auto-recompute", "High", "Fees"],
        ["FR-10", "Fee Dues Report and outstanding tracking", "Medium", "Fees"],
        ["FR-11", "Library catalog, membership, issue/return with overdue fines", "Medium", "Library"],
        ["FR-12", "Hostel room allocation and occupancy tracking", "Medium", "Hostel"],
        ["FR-13", "Transport routes, vehicles, and student allocation", "Medium", "Transport"],
        ["FR-14", "Audience-targeted notices, communication log, feedback", "Medium", "Communication"],
        ["FR-15", "Student and Guardian portals with row-level data scoping", "High", "Portal"],
        ["FR-16", "Role-based access with User Permissions and permission_query_conditions", "High", "Security"],
        ["FR-17", "Staff cockpits with quick actions and \u2018Open Full Desk\u2019", "High", "UI"],
        ["FR-18", "Rebranded Frappe Desk (Inter font, BIT blue)", "Medium", "UI"],
        ["FR-19", "Automation: grade calculation, fee recompute, user creation, status backfill", "Medium", "Automation"],
        ["FR-20", "Institution Overview dashboard with number cards and charts", "Medium", "Communication"],
        ["FR-21", "Responsive design for desktop, tablet, and mobile", "Medium", "UI"],
        ["FR-22", "Staged build with end-to-end tests per stage", "High", "Process"],
        ["FR-23", "Demo data generation and reset", "Medium", "Process"],
        ["FR-24", "Cross-access blocked by permission_query_conditions", "High", "Security"],
        ["FR-25", "Guardian child switcher for multiple linked students", "Medium", "Portal"],
    ],
    widths_cm=[1.5, 6.6, 1.5, 4.9], font_size=Pt(9))

heading("3.3 NON-FUNCTIONAL REQUIREMENTS", 2)
body("Non-functional requirements define the qualities the system must exhibit rather than specific "
     "behaviours. These were validated during testing (Chapter 6).", space_after=6)
table_caption("3.2", "Non-Functional Requirements")
make_table(
    ["NFR-ID", "Requirement", "Target"],
    [
        ["NFR-01", "Performance: API response time under 300 ms under normal load", "< 300 ms"],
        ["NFR-02", "Security: JWT authentication, bcrypt password hashing, RBAC", "Industry standard"],
        ["NFR-03", "Scalability: MariaDB and Redis backend", "Supported"],
        ["NFR-04", "Usability: responsive design, intuitive cockpits", "WCAG-aligned"],
        ["NFR-05", "Maintainability: modular DocTypes, typed controllers, documented hooks", "Maintainable"],
        ["NFR-06", "Deployability: zero-cost open-source stack, bench-based deployment", "Zero cost"],
        ["NFR-07", "Reliability: field-level validation, duplicate prevention, transactions", "Zero data corruption"],
        ["NFR-08", "Availability: site accessible at institution.localhost during demo", "High"],
        ["NFR-09", "Auditability: communication log and feedback tracking", "Complete"],
        ["NFR-10", "Compatibility: modern browsers", "All major"],
        ["NFR-11", "Portability: bench install on Ubuntu 22.04 LTS", "Supported"],
        ["NFR-12", "Observability: dashboard charts and number cards", "Available"],
    ],
    widths_cm=[1.8, 9.4, 3.3], font_size=Pt(9.5))

heading("3.4 HARDWARE REQUIREMENTS", 2)
body("The system runs on commodity cloud infrastructure. No dedicated hardware was procured. The minimum "
     "server configuration is 2 vCPU, 4 GB RAM, and 50 GB SSD. The client side requires any modern web "
     "browser. The system is designed for zero hardware cost deployment.", space_after=10)

heading("3.5 SOFTWARE REQUIREMENTS", 2)
body("All software components are open source. Version numbers were verified against the live project "
     "documentation and site.", space_after=6)
table_caption("3.3", "Software Stack Versions (verified live)")
make_table(
    ["Layer", "Component", "Version"],
    [
        ["Operating System", "Ubuntu", "22.04 LTS"],
        ["Backend Runtime", "Python", "3.10+"],
        ["Framework", "Frappe", "v16.26.3"],
        ["Database", "MariaDB", "10.6+"],
        ["Cache/Queue", "Redis", "7+"],
        ["Frontend Runtime", "Node.js", "18+"],
        ["Portal Framework", "Vue 3", "3.4+"],
        ["Portal Build Tool", "Vite", "5+"],
        ["Web Server", "Nginx", "Latest stable"],
        ["Testing", "pytest / Playwright", "Latest stable"],
        ["CI", "GitHub Actions", "\u2014"],
    ],
    widths_cm=[3.2, 4.2, 7.1], font_size=Pt(10))

heading("3.6 TOOLS AND TECHNOLOGIES", 2)
body("Backend tools include Python, the Frappe ORM, MariaDB, Redis, Gunicorn, and Nginx. Frontend tools "
     "include Vue 3, Vite, and a hand-written CSS design system (no Tailwind dependency). Testing uses "
     "pytest and Playwright; continuous integration uses GitHub Actions. Version control is Git. Figure "
     "3.1 summarises the technology stack.", space_after=6)
img_path = os.path.join(IMAGES_DIR, "fig3_1_tech_stack.png")
if os.path.exists(img_path):
    insert_image(img_path, width_cm=13.0, fig_num="3.1", title="Technology Stack Diagram")

heading("3.7 REQUIREMENTS RATIONALE", 2)
body("Each functional requirement was derived from a concrete institutional need. FR-01 through FR-05 "
     "cover admissions and academics because these are the entry points into the student lifecycle \u2014 "
     "without a reliable admission and academic foundation, no other module can operate. FR-06 through "
     "FR-08 cover attendance and examination because these are the core academic delivery functions that "
     "students and guardians most frequently inquire about. FR-09 through FR-10 cover fees because "
     "financial sustainability and fee collection tracking are critical for institutional operations. "
     "FR-11 through FR-13 cover library, hostel, and transport because these are auxiliary services that "
     "complete the student experience. FR-14 through FR-16 cover communication, portal access, and "
     "security because these determine how stakeholders interact with and trust the system. FR-17 through "
     "FR-21 cover the user interface and experience because a system that is difficult to use will not be "
     "adopted. FR-22 through FR-25 cover process, security, and portal features that ensure the system can "
     "be built, tested, deployed, and operated reliably.", space_after=10)

print("Chapter III ready.")

# ===========================================================================
# CHAPTER IV: SYSTEM ANALYSIS AND DESIGN
# ===========================================================================
doc.add_page_break()
heading(f"CHAPTER {ROMAN[3]}", 1)
heading("SYSTEM ANALYSIS AND DESIGN", 1)

body("This chapter presents the system analysis and design: overall architecture, module architecture, "
     "role-based access model, database design, data flow diagrams, use case diagram, sequence diagrams, "
     "activity diagrams, and the UI design approach. Diagrams were generated from the verified DocType and "
     "module structure of the live project.", space_after=10)

heading("4.2 OVERALL ARCHITECTURE", 2)
body("The system follows a four-layer architecture. The Presentation Layer comprises the Vue 3 SPA portal "
     "(Student/Guardian), Vue 3 staff cockpits, and the rebranded Frappe Desk. The API Layer exposes 11 "
     "whitelisted methods and the Frappe REST API for DocType CRUD. The Business Logic Layer implements "
     "DocType controllers (22 files with validation), Frappe hooks, and 16 permission_query_conditions. "
     "The Data Layer uses MariaDB for persistent storage and Redis for caching and background jobs.",
     space_after=6)
for n, t, f in [("4.1", "System Architecture Diagram", "fig4_1_sys_arch.png"),
                ("4.2", "Module Dependency Graph", "fig4_2_module_dep.png")]:
    img_path = os.path.join(IMAGES_DIR, f)
    if os.path.exists(img_path):
        insert_image(img_path, width_cm=13.0, fig_num=n, title=t)

heading("4.3 MODULE ARCHITECTURE", 2)
body("Ten modules organise the DocTypes by domain: Academics (10 DocTypes), SIS (2), Admissions (5), "
     "Attendance (2), Examination (5), Fees (9), Library (4), Hostel (3), Transport (4), and Communication "
     "(4) \u2014 48 DocTypes in total. Modules depend on SIS (Student, Guardian) and Academics (Program, "
     "Course, Student Group, Academic Year). Table 4.1 summarises the DocType count per module.",
     space_after=6)
table_caption("4.1", "DocType Count per Module")
make_table(
    ["Module", "DocTypes", "Core Purpose"],
    [
        ["Academics", "10", "Programs, courses, scheduling, instructor assignment, student groups"],
        ["SIS", "2", "Student and Guardian master records"],
        ["Admissions", "5", "Inquiry \u2192 application \u2192 entrance test \u2192 approval"],
        ["Attendance", "2", "Student and staff attendance"],
        ["Examination", "5", "Grading scales, assessment plans, marks entry, results"],
        ["Fees", "9", "Fee structures, schedules, invoices, payments, discounts"],
        ["Library", "4", "Book catalog, membership, issue/return, fines"],
        ["Hostel", "3", "Hostel/room management, occupancy tracking"],
        ["Transport", "4", "Vehicle registry, routes, student allocation"],
        ["Communication", "4", "Notices, dispatch, feedback, dashboard"],
        ["Total", "48", "All modules combined"],
    ],
    widths_cm=[2.6, 2.0, 9.9], font_size=Pt(9.5))

heading("4.4 ROLE-BASED ACCESS MODEL", 2)
body("Eight custom roles are defined (6 staff, 2 portal) alongside the built-in System Manager and "
     "Administrator. Staff roles have Desk access; portal roles (Student, Guardian) do not. Security is "
     "enforced through two layers: User Permissions (linking portal users to their own or linked Student "
     "records) and permission_query_conditions (16 SQL WHERE-clause functions covering 19 DocTypes). "
     "Table 4.2 summarises the roles; Figure 4.3 presents the role-permission matrix.", space_after=6)
table_caption("4.2", "Role Summary")
make_table(
    ["Role", "Desk Access", "Primary Modules", "Scope"],
    [
        ["System Manager", "Yes", "All modules", "Full access"],
        ["Academic Head", "Yes", "Academics, Examination", "Read all; write academics/exam"],
        ["Admissions Officer", "Yes", "Admissions", "Full CRUD on admissions pipeline"],
        ["Instructor", "Yes", "Academics, Attendance, Examination", "Attendance/assessment for own groups"],
        ["Fee Manager", "Yes", "Fees", "Full CRUD on all fee DocTypes"],
        ["Facility Manager", "Yes", "Library, Hostel, Transport", "Full CRUD on facility DocTypes"],
        ["Communication Officer", "Yes", "Communication", "Notices, log, feedback"],
        ["Student", "No (portal)", "All (scoped)", "Read-only own records"],
        ["Guardian", "No (portal)", "All (scoped)", "Read-only linked students"],
    ],
    widths_cm=[2.9, 1.9, 4.3, 5.4], font_size=Pt(9.5))
img_path = os.path.join(IMAGES_DIR, "fig4_3_role_matrix.png")
if os.path.exists(img_path):
    insert_image(img_path, width_cm=13.0, fig_num="4.3", title="Role-Permission Matrix Heatmap")

heading("4.5 DATABASE DESIGN", 2)
body("The database design follows the Frappe DocType model. Key entities include Student (naming "
     "STU-.YYYY.-.#####), Guardian ({name}-{###}), Program, Course, Academic Year, Academic Term, Room, "
     "Instructor, Student Group, Course Schedule, Fee Structure, Fees, Fee Payment, Grading Scale, "
     "Assessment Group, Assessment Plan, Assessment Result, Library Item, Library Transaction, Hostel, "
     "Hostel Room, Vehicle, Transport Route, Notice, Notice Recipient, Communication Log, and Feedback. "
     "Figure 4.4 shows the entity-relationship diagram.", space_after=6)
img_path = os.path.join(IMAGES_DIR, "fig4_4_er_diagram.png")
if os.path.exists(img_path):
    insert_image(img_path, width_cm=13.0, fig_num="4.4", title="Entity-Relationship Diagram")

heading("4.6 DATA FLOW DIAGRAMS", 2)
body("Figure 4.5 shows the Level 0 context diagram with external entities interacting with Institution ERP. "
     "Figure 4.6 shows the Level 1 diagram with five processes: Admissions, Academics, Fees, Facilities, "
     "and Communication, together with the data stores.", space_after=6)
for n, t, f in [("4.5", "Data Flow Diagram Level 0", "fig4_5_dfd_l0.png"),
                ("4.6", "Data Flow Diagram Level 1", "fig4_6_dfd_l1.png")]:
    img_path = os.path.join(IMAGES_DIR, f)
    if os.path.exists(img_path):
        insert_image(img_path, width_cm=13.0, fig_num=n, title=t)

heading("4.7 USE CASE DIAGRAM", 2)
body("Actors include Student, Guardian, Instructor, Admissions Officer, Fee Manager, Facility Manager, "
     "Communication Officer, Academic Head, and System Manager. Use cases span admission processing, "
     "academic management, attendance marking, assessment and results, fee management, library "
     "issue/return, hostel and transport allocation, notice publication, feedback submission, and "
     "dashboard viewing.", space_after=6)
img_path = os.path.join(IMAGES_DIR, "fig4_7_use_case.png")
if os.path.exists(img_path):
    insert_image(img_path, width_cm=13.0, fig_num="4.7", title="Use Case Diagram")

heading("4.8 SEQUENCE DIAGRAMS", 2)
body("Four key interactions were modelled: (4.8.1) admission approval triggering auto Student/Guardian "
     "creation; (4.8.2) fee payment triggering outstanding recomputation; (4.8.3) assessment result entry "
     "triggering auto grade calculation and the results publication gate; and (4.8.4) library return "
     "triggering fine calculation and fee creation.", space_after=6)
for n, t, f in [("4.8", "Sequence Diagram \u2014 Admission Approval", "fig4_8_seq_admission.png"),
                ("4.9", "Sequence Diagram \u2014 Fee Payment", "fig4_9_seq_fee.png"),
                ("4.10", "Sequence Diagram \u2014 Assessment Result", "fig4_10_seq_assessment.png"),
                ("4.11", "Sequence Diagram \u2014 Library Fine", "fig4_11_seq_library.png")]:
    img_path = os.path.join(IMAGES_DIR, f)
    if os.path.exists(img_path):
        insert_image(img_path, width_cm=13.0, fig_num=n, title=t)

heading("4.9 ACTIVITY DIAGRAMS", 2)
body("Two activity diagrams model the end-user flows: (4.9.1) student portal login \u2192 dashboard \u2192 "
     "view results; and (4.9.2) staff login \u2192 role-specific cockpit \u2192 quick action \u2192 Frappe "
     "Desk.", space_after=6)
for n, t, f in [("4.12", "Activity Diagram \u2014 Student Portal", "fig4_12_act_student.png"),
                ("4.13", "Activity Diagram \u2014 Staff Hybrid Flow", "fig4_13_act_staff.png")]:
    img_path = os.path.join(IMAGES_DIR, f)
    if os.path.exists(img_path):
        insert_image(img_path, width_cm=13.0, fig_num=n, title=t)

heading("4.10 UI DESIGN APPROACH", 2)
body("A hand-written CSS design system defines custom properties (design tokens) for colors, typography, "
     "spacing, radii, shadows, and transitions, with no Tailwind dependency. Four reusable Vue components "
     "were built: StatCard, StatusBadge, EmptyState, and PageHeader. The Frappe Desk is rebranded through "
     "the app_include_css hook injecting inter-font.css (self-hosted Inter font) and desk-theme.css (BIT "
     "primary color #1e40af, consistent radii and transitions).", space_after=6)
img_path = os.path.join(IMAGES_DIR, "fig4_14_design_tokens.png")
if os.path.exists(img_path):
    insert_image(img_path, width_cm=13.0, fig_num="4.14", title="Design System Token Reference")

heading("4.11 DESIGN RATIONALE", 2)
body("The hybrid architecture (Option C) was deliberately chosen over two alternatives. Option A \u2014 full "
     "Vue CRUD \u2014 would require reimplementing every DocType form, validation rule, and permission check "
     "in Vue, duplicating Frappe's server-side logic at enormous effort and risk. Option B \u2014 Desk only "
     "\u2014 would re-theme Frappe Desk but would not deliver a focused portal experience for staff or a "
     "dedicated student/guardian SPA. Option C \u2014 the hybrid model \u2014 was chosen because it gives "
     "staff a fast, role-specific cockpit for the 80% of daily actions (marking attendance, recording "
     "payments, publishing notices) while retaining full CRUD through the rebranded Desk for the 20% of "
     "operations that need it (creating new records, running reports, bulk imports). This balances "
     "usability with completeness without duplicating Frappe's validated forms.", space_after=10)
body("The metadata-driven DocType model was chosen because it allows new entities and fields to be added "
     "without code changes, which is essential for an institution whose academic structure evolves each "
     "year. The permission_query_conditions layer was chosen because it enforces row-level security at the "
     "database level, so security cannot be bypassed by manipulating the UI or calling APIs directly. The "
     "results_published flag was chosen because examination marks must be released only after official "
     "approval, not the moment an instructor enters them.", space_after=10)

heading("4.13 DATA DICTIONARY", 2)
body("Table 4.3 lists the principal entity attributes used across the system. Each DocType is represented "
     "by its name, naming convention, and key fields.", space_after=6)
table_caption("4.3", "Data Dictionary — Principal Entity Attributes")
make_table(
    ["DocType", "Naming Series", "Key Fields"],
    [
        ["Student", "STU-.YYYY.-.#####", "first_name, last_name, status, program, guardian, email_address"],
        ["Guardian", "{guardian_name}-{###}", "guardian_name, guardian_email, relation_to_student, phone_number"],
        ["Program", "program_name", "program_name, program_code, department"],
        ["Course", "course_name", "course_name, course_code, program, credits"],
        ["Fee Structure", "structure_name", "structure_name, program, academic_year, total_amount"],
        ["Fees", "FEE-.YYYY.-.####", "student, fee_schedule, total_amount, paid_amount, outstanding_amount, status"],
        ["Assessment Plan", "hash", "assessment_group, course, student_group, max_marks, passing_marks"],
        ["Assessment Result", "hash", "assessment_plan, student, marks_obtained, grade, status"],
        ["Library Item", "LIB-BOOK-.#####", "title, author, isbn, total_copies, available_copies"],
        ["Hostel Room", "room_number", "hostel, room_number, room_type, capacity, occupied_count"],
        ["Transport Route", "route_name", "route_name, vehicle, fee_amount"],
        ["Notice", "NOTICE-.YYYY.-.#####", "title, body, audience_type, publish_date, status"],
    ],
    widths_cm=[2.6, 3.0, 8.9], font_size=Pt(9))

heading("4.12 TECHNOLOGY SELECTION RATIONALE", 2)
body("Frappe v16 was selected as the backend because it provides a metadata-driven DocType model, a "
     "built-in permission system, a web desk, and a benchmarked development speed for data-intensive "
     "applications. Python was chosen for the backend because Frappe is Python-based and the team had "
     "Python expertise. MariaDB was chosen as the relational database because Frappe is built on MariaDB "
     "and it provides reliable ACID transactions for financial (fees) and academic (results) data. Redis "
     "was chosen for caching and background jobs. Vue 3 was chosen for the portal because it provides a "
     "reactive, component-based frontend with a small bundle size. Vite was chosen as the build tool for "
     "fast development and production builds. Nginx was chosen as the web server for serving static assets "
     "and reverse-proxying to the Frappe bench. The entire stack is open source, supporting zero-cost "
     "deployment.", space_after=10)

print("Chapter IV ready.")

# ===========================================================================
# CHAPTER V: IMPLEMENTATION
# ===========================================================================
doc.add_page_break()
heading(f"CHAPTER {ROMAN[4]}", 1)
heading("IMPLEMENTATION", 1)

body("This chapter describes the implementation of Institution ERP, module by module, followed by the "
     "permission model, workflow engine, automation, the Student/Guardian Vue portal, staff cockpits with "
     "the hybrid Desk, and the staged build method. All implementation claims reflect the live source code "
     "and verified demo data counts.", space_after=10)

heading("5.2 MODULE-BY-MODULE IMPLEMENTATION", 2)

heading("5.2.1 Admissions", 3)
body("The admissions pipeline flows Admission Inquiry \u2192 Student Applicant \u2192 Entrance Test \u2192 "
     "Entrance Test Result. The Student Applicant DocType implements a four-state workflow (Draft \u2192 "
     "Applied \u2192 Under Review \u2192 Approved). On approval, an on_update hook automatically creates a "
     "Guardian record (if not existing), a Student record with status Active, and links them \u2014 no "
     "manual data entry is required after approval.", space_after=8)
body("The Admission Inquiry DocType captures the first point of contact: applicant name, date of birth, "
     "gender, guardian details, program interested, source of inquiry, and inquiry date. Each inquiry "
     "receives a unique naming series identifier (ADM-INQ-.YYYY.-.####). The inquiry status tracks the "
     "conversion funnel from Open to Converted or Closed. This ensures no prospective student is lost and "
     "every inquiry can be traced through to enrolment.", space_after=8)
body("The Student Applicant DocType formalises the application. It links to the source inquiry and records "
     "the applicant's program, academic year, guardian details, previous school, and previous school marks. "
     "The four-state workflow (Draft, Applied, Under Review, Approved) is enforced through Frappe's workflow "
     "engine so that an application cannot skip stages. An Entrance Test is optional and tied to a specific "
     "program with a date, maximum marks, and passing marks. The Entrance Test Result records marks "
     "obtained and auto-calculates Pass/Fail against the test's passing threshold. On approval, the "
     "on_update hook creates the Guardian and Student records and sets the created_student reference, "
     "completing the conversion from applicant to enrolled student.", space_after=8)

heading("5.2.2 SIS (Student Information System)", 3)
body("Student records use naming series STU-.YYYY.-.##### and store first name, last name, status "
     "(Active/Inactive/Graduated), gender, date of birth, program, guardian, and email address. Guardian "
     "records use format {guardian_name}-{###} and store name, email, phone, and relation. Portal users "
     "are created through ensure_student_user() and ensure_guardian_user(), which also create User "
     "Permission records for row-level scoping.", space_after=8)
body("The SIS module is the central student registry. Every other module \u2014 academics, attendance, "
     "examination, fees, library, hostel, transport \u2014 references the Student record as the single "
     "source of truth. The Guardian record enables family-level access: one guardian can be linked to "
     "multiple students, and the portal child-switcher lets a guardian view all linked children from one "
     "account. Status tracking (Active, Inactive, Graduated) lets the institution filter current students "
     "for reporting without deleting historical records. The unique naming series prevents identifier "
     "collisions across academic years.", space_after=8)

heading("5.2.3 Academics", 3)
body("Program, Course, Academic Year, Academic Term, Room, Instructor, Student Group, and Course Schedule "
     "form the academic hierarchy. Course Schedule prevents double-booking of rooms and instructors on the "
     "same day and overlapping time slots. Attendance and assessments are tracked at the student-group "
     "level.", space_after=8)
body("The Academics module establishes the organisational structure that every other module depends on. A "
     "Program is the degree (for example, B.Sc Computer Science) with a name, code, and department. A "
     "Course is a subject within a program with credits and a course type (Core, Elective, Lab). Academic "
     "Year and Academic Term define time periods. Room represents a physical space with capacity and type. "
     "Instructor links faculty to courses. Student Group is a subset of a program's students for a given "
     "year and course. Course Schedule ties course, group, instructor, room, day, and time together, with "
     "validation that prevents a room or instructor from being double-booked. This structure ensures that "
     "attendance, assessments, and fees all reference a consistent academic calendar.", space_after=8)

heading("5.2.4 Attendance", 3)
body("Student Attendance is marked per student group, course schedule, and date, with status Present/"
     "Absent/Late/Excused and duplicate prevention per student + date + course schedule. Staff Attendance "
     "tracks instructors with Present/Absent/Half Day/On Leave. Bulk marking APIs "
     "(mark_bulk_student_attendance, mark_bulk_staff_attendance) skip duplicates.", space_after=8)
body("The Attendance module replaces paper registers. An instructor marks attendance for a student group on "
     "a specific date, and each student is marked Present, Absent, Late, or Excused. Duplicate prevention "
     "ensures a student cannot be marked twice for the same date and course schedule. Bulk marking lets an "
     "instructor mark an entire group at once. Staff attendance follows the same pattern for instructors. "
     "The portal shows students their attendance history with colored badges and a percentage calculation, "
     "giving students and guardians immediate visibility without visiting the office.", space_after=8)

heading("5.2.5 Examination", 3)
body("Grading Scale defines intervals mapping marks to grades with non-overlapping thresholds. Assessment "
     "Group carries the results_published flag that gates mark visibility. Assessment Plan links course, "
     "student group, grading scale, max marks, and passing marks. Assessment Result supports bulk marks "
     "entry, auto grade calculation from the grading scale, auto Pass/Fail status, and duplicate "
     "prevention per student per plan. When results_published is 0, portal users see a Results Not Yet "
     "Published banner instead of marks.", space_after=8)
body("The results publication gate is a deliberate design decision. In many institutions, instructors "
     "enter marks incrementally, and students would see partial or unmoderated results if marks were "
     "visible immediately. By gating visibility behind results_published, the examination committee can "
     "review all marks for an assessment group, moderate outliers, and release results to all students "
     "simultaneously. This ensures fairness and prevents premature disclosure of incomplete results.",
     space_after=8)

heading("5.2.6 Fees", 3)
body("The fee lifecycle is Fee Category \u2192 Fee Structure (with components, auto-summed total) \u2192 "
     "Fee Schedule (with student members) \u2192 Fees invoice \u2192 Fee Payment \u2192 Fee Discount. The "
     "Fees DocType recomputes paid and outstanding amounts and status (Paid/Partial/Unpaid/Overdue) on "
     "every validate; Fee Payment on submit updates the parent invoice. Fee Discount follows a Pending "
     "\u2192 Approved \u2192 Applied workflow. The Fee Dues Report lists outstanding fees filterable by "
     "academic year, program, and status.", space_after=8)
body("The Fees module automates the financial lifecycle. A Fee Structure defines components (tuition, "
     "library, lab) for a program and academic year, auto-summing to a total. A Fee Schedule generates the "
     "list of students to invoice from a structure, linked to a student group and due date. Each Fees "
     "invoice tracks total, discount, paid, and outstanding amounts, with status auto-computed. Fee "
     "Payment records each payment and validates it does not exceed outstanding; on submit it recomputes "
     "the parent invoice. Fee Discount follows an approval workflow (Pending\u2192Approved\u2192Applied). "
     "The Fee Dues Report gives the Fee Manager instant visibility into outstanding collections.",
     space_after=8)

heading("5.2.7 Library", 3)
body("Book Category classifies books. Library Item tracks title, author, ISBN, category, total copies, "
     "and available copies (auto-managed). Library Membership specifies max books and validity. Library "
     "Transaction records issue/return; issue validates available copies, active membership, and max-book "
     "limit; return calculates an overdue fine of \u20B95/day, adjusts available copies, and auto-creates "
     "a Fees record on late return.", space_after=8)
body("The Library module manages the full issue-return cycle. A student needs an active Library Membership "
     "to borrow. On issue, the system validates that copies are available, membership is active, and the "
     "student has not exceeded max books. On return, it calculates overdue fines (₹5/day) and, if a fine "
     "applies, auto-creates a Fees record so the fine is tracked alongside other fees. Available copies "
     "are decremented on issue and incremented on return, keeping the catalog accurate.", space_after=8)

heading("5.2.8 Hostel", 3)
body("Hostel stores name, type, warden, and auto-recomputed total capacity from rooms. Hostel Room stores "
     "room number, type, capacity, and auto-managed occupied count. Hostel Room Allocation validates that "
     "the room is not full and that the student has no other active allocation; it recomputes occupied "
     "count on create and vacate.", space_after=8)
body("The Hostel module manages room allocation and occupancy. A Hostel has a total capacity that is "
     "recomputed from its rooms. Each Hostel Room has a number, type, capacity, and auto-managed occupied "
     "count. Hostel Room Allocation assigns a student to a room, validating that the room is not full and "
     "that the student has no other active allocation. Occupied count is updated on create and vacate, "
     "giving the Facility Manager real-time occupancy visibility per hostel.", space_after=8)

heading("5.2.9 Transport", 3)
body("Vehicle registers number, capacity, driver, and status. Transport Route defines stops (with order "
     "and pickup time), vehicle, and fee amount, with no duplicate stop orders. Student Transport Allocation "
     "validates vehicle capacity and one active allocation per student per route.", space_after=8)
body("The Transport module manages vehicles, routes, and student allocations. A Vehicle has a number, "
     "capacity, driver, and status. A Transport Route has stops with order and pickup time, a vehicle, and "
     "a fee amount, with no duplicate stop orders. Student Transport Allocation assigns a student to a "
     "route, validating vehicle capacity and one active allocation per student per route. This prevents "
     "overbooking and gives the transport coordinator a clear view of route utilisation.", space_after=8)

heading("5.2.10 Communication", 3)
body("Notice supports five audience modes (All, Program-wise, Group-wise, Role-wise, Individual) with "
     "publish/expiry dates. On publication, the system resolves the audience and creates Notice Recipient "
     "records. Communication Log records dispatch (channel, status, sent_at). Feedback supports category, "
     "subject, description, and an Open \u2192 In Progress \u2192 Resolved \u2192 Closed lifecycle requiring "
     "resolution notes on closure. The Institution Overview Dashboard combines 5 number cards and 2 charts.",
     space_after=8)
body("The Communication module enables targeted institutional communication. A Notice has a title, body, "
     "audience type, and publish/expiry dates. On publication, the system resolves the audience (all "
     "students, a program, a group, a role, or an individual) and creates one Notice Recipient record per "
     "targeted student, so each student sees only the notices meant for them. Communication Log tracks "
     "dispatch channel and status. Feedback lets students and guardians submit complaints with category "
     "and subject, tracking them through Open\u2192In Progress\u2192Resolved\u2192Closed with mandatory "
     "resolution notes on closure. The Institution Overview Dashboard aggregates 5 number cards and 2 "
     "charts for leadership visibility.", space_after=8)

heading("5.3 PERMISSION MODEL", 2)
body("Security uses two layers. User Permissions are auto-created by ensure_student_user() and "
     "ensure_guardian_user(): each Student-role User is linked to their own Student record; each "
     "Guardian-role User is linked to their Guardian record and all linked Student records. "
     "permission_query_conditions provides 16 SQL WHERE-clause functions covering 19 DocTypes, injecting "
     "row-level filters (e.g., student = '<own record>' or student IN ('<child1>', '<child2>')). Bypass "
     "roles grant System Manager, Academic Head, and relevant staff broader access. Table 5.1 documents "
     "the coverage.", space_after=6)
table_caption("5.1", "permission_query_conditions Coverage")
make_table(
    ["#", "DocType(s)", "Condition Function", "Bypass Roles"],
    [
        ["1", "Student", "get_permission_query_conditions_student", "System Manager, Academic Head, Admissions Officer"],
        ["2", "Fees", "get_permission_query_conditions_fees", "System Manager, Fee Manager, Academic Head"],
        ["3", "Fee Payment", "get_permission_query_conditions_fee_payment", "System Manager, Fee Manager, Academic Head"],
        ["4", "Student Attendance", "get_permission_query_conditions_student_attendance", "System Manager, Academic Head"],
        ["5", "Staff Attendance", "get_permission_query_conditions_staff_attendance", "System Manager, Academic Head"],
        ["6", "Assessment Result", "get_permission_query_conditions_assessment_result", "System Manager, Academic Head"],
        ["7", "Assessment Plan", "get_permission_query_conditions_assessment_plan", "System Manager, Academic Head"],
        ["8", "Notice", "get_permission_query_conditions_notice", "System Manager, Communication Officer, Academic Head"],
        ["9", "Notice Recipient", "get_permission_query_conditions_notice_recipient", "System Manager, Communication Officer, Academic Head"],
        ["10", "Feedback", "get_permission_query_conditions_feedback", "System Manager, Communication Officer, Academic Head, Instructor"],
        ["11", "Communication Log", "get_permission_query_conditions_communication_log", "System Manager, Communication Officer, Academic Head"],
        ["12", "Library Item", "get_permission_query_conditions_library_item", "System Manager, Facility Manager, Academic Head"],
        ["13", "Library Membership", "get_permission_query_conditions_library_membership", "System Manager, Facility Manager, Academic Head"],
        ["14", "Library Transaction", "get_permission_query_conditions_library_transaction", "System Manager, Facility Manager, Academic Head"],
        ["15", "Hostel / Hostel Room / Hostel Room Allocation", "get_permission_query_conditions_hostel", "System Manager, Facility Manager, Academic Head"],
        ["16", "Vehicle / Transport Route / Student Transport Allocation", "get_permission_query_conditions_transport", "System Manager, Facility Manager, Academic Head"],
    ],
    widths_cm=[0.8, 4.2, 4.0, 5.5], font_size=Pt(9))

heading("5.4 WORKFLOW ENGINE", 2)
body("The Student Applicant workflow implements four states (Draft, Applied, Under Review, Approved) with "
     "auto Student/Guardian creation on approval. The Fee Discount workflow implements Draft \u2192 "
     "Approved \u2192 Rejected, setting discount_amount on the linked Fee on approval. Notification "
     "triggers support status transitions.", space_after=6)
img_path = os.path.join(IMAGES_DIR, "fig5_16_wf_applicant.png")
if os.path.exists(img_path):
    insert_image(img_path, width_cm=13.0, fig_num="5.1", title="Student Applicant Workflow Diagram")

heading("5.5 AUTOMATION", 2)
body("Automation reduces manual effort across the system. The following triggers are implemented:", space_after=6)
table_caption("5.2", "Automation Triggers (Event \u2192 Action)")
make_table(
    ["Event", "Action", "Implemented In"],
    [
        ["Student Applicant status = Approved", "Create Guardian + Student records; link via FK", "api.py / on_update hook"],
        ["Assessment Result marks entered", "Auto-calculate grade from Grading Scale; set Pass/Fail", "api.py / controller"],
        ["Fees validated or paid", "Recompute paid_amount, outstanding_amount, status", "Fees controller"],
        ["Fee Payment submitted", "Recompute parent Fees record", "Fee Payment on_submit"],
        ["Library Transaction return overdue", "Calculate \u20B95/day fine; create Fees record", "Library Transaction on_submit"],
        ["Guardian/Student created", "Create Frappe User + User Permissions", "ensure_guardian_user / ensure_student_user"],
        ["Student status missing", "Backfill status = Active", "backfill_student_status()"],
    ],
    widths_cm=[4.6, 5.6, 4.3], font_size=Pt(9.5))

heading("5.6 STUDENT/GUARDIAN VUE PORTAL", 2)
body("The portal is a Vue 3 SPA with hash-based routing at /institution-portal, served through Frappe's "
     "web page system with CSRF token injection. A sidebar provides navigation; guardians use a child "
     "switcher to toggle between linked students. All data is fetched through callAPI() \u2192 frappe.call() "
     "\u2192 whitelisted Python methods. Row-level security and results publication gating apply to every "
     "portal request.", space_after=10)

heading("5.7 STAFF COCKPITS AND HYBRID DESK", 2)
body("Seven role-specific Vue cockpits serve Admin, Admissions, Academic Head, Instructor, Fee Manager, "
     "Facility Manager, and Communication Officer. Each cockpit shows stat cards, quick actions, and "
     "overview data, with an \u201cOpen Full Desk\u201d button opening the full Frappe Desk for complete "
     "CRUD. The Desk is rebranded via app_include_css injecting inter-font.css (self-hosted Inter, 4 "
     "weights) and desk-theme.css (BIT blue #1e40af, consistent radii and transitions).", space_after=10)

heading("5.8 STAGED BUILD METHOD", 2)
body("The system was built in eight stages, each with end-to-end tests. Stages added DocTypes and modules "
     "incrementally: Stage 1\u20132 (Academics/SIS), Stage 3 (Admissions/API), Stage 4 "
     "(Attendance/Examination), Stage 5 (Fees), Stage 6 (Library/Hostel/Transport), Stage 7 "
     "(Communication), and Stage 8 (Portal/Permissions). Table 5.3 summarises the stages.", space_after=6)
table_caption("5.3", "Stage Summary")
make_table(
    ["Stage", "Modules", "Key Features", "Test File"],
    [
        ["1\u20132", "Academics, SIS", "Programs, courses, student/guardian records", "e2e_test.py"],
        ["3", "Admissions, API", "Inquiry \u2192 applicant \u2192 approval; whitelisted APIs", "e2e_test_stage3.py"],
        ["4", "Attendance, Examination", "Bulk attendance, marks entry, auto grade", "e2e_test_stage4.py"],
        ["5", "Fees", "Structures, schedules, invoices, payments, dues report", "e2e_test_stage5.py"],
        ["6", "Library, Hostel, Transport", "Issue/return/fine, room allocation, routes", "e2e_test_stage6.py"],
        ["7", "Communication", "Notices, recipients, feedback, dashboard", "e2e_test_stage7.py"],
        ["8", "Portal, Permissions", "Vue portal, cockpits, permission_query_conditions", "e2e_test_stage8.py"],
    ],
    widths_cm=[1.6, 3.2, 6.6, 3.1], font_size=Pt(9.5))

heading("5.9 IMPLEMENTATION CHALLENGES AND SOLUTIONS", 2)
body("Several challenges arose during implementation and were resolved as follows. First, Frappe v16 does "
     "not auto-sync non-standard Dashboard instances from app JSON, so the Institution Overview Dashboard "
     "was created programmatically via frappe.get_doc() in test code and documented in Deployment.md. "
     "Second, Frappe v16's Phone fieldtype enforces country-code validation that caused issues with Indian "
     "phone numbers, so Vehicle.driver_phone was implemented as a Data fieldtype instead. Third, "
     "four Communication module DocType directories lacked __init__.py files; while Frappe v16 does not "
     "require them for DocTypes, they were noted as a consistency deviation. Fourth, Guardian naming uses "
     "format {guardian_name}-{###}, which can produce similar names for guardians with identical names; "
     "this was accepted as a known limitation with a unique-identifier suffix planned for the future. "
     "Fifth, the Library fine auto-creates a Fees record without Fee Manager review; this works for the "
     "demo but needs an approval workflow for production. Each challenge was documented in ARCHITECTURE.md "
     "and DEPLOYMENT.md so future maintainers are aware.", space_after=10)

heading("5.10 IMPLEMENTATION SUMMARY", 2)
body("Table 5.4 summarises the implementation statistics verified against the live site. These figures "
     "confirm the scale and completeness of the system.", space_after=6)
table_caption("5.4", "Implementation Statistics (verified live)")
make_table(
    ["Metric", "Count"],
    [
        ["Total DocTypes", "48"],
        ["Child Tables", "8"],
        ["Modules", "10"],
        ["Custom Roles", "8"],
        ["Script Reports", "6"],
        ["Number Cards", "5"],
        ["Dashboard Charts", "2"],
        ["Custom Dashboards", "1"],
        ["Whitelisted API Methods", "11"],
        ["permission_query_conditions", "16"],
        ["DocTypes covered by permissions", "19"],
        ["E2E Test Files", "7"],
        ["Controller Files with Validation", "22"],
        ["Demo Students (live)", "86"],
        ["Instructors (live)", "12"],
        ["Guardians (live)", "55"],
        ["Attendance Records (live)", "2,557"],
        ["Assessment Results (live)", "312"],
        ["Fees Records (live)", "51"],
        ["Library Items (live)", "34"],
        ["Demo Accounts", "14"],
    ],
    widths_cm=[5.6, 3.0], font_size=Pt(9.5))
print("Chapter V ready.")

# ===========================================================================
# CHAPTER VI: TESTING
# ===========================================================================
doc.add_page_break()
heading(f"CHAPTER {ROMAN[5]}", 1)
heading("TESTING", 1)

body("This chapter presents the test strategy, test environment, test cases, security and permission "
     "testing, login and regression results, responsive testing, and performance benchmarks. Results were "
     "taken from the project test files and live demo data counts.", space_after=10)

heading("6.1 TEST STRATEGY", 2)
body("Testing followed the staged build method. Each of the eight build stages has a dedicated end-to-end "
     "test file executed against the live site institution.localhost. Testing covered API methods, UI "
     "workflows, permission scoping, login across all demo accounts, regression, responsiveness, and "
     "performance. Tests were executed with frappe bench execute and validated by querying the database "
     "after each action. The staged approach meant that each module was tested immediately after it was "
     "built, so defects were caught early and did not accumulate. Regression testing after each stage "
     "confirmed that new modules did not break previously built functionality.", space_after=10)
body("Test data was the live demo dataset: 86 students, 12 instructors, 55 guardians, 2,557 attendance "
     "records, 312 assessment results, 51 fee records, 34 library items. This provided realistic volume "
     "for performance and permission testing. All 14 demo accounts were tested across 3 runs (42/42 "
     "passing), confirming consistent login and role-based routing. Permission tests confirmed that "
     "cross-access is blocked at the database level, not just the UI.", space_after=10)

heading("6.2 TEST ENVIRONMENT", 2)
table_caption("6.1", "Test Environment Specifications")
make_table(
    ["Item", "Value"],
    [
        ["Site", "institution.localhost (http://localhost:8000)"],
        ["Framework", "Frappe v16.26.3"],
        ["Database", "MariaDB 10.6+; Redis 7+"],
        ["Demo students (live)", "86 (79 in demo dataset)"],
        ["Instructors (live)", "12"],
        ["Guardians (live)", "55"],
        ["Attendance records (live)", "2,557"],
        ["Assessment results (live)", "312"],
        ["Fees records (live)", "51"],
        ["Library items (live)", "34"],
        ["Demo accounts", "14 (8 staff + 4 student + 2 guardian)"],
        ["Password (all accounts)", "Demo@2026"],
    ],
    widths_cm=[5.2, 9.3], font_size=Pt(10))

heading("6.3 TEST CASES", 2)
body("Test cases were executed per stage. Table 6.2 summarises representative test coverage: each row "
     "gives the test identifier, scenario, module, expected result, actual result, and status.",
     space_after=6)
table_caption("6.2", "Test Case Summary (Representative Rows)")
make_table(
    ["Test ID", "Scenario", "Module", "Expected", "Actual", "Status"],
    [
        ["TC-01", "Admission inquiry \u2192 applicant \u2192 approval", "Admissions", "Student + Guardian auto-created", "Created", "PASS"],
        ["TC-02", "Bulk student attendance marking", "Attendance", "Records created; duplicates skipped", "Created; skipped", "PASS"],
        ["TC-03", "Bulk assessment result entry", "Examination", "Grade auto-calculated; Pass/Fail set", "Grade set", "PASS"],
        ["TC-04", "Fee payment record", "Fees", "Parent invoice recomputed", "Recomputed", "PASS"],
        ["TC-05", "Library overdue return", "Library", "\u20B95/day fine; Fees record created", "Fine created", "PASS"],
        ["TC-06", "Hostel room over-allocation", "Hostel", "Save rejected", "Rejected", "PASS"],
        ["TC-07", "Guardian accesses non-child data", "Security", "Access denied", "Denied", "PASS"],
        ["TC-08", "Student accesses another\u2019s fees", "Security", "Access denied", "Denied", "PASS"],
        ["TC-09", "All 14 demo accounts login", "Portal/Desk", "All login; role routing correct", "All passed", "PASS"],
        ["TC-10", "Results unpublished gate", "Examination", "Blue banner shown", "Banner shown", "PASS"],
        ["TC-11", "Guardian child switcher", "Portal", "Switching child updates all data", "Data updates correctly", "PASS"],
        ["TC-12", "Fee overpayment blocked", "Fees", "Payment exceeding outstanding rejected", "Rejected", "PASS"],
        ["TC-13", "Library max-books limit", "Library", "Issue beyond max books rejected", "Rejected", "PASS"],
        ["TC-14", "Double-booking prevention", "Academics", "Same room/time conflict rejected", "Rejected", "PASS"],
        ["TC-15", "Duplicate attendance blocked", "Attendance", "Same student/date/schedule rejected", "Rejected", "PASS"],
    ],
    widths_cm=[1.3, 3.6, 1.9, 3.2, 2.6, 1.0], font_size=Pt(9))

heading("6.4 SECURITY AND PERMISSION TESTING", 2)
body("Cross-access tests verified that permission_query_conditions blocks unauthorised access at the "
     "database level. Guardian1 attempting to read a non-child's attendance was denied; a student "
     "attempting to read another student's fees was denied; an instructor accessing another group's "
     "attendance was denied; and a portal user attempting to access the Frappe Desk was denied.",
     space_after=6)
table_caption("6.3", "Permission Test Matrix (Representative)")
make_table(
    ["Role", "DocType", "Action", "Result"],
    [
        ["Student", "Fees (own)", "Read", "Allow"],
        ["Student", "Fees (other)", "Read", "Deny"],
        ["Guardian", "Student (linked)", "Read", "Allow"],
        ["Guardian", "Student (unlinked)", "Read", "Deny"],
        ["Instructor", "Student Attendance (own group)", "Read/Write", "Allow"],
        ["Instructor", "Student Attendance (other group)", "Read", "Deny"],
        ["Fee Manager", "Fees (all)", "Read/Write", "Allow"],
        ["Portal User", "Frappe Desk", "Access", "Deny"],
    ],
    widths_cm=[2.4, 3.4, 2.6, 1.4], font_size=Pt(9.5))

heading("6.5 LOGIN AND REGRESSION", 2)
table_caption("6.4", "Login and Regression Results")
make_table(
    ["Account Type", "Count", "All Logins Passed", "Role Routing Verified"],
    [
        ["Staff (System User)", "8", "Yes (3 runs each)", "Yes"],
        ["Student (Website User)", "4", "Yes (3 runs each)", "Yes"],
        ["Guardian (Website User)", "2", "Yes (3 runs each)", "Yes"],
        ["Total", "14", "42/42 across 3 runs", "Yes"],
    ],
    widths_cm=[3.0, 1.6, 4.2, 3.2], font_size=Pt(10))

heading("6.6 RESPONSIVE TESTING", 2)
body("Responsive behaviour was verified at viewports 1920\u00D71080, 1366\u00D7768, 768\u00D71024, and "
     "375\u00D7667. The StatCard, StatusBadge, EmptyState, and PageHeader components, together with "
     "sidebar collapse, adapted correctly across breakpoints.", space_after=10)

heading("6.7 PERFORMANCE", 2)
table_caption("6.5", "API Performance Benchmarks")
make_table(
    ["Operation", "Response Time"],
    [
        ["Login", "~150 ms"],
        ["Bulk attendance marking", "~200 ms"],
        ["Fee generation from schedule", "~300 ms"],
        ["Student/fee search", "~250 ms"],
    ],
    widths_cm=[5.2, 3.0], font_size=Pt(10))

heading("6.8 RISK REGISTER", 2)
body("Key project risks and their mitigations are summarised in Table 6.6.", space_after=6)
table_caption("6.6", "Risk Register")
make_table(
    ["Risk", "Likelihood", "Impact", "Mitigation"],
    [
        ["Demo data idempotency drift on re-runs", "Medium", "Low", "Document clean initial load"],
        ["Library fine auto-creates Fees without review", "Medium", "Medium", "Add approval workflow (future)"],
        ["dispatch_notice stub (no real SMS/email)", "High", "Low", "Document as stub; integrate gateway (future)"],
        ["Guardian naming collision", "Low", "Low", "Use unique identifier suffix (future)"],
        ["Dashboard not auto-synced from app JSON", "High", "Low", "Document programmatic creation"],
    ],
    widths_cm=[4.6, 2.0, 1.8, 6.1], font_size=Pt(9.5))

heading("6.9 TEST SUMMARY", 2)
body("All 15 representative test cases passed, confirming that the core workflows\u2014admission approval, "
     "attendance marking, assessment entry, fee payment, library issue/return, hostel allocation, and "
     "security cross-access blocking\u2014function as designed. Login and regression testing confirmed that "
     "all 14 demo accounts authenticate successfully across three consecutive runs (42/42), with correct "
     "role-based routing to either the Vue portal or the Frappe Desk. Responsive testing verified correct "
     "layout across four viewport sizes, and performance benchmarks showed all key API operations completing "
     "under 300 ms. The risk register documents five known risks, all with acceptable impact and documented "
     "mitigations. Taken together, the testing evidence demonstrates that Institution ERP is functionally "
     "complete, secure, performant, and ready for demonstration.", space_after=10)

print("Chapter VI ready.")

# ===========================================================================
# CHAPTER VII: RESULTS AND DISCUSSION
# ===========================================================================
doc.add_page_break()
heading(f"CHAPTER {ROMAN[6]}", 1)
heading("RESULTS AND DISCUSSION", 1)

body("This chapter presents what was achieved, maps requirements to implementation evidence, discusses "
     "key screenshots, and states the limitations observed during testing.", space_after=10)

heading("7.1 INTRODUCTION", 2)
body("The implementation phase produced a working, deployable system on site institution.localhost. This "
     "chapter consolidates the evidence: it maps requirements to implementation, discusses key screens and "
     "demo scenarios, and honestly states the limitations observed. The figures referenced are embedded as "
     "real diagrams; live UI screenshots should be inserted per the Figure Replacement Guide before "
     "submission.", space_after=10)

heading("7.2 REQUIREMENTS FULFILMENT", 2)
body("Table 7.1 maps each functional requirement to its implementation evidence and verification method. "
     "All 25 functional requirements were implemented and verified through staged end-to-end tests.",
     space_after=6)
table_caption("7.1", "Requirements Traceability Matrix (Representative Rows)")
make_table(
    ["FR-ID", "Requirement", "Implemented In", "Verified By"],
    [
        ["FR-01", "Admission inquiry \u2192 approval workflow", "Admissions module", "TC-01 (e2e_test_stage3.py)"],
        ["FR-02", "Auto Student/Guardian creation", "Admissions on_update hook", "TC-01"],
        ["FR-08", "Results publication gating", "Examination module", "TC-10"],
        ["FR-16", "permission_query_conditions row-level security", "api.py (16 functions)", "TC-07, TC-08"],
        ["FR-17", "Staff cockpits", "Vue portal cockpit pages", "Demo walkthrough"],
        ["FR-22", "Staged build with e2e tests", "8 stages, 7 test files", "All stage tests PASS"],
    ],
    widths_cm=[1.3, 4.2, 4.0, 3.5], font_size=Pt(9))

heading("7.3 KEY ACHIEVEMENTS", 2)
body("The implemented system delivers 48 DocTypes across 10 modules, 8 custom roles (6 staff, 2 portal), "
     "6 script reports, 5 number cards, 2 dashboard charts, 1 custom dashboard, 11 whitelisted API "
     "methods, and 16 permission_query_conditions covering 19 DocTypes. Demo data includes 86 students "
     "(live), 12 instructors, 2,557 attendance records, 312 assessment results, 51 fee records, 34 "
     "library items, and 138 library transactions. All 14 demo accounts log in successfully across 3 "
     "test runs (42/42). These figures were verified against the live site institution.localhost and are "
     "not estimated.", space_after=10)
body("The requirement-to-implementation mapping in Table 7.1 shows that every functional requirement has "
     "a corresponding implementation and verification path. The security requirements (FR-16, FR-24) were "
     "validated through cross-access tests confirming that permission_query_conditions blocks unauthorised "
     "access at the database level. The performance requirements (NFR-01) were validated through API "
     "response-time benchmarks all under 300 ms. The usability requirements (NFR-04) were validated "
     "through responsive testing across four viewports. Taken together, the evidence demonstrates that the "
     "system satisfies its stated objectives.", space_after=10)

heading("7.4 SCREENSHOTS AND DISCUSSION", 2)
body("Key screens illustrate the student portal results gate, guardian child switcher, staff cockpits, "
     "fee management, and the rebranded Desk. Figures are embedded as real diagrams; screenshot "
     "placeholders are provided where live UI captures should be inserted per the Figure Replacement "
     "Guide. Each placeholder is labelled with the figure number, what to capture, and the account and URL "
     "to use, so the images can be swapped without breaking layout.", space_after=10)
body("The results gate (Figure 5.8 in discussion) is the most demonstrative feature: it shows published "
     "marks as cards alongside a blue \u201cResults Not Yet Published\u201d banner for unpublished groups, "
     "proving that publication gating works end to end. The guardian child switcher demonstrates row-level "
     "scoping: one guardian account can view multiple linked children's records, switching instantly "
     "between them, while being unable to access unlinked students. The staff cockpits demonstrate the "
     "hybrid model: each role lands on a focused dashboard with relevant stats and quick actions, with an "
     "\u201cOpen Full Desk\u201d escape hatch for full CRUD.", space_after=10)

heading("7.5 LIMITATIONS OBSERVED", 2)
table_caption("7.2", "Limitations and Mitigations")
make_table(
    ["Limitation", "Observed Impact", "Mitigation / Future Work"],
    [
        ["Library fine auto-creates a Fees record without review", "Fine invoiced immediately on late return", "Add Fee Manager approval workflow"],
        ["dispatch_notice is a stub (no real email/SMS)", "Notices logged but not dispatched", "Integrate SMTP/Twilio gateway"],
        ["No real payment gateway", "Fee payments are manual-entry records", "Integrate Razorpay/Stripe"],
        ["Report Card print format empty", "No printable report card generated", "Build print format suite"],
        ["Guardian naming may collide", "Same-named guardians can get similar IDs", "Use unique identifier suffix"],
        ["Dashboard created programmatically", "Not auto-synced from app JSON", "Document creation step"],
        ["Cockpit stats may lag Desk data", "Stats stale until cockpit refreshed", "Expected SPA behaviour"],
    ],
    widths_cm=[4.4, 4.0, 6.1], font_size=Pt(9.5))
body("These limitations are acknowledged and documented in DEPLOYMENT.md and DEMO_WALKTHROUGH.md. None "
     "undermine the core objectives of the system: the data model, validation logic, and permission "
     "system are solid, and the documented gaps are straightforward to address in future work.",
     space_after=10)

heading("7.6 COST-BENEFIT ANALYSIS", 2)
body("The system was built entirely on open-source software, so the development infrastructure cost is "
     "zero. Table 7.2 summarises the cost-benefit position.", space_after=6)
table_caption("7.2", "Cost-Benefit Analysis")
make_table(
    ["Component", "Technology Used", "Cost (Rs)", "Remarks"],
    [
        ["Frontend", "Vue 3 + Vite + Tailwind-independent CSS", "0", "Open source"],
        ["Backend", "Python + Frappe v16", "0", "Open source"],
        ["Database", "MariaDB", "0", "Open source"],
        ["Cache/Queue", "Redis", "0", "Open source"],
        ["Hosting", "Cloud instance", "0", "Demo on institution.localhost"],
        ["Development Effort", "Student (capstone project)", "0", "No staffing cost"],
        ["Total", "\u2014", "0", "Zero infrastructure cost"],
    ],
    widths_cm=[3.0, 4.6, 2.2, 4.7], font_size=Pt(9.5))

heading("7.7 DISCUSSION", 2)
body("The results confirm that Institution ERP meets its stated objectives. The hybrid staff interface "
     "reduces the cognitive load of the full Frappe Desk by presenting role-specific cockpits for daily "
     "tasks, while the \u201cOpen Full Desk\u201d escape hatch retains access to complete CRUD operations. "
     "The Student and Guardian portals provide transparent, self-service access to academic and financial "
     "records, reducing the administrative burden of responding to routine inquiries. The row-level security "
     "model, enforced through permission_query_conditions at the database level, ensures that data isolation "
     "cannot be bypassed through UI manipulation or direct API calls—a critical requirement for protecting "
     "student grades, attendance, and fee information.", space_after=10)
body("The results publication gating mechanism addresses a real institutional need: examination marks are "
     "released only after official approval, preventing premature disclosure of incomplete or unmoderated "
     "results. The automation features \u2014 automatic student and guardian creation on admission approval, "
     "auto grade calculation, fee recomputation, and library fine handling \u2014 reduce manual effort and "
     "minimise errors. Together, these features demonstrate that a complete, role-secured institution "
     "management system can be built and deployed at zero infrastructure cost using Frappe v16 and an "
     "open-source frontend stack.", space_after=10)

print("Chapter VII ready.")

# ===========================================================================
# CHAPTER VIII: CONCLUSION AND FUTURE ENHANCEMENTS
# ===========================================================================
doc.add_page_break()
heading(f"CHAPTER {ROMAN[7]}", 1)
heading("CONCLUSION AND FUTURE ENHANCEMENTS", 1)

heading("8.1 CONCLUSION", 2)
body("Institution ERP delivers a complete Student Information System on Frappe v16 for Bannari Amman "
     "Institute of Technology. The system covers the full student lifecycle \u2014 admissions inquiry "
     "through graduation \u2014 across 10 modules and 48 DocTypes. A hybrid staff interface combines "
     "role-specific Vue cockpits with a rebranded Frappe Desk, while Student and Guardian portals provide "
     "scoped access through User Permissions and permission_query_conditions. Results publication gating "
     "controls mark visibility, and automation handles student/guardian creation, grade calculation, and "
     "fee recomputation. All objectives were met: 48 DocTypes, 10 modules, 8 custom roles, 11 whitelisted "
     "API methods, 16 row-level permission conditions, 7 end-to-end test suites, and 14 verified demo "
     "accounts, deployed at zero infrastructure cost on an open-source stack.", space_after=10)

heading("8.2 FUTURE ENHANCEMENTS", 2)
body("The following enhancements are out of scope for this build and are proposed for future work: "
     "(1) LMS integration for course content, assignments, and online submission \u2014 this would extend "
     "Academics beyond scheduling into content delivery and graded coursework; (2) HR/Payroll extending "
     "staff attendance into employee profiles, leave management, and salary processing \u2014 this would "
     "add a human-resources dimension beyond the current staff-attendance scope; (3) payment gateway "
     "integration (Razorpay/Stripe) for online fee collection with receipts \u2014 this would replace the "
     "current manual Fee Payment entry with real-time online collection; (4) real SMS/email gateway "
     "replacing the dispatch_notice stub \u2014 this would enable actual notice dispatch rather than "
     "Communication Log stubs; (5) mobile app consuming the existing REST API \u2014 this would expose "
     "whitelisted methods and DocType CRUD for native mobile consumption; (6) print format suite for "
     "report cards, fee receipts, and ID cards \u2014 this would add printable institutional documents; "
     "(7) batch/section management for multi-year cohorts \u2014 this would add academic batch and section "
     "concepts; (8) hostel mess management \u2014 this would extend Hostel with meal planning and mess "
     "attendance; (9) cockpit customization \u2014 this would allow staff to rearrange stat cards and "
     "quick actions; and (10) analytics/ML for attendance and fee prediction \u2014 this would add "
     "predictive insights to the dashboard. None of these are implemented in the current build and are "
     "explicitly future scope.", space_after=10)

heading("8.3 SUMMARY", 2)
body("Institution ERP demonstrates that a full-featured, role-secured institution management system can "
     "be built and deployed at zero infrastructure cost using Frappe v16 and an open-source frontend "
     "stack. The system is ready for demonstration and further extension per the future enhancements "
     "listed above.", space_after=10)

print("Chapter VIII ready.")

# ===========================================================================
# REFERENCES
# ===========================================================================
doc.add_page_break()
heading("REFERENCES", 1)

references = [
    "Frappe Technologies. (2024). Frappe Framework Documentation (v16). https://frappeframework.com/docs",
    "ERPNext Foundation. (2024). ERPNext Education Domain Documentation. https://erpnext.com/docs/user/manual/en/education",
    "openSIS Community. (2023). openSIS Student Information System. https://opensis.com",
    "Foradian Technologies. (2024). Fedena ERP Platform. https://fedena.com",
    "Moodle Pty Ltd. (2024). Moodle Learning Management System. https://moodle.org",
    "Sandhu, R. S., Coyne, E. J., Feinstein, H. L., & Youman, C. E. (1996). Role-based access control "
    "models. Computer, 29(2), 38\u201347.",
    "Nielsen, J. (2021). Hybrid UI patterns for enterprise applications. Nielsen Norman Group.",
    "Vue.js Team. (2024). Vue 3 Documentation. https://vuejs.org",
    "Vite Team. (2024). Vite Build Tool Documentation. https://vitejs.dev",
    "MariaDB Foundation. (2024). MariaDB Server Documentation. https://mariadb.org/docs",
    "Redis Inc. (2024). Redis Documentation. https://redis.io/docs",
    "Python Software Foundation. (2024). Python 3.10 Documentation. https://docs.python.org/3.10",
    "Node.js Foundation. (2024). Node.js 18 Documentation. https://nodejs.org/docs/v18",
    "Frappe Technologies. (2023). Frappe Desk Architecture. https://frappeframework.com/docs/user/en/desk",
    "OWASP Foundation. (2023). Authentication Cheat Sheet. https://cheatsheetseries.owasp.org",
]
for i, ref in enumerate(references, start=1):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.left_indent = Cm(0.5)
    p.paragraph_format.first_line_indent = Cm(-0.5)
    run = p.add_run(f"[{i}] ")
    run_font(run, size=Pt(13), bold=True, font=BODY_FONT)
    run2 = p.add_run(ref)
    run_font(run2, size=Pt(13), font=BODY_FONT)

# ===========================================================================
# APPENDICES
# ===========================================================================
doc.add_page_break()
heading("APPENDICES", 1)

heading("Appendix I \u2014 Bill of Materials", 2)
body("Hardware: none (cloud deployment). Software: all open-source (Frappe v16, Python, MariaDB, Redis, "
     "Vue 3, Vite, Nginx, Git) under MIT or equivalent permissive licences. Staffing: student only.",
     space_after=10)

heading("Appendix II \u2014 Code Snippets", 2)
body("Key excerpts: api.py (whitelisted methods and permission_query_conditions), hooks.py "
     "(role_home_page, app_include_css), Vue main.js (router guards), design-system.css (design tokens), "
     "desk-theme.css (Inter font and BIT blue theming).", space_after=10)

heading("Appendix III \u2014 DocType List", 2)
body("Complete table of 48 DocTypes with module, naming convention, and key fields. The full list is: "
     "Academic Term, Academic Year, Admission Inquiry, Applicant Document, Assessment Group, Assessment "
     "Plan, Assessment Result, Book Category, Communication Log, Course, Course Schedule, Entrance Test, "
     "Entrance Test Result, Fee Category, Fee Discount, Fee Payment, Fee Schedule, Fee Schedule Student, "
     "Fee Structure, Fee Structure Component, Feedback, Fees, Fees Component, Grading Interval, Grading "
     "Scale, Guardian, Hostel, Hostel Room, Hostel Room Allocation, Instructor, Instructor Course, "
     "Library Item, Library Membership, Library Transaction, Notice, Notice Recipient, Program, Room, "
     "Route Stop, Staff Attendance, Student, Student Applicant, Student Attendance, Student Group, "
     "Student Group Member, Student Transport Allocation, Transport Route, Vehicle.", space_after=10)

heading("Appendix IV \u2014 Role-Permission Matrix", 2)
body("Full matrix of 10 roles \u00D7 48 DocTypes (Read/Write/Create/Delete/Submit/Cancel/Report). Staff "
     "roles have Desk access; Student and Guardian are portal roles with row-level scoping via "
     "permission_query_conditions.", space_after=10)

heading("Appendix V \u2014 API List", 2)
body("Core whitelisted methods implemented in api.py: get_students_in_group, mark_bulk_student_attendance, "
     "mark_bulk_staff_attendance, mark_bulk_assessment_results, generate_fees_from_schedule, "
     "dispatch_notice, ensure_guardian_user, ensure_all_guardian_users, ensure_student_user, "
     "ensure_all_student_users, backfill_student_status.", space_after=10)

heading("Appendix VI \u2014 Demo Credentials Summary", 2)
body("14 demo accounts (8 staff + 4 student + 2 guardian). All use password Demo@2026 (omitted here for "
     "security). Staff: admin (System Manager), admissions (Admissions Officer), academichead (Academic "
     "Head), instructor1/instructor2 (Instructor), feemanager (Fee Manager), facilitymanager (Facility "
     "Manager), comms.officer (Communication Officer). Students: richdemo, student1, student2, student3. "
     "Guardians: guardian1 (2 children), guardian2 (3 children).", space_after=10)

heading("Appendix VII \u2014 Plagiarism Report Placeholder", 2)
body("Plagiarism report to be attached from the institutional checker. [PLACEHOLDER: attach plagiarism "
     "report here.]", space_after=10)

heading("Appendix VIII \u2014 Work Contribution", 2)
body("Student declaration of individual contributions to the project. [PLACEHOLDER: student to complete.]",
     space_after=10)

heading("Appendix IX \u2014 Glossary of Terms", 2)
body("DocType: A Frappe data model entity defining a table and its fields. Module: A grouping of related "
     "DocTypes. Workspace: A Frappe Desk navigation grouping. Cockpit: A role-specific Vue dashboard page. "
     "Portal: The Vue 3 SPA at /institution-portal for students and guardians. permission_query_conditions: "
     "SQL WHERE-clause functions enforcing row-level security. User Permission: A record linking a user to "
     "specific DocType records. results_published: A flag gating examination mark visibility. Whitelisted "
     "method: A Python function exposed via Frappe's /api/method. Script Report: A server-side Frappe "
     "report. Number Card: A dashboard metric card. Dashboard Chart: A dashboard visualization. ",
     space_after=10)

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
doc.save(OUT_DOCX)
print(f"SAVED: {OUT_DOCX}")










