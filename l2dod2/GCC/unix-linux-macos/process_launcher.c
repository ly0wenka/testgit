#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

void print_number_as_text(const char *number) {
    if (number[0] == '-') {
        printf("мінус ");
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
        printf("Введіть число: ");
        char input[100];
        fgets(input, sizeof(input), stdin);
        input[strcspn(input, "\n")] = 0;  // Remove newline character
        number = input;
    }

    // Fork to create a child process
    pid_t pid = fork();
    
    if (pid == -1) {
        perror("Fork failed");
        return 1;
    }
    
    if (pid == 0) {  // Child process
        // Prepare the arguments for exec
        char *executable = "/home/oleksii_kondratov/testgit/l2dod2/GCC/1.out";  // Path to the executable
        char *args[] = {executable, "-n", number, NULL};

        // Execute the external program
        execvp(executable, args);

        // If execvp fails
        perror("Exec failed");
        exit(1);
    } else {  // Parent process
        // Wait for the child process to finish
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

