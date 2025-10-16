#include <stdio.h>
#include <process.h>
#include <string.h>
#include <windows.h>

int main() {
    
    SetConsoleOutputCP(CP_UTF8);
    char number[100];

    printf("Введіть номер числа Фібоначчі: ");
    fgets(number, sizeof(number), stdin);
    number[strcspn(number, "\n")] = 0;  // видаляємо '\n'

    // Шлях до першої програми (змінити під свій)
    const char *exePath = "S:\\Users\\L\\Downloads\\New folder (175)\\testgit\\l2dod2\\GCC\\l2dod2n2\\fib.exe";

    // Запуск процесу
    int result = _spawnl(_P_WAIT, exePath, "fib.exe", "-n", number, NULL);
    if (result == -1) {
        printf("Помилка запуску процесу\n");
        return 1;
    }

    return 0;
}
