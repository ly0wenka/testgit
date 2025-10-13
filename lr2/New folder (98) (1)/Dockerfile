# 1. Вибір базового образу для збірки
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build

# 2. Встановлюємо робочу директорію
WORKDIR /app

# 3. Копіюємо csproj і відновлюємо залежності
COPY *.csproj ./
RUN dotnet restore

# 4. Копіюємо всі файли проекту та збираємо програму
COPY . ./
RUN dotnet publish -c Release -o out

# 5. Створюємо образ для виконання програми
FROM mcr.microsoft.com/dotnet/runtime:7.0

WORKDIR /app

# Копіюємо зібрані файли з образу build
COPY --from=build /app/out .

# Встановлюємо команду запуску за замовчуванням
ENTRYPOINT ["dotnet", "YourApp.dll"]
