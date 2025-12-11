from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml.ns import qn
from pathlib import Path

folder = Path(r"S:\Users\L\Downloads\New folder (175)\testgit\os\l8\imgs")
doc = Document()

# ---------------------------
# Заголовок документа
# ---------------------------
heading = doc.add_heading("Зображення з теки imgs", level=1)

# Arial 16
run = heading.runs[0]
run.font.name = 'Arial'
run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Arial')
run.font.size = Pt(16)
run.font.color.rgb = RGBColor(0, 0, 0)  # чорний

# ---------------------------
# Стиль підписів
# ---------------------------
caption_style = "Caption"
if caption_style not in doc.styles:
    if "Підпис" in doc.styles:
        caption_style = "Підпис"
    else:
        caption_style = None

# формати зображень
exts = {".png", ".jpg", ".jpeg", ".gif", ".bmp"}

index = 1  # лічильник зображень

for img in sorted(folder.iterdir()):
    if img.suffix.lower() in exts:

        # ---------------------------
        # 1. Текст-посилання
        # ---------------------------
        reference_text = f"На рис. {index} зображено {img.stem}."
        ref_p = doc.add_paragraph(reference_text)
        ref_p.alignment = 0  # ліворуч

        run = ref_p.runs[0]
        run.font.name = 'Arial'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Arial')
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(0, 0, 0)  # чорний

        doc.add_paragraph()  # відступ

        # ---------------------------
        # 2. Додаємо зображення
        # ---------------------------
        doc.add_picture(str(img), width=Inches(6))

        # ---------------------------
        # 3. Підпис під малюнком
        # ---------------------------
        caption_text = f"Рис. {index} — {img.stem}"
        p = doc.add_paragraph(caption_text)
        if caption_style:
            p.style = caption_style
        p.alignment = 1  # центр

        run = p.runs[0]
        run.font.name = 'Arial'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Arial')
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(0, 0, 0)  # чорний

        doc.add_paragraph()  # відступ

        index += 1

# ---------------------------
# Збереження документа
# ---------------------------
output_path = folder / "imgs.docx"
doc.save(output_path)

print("Готово:", output_path)
