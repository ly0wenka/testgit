import os

# Шлях до директорії
dir_path = r"S:\Users\L\Downloads\New folder (175)\testgit\os\l8\imgs\imgsdocx"

# Розширення файлів, які вважаємо зображеннями
image_exts = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}

for root, dirs, files in os.walk(dir_path):
    for file in files:
        file_path = os.path.join(root, file)
        ext = os.path.splitext(file)[1].lower()
        print(f"Файл: {file_path}")
        if ext in image_exts:
            print("<Зображення пропущено>")
        else:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    print(content)
            except Exception as e:
                print(f"<Не вдалося прочитати файл: {e}>")
        print("-" * 80)
