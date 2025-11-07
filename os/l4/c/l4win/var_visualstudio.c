#include <windows.h>
#include <process.h>
#include <stdio.h>

char message[] = "Hello World";

unsigned __stdcall thread_function(void* arg) {
    printf_s("thread_function is running. Argument was %s\n", (char*)arg);
    Sleep(3000);  // Sleep у мс (3000 = 3 с)
    strcpy_s(message, sizeof(message), "Bye!");
    _endthreadex(0);
    return 0;
}

int main() {
    HANDLE a_thread;
    unsigned threadID;

    printf_s("Creating thread...\n");

    a_thread = (HANDLE)_beginthreadex(NULL, 0, thread_function, (void*)message, 0, &threadID);
    if (a_thread == 0) {
        perror("Thread creation failed");
        return 1;
    }

    printf_s("Waiting for thread to finish...\n");

    WaitForSingleObject(a_thread, INFINITE); // очікування завершення
    printf_s("Thread joined.\n");
    printf_s("Message is now: %s\n", message);

    CloseHandle(a_thread);
    return 0;
}
