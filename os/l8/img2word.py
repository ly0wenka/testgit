from docx import Document
from docx.shared import Inches
from pathlib import Path

folder = Path(r"S:\Users\L\Downloads\New folder (175)\testgit\os\l8\imgs")
doc = Document()

doc.add_heading("Зображення з теки imgs", level=1)

# формати зображень
exts = {".png", ".jpg", ".jpeg", ".gif", ".bmp"}

for img in sorted(folder.iterdir()):
    if img.suffix.lower() in exts:
        doc.add_picture(str(img), width=Inches(6))
        p = doc.add_paragraph(img.stem)
        p.alignment = 1
        doc.add_paragraph()  # відступ між зображеннями

output_path = "imgs.docx"
doc.save(output_path)

print("Готово:", output_path)
