using System;

namespace ConsoleApp4
{
    internal class Program
    {
        static void Main(string[] args)
        {
            int l, n, m, k, s = 0;
            l = 7; // расстояние от колодца до первой грядки
            n = 5; // длина грядки
            m = 10; // ширина грядки
            Console.WriteLine("Введите количество грядок");
            k = int.Parse(Console.ReadLine()); // ввод количества грядок

           
            for (int i = 0; i < k; i++)
            {
                s += 2 * l + 2 * (m + n) + i * 2 * m;
            }
            switch (k)
            {
                case 1:
                    Console.WriteLine("Расстояние при " + k + " грядке: " + s);
                    break;
                default:
                    Console.WriteLine("Расстояние при " + k + " грядках: " + s);
                    break;
            }

            
        }
    }
}