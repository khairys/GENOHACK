"""PDF from the visually reviewed render of the same editable pitch deck."""
import hashlib
import json
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parents[1]
work = ROOT / "artifacts/qa/audited-pitch"
pptx = ROOT / "artifacts/pitch/BantengPanel_GENOHACK_2026_Audited.pptx"
output = pptx.with_suffix(".pdf")
facts = json.loads((ROOT / "artifacts/public/pitch_facts.json").read_text())
pdf = canvas.Canvas(str(output), pagesize=(960, 540), pageCompression=1)
pdf.setTitle("BantengPanel — Exastra — GENOHACK 2026")
pdf.setAuthor("Exastra")
pdf.setSubject("Research prototype; S1 simulation and business assumptions explicitly labelled")
images = []
with zipfile.ZipFile(pptx) as z:
    for i in range(1, 12):
        image = work / f"slide-{i:02d}.png"
        pdf.drawImage(ImageReader(str(image)), 0, 0, width=960, height=540)
        # Searchable text mirrors the PPTX. Invisible render mode preserves the exact slide appearance.
        xml = ET.fromstring(z.read(f"ppt/slides/slide{i}.xml"))
        text = " ".join(t.text or "" for t in xml.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}t"))
        hidden = pdf.beginText(1, 1)
        hidden.setFont("Helvetica", 1)
        hidden.setTextRenderMode(3)
        hidden.textLine(text)
        pdf.drawText(hidden)
        pdf.bookmarkPage(f"slide{i}")
        pdf.addOutlineEntry(f"{i}. {facts['speakerSegments'][i-1]['title']}", f"slide{i}")
        if i == 5:
            pdf.linkURL(facts["liveDemo"], (55, 36, 900, 64), relative=0, thickness=0)
        images.append({"slide": i, "pngSha256": hashlib.sha256(image.read_bytes()).hexdigest()})
        pdf.showPage()
pdf.save()
(ROOT / "artifacts/public/pitch_pdf_render_manifest.json").write_text(json.dumps({"sourceCommit": facts["sourceCommit"], "pptxSha256": hashlib.sha256(pptx.read_bytes()).hexdigest(), "pdfSha256": hashlib.sha256(output.read_bytes()).hexdigest(), "pages": images, "method": "Full-slide reviewed renders plus invisible searchable text from the same PPTX"}, indent=2), encoding="utf-8")
print(output)
