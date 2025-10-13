# Використовуємо офіційний образ .NET SDK для побудови
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /app

# Копіюємо вихідний код
COPY . .

# Компілюємо програму
RUN dotnet publish -c Release -o out

# Використовуємо легкий runtime-образ для запуску
FROM mcr.microsoft.com/dotnet/runtime:8.0
WORKDIR /app

# Копіюємо збірку з етапу build
COPY --from=build /app/out .

# Встановлюємо команду за замовчуванням
ENTRYPOINT ["dotnet", "l2csharp.dll"]
