using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Работники
{
    public class Worker
    {
        public int WorkerNum { get; set; }
        public string Fio { get; set; }
        public string Education { get; set; }
        public string Specialty { get; set; }
        public decimal Salary { get; set; }
        public int ProductsNumber { get; set; }
        public decimal ProductPrice { get; set; }
        public decimal TotalProductPrice => ProductsNumber * ProductPrice;
    }
    internal class Program
    {
        static void Main(string[] args)
        {
            var workers = new List<Worker>
            {
                new Worker { WorkerNum = 1, Fio = "Иван Иванов", Education = "Высшее", Specialty = "Инженер", Salary = 50000, ProductsNumber = 200, ProductPrice = 300 },
                new Worker { WorkerNum = 2, Fio = "Петр Петров", Education = "Среднее", Specialty = "Слесарь", Salary = 30000, ProductsNumber = 150, ProductPrice = 200 },
                new Worker { WorkerNum = 3, Fio = "Сергей Сергеев", Education = "Высшее", Specialty = "Программист", Salary = 60000, ProductsNumber = 100, ProductPrice = 700 },
                new Worker { WorkerNum = 4, Fio = "Анна Антонова", Education = "Среднее", Specialty = "Оператор", Salary = 25000, ProductsNumber = 80, ProductPrice = 500 }
            };

            var underpaidWorkers = workers.Where(w => w.Salary < w.TotalProductPrice).ToList();
            foreach (var worker in underpaidWorkers)
            {
                Console.WriteLine($"{worker.Fio} - Зарплата: {worker.Salary}, Стоимость продукции: {worker.TotalProductPrice}");
            }
            Console.WriteLine();
            int totalProducedItems = workers.Sum(w => w.ProductsNumber);
            Console.WriteLine($"Общее количество произведенных единиц продукции: {totalProducedItems}");
            Console.WriteLine();
            int countWorkersWithFairSalary = workers.Count(w => w.Salary >= 0.5m * w.TotalProductPrice);
            Console.WriteLine($"Количество сотрудников, получающих не менее 50% от суммы производимого продукта: {countWorkersWithFairSalary}");

        }
    }
}
