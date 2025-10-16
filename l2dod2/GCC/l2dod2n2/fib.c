#include <stdio.h>
#include <stdlib.h>
#ifdef _WIN32
#include <windows.h>
#endif
long long fibonacci(int n)
{
    if (n == 0 || n == 1)
        return 1;

    long long a = 1, b = 1, c;
    for (int i = 2; i <= n; i++)
    {
        c = a + b;
        a = b;
        b = c;
    }
    return b;
}

int main(int argc, char *argv[])
{
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
#endif
    int n = -1;

    // Перевірка аргументів
    if (argc > 2 && strcmp(argv[1], "-n") == 0)
    {
        n = atoi(argv[2]);
    }
    else
    {
        // Якщо аргументів немає, запитуємо у користувача
        printf("Введіть номер числа Фібоначчі: ");
        scanf("%d", &n);
    }

    if (n < 0)
    {
        printf("Помилка: номер повинен бути невід'ємним числом\n");
        return 1;
    }

    long long result = fibonacci(n);
    printf("Fibonacci(%d) = %lld\n", n, result);

    return 0;
}
