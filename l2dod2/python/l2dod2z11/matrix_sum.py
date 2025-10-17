# matrix_sum.py

def main():
    n = int(input("Введіть розмір квадратної матриці (n): "))

    matrix = []
    print("Введіть елементи матриці построково через пробіл:")
    for i in range(n):
        row = list(map(int, input().split()))
        if len(row) != n:
            print(f"Помилка: рядок {i+1} має {len(row)} елементів, очікувалось {n}")
            return
        matrix.append(row)

    total = 0
    for i in range(n):
        for j in range(n):
            # Пропускаємо головну та побічну діагональ
            if i != j and i + j != n - 1:
                total += matrix[i][j]

    print("Сума елементів, що не лежать на головній та побічній діагоналі:", total)

if __name__ == "__main__":
    main()
