# Використовуємо легкий Python образ
FROM python:3.11-slim

# Робоча папка в контейнері
WORKDIR /app

# Копіюємо файли
COPY . .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Відкриваємо порт
EXPOSE 5000

# Запуск Flask
CMD ["python", "app.py"]