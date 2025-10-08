#include <stdio.h>
#include <unistd.h>  // for sleep() on Linux/macOS
// #include <windows.h> // for Sleep() on Windows

int main() {
    while (1) {
        printf("Hello, World!\n");
        fflush(stdout);  // ensure output appears immediately
        sleep(5);        // wait for 5 seconds (Linux/macOS)
        // Sleep(5000);  // use this instead for Windows (milliseconds)
    }
    return 0;
}
