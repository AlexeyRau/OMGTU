import os
import tkinter as tk
from tkinter import filedialog
import matplotlib
matplotlib.use('TkAgg')
from collections import Counter
import math

dir_path = "A:\\OMGTU\\OMGTU\\3year\\5semester\\CryptoMath\\lab2\\lab2"

alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
m = len(alphabet)

freq_table_russian = [
    'о', 'е', 'а', 'и', 'н', 'т', 'с', 'р', 'в', 'л', 
    'к', 'м', 'д', 'п', 'у', 'я', 'ы', 'з', 'ъ', 'б', 
    'г', 'ч', 'й', 'х', 'ж', 'ю', 'ш', 'ц', 'щ', 'э', 'ф'
]

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
    try:
        full_path = os.path.join(dir_path, filename)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(data)
    except Exception as e:
        print(f"  Ошибка при сохранении: {e}")

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

def frequency_analysis(text):
    """Анализ частот символов в тексте"""
    prepared = prepare_text(text)
    counter = Counter(prepared)
    total = len(prepared)
    
    freq_list = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    
    result = []
    for char, count in freq_list:
        percentage = (count / total) * 100
        result.append((char, count, percentage))
    
    return result

def generate_hypotheses(freq_list, max_hypotheses=10):
    """Генерация гипотез о соответствии символов"""
    hypotheses = []
    
    if len(freq_list) < 2:
        return hypotheses
    
    top1_char, top1_count, top1_perc = freq_list[0]
    top2_char, top2_count, top2_perc = freq_list[1]
    
    for i in range(min(max_hypotheses, len(freq_table_russian))):
        for j in range(i + 1, min(max_hypotheses, len(freq_table_russian))):
            hypotheses.append({
                'cipher_chars': [top1_char, top2_char],
                'plain_chars': [freq_table_russian[i], freq_table_russian[j]],
                'description': f"'{top1_char}'->'{freq_table_russian[i]}', '{top2_char}'->'{freq_table_russian[j]}'"
            })
            
            hypotheses.append({
                'cipher_chars': [top1_char, top2_char],
                'plain_chars': [freq_table_russian[j], freq_table_russian[i]],
                'description': f"'{top1_char}'->'{freq_table_russian[j]}', '{top2_char}'->'{freq_table_russian[i]}'"
            })
    
    return hypotheses

def crack_affine_cipher(ciphertext):
    """Криптоанализ аффинного шифра"""
    prepared_cipher = prepare_text(ciphertext)
    
    freq_list = frequency_analysis(prepared_cipher)
    
    print("\n" + "="*50)
    print("РЕЗУЛЬТАТЫ ЧАСТОТНОГО АНАЛИЗА:")
    print("Символ | Количество | Процент")
    print("-" * 30)
    for char, count, perc in freq_list[:10]: 
        print(f"  {char}    |     {count}     |   {perc:.2f}%")
    
    hypotheses = generate_hypotheses(freq_list)
    
    print(f"\nСгенерировано {len(hypotheses)} гипотез")
    
    results = []
    
    for i, hypothesis in enumerate(hypotheses, 1):
        print(f"\n--- Проверка гипотезы {i}: {hypothesis['description']}")
        
        y1 = symbol_to_num(hypothesis['cipher_chars'][0])  # Зашифрованная буква 1
        y2 = symbol_to_num(hypothesis['cipher_chars'][1])  # Зашифрованная буква 2
        x1 = symbol_to_num(hypothesis['plain_chars'][0])   # Открытая буква 1
        x2 = symbol_to_num(hypothesis['plain_chars'][1])   # Открытая буква 2
        
        solutions = solve_system_of_congruences(x1, x2, y1, y2, m)
        
        if not solutions:
            print("  Система не имеет решений")
            continue
        
        for a, b in solutions:
            if not is_valid_key(a, b):
                continue
                
            try:
                decrypted = affine_cipher(prepared_cipher, a, b, 1)
                
                result = {
                    'hypothesis': hypothesis['description'],
                    'key': (a, b),
                    'decrypted': decrypted,
                    'valid': True
                }
                results.append(result)
                
                print(f"  Найден ключ: a={a}, b={b}")
                print(f"  Расшифрованный текст: {decrypted[:100]}...")  
                
                choice = input("  Сохранить этот вариант? (y/n): ").strip().lower()
                if choice == 'y':
                    filename = f"decrypted_a{a}_b{b}.txt"
                    save_to_file(filename, decrypted)
                    print(f"  Текст сохранен в файл: {filename}")
                
            except Exception as e:
                print(f"  Ошибка при расшифровке: {e}")
    
    return results, freq_list

def crypto_analysis_menu():
    """Меню для криптоанализа"""
    print("\n" + "="*50)
    print("КРИПТОАНАЛИЗ АФФИННОГО ШИФРА")
    
    ciphertext = get_text_input()
    if not ciphertext:
        return
    
    protocol_filename = "crypto_analysis_protocol.txt"
    protocol_content = []
    
    def add_to_protocol(text):
        print(text)
        protocol_content.append(text)
    
    results, freq_list = crack_affine_cipher(ciphertext)
    
    protocol_text = "\n".join(protocol_content)
    save_to_file(protocol_filename, protocol_text)
    print(f"\nПротокол сохранен в файл: {protocol_filename}")

def frequency_analysis_menu():
    """Меню для частотного анализа"""
    print("\n" + "="*50)
    print("ЧАСТОТНЫЙ АНАЛИЗ ТЕКСТА")
    
    text = get_text_input()
    if not text:
        return
    
    results = frequency_analysis(text)
    
    print("\n" + "="*50)
    print("РЕЗУЛЬТАТЫ ЧАСТОТНОГО АНАЛИЗА:")
    print("Символ | Количество | Процент")
    print("-" * 30)
    for char, count, perc in results:
        print(f"  {char}    |     {count}     |   {perc:.2f}%")
    
    filename = "frequency_analysis.txt"
    content = "Символ | Количество | Процент\n"
    content += "-" * 30 + "\n"
    for char, count, perc in results:
        content += f"  {char}    |     {count}     |   {perc:.2f}%\n"
    
    save_to_file(filename, content)
    print(f"\nРезультаты сохранены в файл: {filename}")

def main():
    while True:
        print("\n"+"="*50)
        print("ВЫБЕРИТЕ ДЕЙСТВИЕ:")
        print("1. Шифрование аффинным шифром")
        print("2. Расшифрование аффинным шифром")
        print("3. Нахождение обратного элемента")
        print("4. Решение линейного сравнения")
        print("5. Решение системы сравнений")
        print("6. Частотный анализ текста")
        print("7. Криптоанализ аффинного шифра")
        print("8. Выход")
        
        choice = input("\nВаш выбор (1-8): ").strip()
        
        if choice == '1':
            text = get_text_input()
            if not text:
                continue

            print("\n"+"="*50)
            print("ВВОД КЛЮЧА")
            a = int(input(f"Введите a (должно быть взаимно простым с {m}): "))
            b = int(input(f"Введите b (любое число от 0 до {m-1}): "))

            prepared_text = prepare_text(text)
            encrypted_text = affine_cipher(prepared_text, a, b, 0)

            result = f"Исходный текст: {text}\n"
            result += f"Подготовленный текст: {prepared_text}\n"
            result += f"Ключ: [{a}, {b}]\n"
            result += f"Зашифрованный текст: {encrypted_text}\n"

            print("\n"+"="*50)
            print("РЕЗУЛЬТАТ:")
            print(result)
            
            save_choice = input("Сохранить результат в файл? (y/n): ").strip().lower()
            if save_choice == 'y':
                filename = input("Введите имя файла для сохранения: ")
                save_to_file(filename, encrypted_text)
                print(f"Результат сохранен в файл '{filename}'")

        elif choice == '2':
            text = get_text_input()
            if not text:
                continue

            print("\n"+"="*50)
            print("ВВОД КЛЮЧА")
            a = int(input(f"Введите a (должно быть взаимно простым с {m}): "))
            b = int(input(f"Введите b (любое число от 0 до {m-1}): "))

            prepared_text = prepare_text(text)
            decrypted_text = affine_cipher(prepared_text, a, b, 1)

            result = f"Исходный текст: {text}\n"
            result += f"Подготовленный текст: {prepared_text}\n"
            result += f"Ключ: [{a}, {b}]\n"
            result += f"Расшифрованный текст: {decrypted_text}\n"

            print("\n"+"="*50)
            print("РЕЗУЛЬТАТ:")
            print(result)
            
            save_choice = input("Сохранить результат в файл? (y/n): ").strip().lower()
            if save_choice == 'y':
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

        elif choice == '6':
            frequency_analysis_menu()

        elif choice == '7':
            crypto_analysis_menu()

        elif choice == '8':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор! Попробуйте снова.")

if __name__ == "__main__":
    main()