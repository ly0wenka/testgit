using System;
using System.Diagnostics;
using System.ServiceProcess;
using System.Threading;

public class MyDaemonCsharp : ServiceBase
{
    private Thread workerThread;
    public static string ServiceNameConst = "MyDaemonCsharp";

    public MyDaemonCsharp()
    {
        this.ServiceName = ServiceNameConst;
        this.CanStop = true;
        this.CanPauseAndContinue = false;
        this.AutoLog = true;
    }

    protected override void OnStart(string[] args)
    {
        if (!EventLog.SourceExists(ServiceNameConst))
        {
            EventLog.CreateEventSource(ServiceNameConst, "Application");
        }

        EventLog.WriteEntry(ServiceNameConst, "Служба запущена.", EventLogEntryType.Information);

        // Основний цикл в окремому потоці
        workerThread = new Thread(new ThreadStart(WorkerLoop));
        workerThread.Start();
    }

    protected override void OnStop()
    {
        EventLog.WriteEntry(ServiceNameConst, "Служба зупиняється.", EventLogEntryType.Information);
        workerThread?.Interrupt();
        workerThread?.Join();
    }

    private void WorkerLoop()
    {
        try
        {
            while (true)
            {
                Thread.Sleep(10000); // робота демона
            }
        }
        catch (ThreadInterruptedException)
        {
            EventLog.WriteEntry(ServiceNameConst, "Демон завершив роботу через сигнал.", EventLogEntryType.Information);
        }
    }

    public static void Main()
    {
        ServiceBase.Run(new MyDaemonCsharp());
    }
}
