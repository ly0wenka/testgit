#include <unistd.h>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <pthread.h>

char message[] = "Hello World";

int main() {
    int res;
    pthread_t a_thread;
    void *thread_result;

    // Lambda function to be run in a thread
    auto lambda_func = [](void *arg) -> void* {
        std::cout << "Lambda is running. Argument was " << static_cast<char*>(arg) << std::endl;
        sleep(3);
        std::strcpy(message, "Bye!");
        pthread_exit((void*)"Always for a CPU time");
        return nullptr;
    };

    // Create the thread and pass the lambda via a trampoline
    res = pthread_create(&a_thread, nullptr,
                         +[](void *arg) -> void* {
                             auto lambda = *static_cast<decltype(lambda_func)*>(arg);
                             return lambda(message);
                         },
                         &lambda_func);

    if (res != 0) {
        std::cerr << "Thread creation failed" << std::endl;
        std::exit(EXIT_FAILURE);
    }

    std::cout << "Waiting for thread to finish..." << std::endl;

    res = pthread_join(a_thread, &thread_result);
    if (res != 0) {
        std::cerr << "Thread join failed" << std::endl;
        std::exit(EXIT_FAILURE);
    }

    std::cout << "Thread joined, it returned: " << static_cast<char*>(thread_result) << std::endl;
    std::cout << "Message is now: " << message << std::endl;

    return EXIT_SUCCESS;
}
