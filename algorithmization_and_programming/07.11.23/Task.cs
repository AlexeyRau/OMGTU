using System;

/*
1. На вход подаётся строка. Надо определить сумму чётных цифр строки
2. является ли строка палиндромом?
*/

internal class Program
{
    static void Main(string[] args)
    {
        Console.Write("Введите текст: ");
        string text = Console.ReadLine();
        text = text.Replace(" ", "");

        int num;
        int sum = 0;
        bool digital;
        for (int i = 0; i < text.Length; i++)
        {
            digital = int.TryParse("" + text[i], out num);
            if (digital == true && num % 2 == 0)
            {
                sum = sum + num;
            }
        }
        Console.Write("Сумма чётных чисел: " + sum);
        Console.WriteLine();

        string reverce = "";
        for (int i = text.Length - 1; i >= 0; i--)
        {
            reverce += text[i];
        }
        if (String.Compare(reverce, text, true) == 0)
        {
            Console.WriteLine("Палиндром");
        }
        else
        {
            Console.WriteLine("Не палиндром");
        }
    }
}

