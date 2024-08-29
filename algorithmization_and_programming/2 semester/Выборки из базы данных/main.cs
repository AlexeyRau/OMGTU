using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;

struct Person
{
    public string FIO;
    public string PhoneNumber;
    public string City;

    public Person(string fio, string phoneNumber, string city)
    {
        FIO = fio;
        PhoneNumber = phoneNumber;
        City = city;
    }
}

class Program
{
    static void Main(string[] args)
    {
        string inputFilePath = "input.txt"; // Путь к входному файлу
        string outputCity = "City.txt"; // Файл для выборки по городу
        string outputLastName = "Lastname.txt"; // Файл для выборки по фамилии
        string outputFioCity = "FioAndCity.txt"; // Файл для выборки по ФИО и городу

        List<Person> people = new List<Person>();

        foreach (var line in File.ReadAllLines(inputFilePath))
        {
            var parts = line.Split(' ');

            if (parts.Length < 5)
            {
                Console.WriteLine($"Следующая строка введена неккоректно: {line}");
                continue;
            }

            string fio = $"{parts[0]} {parts[1]} {parts[2]}";
            string phoneNumber = parts[3];
            string city = parts[4];

            people.Add(new Person(fio, phoneNumber, city));
        }

        Console.WriteLine("Выборка по городу");
        Console.Write("Введите город: ");
        var selectedCity = Console.ReadLine();
        var citySelection = people.Where(p => p.City == selectedCity);
        File.WriteAllLines(outputCity, citySelection.Select(p => $"{p.FIO} {p.PhoneNumber} {p.City}"));
        Console.WriteLine();

        Console.WriteLine("Выборка по фамилии");
        Console.Write("Введите фамилию: ");
        var selectedLastName = Console.ReadLine();
        var lastNameSelection = people.Where(p => p.FIO.StartsWith(selectedLastName));
        File.WriteAllLines(outputLastName, lastNameSelection.Select(p => $"{p.FIO} {p.PhoneNumber} {p.City}"));
        Console.WriteLine();

        Console.WriteLine("Выборка по городу и фио");
        Console.Write("Введите город: ");
        selectedCity = Console.ReadLine();
        Console.Write("Введите фио: ");
        var selectedFIO = Console.ReadLine();
        var fioCitySelection = people.Where(p => p.FIO == selectedFIO && p.City == selectedCity);
        File.WriteAllLines(outputFioCity, fioCitySelection.Select(p => $"{p.FIO} {p.PhoneNumber} {p.City}"));
        Console.WriteLine();

        Console.WriteLine("Файлы выборок успешно сформированы.");
    }
}
