from docx import Document
from docx.shared import Inches
from pathlib import Path

folder = Path(r"S:\Users\L\Downloads\New folder (175)\testgit\os\l8\imgs")
doc = Document()

doc.add_heading("Зображення з теки imgs", level=1)

# визначення стилю Caption
caption_style = "Caption"
if caption_style not in doc.styles:
    if "Підпис" in doc.styles:  # українська версія Word
        caption_style = "Підпис"
    else:
        caption_style = None

# формати зображень
exts = {".png", ".jpg", ".jpeg", ".gif", ".bmp"}

index = 1  # лічильник зображень

for img in sorted(folder.iterdir()):
    if img.suffix.lower() in exts:

        # ---------------------------
        # 1. Додаємо текст-посилання
        # ---------------------------
        reference_text = f"На рис. {index} зображено {img.stem}."
        ref_p = doc.add_paragraph(reference_text)
        ref_p.alignment = 0  # вирівнювання зліва

        doc.add_paragraph()  # невеликий відступ

        # ---------------------------
        # 2. Вставляємо зображення
        # ---------------------------
        doc.add_picture(str(img), width=Inches(6))

        # ---------------------------
        # 3. Додаємо підпис під малюнком
        # ---------------------------
        caption_text = f"Рис. {index} — {img.stem}"
        p = doc.add_paragraph(caption_text)
        if caption_style:
            p.style = caption_style
        p.alignment = 1  # центр підпису

        doc.add_paragraph()  # відступ між блоками

        index += 1

# вихідний файл
output_path = folder / "imgs.docx"
doc.save(output_path)

print("Готово:", output_path)
