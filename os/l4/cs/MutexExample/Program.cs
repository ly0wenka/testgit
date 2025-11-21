using System;
using System.Threading;

class MutexExample
{
    static Mutex mutex = new Mutex();

    static void Worker(object id)
    {
        Console.WriteLine($"Thread {id} is waiting for mutex...");
        mutex.WaitOne(); // Блокування
        Console.WriteLine($"Thread {id} entered critical section.");
        Thread.Sleep(1000);
        Console.WriteLine($"Thread {id} is leaving critical section.");
        mutex.ReleaseMutex(); // Звільнення
    }

    static void Main()
    {
        for (int i = 1; i <= 3; i++)
        {
            new Thread(Worker).Start(i);
        }
    }
}
