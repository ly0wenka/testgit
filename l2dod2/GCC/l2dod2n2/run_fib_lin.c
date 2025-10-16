#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    char number[100];

    // Отримуємо номер від користувача
    printf("Введіть номер числа Фібоначчі: ");
    fgets(number, sizeof(number), stdin);
    number[strcspn(number, "\n")] = 0;  // Видаляємо '\n'

    // Створюємо дочірній процес
    pid_t pid = fork();
    if (pid < 0) {
        perror("Fork failed");
        return 1;
    }

    if (pid == 0) {  // Дочірній процес
        char *executable = "./fib.out";  // Шлях до першої програми
        char *args[] = {executable, "-n", number, NULL};
        execvp(executable, args);

        // Якщо execvp не вдалось
        perror("Exec failed");
        exit(1);
    } else {  // Батьківський процес
        int status;
        waitpid(pid, &status, 0);

        if (WIFEXITED(status)) {
            printf("Child process finished with exit status %d\n", WEXITSTATUS(status));
        } else {
            printf("Child process terminated abnormally\n");
        }
    }

    return 0;
}
