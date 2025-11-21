using System;
using System.Threading;

class LockSemaphoreExample
{
    private static readonly object locker = new object();
    private static int availableSlots; // кількість доступних "місць"

    static void Main()
    {
        int maxSlots = 2; // як у семафорі: максимум потоків одночасно
        availableSlots = maxSlots;

        for (int i = 1; i <= 5; i++)
        {
            int id = i;
            new Thread(() => Worker(id)).Start();
        }
    }

    static void Worker(int id)
    {
        Enter(); // спроба зайти в критичну секцію

        // Критична секція
        Console.WriteLine($"Thread {id} entered critical section.");
        Thread.Sleep(2000);
        Console.WriteLine($"Thread {id} leaving critical section.");

        Exit(); // вихід з критичної секції
    }

    static void Enter()
    {
        lock (locker)
        {
            while (availableSlots == 0) // чекаємо, поки не буде вільного місця
            {
                Monitor.Wait(locker);
            }
            availableSlots--; // резервуємо місце
        }
    }

    static void Exit()
    {
        lock (locker)
        {
            availableSlots++;       // звільняємо місце
            Monitor.Pulse(locker);  // повідомляємо один потік, що може увійти
        }
    }
}
