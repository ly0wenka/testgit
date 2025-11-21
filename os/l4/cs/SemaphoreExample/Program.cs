using System;
using System.Threading;

class SemaphoreExample
{
    static Semaphore semaphore = new Semaphore(2, 2); // Максимум 2 потоки

    static void Worker(object id)
    {
        Console.WriteLine($"Thread {id} is waiting to enter...");
        semaphore.WaitOne();
        Console.WriteLine($"Thread {id} entered!");
        Thread.Sleep(2000);
        Console.WriteLine($"Thread {id} is leaving...");
        semaphore.Release();
    }

    static void Main()
    {
        for (int i = 1; i <= 5; i++)
        {
            new Thread(Worker).Start(i);
        }
    }
}
