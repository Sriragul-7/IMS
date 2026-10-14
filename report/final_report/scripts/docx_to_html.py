#!/usr/bin/env python3
"""
Convert Project_Report.docx to HTML, then to PDF via wkhtmltopdf.
Reuses the generated docx content (headings, paragraphs, tables, images).
"""
import os
import zipfile
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn
from PIL import Image

APP_ROOT = "/home/sriragul/frappe-bench/apps/institution_erp"
FINAL_DIR = os.path.join(APP_ROOT, "report", "final_report")
DOCX = os.path.join(FINAL_DIR, "Project_Report.docx")
HTML_OUT = os.path.join(FINAL_DIR, "report.html")
PDF_OUT = os.path.join(FINAL_DIR, "Project_Report.pdf")
IMAGES_DIR = os.path.join(FINAL_DIR, "images")

# Extract embedded images from docx to a temp folder for HTML img src
MEDIA_DIR = "/tmp/opencode/docx_media"
os.makedirs(MEDIA_DIR, exist_ok=True)

# Map relationship id -> image file path (extract from docx media)
docx_zip = zipfile.ZipFile(DOCX)
image_rel_map = {}
# word/_rels/document.xml.rels maps rId to media
import re
rels_xml = docx_zip.read("word/_rels/document.xml.rels").decode("utf-8")
for m in re.finditer(r'Id="(rId\d+)"[^>]*Target="media/([^"]+)"', rels_xml):
    rid, fname = m.group(1), m.group(2)
    # extract media file
    data = docx_zip.read(f"word/media/{fname}")
    outpath = os.path.join(MEDIA_DIR, fname)
    with open(outpath, "wb") as f:
        f.write(data)
    image_rel_map[rid] = outpath

doc = Document(DOCX)

html_parts = []
html_parts.append("""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>Institution ERP - Project Report</title>
<style>
@page { size: A4; margin: 25.4mm 25.4mm 25.4mm 31.75mm; @bottom-center { content: counter(page); font-family:'Times New Roman'; font-size: 12pt; } }
body { font-family: "Times New Roman", serif; font-size: 13pt; line-height: 1.5; text-align: justify; color: #000; margin: 0; }
h1.ch { font-size: 14pt; font-weight: bold; text-align: center; text-transform: uppercase; page-break-before: always; margin: 0 0 12pt 0; line-height: 1.5; }
h2.sec { font-size: 14pt; font-weight: bold; text-transform: uppercase; text-align: left; margin: 6pt 0 6pt 0; line-height: 1.5; page-break-after: avoid; }
h3.sub { font-size: 14pt; font-weight: bold; text-align: left; margin: 6pt 0 6pt 0; line-height: 1.5; page-break-after: avoid; }
p { margin: 0 0 6pt 0; text-align: justify; }
p.center { text-align: center; }
.caption { font-size: 13pt; text-align: center; margin: 4pt 0 8pt 0; }
.caption b { font-weight: bold; }
table { border-collapse: collapse; margin: 6pt auto; font-size: 10pt; }
th, td { border: 1px solid #000; padding: 3pt 6pt; text-align: left; vertical-align: top; }
th { background: #D9D9D9; font-weight: bold; text-align: center; }
ul { margin: 0 0 6pt 0; text-align: justify; }
ul li { margin-bottom: 2pt; text-align: justify; }
img { display: block; margin: 6pt auto; max-width: 14.5cm; }
.cover { text-align: center; page-break-after: always; }
.toc-field, .lof-field, .lot-field { text-align: left; margin: 10pt 0; }
.nobreak { page-break-inside: avoid; }
</style></head><body>""")

def iter_block_items(parent):
    """Yield paragraphs and tables in document order."""
    from docx.oxml.text.paragraph import CT_P
    from docx.oxml.table import CT_Tbl
    parent_element = parent.element.body
    for child in parent_element.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)

def run_to_html(run):
    r = run._r
    text = run.text
    # escape
    import html as ihtml
    text = ihtml.escape(text)
    # bold/italic/caps
    bold = run.bold
    italic = run.italic
    # caps via w:caps
    caps = r.find(qn('w:rPr'))
    is_caps = False
    if caps is not None and caps.find(qn('w:caps')) is not None:
        is_caps = True
    if is_caps:
        text = text.upper()
    tag = "span"
    attrs = []
    if bold:
        text = f"<b>{text}</b>"
    if italic:
        text = f"<i>{text}</i>"
    return text

def para_to_html(p):
    text = "".join(run_to_html(r) for r in p.runs)
    # alignment
    align = p.alignment
    style = ""
    if align is not None:
        name = str(align).split(".")[-1]
        style = f' style="text-align: {name.lower()};"'
    # detect heading style
    pstyle = p.style.name
    if pstyle == "Heading 1":
        return f'<h1 class="ch">{text}</h1>'
    if pstyle == "Heading 2":
        return f'<h2 class="sec">{text}</h2>'
    if pstyle == "Heading 3":
        return f'<h3 class="sub">{text}</h3>'
    # bullet
    if pstyle.startswith("List Bullet"):
        return f'<li>{text}</li>'
    # field placeholders
    if "Right-click and select" in text:
        return f'<p class="toc-field">{text}</p>'
    return f'<p{style}>{text}</p>'

def table_to_html(t):
    out = ['<table>']
    for i, row in enumerate(t.rows):
        tag = "th" if i == 0 else "td"
        out.append("<tr>")
        for cell in row.cells:
            cell_text = ""
            for cp in cell.paragraphs:
                cell_text += "".join(run_to_html(r) for r in cp.runs) + " "
            out.append(f"<{tag}>{cell_text.strip()}</{tag}>")
        out.append("</tr>")
    out.append("</table>")
    return "\n".join(out)

for block in iter_block_items(doc):
    if isinstance(block, Paragraph):
        html_parts.append(para_to_html(block))
    elif isinstance(block, Table):
        html_parts.append(table_to_html(block))
    # images: handle via inline shapes in paragraphs - find drawings
    # We also need to place images. python-docx: paragraph._element finds w:drawing
    if isinstance(block, Paragraph):
        import re as _re
        drawings = block._element.findall('.//' + qn('w:drawing'))
        for dw in drawings:
            blip = dw.find('.//' + qn('a:blip'))
            embed = None
            if blip is not None:
                embed = blip.get(qn('r:embed'))
                if embed and embed in image_rel_map:
                    imgpath = image_rel_map[embed]
                    fname = os.path.basename(imgpath)
                    html_parts.append(f'<p class="center"><img src="{fname}" alt="figure" style="max-width:14.5cm;"></p>')

html_parts.append("</body></html>")

html = "\n".join(html_parts)
with open(HTML_OUT, "w") as f:
    f.write(html)
print("Wrote HTML:", HTML_OUT, len(html), "chars")
