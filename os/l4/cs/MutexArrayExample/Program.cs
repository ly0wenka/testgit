using System;
using System.Threading;

class MutexArrayExample
{
    static Mutex[] slotMutexes;
    static int maxSlots = 2;

    static void Main()
    {
        slotMutexes = new Mutex[maxSlots];
        for (int i = 0; i < maxSlots; i++)
            slotMutexes[i] = new Mutex();

        for (int i = 1; i <= 5; i++)
        {
            Thread t = new Thread(Worker);
            t.Start(i);
        }
    }

    static void Worker(object obj)
    {
        int id = (int)obj;
        int mySlot = -1;

        // спробуємо заблокувати будь-який вільний слот
        while (mySlot == -1)
        {
            for (int i = 0; i < maxSlots; i++)
            {
                if (slotMutexes[i].WaitOne(0)) // пробуємо захопити слот без блокування
                {
                    mySlot = i;
                    break;
                }
            }

            if (mySlot == -1)
                Thread.Sleep(50); // чекати, якщо немає вільних слотів
        }

        Console.WriteLine($"Thread {id} entered slot {mySlot}.");
        Thread.Sleep(2000);
        Console.WriteLine($"Thread {id} leaving slot {mySlot}.");

        slotMutexes[mySlot].ReleaseMutex(); // звільняємо слот
    }

}
