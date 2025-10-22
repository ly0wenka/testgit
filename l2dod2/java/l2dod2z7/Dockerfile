# Базовий образ із Java
FROM openjdk:21-slim

# Створюємо робочу директорію
WORKDIR /app

# Копіюємо файли у контейнер
COPY Runner.java .
COPY Sorter.java .

# Компілюємо Java-файли
RUN javac Runner.java Sorter.java

# Встановлюємо команду запуску
CMD ["java", "Runner"]
