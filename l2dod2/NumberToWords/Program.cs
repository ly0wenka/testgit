// See https://aka.ms/new-console-template for more information
using System;
using System.Linq;

class Program
{
    static void Main(string[] args)
    {
        // Отримуємо значення після -n, якщо воно є
        string number = args
            .SkipWhile(arg => arg != "-n") // Пропускаємо елементи до -n
            .Skip(1)                        // Пропускаємо сам -n
            .FirstOrDefault();              // Отримуємо перший доступний елемент після -n

        if (number != null)
        {
            PrintNumberAsText(number);
        }
        else
        {
            Console.WriteLine($"Використання: {AppDomain.CurrentDomain.FriendlyName} -n <число>");
        }
    }

    static void PrintNumberAsText(string number)
    {
        if (number[0] == '-')
        {
            Console.Write("мінус ");
            number = number.Substring(1);  // Пропускаємо знак мінус
        }
        Console.WriteLine(number);
    }
}

