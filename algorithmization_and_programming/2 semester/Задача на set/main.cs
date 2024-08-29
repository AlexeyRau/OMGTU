using System;
using System.Collections.Generic;

class Program
{
    static void Main(string[] args)
    {
        List<HashSet<int>> sets = new List<HashSet<int>>();
        sets.Add(new HashSet<int>());
        sets.Add(new HashSet<int>());
        sets.Add(new HashSet<int>());
        Set(sets);
        Console.Write("Объединение: ");
        foreach (int el in Union(sets))
        {
            Console.Write($"{el} ");
        }
        Console.WriteLine();

        Console.Write("Пересечение: ");
        foreach (int el in Intersection(sets))
        {
            Console.Write($"{el} ");
        }
        Console.WriteLine();

        for (int i = 0; i < 3; i++)
        {
            Console.Write($"Дополнение {i + 1}-го множества: ");
            foreach (int el in Complement(sets[i], Union(sets)))
            {
                Console.Write($"{el} ");
            }
            Console.WriteLine();
        }

    }
    public static void Set(List<HashSet<int>> sets)
    {
        for (int i = 0; i < 3; i++)
        {
            Console.Write($"Количество элементов в {i + 1}-м множестве: ");
            int numberOfElements = int.Parse(Console.ReadLine());
            for (int j = 0; j < numberOfElements; j++)
            {
                Console.Write($"{j + 1}-й элемент: ");
                sets[i].Add(int.Parse(Console.ReadLine()));
            }
        }
    }
    static SortedSet<int> Union(List<HashSet<int>> sets)
    {
        SortedSet<int> union = new SortedSet<int>();
        foreach (HashSet<int> set in sets)
        {
            union.UnionWith(set);
        }
        return union;
    }
    static SortedSet<int> Intersection(List<HashSet<int>> sets)
    {
        SortedSet<int> intersection = new SortedSet<int>();
        intersection.UnionWith(sets[0]);
        foreach (HashSet<int> set in sets)
        {
            intersection.IntersectWith(set);
        }
        return intersection;
    }
    static SortedSet<int> Complement(HashSet<int> set, SortedSet<int> union)
    {
        SortedSet<int> complement = new SortedSet<int>(union);
        complement.ExceptWith(set);
        return complement;
    }

}
