#!/usr/bin/env python3
"""Final programmatic verification of Project_Report.docx."""
import os, re, zipfile
from docx import Document
from docx.shared import Pt, Cm, Emu

DOCX = "/home/sriragul/frappe-bench/apps/institution_erp/report/final_report/Project_Report.docx"
PDF = "/home/sriragul/frappe-bench/apps/institution_erp/report/final_report/Project_Report.pdf"
doc = Document(DOCX)
sec = doc.sections[0]
results = []
def check(name, ok, detail=""):
    results.append((name, "PASS" if ok else "FAIL", detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))

# Page setup
check("A4 size", abs(sec.page_width - Cm(21.0)) < Emu(5000) and abs(sec.page_height - Cm(29.7)) < Emu(5000), f"{sec.page_width.cm}x{sec.page_height.cm}cm")
check("Portrait", sec.orientation.value == 0, "value 0=portrait")
check("Margins 1in T/B/R", abs(sec.top_margin.cm-2.54)<0.05 and abs(sec.bottom_margin.cm-2.54)<0.05 and abs(sec.right_margin.cm-2.54)<0.05, "1in")
check("Margin L 1.25in binding", abs(sec.left_margin.cm-3.175)<0.05, f"{sec.left_margin.cm}cm")
# Styles
n = doc.styles["Normal"]
check("Normal TNR 13pt justified 1.5", n.font.name=="Times New Roman" and n.font.size.pt==13 and n.paragraph_format.alignment.value==3 and n.paragraph_format.line_spacing==1.5, "TNR/13/justify/1.5")
for lvl in ["Heading 1","Heading 2","Heading 3"]:
    st=doc.styles[lvl]
    check(f"{lvl} TNR 14pt bold", st.font.name=="Times New Roman" and st.font.size.pt==14 and st.font.bold==True, lvl)
# Fields in body + footers
xml = doc.element.xml
z = zipfile.ZipFile(DOCX)
footer_xml = "".join(z.read(n).decode('utf-8',errors='ignore') for n in z.namelist() if 'footer' in n.lower())
check("TOC field", 'TOC' in xml, "body")
check("LOF field", '\\c "Figure"' in xml, "body")
check("LOT field", '\\c "Table"' in xml, "body")
check("PAGE field in footers", 'PAGE' in footer_xml, "footers")
# Images
media=[m for m in z.namelist() if m.startswith("word/media/")]
check("16 images embedded (reduced set)", len(media)==16, f"{len(media)}")
# Tables & captions
check("17+ tables", len(doc.tables)>=17, f"{len(doc.tables)}")
fig_caps=[p.text for p in doc.paragraphs if p.text.startswith("Figure ")]
tab_caps=[p.text for p in doc.paragraphs if p.text.startswith("Table ")]
check("15+ figure captions", len(fig_caps)>=15, f"{len(fig_caps)}")
check("12+ table captions", len(tab_caps)>=12, f"{len(tab_caps)}")
# Headings
h1s=[p.text for p in doc.paragraphs if p.style.name=="Heading 1"]
check("6+ chapter H1s", len(h1s)>=6, f"{len(h1s)}")
# PDF
pdf_ok = False
pdf_pages = 0
try:
    import fitz
    d=fitz.open(PDF)
    pdf_ok = len(d)>0
    pdf_pages = len(d)
except Exception:
    pdf_ok = os.path.exists(PDF)
    pdf_pages = -1
check("PDF generated", pdf_ok, f"{pdf_pages} pages" if pdf_pages>0 else "exists on disk")

passed=sum(1 for _,s,_ in results if s=="PASS")
failed=sum(1 for _,s,_ in results if s=="FAIL")
print(f"\n=== PASS: {passed} | FAIL: {failed} ===")
for n,s,d in results:
    if s=="FAIL": print(f"  FAIL: {n} — {d}")
