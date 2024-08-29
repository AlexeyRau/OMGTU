using System;
using System.Collections.Generic;
using System.Linq;


namespace Номера_телефонов
{
    class Call
    {
        public string Outgoing { get; set; }
        public string Incoming { get; set; }
        public DateTime Date { get; set; }
        public int Minutes { get; set; }
    }
    internal class Program
    {
        static void Main(string[] args)
        {
            var callData = new List<Call>()
            {
                new Call { Outgoing = "123", Incoming = "456", Date = new DateTime(2024, 8, 25), Minutes = 10 },
                new Call { Outgoing = "123", Incoming = "456", Date = new DateTime(2024, 8, 25), Minutes = 5 },
                new Call { Outgoing = "456", Incoming = "789", Date = new DateTime(2024, 8, 25), Minutes = 15 },
                new Call { Outgoing = "789", Incoming = "123", Date = new DateTime(2024, 8, 25), Minutes = 20 },
                new Call { Outgoing = "123", Incoming = "789", Date = new DateTime(2024, 8, 25), Minutes = 25 }
            };
            Console.Write("Укажите номер абонента: ");
            FrequentNumber(callData, Console.ReadLine());
            Console.WriteLine();
            MostMinutes(callData);
        }
        public static void FrequentNumber(List<Call> callData, string caller)
        {
            var frequentNumber = callData
                .Where(c => c.Outgoing == caller)
                .GroupBy(c => new { c.Date, c.Incoming })
                .Select(g => new 
                { 
                    Date = g.Key.Date, 
                    Number = g.Key.Incoming, 
                    Count = g.Count() 
                })
                .ToList();

            foreach (var res in frequentNumber)
            {
                Console.WriteLine($"Дата: {res.Date.ToShortDateString()}, Номер на который звонили: {res.Number}, Звонков в этот день: {res.Count}");
            }

        }
        public static void MostMinutes(List<Call> callData)
        {
            var mostMinutesData = callData
                .GroupBy(c => new { c.Outgoing, c.Date })
                .Select(g => new
                {
                    Date = g.Key.Date,
                    Outgoing = g.Key.Outgoing,
                    Incoming = g.OrderByDescending(c => c.Minutes).FirstOrDefault().Incoming,
                    Minutes = g.Sum(c => c.Minutes)
                })
                .ToList();

            foreach (var res in mostMinutesData)
            {
                Console.WriteLine($"Дата: {res.Date.ToShortDateString()}, Исходящий номер: {res.Outgoing}, Номер, с которым больше всего говорили в этот день: {res.Incoming}, Всего минут: {res.Minutes}");
            }
        }

    }
}
