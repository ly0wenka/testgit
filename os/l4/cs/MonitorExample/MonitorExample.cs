using System;
using System.Threading;

class MonitorExample
{
    private static readonly object locker = new object();
    private static bool dataReady = false;

    static void Main()
    {
        Thread producer = new Thread(Produce);
        Thread consumer = new Thread(Consume);

        producer.Start();
        consumer.Start();
    }

    static void Produce()
    {
        lock (locker)
        {
            Console.WriteLine("Producer: preparing data...");
            Thread.Sleep(1000);
            dataReady = true;
            Monitor.Pulse(locker); // Сповіщення
            Console.WriteLine("Producer: data ready!");
        }
    }

    static void Consume()
    {
        lock (locker)
        {
            while (!dataReady)
            {
                Console.WriteLine("Consumer: waiting for data...");
                Monitor.Wait(locker); // Очікування
            }
            Console.WriteLine("Consumer: data consumed!");
        }
    }
}
