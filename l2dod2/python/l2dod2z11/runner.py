# runner.py
import subprocess
import sys

def main():
    try:
        # Запускаємо matrix_sum.py як новий процес
        process = subprocess.run(
            [sys.executable, "matrix_sum.py"],  # або "python3" залежно від системи
            check=True
        )
    except subprocess.CalledProcessError as e:
        print("Процес завершився з помилкою:", e)

if __name__ == "__main__":
    main()
