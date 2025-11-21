using System;
using System.Threading;

class Program
{
    const int NUM_CHAIRS = 3;
    const int NUM_CLIENTS = 10;

    static Semaphore barberSleep = new Semaphore(0, 1); // Перукар спить
    static Semaphore chair = new Semaphore(1, 1);       // Крісло для стрижки
    static Semaphore waitingRoom = new Semaphore(NUM_CHAIRS, NUM_CHAIRS); // Кімната очікування
    static AutoResetEvent haircutDone = new AutoResetEvent(false);

    static void Barber()
    {
        while (true)
        {
            barberSleep.WaitOne(); // чекає клієнта
            Console.WriteLine("Перукар стриже клієнта...");
            Thread.Sleep(3000);
            Console.WriteLine("Перукар завершив стрижку.");
            haircutDone.Set();  // сигналізує клієнту, що стрижка завершена
        }
    }

    static void Client(object obj)
    {
        int id = (int)obj;
        Console.WriteLine($"Клієнт {id} прийшов.");

        if (waitingRoom.WaitOne(0)) // якщо є місце
        {
            Console.WriteLine($"Клієнт {id} сів у кімнаті очікування.");

            chair.WaitOne();          // Займає крісло
            barberSleep.Release(); // Будить перукаря

            haircutDone.WaitOne(); // Чекає, поки перукар завершить стрижку

            chair.Release();       // Звільняє крісло
            waitingRoom.Release(); // Звільняє місце у кімнаті очікування
        }
        else
        {
            Console.WriteLine($"Клієнт {id} повертається, бо немає місця.");
        }
    }


    static void Main(string[] args)
    {
        Console.OutputEncoding = System.Text.Encoding.UTF8;
        System.Threading.Thread.CurrentThread.CurrentUICulture = new System.Globalization.CultureInfo("uk-UA");

        Thread barberThread = new Thread(Barber);
        barberThread.Start();

        Thread[] clientThreads = new Thread[NUM_CLIENTS];
        for (int i = 0; i < NUM_CLIENTS; i++)
        {
            clientThreads[i] = new Thread(Client);
            clientThreads[i].Start(i + 1);
            Thread.Sleep(1000); // Імітація різного часу приходу клієнтів
        }

        // Чекаємо завершення всіх клієнтів
        for (int i = 0; i < NUM_CLIENTS; i++)
        {
            clientThreads[i].Join();
        }

        // Перукар може працювати далі в нескінченному циклі
    }
}
