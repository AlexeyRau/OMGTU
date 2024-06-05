using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;

class Program
{
    static void StackWriting(Stack<char> stack, string input)
    {
        foreach (char element in input)
        {
            stack.Push(element);
        }
    }
    static bool Check(Stack<char> stack)
    {
        char lastelement;
        for (int i = 0; i < stack.Count; i++)
        {
            lastelement = stack.Pop();
            if (lastelement == ')' || lastelement == '}' || lastelement == ']') { return false; }
        }
        return true;
    }
    static void Main()
    {
        string input = Console.ReadLine();
        Stack<char> stack = new Stack<char>();
        StackWriting(stack, input);
        if (Check(stack)) { Console.WriteLine("Правильные"); }
        else { Console.WriteLine("Неправильные"); }
    }
}
