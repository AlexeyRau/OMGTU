import os
import tkinter as tk
from tkinter import filedialog
import matplotlib
matplotlib.use('TkAgg')
from collections import Counter
import math

dir_path = "D:\\OMGTU\\OMGTU\\3year\\5semester\\CryptoMath\\lab1\\lab1"

alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
m = len(alphabet)

def prepare_text(text):
    result = []
    for b_i in text:
        if b_i.lower() in alphabet:
            result.append(b_i.lower())
        elif b_i.lower() == 'ё':
            result.append('е')
        elif b_i != ' ':
            result.append(b_i)
    return ''.join(result)

def symbol_to_num(symbol):
    return alphabet.index(symbol)

def num_to_symbol(num):
    return alphabet[num % m]

def extended_gcd(a, m):
    if a == 0:
        return m, 0, 1
    gcd, x1, y1 = extended_gcd(m % a, a)
    x = y1 - (m // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        return None
    return x % m

def affine_cipher(text, a, b, c):
    result = []
    a_inverse = mod_inverse(a, m)
    for symbol in text:
        if symbol in alphabet:
            x = symbol_to_num(symbol)
            if c == 0:
                y = (a * x + b) % m
            elif c == 1:
                y = a_inverse * (x - b) % m
            result.append(num_to_symbol(y))
        else:
            result.append(symbol)
    return ''.join(result)

def solve_linear_congruence(a, b, m):
    gcd, x0, y0 = extended_gcd(a, m)
    
    if b % gcd != 0:
        return []
    
    solutions = []
    x = (x0 * (b // gcd)) % m
    for i in range(gcd):
        solutions.append((x + i * (m // gcd)) % m)
    
    return solutions

def solve_system_of_congruences(a, c, b, d, m):
    diff_a = (a - c) % m
    diff_b = (b - d) % m
    
    x_solutions = solve_linear_congruence(diff_a, diff_b, m)
    
    solutions = []
    for x in x_solutions:
        y = (b - a * x) % m
        solutions.append((x, y))
    
    return solutions

def is_valid_key(a, b):
    return math.gcd(a, m) == 1 and 1 <= a < m and 0 <= b < m

def save_to_file(filename, data):
    full_path = os.path.join(dir_path, filename)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(data)

def get_text_input():
    print("\n"+"="*50)
    print("Выберите способ ввода текста:")
    print("1. Ввод с консоли")
    print("2. Чтение из файла")
    
    choice = input("\nВаш выбор (1-2): ").strip()
    
    if choice == '1':
        print("\n"+"="*50)
        return input("Введите текст: ")
    elif choice == '2':
        return read_from_file_dialog()
    else:
        print("Неверный выбор!")
        return None

def read_from_file_dialog():
    try:
        root = tk.Tk()
        root.withdraw() 
        root.attributes('-topmost', True) 
        
        file_path = filedialog.askopenfilename(
            title="Выберите текстовый файл",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        
        root.destroy()
        
        if not file_path:
            print("Выбор файла отменен.")
            return None
        
        print(f"Выбран файл: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            print(f"Файл успешно прочитан. Размер: {len(content)} символов")
            return content
            
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None

def main():
    while True:
        print("\n"+"="*50)
        print("Выберите действие:")
        print("1. Шифрование аффинным шифром")
        print("2. Расшифрование аффинным шифром")
        print("3. Нахождение обратного элемента")
        print("4. Решение линейного сравнения")
        print("5. Решение системы сравнений")
        
        choice = input("\nВаш выбор (1-8): ").strip()
        
        if choice == '1':
            text = get_text_input()
            if text == "":
                print("")
                input("Поле пустое, нажмите Enter чтобы продолжить")
                continue

            print("\n"+"="*50)
            print("Ввод ключа")
            a = int(input(f"Введите a (Должно быть взаимно простым с {m}): "))
            b = int(input(f"Введите b (любое число от 0 до {m-1}): "))

            prepared_text = prepare_text(text)
            encrypted_text = affine_cipher(prepared_text, a, b, 0)

            result = f"Исходный текст: {text}\n"
            result += f"Подготовленный текст: {prepared_text}\n"
            result += f"Ключ: [{a}, {b}]\n"
            result += f"Зашифрованный текст: {encrypted_text}\n"

            print("\n"+"="*50)
            print("Результат:")
            print(result)
            print("Хотите сохранить файл?")
            print("1. Да")
            print("2. Нет")
            save_choice = input("\nВаш выбор (1-2): ")
            if save_choice == '1':
                print("\n"+"="*50)
                filename = input("Введите имя файла для сохранения: ")
                save_to_file(filename, encrypted_text)
                print(f"Результат сохранен в файл '{filename}'")

        elif choice == '2':
            text = get_text_input()
            if text == "":
                print("")
                input("Поле пустое, нажмите Enter чтобы продолжить")
                continue

            print("\n"+"="*50)
            print("Ввод ключа")
            a = int(input(f"Введите a (Должно быть взаимно простым с {m}): "))
            b = int(input(f"Введите b (любое число от 0 до {m-1}): "))

            prepared_text = prepare_text(text)
            decrypted_text = affine_cipher(prepared_text, a, b, 1)

            result = f"Исходный текст: {text}\n"
            result += f"Подготовленный текст: {prepared_text}\n"
            result += f"Ключ: [{a}, {b}]\n"
            result += f"Расшифрованный текст: {decrypted_text}\n"

            print("\n"+"="*50)
            print("Результат:")
            print(result)
            print("Хотите сохранить файл?")
            print("1. Да")
            print("2. Нет")
            save_choice = input("\nВаш выбор (1-2): ")
            if save_choice == '1':
                print("\n"+"="*50)
                filename = input("Введите имя файла для сохранения: ")
                save_to_file(filename, decrypted_text)
                print(f"Результат сохранен в файл '{filename}'")

        elif choice == '3':
            try:
                a = int(input("Введите элемент a: "))
                modulus = int(input("Введите модуль m: "))
                
                inverse = mod_inverse(a, modulus)
                
                if inverse is None:
                    print(f"Обратный элемент для {a} mod {modulus} не существует")
                else:
                    print(f"Обратный элемент для {a} mod {modulus}: {inverse}")
                    print(f"Проверка: {a} * {inverse} mod {modulus} = {(a * inverse) % modulus}")
                    
            except ValueError:
                print("Введите корректные числа!")

        elif choice == '4':
            try:
                a = int(input("Введите a: "))
                b = int(input("Введите b: "))
                modulus = int(input("Введите модуль m: "))
                
                solutions = solve_linear_congruence(a, b, modulus)
                
                if not solutions:
                    print(f"Сравнение {a}x ≡ {b} (mod {modulus}) не имеет решений")
                else:
                    print(f"Решения сравнения {a}x ≡ {b} (mod {modulus}): {solutions}")
                    
            except ValueError:
                print("Введите корректные числа!")

        elif choice == '5':
            try:
                a = int(input("Введите a (из первого уравнения): "))
                b1 = int(input("Введите b (из первого уравнения): "))
                c = int(input("Введите c (из второго уравнения): "))
                d = int(input("Введите d (из второго уравнения): "))
                modulus = int(input("Введите модуль m: "))
                
                solutions = solve_system_of_congruences(a, c, b1, d, modulus)
                
                if not solutions:
                    print("Система не имеет решений")
                else:
                    print("Решения системы:")
                    for i, (x, y) in enumerate(solutions, 1):
                        print(f"Решение {i}: x = {x}, y = {y}")
                        
            except ValueError:
                print("Введите корректные числа!")        
                    
if __name__ == "__main__":
    main()