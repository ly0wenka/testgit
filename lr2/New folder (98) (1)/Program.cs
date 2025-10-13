using System;
using System.Diagnostics;

class Program
{
    static void Main(string[] args)
    {
        if (args.Length < 1)
        {
            Console.WriteLine("Usage: <application_path>");
            return;
        }

        foreach (string applicationPath in args)
        {
            try
            {
                Console.WriteLine($"Parent Process (PID: {Process.GetCurrentProcess().Id})");
                
                Process process = new Process();
                process.StartInfo.FileName = applicationPath;
                process.Start();
                
                Console.WriteLine($"Child Process Started (PID: {process.Id})");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Process creation failed: {ex.Message}");
            }
        }
    }
}

