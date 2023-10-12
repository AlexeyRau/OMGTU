

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApplication6
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Выберите номер задачи: 1, 2, 3, 4");
            int WorkNum = int.Parse(Console.ReadLine());
            if (WorkNum == 1)//ЗАДАЧА 1<----------------------------------------------------------------------------------------------------
            {
                int FirstNum, SecondNum, ThirdNum;//Первый, второй и третий элементы
                Console.WriteLine("Введите количество элементов");
                int N = int.Parse(Console.ReadLine());//Количество элементов
                int result = 0;//Резултат 

                if (N < 3) //Если элемнтов меньше чем 3, то не будет двух соседей
                {
                    Console.WriteLine("Введено всего " + N + " элемент(а), для выполнения задачи требуется минимум 3 элемента");
                }
                else
                {
                    //Ввод первых двух элементов
                    Console.WriteLine("Введите 1-й элемент");
                    FirstNum = int.Parse(Console.ReadLine());
                    Console.WriteLine("Введите 2-й элемент");
                    SecondNum = int.Parse(Console.ReadLine());

                    for (int i = 0; i < (N - 2); i++) //Цикл для ввода и проверки последующих элементов
                    {
                        Console.WriteLine("Введите " + (i + 3) + "-й элемент");
                        ThirdNum = int.Parse(Console.ReadLine());
                        if (SecondNum < FirstNum & SecondNum < ThirdNum) //Если соседи справа и слева соответствуют условию, то +1 к результату
                        {
                            result++;
                        }
                        //Смещение на следующую тройку
                        FirstNum = SecondNum;
                        SecondNum = ThirdNum;

                    }

                    Console.WriteLine("Количество элементов, которые меньше чем соседи справа и слева: " + result);
                    if (SecondNum < FirstNum)
                    {
                        Console.WriteLine("Последний элемент не учитывается, т.к. нет соседа справа");
                    }
                }
            }
            if (WorkNum == 2)//ЗАДАЧА 2<----------------------------------------------------------------------------------------------------
            {
                Console.WriteLine("Введите количество элементов");
                int N = int.Parse(Console.ReadLine());
                int FirstNum;//Первый элемент
                int SecondNum;//Второй элемент
                int result = 0;
                FirstNum = int.Parse(Console.ReadLine());
                for (int i = 0; i < (N - 1); i++)//Ввод, начиная со второго элемента и проверка
                {
                    SecondNum = int.Parse(Console.ReadLine());
                    if (FirstNum != SecondNum)
                    {
                        result++;
                    }
                    FirstNum = SecondNum;
                }
                Console.WriteLine("Количество смен знаков: " + result);
            }
            if (WorkNum == 3)//ЗАДАЧА 3<----------------------------------------------------------------------------------------------------
            {
                Console.WriteLine("Введите количество элементов");
                int N = int.Parse(Console.ReadLine());
                int SecondNum;//Первый элемент
                int FirstNum;//Второй элемент
                int Lenght = 1;//Длина последовательности, по умолчанию = 1
                int MaxLenght = 0;//Максимальная длина
                FirstNum = int.Parse(Console.ReadLine());//Ввод первого элемента
                for (int i = 0; i < (N - 1); i++)
                {
                    SecondNum = int.Parse(Console.ReadLine());
                    if (SecondNum == FirstNum)
                    {
                        Lenght++;
                        if (i == (N - 2) & Lenght > MaxLenght) //Если идёт последнее повторение цикла
                        {
                            MaxLenght = Lenght;
                        }
                    }
                    else
                    {
                        if (Lenght > MaxLenght)
                        {
                            MaxLenght = Lenght;
                        }
                        Lenght = 1;
                    }
                    FirstNum = SecondNum;
                    
                }
                Console.WriteLine("Максимальная длина от последовательности состоящих из одинаковых элементов: " + MaxLenght);
            }
            if (WorkNum == 4)//ЗАДАЧА 4<-------------------------
            {
                Console.WriteLine("Введите количество чисел");
                int N = int.Parse(Console.ReadLine());
                Console.WriteLine("Введите 1-е число");
                int PreviousNum = int.Parse(Console.ReadLine());//Предыдущее число
                int CurrentNum;//Текущее число
                int Lenght = 0;//Длина
                int minLenght = int.MaxValue;//Минимальная длина
                if (N == 1) //В случае, если вводится всего одно число
                {
                    if (PreviousNum < 0)
                    {
                        minLenght = 1;
                    }
                    else
                    {
                        minLenght = 0;
                    }
                }
                for (int i = 0; i < (N - 1); i++) //Цикл, начиная со второго числа
                {
                    Console.WriteLine("Введите " + (i + 2) + "-е число");
                    CurrentNum = int.Parse(Console.ReadLine());
                    if (PreviousNum < 0) //Если предыдущее меньше 0
                    {
                        if(Lenght == 0) //При наличии отрицательного числа длина по умолчанию = 1
                        {
                            Lenght = 1;
                        }
                        if (CurrentNum < 0 & PreviousNum == CurrentNum) //Если текущее < 0 и текущее = предыдущему, то ++ к длине последовательности
                        {
                            Lenght++;
                        }
                        else //Иначе проверка на минимальность и обнуление текущей длины
                        {
                            if (minLenght > Lenght)
                            {
                                minLenght = Lenght;
                            }
                            Lenght = 0;
                        }
                    }
                    if (i != (N - 2)) //Замена предыдущего значения текущим происходит только если это не последнее повторение цикла
                    {
                        PreviousNum = CurrentNum;
                    }
                    else //Иначе проверка последнего значения на отрицательность
                    {
                        if (CurrentNum < 0)
                        {
                            if (Lenght == 0)//Если последнее значение отрицательно и текущая длина так и не изменилась, то ++ к текущей длине
                            {
                                Lenght++;
                            }
                            minLenght = Lenght;
                        }
                    }
                }
                if (minLenght == 0 || minLenght == int.MaxValue) //В случае если минимальная длина = 0 или не изменилась вообще
                {
                    Console.WriteLine("Нет отрицательных чисел");
                }
                else
                {
                    Console.WriteLine("Длина минимальной последовательности одинаковых отрицательных чисел: " + minLenght);
                }
            }
        }
    }
}
