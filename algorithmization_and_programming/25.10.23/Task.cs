using System;
using System.Collections.Generic;
using System.Linq;


/*
 Дан массив, в котором элементы строк - это множества целых неотрицательных чисел разной размерности
Необходимо сформировать одномерные массивы, которые содержат 
1) Элементы пересечения множества
2) Элементы объединения множеств
3) Массив из максимальных элементов множеств
 */
internal class Program
{
    static void Main(string[] args)
    {
        Console.Write("Количество множеств: ");
        int lotsNumber = int.Parse(Console.ReadLine());
        if (lotsNumber == 0)
        {
            Console.WriteLine("Во всех случаях будет пустое множество");
            return;
        }
        int[][] lots = new int[lotsNumber][];
        for (int i = 0; i < lots.Length; i++)
        {
            Console.Write("Длина " + (i + 1) + "-го множества: ");
            lots[i] = new int[int.Parse(Console.ReadLine())];
            Console.WriteLine("[" + i + "]: ");
            for (int j = 0; j < lots[i].Length; j++)
            {
                lots[i][j] = int.Parse(Console.ReadLine());
            }
        }

        Console.WriteLine("---------------------------------------");
        Console.Write("пересечение множеств: ");
        for (int i = 0; i < lots.Length; i++)
        {
            lots[i] = Sort(lots[i]);
        }
        int[] interlots = Intersection(lots);
        if (interlots.Length == 0)
        {
            Console.WriteLine("Нет пересечений");
        }
        else
        {
            for (int i = 0; i < interlots.Length; i++)
            {
                Console.Write(interlots[i] + " ");
            }
            Console.WriteLine();
        }

        Console.WriteLine("---------------------------------------");
        Console.Write("Объединение множеств: ");
        int[] comblots = Combining(lots);
        comblots = Sort(comblots);
        for (int i = 0; i < comblots.Length; i++)
        {
            Console.Write(comblots[i] + " ");
        }
        Console.WriteLine();

        Console.WriteLine("---------------------------------------");
        Console.Write("Множество из максимальных элементов множеств: ");
        int[] maxlots = MaxSearch(lots);
        for (int i = 0; i < maxlots.Length; i++)
        {
            Console.Write(maxlots[i] + " ");
        }
        Console.WriteLine("---------------------------------------");
    }
    static int[] Combining(int[][] arr)
    {
        List<int> list = new List<int>();
        for (int i = 0; i < arr.Length; i++)
        {
            for (int j = 0; j < arr[i].Length; j++)
            {
                list.Add(arr[i][j]);
            }
        }
        int[] comblots = list.ToArray();
        return comblots;
    }
    static int[] Intersection(int[][] arr)
    {
        List<int> backup = new List<int>();
        List<int> list = new List<int>();
        backup = arr[0].ToList();
        for (int k = 0; k < arr.Length - 1; k++)
        {
            for (int i = 0; i < arr[k].Length; i++)
            {
                for (int j = 0; j < arr[k + 1].Length; j++)
                {
                    if (arr[k][i] == arr[k + 1][j])
                    {
                        list.Add(arr[k][i]);
                    }
                }
            }
            arr[k] = backup.ToArray();
            backup = arr[k + 1].ToList();
            arr[k + 1] = list.ToArray();
            list.Clear();
        }
        int[] interlots = arr[arr.Length - 1];
        arr[arr.Length - 1] = backup.ToArray();
        return interlots;
    }

    static int[] MaxSearch(int[][] arr)
    {
        int[] maxlots = new int[arr.Length];
        for (int i = 0; i < arr.Length; i++)
        {
            for (int j = 0; j < arr[i].Length; j++)
            {
                if (arr[i][j] > maxlots[i])
                {
                    maxlots[i] = arr[i][j];
                }
            }
        }
        return maxlots;
    }
    static int[] Sort(int[] arr)
    {
        bool sw = true;
        List<int> list = new List<int>();

        for (int i = 0; i < arr.Length; i++)
        {
            for (int j = i + 1; j < arr.Length; j++)
            {
                if (arr[i] == arr[j]) { sw = false; break; }
            }
            if (sw == true) { list.Add(arr[i]); }
            sw = true;
        }
        int[] sortlot = list.ToArray();
        return sortlot;
    }
}

