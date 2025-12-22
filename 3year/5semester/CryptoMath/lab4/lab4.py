import math
import random
import os
import tkinter as tk
from tkinter import filedialog

RUSSIAN_ALPHABET = {
    'А': 10, 'Б': 11, 'В': 12, 'Г': 13, 'Д': 14, 'Е': 15, 'Ж': 16, 'З': 17,
    'И': 18, 'Й': 19, 'К': 20, 'Л': 21, 'М': 22, 'Н': 23, 'О': 24, 'П': 25,
    'Р': 26, 'С': 27, 'Т': 28, 'У': 29, 'Ф': 30, 'Х': 31, 'Ц': 32, 'Ч': 33,
    'Ш': 34, 'Щ': 35, 'Ъ': 36, 'Ы': 37, 'Ь': 38, 'Э': 39, 'Ю': 40, 'Я': 41,
}
SPACE_CODE = 99

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(e, phi):
    gcd, x, y = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("Обратный элемент не существует")
    return x % phi

def bin_pow(a, k, n):
    b = 1
    a = a % n
    while k > 0:
        if k % 2 == 0:
            k //= 2
            a = (a * a) % n
        else:
            k -= 1
            b = (b * a) % n
    return b

def text_to_numbers(text):
    nums = []
    for char in text.upper():
        if char == ' ':
            nums.append(SPACE_CODE)
        elif char in RUSSIAN_ALPHABET:
            nums.append(RUSSIAN_ALPHABET[char])
    return nums

def numbers_to_text(nums):
    reverse_map = {v: k for k, v in RUSSIAN_ALPHABET.items()}
    reverse_map[SPACE_CODE] = ' '
    return ''.join(reverse_map.get(num, '?') for num in nums)

def split_into_blocks(nums, n):
    blocks = []
    current = 0
    
    for num in nums:
        candidate = current * 100 + num
        if candidate < n:
            current = candidate
        else:
            if current > 0:
                blocks.append(current)
            current = num
    
    if current > 0:
        blocks.append(current)
    
    return blocks

def blocks_to_numbers(blocks):
    nums = []
    for block in blocks:
        temp = block
        block_nums = []
        while temp > 0:
            block_nums.insert(0, temp % 100)
            temp //= 100
        nums.extend(block_nums)
    return nums

def generate_multiple_key_pairs(p, q, count=3):
    if count < 3:
        count = 3
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    key_pairs = []
    used_e_values = set()
    
    print(f"\n[Генерация {count} пар ключей]")
    print(f"n = {p} * {q} = {n}")
    print(f"φ(n) = ({p}-1)*({q}-1) = {phi}")
    
    for i in range(count):
        attempts = 0
        
        while attempts < 1000:
            attempts += 1
            
            e = random.randint(3, phi - 1)
            
            if math.gcd(e, phi) == 1 and e not in used_e_values:
                try:
                    d = mod_inverse(e, phi)
                    
                    key_pair = {
                        'p': p, 'q': q, 'n': n, 'phi': phi,
                        'public': (e, n),
                        'private': (d, n),
                        'e': e, 'd': d
                    }
                    
                    key_pairs.append(key_pair)
                    used_e_values.add(e)
                    
                    print(f"\n  Пара ключей #{i+1}:")
                    print(f"    e = {e}")
                    print(f"    d = {d}")
                    print(f"    Проверка: e*d mod φ(n) = {(e * d) % phi}")
                    
                    break
                    
                except ValueError:
                    continue
        
        if attempts >= 1000:
            print(f"⚠️ Не удалось найти подходящее e для пары #{i+1}")
            break
    
    if len(key_pairs) < count:
        print(f"\n⚠️ Сгенерировано только {len(key_pairs)} пар из {count}")
    
    return key_pairs

def save_to_file(content, default_name="output.txt"):
    print("\n" + "="*40)
    save_choice = input("Сохранить результат в файл? (y/n): ").lower().strip()
    
    if save_choice == 'y':
        filename = input(f"Введите имя файла (по умолчанию: {default_name}): ").strip()
        if not filename:
            filename = default_name
        
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                if isinstance(content, list):
                    f.write(', '.join(map(str, content)))
                else:
                    f.write(content)
            
            print(f"✓ Результат сохранен в файл: {filename}")
            return True
        except Exception as e:
            print(f"✗ Ошибка при сохранении файла: {e}")
            return False
    return False

def get_text_input():
    print("\n" + "="*40)
    print("ИСТОЧНИК ТЕКСТА:")
    print("1. Ввод с консоли")
    print("2. Чтение из файла")
    
    choice = input("\nВаш выбор (1-2): ").strip()
    
    if choice == '1':
        print("\n" + "="*40)
        text = input("Введите текст для обработки: ").strip()
        if not text:
            print("✗ Текст не может быть пустым!")
            return None
        return text
    
    elif choice == '2':
        return read_from_file("текст")
    
    else:
        print("✗ Неверный выбор!")
        return None

def get_encrypted_blocks_input():
    print("\n" + "="*40)
    print("ИСТОЧНИК ЗАШИФРОВАННЫХ ДАННЫХ:")
    print("1. Ввод с консоли")
    print("2. Чтение из файла")
    
    choice = input("\nВаш выбор (1-2): ").strip()
    
    if choice == '1':
        print("\n" + "="*40)
        input_str = input("Введите блоки для расшифрования (через запятую): ").strip()
        if not input_str:
            print("✗ Данные не могут быть пустыми!")
            return None
        
        try:
            blocks = [int(x.strip()) for x in input_str.split(',')]
            return blocks
        except ValueError:
            print("✗ Неверный формат данных! Используйте числа, разделенные запятыми.")
            return None
    
    elif choice == '2':
        return read_encrypted_blocks_from_file()
    
    else:
        print("✗ Неверный выбор!")
        return None

def read_from_file(data_type="текст"):
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        file_path = filedialog.askopenfilename(
            title=f"Выберите файл с {data_type}ом",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        
        root.destroy()
        
        if not file_path:
            print("Выбор файла отменен.")
            return None
        
        print(f"✓ Выбран файл: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            print(f"✓ Файл успешно прочитан. Размер: {len(content)} символов")
            return content
            
    except Exception as e:
        print(f"✗ Ошибка при чтении файла: {e}")
        return None

def read_encrypted_blocks_from_file():
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        file_path = filedialog.askopenfilename(
            title="Выберите файл с зашифрованными блоками",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        
        root.destroy()
        
        if not file_path:
            print("Выбор файла отменен.")
            return None
        
        print(f"✓ Выбран файл: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            
            try:
                blocks = [int(x.strip()) for x in content.split(',')]
                print(f"✓ Файл успешно прочитан. Найдено {len(blocks)} блоков")
                return blocks
            except ValueError:
                print("✗ Неверный формат файла! Ожидаются числа, разделенные запятыми.")
                print(f"  Пример правильного формата: 12345, 67890, 54321")
                return None
            
    except Exception as e:
        print(f"✗ Ошибка при чтении файла: {e}")
        return None

def print_menu():
    print("\n" + "="*50)
    print("ЛАБОРАТОРНАЯ РАБОТА №4: RSA")
    print("="*50)
    print("1. Генерация нескольких пар ключей")
    print("2. Шифрование текста")
    print("3. Расшифрование текста")
    print("4. Показать все сгенерированные ключи")
    print("5. Выход")
    print("="*50)

def main():
    print("="*50)
    print("ЛАБОРАТОРНАЯ РАБОТА №4: RSA")
    print("="*50)
    print("Задание: Генерация не менее трех пар открытого/закрытого ключа")
    print("="*50)
    
    all_key_pairs = []
    
    while True:
        print_menu()
        choice = input("Выберите действие (1-5): ").strip()
        
        if choice == '1':
            try:
                p = int(input("Введите p (простое число): "))
                q = int(input("Введите q (простое число): "))
                
                if p == q:
                    print("✗ Ошибка: p и q должны быть разными!")
                    continue
                
                count = int(input("Сколько пар ключей сгенерировать? (минимум 3): "))
                if count < 3:
                    count = 3
                    print(f"✓ Будет сгенерировано минимум 3 пары ключей")
                
                print(f"\n[Генерация {count} пар ключей для p={p}, q={q}]")
                
                new_key_pairs = generate_multiple_key_pairs(p, q, count)
                all_key_pairs.extend(new_key_pairs)
                
                print(f"\n✓ Успешно сгенерировано {len(new_key_pairs)} пар ключей")
                print(f"✓ Всего пар ключей в системе: {len(all_key_pairs)}")
                
                if new_key_pairs:
                    print("\n" + "="*40)
                    save_keys = input("Сохранить ключи в файл? (y/n): ").lower().strip()
                    if save_keys == 'y':
                        filename = input("Введите имя файла (по умолчанию: keys.txt): ").strip()
                        if not filename:
                            filename = "keys.txt"
                        
                        if not filename.endswith('.txt'):
                            filename += '.txt'
                        
                        try:
                            with open(filename, 'w', encoding='utf-8') as f:
                                f.write("СГЕНЕРИРОВАННЫЕ КЛЮЧИ RSA\n")
                                f.write("="*50 + "\n\n")
                                f.write(f"Параметры: p={p}, q={q}\n")
                                f.write(f"Модуль: n={p*q}\n")
                                f.write(f"φ(n)={(p-1)*(q-1)}\n")
                                f.write("="*50 + "\n\n")
                                
                                for i, kp in enumerate(new_key_pairs, 1):
                                    f.write(f"ПАРА КЛЮЧЕЙ #{i}:\n")
                                    f.write(f"  Открытый ключ (e, n): ({kp['e']}, {kp['n']})\n")
                                    f.write(f"  Закрытый ключ (d, n): ({kp['d']}, {kp['n']})\n")
                                    f.write(f"  Проверка: e*d mod φ(n) = {(kp['e'] * kp['d']) % kp['phi']}\n")
                                    f.write("-"*40 + "\n\n")
                            
                            print(f"✓ Ключи сохранены в файл: {filename}")
                        except Exception as e:
                            print(f"✗ Ошибка при сохранении ключей: {e}")
                
            except ValueError as e:
                print(f"✗ Ошибка: {e}")
            except Exception as e:
                print(f"✗ Ошибка при генерации ключей: {e}")
        
        elif choice == '2':
            if not all_key_pairs:
                print("✗ Ошибка: сначала сгенерируйте ключи!")
                continue
            
            print("\n[ВЫБОР КЛЮЧА ДЛЯ ШИФРОВАНИЯ]")
            for i, kp in enumerate(all_key_pairs):
                e, n = kp['public']
                print(f"{i+1:2d}. Открытый ключ: e={e:5d}, n={n:8d} (p={kp['p']}, q={kp['q']})")
            
            try:
                key_idx = int(input(f"Выберите ключ (1-{len(all_key_pairs)}): ")) - 1
                if key_idx < 0 or key_idx >= len(all_key_pairs):
                    print("✗ Неверный номер ключа!")
                    continue
                
                key_pair = all_key_pairs[key_idx]
                e, n = key_pair['public']
                
                text = get_text_input()
                if text is None:
                    continue
                
                print(f"\n[ОБРАБОТКА ТЕКСТА]")
                print(f"Текст: {text[:50]}..." if len(text) > 50 else f"Текст: {text}")
                
                nums = text_to_numbers(text)
                if not nums:
                    print("✗ Ошибка: текст не содержит русских букв!")
                    continue
                
                print(f"Числовое представление: {nums[:20]}..." if len(nums) > 20 else f"Числовое представление: {nums}")
                
                blocks = split_into_blocks(nums, n)
                print(f"Блоки для шифрования: {blocks}")
                
                encrypted_blocks = [bin_pow(block, e, n) for block in blocks]
                
                print(f"\n[РЕЗУЛЬТАТ ШИФРОВАНИЯ]")
                print(f"Использован ключ: e={e}, n={n}")
                print(f"Зашифрованные блоки: {encrypted_blocks}")
                print(f"Строка для передачи: {', '.join(map(str, encrypted_blocks))}")
                
                global last_encrypted_data
                last_encrypted_data = {
                    'blocks': encrypted_blocks,
                    'key_idx': key_idx
                }
                
                save_to_file(encrypted_blocks, "encrypted.txt")
                
            except ValueError:
                print("✗ Ошибка: введите номер ключа!")
            except Exception as e:
                print(f"✗ Ошибка при шифровании: {e}")
        
        elif choice == '3':
            if not all_key_pairs:
                print("✗ Ошибка: сначала сгенерируйте ключи!")
                continue
            
            print("\n[ВЫБОР КЛЮЧА ДЛЯ РАСШИФРОВАНИЯ]")
            for i, kp in enumerate(all_key_pairs):
                d, n = kp['private']
                print(f"{i+1:2d}. Закрытый ключ: d={d:5d}, n={n:8d} (p={kp['p']}, q={kp['q']})")
            
            try:
                key_idx = int(input(f"Выберите ключ (1-{len(all_key_pairs)}): ")) - 1
                if key_idx < 0 or key_idx >= len(all_key_pairs):
                    print("✗ Неверный номер ключа!")
                    continue
                
                key_pair = all_key_pairs[key_idx]
                d, n = key_pair['private']
                
                encrypted_blocks = get_encrypted_blocks_input()
                if encrypted_blocks is None:
                    continue
                
                print(f"\n[РАСШИФРОВАНИЕ]")
                print(f"Получено блоков: {len(encrypted_blocks)}")
                print(f"Блоки: {encrypted_blocks}")
                
                decrypted_blocks = [bin_pow(block, d, n) for block in encrypted_blocks]
                print(f"Расшифрованные блоки: {decrypted_blocks}")
                
                nums = blocks_to_numbers(decrypted_blocks)
                print(f"Числовая последовательность: {nums}")
                
                text = numbers_to_text(nums)
                
                print(f"\n[РЕЗУЛЬТАТ РАСШИФРОВАНИЯ]")
                print(f"Использован ключ: d={d}, n={n}")
                print(f"Текст: {text}")
                
                save_to_file(text, "decrypted.txt")
                
            except ValueError:
                print("✗ Ошибка: неверный формат ввода!")
            except Exception as e:
                print(f"✗ Ошибка при расшифровании: {e}")
        
        elif choice == '4':
            if not all_key_pairs:
                print("✗ Нет сгенерированных ключей!")
                continue
            
            print(f"\n[ВСЕГО СГЕНЕРИРОВАНО ПАР КЛЮЧЕЙ: {len(all_key_pairs)}]")
            print("="*70)
            
            for i, kp in enumerate(all_key_pairs):
                print(f"\nПАРА КЛЮЧЕЙ #{i+1}:")
                print(f"  p = {kp['p']}, q = {kp['q']}")
                print(f"  n = {kp['n']}, φ(n) = {kp['phi']}")
                print(f"  Открытый ключ (e, n): ({kp['public'][0]}, {kp['public'][1]})")
                print(f"  Закрытый ключ (d, n): ({kp['private'][0]}, {kp['private'][1]})")
                print("-"*50)
        
        elif choice == '5':
            print("Выход из программы.")
            break
        
        else:
            print("✗ Неверный выбор! Попробуйте снова.")

if __name__ == "__main__":
    main()