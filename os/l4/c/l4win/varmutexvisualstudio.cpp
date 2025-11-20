#include <windows.h>
#include <process.h>
#include <stdio.h>

#define BUFFER_SIZE 5
int buffer[BUFFER_SIZE];
int count = 0;

CRITICAL_SECTION cs;
CONDITION_VARIABLE not_full;
CONDITION_VARIABLE not_empty;

unsigned __stdcall producer(void* arg) {
    for (int i = 0; i < 10; i++) {
        EnterCriticalSection(&cs);
        while (count == BUFFER_SIZE)
            SleepConditionVariableCS(&not_full, &cs, INFINITE);

        buffer[count++] = i;
        printf("Produced: %d\n", i);

        WakeConditionVariable(&not_empty);
        LeaveCriticalSection(&cs);
        Sleep(200); // щоб бачити взаємодію
    }
    return 0;
}

unsigned __stdcall consumer(void* arg) {
    for (int i = 0; i < 10; i++) {
        EnterCriticalSection(&cs);
        while (count == 0)
            SleepConditionVariableCS(&not_empty, &cs, INFINITE);

        int item = buffer[--count];
        printf("Consumed: %d\n", item);

        WakeConditionVariable(&not_full);
        LeaveCriticalSection(&cs);
        Sleep(400); // для наочності
    }
    return 0;
}

int main() {
    InitializeCriticalSection(&cs);
    InitializeConditionVariable(&not_full);
    InitializeConditionVariable(&not_empty);

    HANDLE prodThread = (HANDLE)_beginthreadex(NULL, 0, producer, NULL, 0, NULL);
    HANDLE consThread = (HANDLE)_beginthreadex(NULL, 0, consumer, NULL, 0, NULL);

    WaitForSingleObject(prodThread, INFINITE);
    WaitForSingleObject(consThread, INFINITE);

    CloseHandle(prodThread);
    CloseHandle(consThread);

    DeleteCriticalSection(&cs);

    printf("All threads finished.\n");
    return 0;
}
