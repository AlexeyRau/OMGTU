using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace mouses
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Console.Write("Количество мышей: ");
            int n = int.Parse(Console.ReadLine());
            Console.Write("Шаг k: ");
            int k = int.Parse(Console.ReadLine());
            Console.Write("Укажите номер белой мыши(нумерация начинается с 1): ");
            int pos = int.Parse(Console.ReadLine());
            int num = 0;
            for (int i = 0; i < n; i++)
            {
                List<int> list = new List<int>();
                for (int j = 1; j <= n; j++)
                {
                    list.Add(j);
                }
                num = i + k;
                if (num >= list.Count)
                {
                    num -= list.Count;
                }
                list.RemoveAt(num);
                while (true)
                {
                    num += (k-1);
                    while (num >= list.Count)
                    {
                        num -= list.Count;
                    }
                    if (list.Count == 1)
                    {
                        break;
                    }
                    list.RemoveAt(num);

                }
                if (list[0] == pos)
                {
                    Console.WriteLine("Съедать нужно с " + (i + 1) + "-й мыши");
                    break;
                }
            }
        }
    }
}
