#!/usr/bin/env python3
"""Fix page-numbering format in Project_Report.docx:
- Section 0 (cover + inner title): unnumbered (no footer) — already OK
- Section 1 (front matter): lowercase Roman (i, ii, iii...)
- Section 2 (chapters): Arabic (1, 2, 3...) starting at 1
"""
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

DOCX = "/home/sriragul/frappe-bench/apps/institution_erp/report/final_report/Project_Report.docx"
doc = Document(DOCX)
sections = doc.sections
print("Number of sections:", len(sections))

def set_pgNumType(sect, fmt, start=1):
    sectPr = sect._sectPr
    # remove existing pgNumType
    for old in sectPr.findall(qn("w:pgNumType")):
        sectPr.remove(old)
    pg = OxmlElement("w:pgNumType")
    pg.set(qn("w:fmt"), fmt)
    pg.set(qn("w:start"), str(start))
    sectPr.append(pg)

# Section 1: front matter -> lowerRoman
set_pgNumType(sections[1], "lowerRoman", 1)
print("Section 1 (front matter) -> lowerRoman, start=1")

# Section 2: chapters -> decimal, start=1
set_pgNumType(sections[2], "decimal", 1)
print("Section 2 (chapters) -> decimal, start=1")

# Ensure section 0 has NO page number in footer (unnumbered). Remove any footer ref.
s0 = sections[0]
# footer is empty by default; ensure not linked to a numbered footer
print("Section 0 footer is_linked_to_previous:", s0.footer.is_linked_to_previous)

doc.save(DOCX)
print("Saved patched docx:", DOCX)
