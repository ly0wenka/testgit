#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#define NUM_CHAIRS 3 // Кількість стільців для клієнтів
#define NUM_CLIENTS 10 // Кількість клієнтів

sem_t barber_sleep; // Семофор, щоб перукар міг заснути
sem_t chair; // Семофор для доступу до крісла
sem_t waiting_room; // Семофор для стільців у кімнаті очікування
int waiting_clients = 0; // Лічильник клієнтів у кімнаті очікування

void* barber(void* arg) {
    while (1) {
        // Чекаємо, поки клієнт не займе крісло
        sem_wait(&barber_sleep);
        
        // Перукар працює
        printf("Перукар стриже клієнта...\n");
        sleep(3); // Стрижка займає 3 секунди
        printf("Перукар завершив стрижку.\n");
        
        // Після завершення стрижки перукар знову засинає
        sem_post(&barber_sleep);
    }
    return NULL;
}

void* client(void* arg) {
    int id = *((int*)arg);
    printf("Клієнт %d прийшов в перукарню.\n", id);
    
    if (sem_trywait(&waiting_room) == 0) { // Якщо є вільний стілець
        printf("Клієнт %d сів у стілець і чекає.\n", id);
        
        // Якщо є вільне крісло, клієнт займе його
        sem_wait(&chair);
        
        // Клієнт будить перукаря, якщо він спав
        sem_post(&barber_sleep);
        
        // Клієнт чекає на стрижку
        printf("Клієнт %d сідає в крісло для стрижки.\n", id);
        sleep(3); // Стрижка клієнта займає 3 секунди
        sem_post(&chair); // Клієнт вільний, перукар може спати
    } else {
        // Якщо всі стільці зайняті, клієнт йде
        printf("Клієнт %d повертається, бо немає вільних стільців.\n", id);
    }
    
    return NULL;
}

int main() {
    pthread_t barber_thread;
    pthread_t client_threads[NUM_CLIENTS];
    int client_ids[NUM_CLIENTS];
    
    // Ініціалізація семафорів
    sem_init(&barber_sleep, 0, 1); // Перукар спить спочатку
    sem_init(&chair, 0, 1); // Крісло для одного клієнта
    sem_init(&waiting_room, 0, NUM_CHAIRS); // Столиці в кімнаті очікування

    // Створення потоку для перукаря
    pthread_create(&barber_thread, NULL, barber, NULL);

    // Створення потоків для клієнтів
    for (int i = 0; i < NUM_CLIENTS; i++) {
        client_ids[i] = i + 1;
        pthread_create(&client_threads[i], NULL, client, &client_ids[i]);
        sleep(1); // Затримка для імітації різного часу приходу клієнтів
    }

    // Очікуємо завершення всіх клієнтів
    for (int i = 0; i < NUM_CLIENTS; i++) {
        pthread_join(client_threads[i], NULL);
    }
    
    // Завершення роботи семафорів
    sem_destroy(&barber_sleep);
    sem_destroy(&chair);
    sem_destroy(&waiting_room);
    
    return 0;
}
