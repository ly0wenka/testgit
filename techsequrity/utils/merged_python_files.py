import os

# Шлях до теки з .py файлами
folder_path = r"S:\Users\L\Downloads\New folder (175)\testgit\techsequrity\pr1.1"

# Назва вихідного файлу
output_file = "merged_python_files.py"

with open(output_file, "w", encoding="utf-8") as outfile:
    # Перебір усіх файлів у теці
    for filename in os.listdir(folder_path):
        if filename.endswith(".py"):
            file_path = os.path.join(folder_path, filename)

            # Заголовок файлу
            outfile.write(f"\n# ===== FILE: {filename} =====\n\n")

            # Читання та запис вмісту
            with open(file_path, "r", encoding="utf-8") as infile:
                outfile.write(infile.read())
                outfile.write("\n\n")

print(f"Усі Python-файли об'єднано у: {output_file}")