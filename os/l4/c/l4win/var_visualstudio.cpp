#include <windows.h>
#include <process.h>
#include <iostream>
#include <cstring>

char message[] = "Hello World";

int main() {
    HANDLE a_thread;
    unsigned threadID;

    // Lambda для виконання в окремому потоці
    auto lambda_func = [](void* arg) -> unsigned {
        std::cout << "Lambda is running. Argument was "
            << static_cast<char*>(arg) << std::endl;
        Sleep(3000);  // 3 секунди (в мілісекундах)
        strcpy_s(message, sizeof(message), "Bye!");
        _endthreadex(0);  // завершення потоку
        return 0;
        };

    // "трамплін" — функція, що передає lambda до потоку
    auto trampoline = [](void* arg) -> unsigned __stdcall {
        auto lambda = *static_cast<decltype(lambda_func)*>(arg);
        return lambda(message);
    };

    // Створення потоку
    a_thread = (HANDLE)_beginthreadex(nullptr, 0, trampoline, &lambda_func, 0, &threadID);
    if (a_thread == 0) {
        std::cerr << "Thread creation failed" << std::endl;
        return 1;
    }

    std::cout << "Waiting for thread to finish..." << std::endl;

    // Очікування завершення потоку
    WaitForSingleObject(a_thread, INFINITE);
    std::cout << "Thread joined.\n";
    std::cout << "Message is now: " << message << std::endl;

    // Закриття дескриптора потоку
    CloseHandle(a_thread);
    return 0;
}
