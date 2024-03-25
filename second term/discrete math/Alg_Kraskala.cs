using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;

namespace Alg_Kraskala
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Введите количество рёбер: ");
            int numberOfEdges = int.Parse(Console.ReadLine());
            int[][] ribsAndWeights = new int[3][];
            ribsAndWeights[0] = new int[numberOfEdges];
            ribsAndWeights[1] = new int[numberOfEdges];
            ribsAndWeights[2] = new int[numberOfEdges];
            Console.WriteLine("Введите информацию о рёбрах в формате {номер первой точки(пробел)номер второй точки(пробел)вес ребра между ними}");
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
                        ribsAndWeights[count][i] = int.Parse(storage);
                        storage = "";
                        count++;
                    }
                    else
                    {
                        storage += info[j];
                    }
                }
            }
            ribsAndWeights = Sort(ribsAndWeights);
            int res = Kruskal(ribsAndWeights);
            Console.WriteLine("Минимальная длина оставного дерева: " + res);
        }
        static int[][] Sort(int[][] matrix)
        {
            int min = int.MaxValue;
            int count = 0;
            int[][] matrixSort = new int[matrix.Length][];
            matrixSort[0] = new int[matrix[0].Length];
            matrixSort[1] = new int[matrix[1].Length];
            matrixSort[2] = new int[matrix[2].Length];
            for (int i = 0; i < matrix[2].Length; i++)
            {
                for (int j = 0; j < matrix[2].Length; j++)
                {
                    if (min > matrix[2][j])
                    {
                        count = j;
                        min = matrix[2][j];
                    }
                }
                matrixSort[0][i] = matrix[0][count];
                matrixSort[1][i] = matrix[1][count];
                matrixSort[2][i] = matrix[2][count];
                matrix[2][count] = int.MaxValue;
                min = int.MaxValue;
                count = 0;
            }
            return matrixSort;
        }

        static int Kruskal(int[][] matrix)
        {
            bool intersection = false;
            int count = 0;
            int res = matrix[2][0];
            List<int[]> set = new List<int[]>();
            int[] firstArray = new int[] { matrix[0][0], matrix[1][0] };
            set.Add(firstArray);
            for (int i = 1; i < matrix[0].Length; i++)
            {
                for (int j = 0; j < set.Count; j++)
                {
                    foreach (int k in set[j])
                    {
                        if (k == matrix[0][i] || k == matrix[1][i])
                        {
                            count++;
                        }
                    }
                    if (count == 2 || count == 1)
                    {
                        break;
                    }
                }
                if (count == 0 || count == 1)
                {
                    firstArray = new int[] { matrix[0][i], matrix[1][i] };
                    set.Add(firstArray);
                    count = 0;
                    res += matrix[2][i];
                    for (int j = 0; j < (set.Count - 1); j++)
                    {
                        for (int k = 0; k < (set.Count - 1 - j); k++)
                        {
                            intersection = Intersection(set[set.Count - 1 - j], set[k]);
                            if (intersection)
                            {
                                set[k] = set[k].Union(set[set.Count - 1 - j]).ToArray();
                                set.RemoveAt(set.Count - 1 - j);
                                j -= 1;
                                break;
                            }
                        }
                    }
                }
                else
                {
                    count = 0;
                }
            }
            return res;
        }

        static bool Intersection(int[] set1, int[] set2)
        {
            for (int i = 0; i < set1.Length; i++)
            {
                for (int j = 0; j < set2.Length; j++)
                {
                    if (set1[i] == set2[j])
                    {
                        return true;
                    }
                }
            }
            return false;
        }
    }
}
