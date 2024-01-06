using System;
/*
1. Количество чётных чисел между максимальным и минимальным значениями
2. Все ли элементы на чётных позициях имеют в своей записи хотя бы одну 5
3. Заменить все нечётные числа в массиве на сумму их же цифр
4. Определить количество элементов, которые больше ср. арифметического всех нечётных чисел
 */

{
    internal class Program
    {
        static void Main(string[] args)
        {
            int maxNum = int.MinValue;
            int minNum = int.MaxValue;
            Console.Write("Размер массива: ");
            int n = int.Parse(Console.ReadLine());
            int[] numbers = new int[n];
            for (int i = 0; i < n; i++)
            {
                Console.Write("[" + (i + 1) + "]: ");
                numbers[i] = int.Parse(Console.ReadLine());
            }
            for (int i = 0; i < n; i++)
            {
                if (numbers[i] > maxNum) { maxNum = numbers[i]; }
                if (numbers[i] < minNum) { minNum = numbers[i]; }
            }
            if (Array.IndexOf(numbers, maxNum) > Array.IndexOf(numbers, minNum)) { EvenCount(numbers, minNum, maxNum); }
            else { EvenCount(numbers, maxNum, minNum); }
            ElementSearch(numbers, 5);
            NumReplace(numbers);
            LastElelmentSearch(numbers, 3);

        }

        static void EvenCount(int[] numbers, int firstNum, int secondNum)
        {
            int evenCount = 0;
            for (int i = (Array.IndexOf(numbers, firstNum) + 1); i < Array.IndexOf(numbers, secondNum); i++)
            {
                if (numbers[i] % 2 == 0) { evenCount++; }
            }
            Console.WriteLine("1. Количество чётных чисел между максимальным и минимальным значениями: " + evenCount);
        }

        static void ElementSearch(int[] numbers, int element)
        {
            int backup = 0;
            int count = 0;
            for (int i = 0; i < numbers.Length; i++)
            {
                if ((i + 1) % 2 == 0)
                {
                    backup = numbers[i];
                    while (numbers[i] != 0)
                    {
                        if (numbers[i] % 10 == element || numbers[i] % 10 == -(element)) { count = 1; break; }
                        else { count = 0; }
                        numbers[i] /= 10;
                    }
                    numbers[i] = backup;
                    if (count == 0) { break; }
                }
            }
            if (count == 0) { Console.WriteLine("2. Не все числа на чётных позициях имеют в записи цифру 5"); }
            else { Console.WriteLine("2. Все числа на чётных позициях имеют в записи цифру 5"); }
        }

        static void NumReplace(int[] numbers)
        {
            int[] replaceNumbers = new int[numbers.Length];
            int backup = 0;
            double nonEvenSum = 0;
            double nonEvenMean = 0;
            int count = 0;
            for (int i = 0; i < numbers.Length; i++)
            {
                replaceNumbers[i] = numbers[i];
                if (numbers[i] % 2 != 0)
                {
                    nonEvenSum += numbers[i];
                    backup = numbers[i];
                    replaceNumbers[i] = 0;
                    while (numbers[i] != 0)
                    {
                        replaceNumbers[i] = replaceNumbers[i] + (numbers[i] % 10);
                        numbers[i] /= 10;
                    }
                    numbers[i] = backup;
                }
            }
            nonEvenMean = nonEvenSum / numbers.Length;
            Console.WriteLine("3. Изменённый массив:");
            for (int i = 0; i < numbers.Length; i++)
            {
                if (numbers[i] > nonEvenMean)
                {
                    count++;
                }
                Console.WriteLine("[" + (i + 1) + "]: " + replaceNumbers[i]);
            }
            Console.WriteLine("4. Количество элементов, которые больше ср. арифметического нечётных чисел: " + count);

        }

        static void LastElelmentSearch(int[] numbers, int element)
        {
            int count = 0;
            for (int i = 0; i < numbers.Length; i++)
            {
                if (numbers[i] % 10 == element || numbers[i] % 10 == -(element)) { count = 1; break; }
            }
            if (count == 0) { Console.WriteLine("5. В массиве нет элементов оканчивающихся на 3"); }
            else { Console.WriteLine("5. В массиве есть элемент, оканчивающийся на 3"); }
        }
    }
}
