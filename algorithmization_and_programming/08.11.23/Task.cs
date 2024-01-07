using System;

/*
В массиве размерность н на м определить количество строк в которыз минимальный и максимальный элементы четные
Ввод данных в массив, нахождение минимального и максимального с помощью своих функций
 */
internal class Program
{
    static void Main(string[] args)
    {
        Console.Write("Введите количество строк: ");
        int n = int.Parse(Console.ReadLine());
        Console.Write("Введите количество столбцов: ");
        int m = int.Parse(Console.ReadLine());
        int[,] arr = new int[n, m];
        int maxelement = int.MinValue;
        int minelement = int.MaxValue;
        int count = 0;
        for (int i = 0; i < n; i++)
        {
            Console.WriteLine((i+1) + "-я строка");
            for (int j = 0; j < m; j++)
            {
                Console.Write("[" + (i+1) + ", " + (j+1) + "]: ");
                arr[i, j] = int.Parse(Console.ReadLine());
                if (arr[i, j] > maxelement)
                {
                    maxelement = arr[i, j];
                }
                if (arr[i, j] < minelement)
                {
                    minelement = arr[i, j];
                }
            }
            if (maxelement % 2 == 0 && minelement % 2 == 0)
            {
                count++;
            }
            maxelement = int.MinValue;
            minelement = int.MaxValue;
        }
        Console.WriteLine("Количество строк где макс и мин чётные: " + count);
    }
}
