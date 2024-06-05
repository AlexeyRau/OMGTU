using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Polysh
{
    internal class Program
    {
        static void Main(string[] args)
        {
            string input = "2 2 + 2 +"; //Входные данные
            double result = PolyshEntryCalc(input);
            Console.WriteLine(result);
        }
        static double PolyshEntryCalc(string input)
        {
            Stack<double> stack = new Stack<double>();
            double result;
            string num = "";
            for (int i = 0; i < input.Length; i++)
            {
                if (input[i] != ' ')
                {
                    if (input[i] != '+' && input[i] != '-' && input[i] != '*' && input[i] != '/' && input[i] != '^')
                    {
                        num += input[i];
                    }
                    else
                    {
                        if (stack.Count > 1)
                        {
                            switch (input[i])
                            {
                                case '+':
                                    stack.Push(stack.Pop() + stack.Pop());
                                    break;
                                case '-':
                                    stack.Push(-stack.Pop() + stack.Pop());
                                    break;
                                case '*':
                                    stack.Push(stack.Pop() * stack.Pop());
                                    break;
                                case '/':
                                    try
                                    {
                                        stack.Push(1 / stack.Pop() * stack.Pop());
                                    }
                                    catch (DivideByZeroException)
                                    {
                                        Console.WriteLine("На ноль делить нельзя");
                                    }
                                    break;
                                default:
                                    Console.WriteLine("данные введены неккоректно");
                                    return 0;
                            }
                        }
                        else
                        {
                            Console.WriteLine("даные введены неккоректно");
                            return 0;
                        }
                    }
                }
                else if (num != "")
                {
                    stack.Push(int.Parse(num));
                    num = "";
                }
            }
            result = stack.Pop();
            if (stack.Count > 0)
            {
                Console.WriteLine("даные введены неккоректно");
                return 0;
            }
            return result;
        }
    }
}
