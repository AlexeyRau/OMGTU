using System;

    internal class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Введите количество элементов");
            int N = int.Parse(Console.ReadLine());
            int [] MyArray = new int[N];
            int test = 1, test2 = 1;
            int firstEvenPos = int.MaxValue;
            int lastZeroPos = 0;
            int minElement = int.MaxValue, maxElement = int.MinValue;
            int multiplesMin = 0;
            
            for (int i = 0; i < N; i++)
            {
                Console.Write("["+(i+1)+"]: ");
                MyArray[i] = int.Parse(Console.ReadLine());
                if (MyArray[i] % (i + 1) != 0) {test = 0;}
                if (MyArray[i] % 2 == 0 && firstEvenPos == int.MaxValue) {firstEvenPos = (i + 1);}
                if (MyArray[i] == 0) {lastZeroPos = (i+1);}
                if (MyArray[i] < minElement && MyArray[i] != 0) {minElement = MyArray[i];}
                if (MyArray[i] > maxElement) {maxElement = MyArray[i];}
            }
            if (test == 1) { Console.WriteLine("1. Все элементы кратны своему номеру"); }
            else { Console.WriteLine("1. Не все элементы кратны своему номеру"); }

            if (firstEvenPos == int.MaxValue) { Console.WriteLine("2. Нет чётных элементов"); }
            else { Console.WriteLine("2. Позиция первого чётного элемента: " + firstEvenPos); }

            Console.WriteLine("3. Позиция последнего нулевого элемента:" + lastZeroPos);

            for (int i = 0; i < N; i++)
            {
                if (MyArray[i] % minElement == 0) {multiplesMin++;}
            }

            if (minElement == int.MaxValue) {Console.WriteLine("4. Недостаточно значений для определения минимального элемента не равного нулю");}
            else {Console.WriteLine("4. Минимальный элемент не равный нулю: " + minElement + ". Количество элементов кратных ему: " + multiplesMin);}

            if ((Array.IndexOf(MyArray, maxElement)) > (Array.IndexOf(MyArray, minElement)))
            {
                for (int i = (Array.IndexOf(MyArray, minElement) + 1); i < (Array.IndexOf(MyArray, maxElement) - 1); i++)
                {
                    if (MyArray[i] < MyArray[(i + 1)]) {test2 = 0;}
                }
            }
            else
            {
                for (int i = (Array.IndexOf(MyArray, maxElement) + 1); i < (Array.IndexOf(MyArray, minElement) - 1); i++)
                {
                    if (MyArray[i] < MyArray[(i + 1)]) {test2 = 0;}
                }
            }
         
            int valueDif = Array.IndexOf(MyArray, maxElement) - Array.IndexOf(MyArray, minElement);
            if (N == 1) {Console.WriteLine("5. Недостаточно значений для определения");}
            else if (valueDif == 1 || valueDif == (-1)) {Console.WriteLine("5. Между максимальным и минимальным значениями нет чисел");}
            else
            {
                if (test2 == 0) { Console.WriteLine("5. Нет убывания"); }
                if (test2 == 1) { Console.WriteLine("5. Есть убывание"); }
            }
            
        }
    }
