using System;
using System.Collections.Generic;
using System.Linq;

class Account
{
    public string AccountNumber { get; set; }
    public string FIO { get; set; }
    public string PhoneNumber { get; set; }
    public decimal Income { get; set; }
    public decimal Expenses { get; set; }
    public decimal Tax => Income * 0.05m;
}

class Program
{
    static void Main()
    {
        List<Account> accounts = new List<Account>
        {
            new Account { AccountNumber = "123", FIO = "Иван Иванов", PhoneNumber = "1234567890", Income = 1000, Expenses = 500 },
            new Account { AccountNumber = "456", FIO = "Петр Петров", PhoneNumber = "2345678901", Income = 2000, Expenses = 2500 },
            new Account { AccountNumber = "789", FIO = "Сергей Сергеев", PhoneNumber = "3456789012", Income = 1500, Expenses = 1200 }
        };

        var negativeBalanceCount = accounts.Count(a => a.Income - a.Expenses < 0);
        Console.WriteLine($"Количество клиентов с отрицательным балансом: {negativeBalanceCount}");

        var maxBalance = accounts.Max(a => a.Income - a.Expenses);
        var richestClients = accounts.Where(a => a.Income - a.Expenses == maxBalance);
        Console.WriteLine("Клиенты с наибольшим балансом:");
        foreach (var client in richestClients)
        {
            Console.WriteLine($"{client.FIO} с балансом {client.Income - client.Expenses}");
        }

        var averageIncome = accounts.Average(a => a.Income);
        Console.WriteLine($"Средний доход по счетам: {averageIncome}");

        var totalTax = accounts.Sum(a => a.Tax);
        Console.WriteLine($"Суммарная сумма налогов: {totalTax}");
    }
}
