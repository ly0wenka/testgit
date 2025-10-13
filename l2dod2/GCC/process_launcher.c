#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <process.h>  // For spawnl
#include <windows.h>

void print_number_as_text(const char *number) {
    if (number[0] == '-') {
        printf("minus ");
        number = number + 1;  // Skip the minus sign
    }
    printf("%s\n", number);
}

int main(int argc, char *argv[]) {
    char *number = NULL;

    // Handle command line arguments or prompt user for input
    if (argc > 1 && strcmp(argv[1], "-n") == 0 && argc > 2) {
        number = argv[2];  // Get the number argument after -n
    }

    if (number != NULL) {
        print_number_as_text(number);
    } else {
        // If no argument, prompt the user for input
        printf("Input the number: ");
        char input[100];
        fgets(input, sizeof(input), stdin);
        input[strcspn(input, "\n")] = 0;  // Remove newline character
        number = input;
    }

    // Prepare the command to run the external process
    // char command[256];
    // snprintf(command, sizeof(command), "\"S:\\Users\\L\\Downloads\\New folder (100)\\GCC\\number_to_words.exe\" -n %s", number);

    // Spawn the process using spawnl with _P_NOWAIT
    int result = _spawnl(_P_NOWAIT, "S:\\Users\\L\\Downloads\\New folder (100)\\GCC\\number_to_words.exe", "number_to_words.exe", "-n", number, NULL);

    if (result == -1) {
        // If spawnl fails, print error and return
        printf("Error creating process: %d\n", errno);
        return 1;
    }

    printf("Process spawned successfully\n");

    return 0;
}
