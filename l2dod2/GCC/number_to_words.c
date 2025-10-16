#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>  // Для getopt

void print_number_as_text(const char *number) {
    if (number[0] == '-') {
        printf("мінус ");
        number++;  // Пропустити знак мінус
    }
    printf("%s\n", number);
}

int main(int argc, char *argv[]) {
    SetConsoleOutputCP(CP_UTF8);
    int opt;
    char *number = NULL;

    while ((opt = getopt(argc, argv, "n:")) != -1) {
        switch (opt) {
            case 'n':
                number = optarg;
                break;
            default:
                fprintf(stderr, "Використання: %s -n <число>\n", argv[0]);
                return 1;
        }
    }

    if (number) {
        print_number_as_text(number);
    } else {
        fprintf(stderr, "Помилка: відсутній аргумент -n\n");
        return 1;
    }

    return 0;
}
