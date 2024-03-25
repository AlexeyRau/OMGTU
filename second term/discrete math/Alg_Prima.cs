using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Alg_Prima
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Console.Write("Количество рёбер: ");
            int numberOfEdges = int.Parse(Console.ReadLine());
            int res = 0;
            List<List<int>> list = new List<List<int>>();
            list.Add(new List<int> { });
            list.Add(new List<int> { });
            list.Add(new List<int> { });
            List<List<int>> binding = new List<List<int>>();
            binding.Add(new List<int> { });
            binding.Add(new List<int> { });
            binding.Add(new List<int> { });
            List<int> set = new List<int>();
            Console.WriteLine("Введите информацию о рёбрах в формате {номер первой точки(пробел)номер второй точки(пробел)вес ребра между ними}");
            Input(list, numberOfEdges);
            int numberOfPoints = DeterminingTheNumberOfPoints(list);
            int[] firstPoint = new int[] { 1, 1 };
            for (int i = 0; i < numberOfPoints; i++)
            {
                AddAndRemove(list, binding, firstPoint);
                for (int l = 0; l < binding[2].Count; l++)
                {
                    int minIndex = MinIndexSearch(binding);
                    if (IntersectionCheck(set, binding, minIndex))
                    {
                        firstPoint[0] = binding[0][minIndex];
                        firstPoint[1] = binding[1][minIndex];
                        set.Add(binding[0][minIndex]);
                        set.Add(binding[1][minIndex]);
                        res += binding[2][minIndex];
                        set = set.Distinct().ToList();
                        binding[0].RemoveAt(minIndex);
                        binding[1].RemoveAt(minIndex);
                        binding[2].RemoveAt(minIndex);
                        break;
                    }
                    else
                    {
                        binding[0].RemoveAt(minIndex);
                        binding[1].RemoveAt(minIndex);
                        binding[2].RemoveAt(minIndex);
                    }
                }
            }
            Console.WriteLine(res);
        }
        static int DeterminingTheNumberOfPoints(List<List<int>> list)
        {
            List<int> union = new List<int>();
            union.AddRange(list[0]);
            union.AddRange(list[1]);
            int numberOfPoints = union.Distinct().Count();
            return numberOfPoints;
        }
        static void Input(List<List<int>> list, int numberOfEdges)
        {
            for (int i = 0; i < numberOfEdges; i++)
            {
                Console.Write((i + 1) + "-е ребро: ");
                string info = Console.ReadLine();
                info += " ";
                int count = 0;
                string storage = "";
                for (int j = 0; j < info.Length; j++)
                {
                    if (info[j] == ' ')
                    {
                        list[count].Add(int.Parse(storage));
                        storage = "";
                        count++;
                    }
                    else
                    {
                        storage += info[j];
                    }
                }
            }
        }
        static void AddAndRemove(List<List<int>> list, List<List<int>> binding, int[] firstPoint)
        {
            for (int j = 0; j < list[0].Count; j++)
            {
                if (firstPoint[0] == list[0][j] || firstPoint[1] == list[0][j] || firstPoint[0] == list[1][j] || firstPoint[1] == list[1][j])
                {
                    binding[0].Add(list[0][j]);
                    binding[1].Add(list[1][j]);
                    binding[2].Add(list[2][j]);
                    list[0].RemoveAt(j);
                    list[1].RemoveAt(j);
                    list[2].RemoveAt(j);
                    j--;
                }
            }
        }
        static int MinIndexSearch(List<List<int>> binding)
        {
            int minIndex = 0;
            int min = int.MaxValue;
            for (int j = 0; j < binding[2].Count; j++)
            {
                if (binding[2][j] < min)
                {
                    min = binding[2][j];
                    minIndex = j;
                }
            }
            return minIndex;
        }
        static bool IntersectionCheck(List<int> set, List<List<int>> binding, int minIndex)
        {
            int intersectionCount = 0;
            for (int j = 0; j < 2; j++)
            {
                foreach (int k in set)
                {
                    if (k == binding[j][minIndex])
                    {
                        intersectionCount++;
                    }
                }
            }
            if (intersectionCount != 2)
            {
                return true;
            }
            return false;
        }

    }
}
