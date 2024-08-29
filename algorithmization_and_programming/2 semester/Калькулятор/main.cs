using System;

namespace Калькулятор
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Выберите тип данных:");
            Console.WriteLine("1) Работа с целыми");
            Console.WriteLine("2) Работа с вещественными");
            int choice = int.Parse(Console.ReadLine());

            switch (choice)
            {
                case 1:
                    IntOperations();
                    break;
                case 2:
                    DoubleOperations();
                    break;
                default:
                    Console.WriteLine("Неверный выбор");
                    break;
            }
        }
        static void DoubleOperations()
        {
            double a = GetValidDouble("Введите первое число: ");
            double b = GetValidDouble("Введите второе число: ");

            Calc<double> calc = new Calc<double>();
            Console.WriteLine($"{a} + {b} = {calc.Plus(a, b)}");
            Console.WriteLine($"{a} - {b} = {calc.Minus(a, b)}");
            Console.WriteLine($"{a} * {b} = {calc.Multiply(a, b)}");
            Console.WriteLine($"{a} / {b} = {calc.Divide(a, b)}");
        }
        static void IntOperations()
        {
            int a = GetValidInt("Введите первое число: ");
            int b = GetValidInt("Введите второе число: ");

            Calc<int> calc = new Calc<int>();
            Console.WriteLine($"{a} + {b} = {calc.Plus(a, b)}");
            Console.WriteLine($"{a} - {b} = {calc.Minus(a, b)}");
            Console.WriteLine($"{a} * {b} = {calc.Multiply(a, b)}");
            Console.WriteLine($"{a} / {b} = {calc.Divide(a, b)}");

        }
        static int GetValidInt(string message)
        {
            int result;
            while (true)
            {
                Console.WriteLine(message);
                if (int.TryParse(Console.ReadLine(), out result))
                {
                    return result;
                }
                Console.WriteLine("Ошибка: Введите корректное целое число.");
            }
        }

        static double GetValidDouble(string message)
        {
            double result;
            while (true)
            {
                Console.WriteLine(message);
                if (double.TryParse(Console.ReadLine(), out result))
                {
                    return result;
                }
                Console.WriteLine("Ошибка: Введите корректное вещественное число.");
            }
        }

    }

    class Calc<T>
    {
        public T Plus(T a, T b)
        {
            dynamic num1 = a;
            dynamic num2 = b;
            return num1 + num2;
        }
        public T Minus(T a, T b)
        {
            dynamic num1 = a;
            dynamic num2 = b;
            return num1 - num2;
        }
        public T Multiply(T a, T b)
        {
            dynamic num1 = a;
            dynamic num2 = b;
            return num1 * num2;
        }
        public T Divide(T a, T b)
        {
            dynamic num1 = a;
            dynamic num2 = b;
            return num1 / num2;
        }
    }
}
