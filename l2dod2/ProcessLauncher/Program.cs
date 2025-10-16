using System;
using System.Diagnostics;
using System.Text;

class Program
{
    static void Main(string[] args)
    {
        string number = string.Empty;
        if (args.Length == 0)
        {
            Console.Write("Введіть число: ");
            number = Console.ReadLine();
        } 
        else
            number = args[0];

        ProcessStartInfo psi = new ProcessStartInfo
        {
            FileName = @"S:\Users\L\Downloads\New folder (175)\testgit\l2dod2\NumberToWords\bin\Debug\net8.0\NumberToWords.exe",
            Arguments = $"dsadad sadasd -n {number}",
            RedirectStandardOutput = true,
            UseShellExecute = false,
            CreateNoWindow = true
        };

        try
        {
            using (Process process = new Process { StartInfo = psi })
            {
                process.Start();
                string output = process.StandardOutput.ReadToEnd();
                process.WaitForExit();
                Console.WriteLine("Вивід процесу: " + output);
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine("Помилка запуску процесу: " + ex.Message);
        }
    }
}
