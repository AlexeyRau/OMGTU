using System;


namespace date
{
    internal class Program
    {
        static void Main(string[] args)
        {
            string InputFirstDate = Console.ReadLine(); //Ввод начальной даты
            string InputSecondDate = Console.ReadLine(); //Ввод конечной даты
            int InitialProduction = int.Parse(Console.ReadLine()); //Ввод начального выпуска
            int sum = 0; //Суммарный объём продукции
            DateTime FirstDate; //Объявление начальной даты в виде формата даты и времени
            DateTime SecondDate;//Объявление конечной даты в виде формата даты и времени
            DateTime.TryParse(InputFirstDate, out FirstDate); //Конвертация из string и присваивание значений переменной формата DateTime
            DateTime.TryParse(InputSecondDate, out SecondDate);//Конвертация из string и присваивание значений переменной формата DateTime
            TimeSpan DateDifference = SecondDate - FirstDate; //Подсчёт разницы между началом и концом
            for (int i = 0; i <= DateDifference.Days; i++)
            {
                sum = sum + InitialProduction;
                InitialProduction++;
            }
            Console.WriteLine(sum);
        }
    }
}
