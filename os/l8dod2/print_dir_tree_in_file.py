import os

# Шлях до директорії
dir_path = r"S:\Users\L\Downloads\New folder (175)\testgit\os\l8\imgs\imgsdocx"

# Вивідний файл
output_file = r"S:\Users\L\Downloads\New folder (175)\testgit\os\l8\imgs\output.txt"

# Розширення файлів, які вважаємо зображеннями
image_exts = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}

with open(output_file, 'w', encoding='utf-8') as out_f:
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()
            out_f.write(f"Файл: {file_path}\n")
            if ext in image_exts:
                out_f.write("<Зображення пропущено>\n")
            else:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        out_f.write(content + "\n")
                except Exception as e:
                    out_f.write(f"<Не вдалося прочитати файл: {e}>\n")
            out_f.write("-" * 80 + "\n")
