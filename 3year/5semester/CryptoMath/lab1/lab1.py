import os
import tkinter as tk
from tkinter import filedialog
import matplotlib
matplotlib.use('TkAgg') 

dir_path = "A:\\OMGTU\\OMGTU\\3year\\5semester\\CryptoMath\\lab1"

alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
m = len(alphabet)

def prepare_text(text):
    result = []
    for b_i in text.lower():
        if b_i == 'ё':
            result.append('е')
        elif b_i != ' ':
            result.append(b_i)
    return ''.join(result)

def symbol_to_num(symbol):
    return alphabet.index(symbol)

def num_to_symbol(num):
    return alphabet[num % m]

def encrypt(text, k):
    encrypted_codes = []
    for b_i in text:
        if b_i in alphabet:
            x_i = symbol_to_num(b_i)
            y_i = (x_i + k) % m
            encrypted_codes.append(y_i)
        else:
            encrypted_codes.append(b_i)

    result = []
    for item in encrypted_codes:
        if isinstance(item, int):
            result.append(num_to_symbol(item))
        else:
            result.append(item)
    return ''.join(result)

def decrypt(text, k):
    decrypted_codes = []
    for sym in text:
        if sym in alphabet:
            y_i = symbol_to_num(sym)
            x_i = (y_i - k) % m
            decrypted_codes.append(x_i)
        else:
            decrypted_codes.append(sym)
    
    result = []
    for item in decrypted_codes:
        if isinstance(item, int):
            result.append(num_to_symbol(item))
        else:
            result.append(item)
    return ''.join(result)

def brute_force(ciphertext):
    results = []
    for k in range(1, m):
        decrypted_text = decrypt(ciphertext, k)
        results.append((k, decrypted_text))
    return results

def save_to_file(filename, data):
    full_path = os.path.join(dir_path, filename)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(data)

def get_text_input():
    print("\nВыберите способ ввода текста:")
    print("1. Ввод с консоли")
    print("2. Чтение из файла")
    
    choice = input("Ваш выбор (1-2): ").strip()
    
    if choice == '1':
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
    print("Шифр Цезаря - Лабораторная работа")
    print("=" * 40)
    
    while True:
        print("\nВыберите действие:")
        print("1. Шифрование текста")
        print("2. Расшифрование текста")
        print("3. Атака полным перебором")
        print("4. Выход")
        
        choice = input("Ваш выбор (1-4): ").strip()
        
        if choice == '1':
            text = get_text_input()
            if text is None:
                continue
                
            try:
                key = int(input("Введите ключ (1-31): "))
                if not 1 <= key <= 31:
                    print("Ключ должен быть в диапазоне 1-31!")
                    continue
            except ValueError:
                print("Ключ должен быть числом!")
                continue
            
            prepared_text = prepare_text(text)
            encrypted_text = encrypt(prepared_text, key)
            
            result = f"Исходный текст: {text}\n"
            result += f"Подготовленный текст: {prepared_text}\n"
            result += f"Ключ: {key}\n"
            result += f"Зашифрованный текст: {encrypted_text}\n"
            print("\n=================================================")
            print("Результат:")
            print(result)
            print("Хотите сохранить файл?")
            print("1. Да")
            print("2. Нет")
            save_choice = input("Ваш выбор (1-2): ")
            if save_choice == '1':
                filename = input("Введите имя файла для сохранения: ")
                save_to_file(filename, encrypted_text)
                print(f"Результат сохранен в файл '{filename}'")
                print("=================================================")
            elif save_choice == '2':
                print("=================================================")
            else:
                print("Неверный выбор. Попробуйте снова.")    
                print("=================================================")
                    
        elif choice == '2':
            text = get_text_input()
            if text is None:
                continue
                
            try:
                key = int(input("Введите ключ (1-31): "))
                if not 1 <= key <= 31:
                    print("Ключ должен быть в диапазоне 1-31!")
                    continue
            except ValueError:
                print("Ключ должен быть числом!")
                continue
            
            prepared_text = prepare_text(text)
            decrypted_text = decrypt(prepared_text, key)
            
            result = f"Исходный текст: {text}\n"
            result += f"Подготовленный текст: {prepared_text}\n"
            result += f"Ключ: {key}\n"
            result += f"Расшифрованный текст: {decrypted_text}\n"
            print("\n=================================================")
            print("Результат:")
            print(result)
            print("Хотите сохранить файл?")
            print("1. Да")
            print("2. Нет")
            save_choice = input("Ваш выбор (1-2): ")
            if save_choice == '1':
                filename = input("Введите имя файла для сохранения: ")
                save_to_file(filename, decrypted_text)
                print(f"Результат сохранен в файл '{filename}'")
                print("=================================================")
            elif save_choice == '2':
                print("=================================================")
            else:
                print("Неверный выбор. Попробуйте снова.")    
                print("=================================================")
            
        elif choice == '3':
            ciphertext_variant_14 = "ауцаугзмэьвифвгжзехввгуауцгчсувъдгцъщэзъъехжжищгябгю"
            data = ""
            results = brute_force(ciphertext_variant_14)
            for key, decrypted in results:
                data += f"Ключ {key}: {decrypted}\n"
            
            print("Хотите сохранить все варианты расшифровки в файл?")
            print("1. Да")
            print("2. Нет")
            save_choice = input("Ваш выбор (1-2): ")
            if save_choice == '1':
                filename = input("Введите имя файла для сохранения: ")
                save_to_file(filename, data)
                print(f"Результат сохранен в файл '{filename}'")
                print("=================================================")
            elif save_choice == '2':
                print("=================================================")
            else:
                print("Неверный выбор. Попробуйте снова.")    
                print("=================================================")

            right_key = 1

            print("\n=================================================")
            print("\nВыберите подходящий вариант расшифровки:")
            for key, decrypted in results:

                print("\n=================================================")
                print(f"Ключ: {key}")
                print(f"Расшифровка: {decrypted}")
                print("\nВыбрать этот вариант расшифровки?:")
                print("1. Да")
                print("2. Нет")
                choice = input("Ваш выбор (1-2): ").strip()
                if choice == '1':
                    right_key = key
                    break
                elif choice == '2':
                    continue
                else:
                    print("Неверный выбор.")
                    break
                

            key, text = results[right_key - 1]
            author_work = "лермонтовродина"
            encrypted_author_work = encrypt(author_work, 10)
            
            print("=================================================")
            print("Ответ на задание 3, вариант 14:")
            print(f"ШИФР-ТЕКСТ: {ciphertext_variant_14}")
            print(f"РАСШИФРОВАННЫЙ ТЕКСТ: {text}")
            print(f"КЛЮЧ: {key}")
            print(f"АВТОР И ПРОИЗВЕДЕНИЕ: {author_work}")
            print(f"ЗАШИФРОВАННЫЕ ФАМИЛИЯ И НАЗВАНИЕ: {encrypted_author_work}")
            print("=================================================")

        elif choice == '4':
            print("Выход из программы.")
            break
            
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()