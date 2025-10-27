using System;
using System.Diagnostics;
using System.ServiceProcess;
using System.Threading;

public class Program
{
    public static string ServiceName = "MyDaemonCsharp";
    static void Main(string[] args)
    {
        // Створюємо новий процес фонової служби
        RunDaemon();
    }

    static void RunDaemon()
    {
        // Перевіряємо чи є необхідні права для запису в журнал
        if (!EventLog.SourceExists(ServiceName))
        {
            EventLog.CreateEventSource(ServiceName, "Application");
        }

        EventLog.WriteEntry(ServiceName, "Демон запущений.", EventLogEntryType.Information);

        // Основний цикл роботи демона
        while (true)
        {
            try
            {
                // Чекаємо 10 секунд перед перевіркою стану
                Thread.Sleep(10000);

                // У реальній ситуації тут можна додати код для обробки команд або подій
                // Наприклад, можна створити обробник сигналу або події для завершення роботи
            }
            catch (ThreadInterruptedException)
            {
                EventLog.WriteEntry(ServiceName, "Демон завершив роботу через сигнал.", EventLogEntryType.Information);
                break; // Вихід із циклу при отриманні сигналу завершення
            }
        }
    }
}

