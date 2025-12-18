import math
import random

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

def bin_pow(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        exp >>= 1
        base = (base * base) % mod
    return result

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

def generate_key_pair(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e_candidates = [3, 17, 257, 65537]
    e = None
    for candidate in e_candidates:
        if 1 < candidate < phi and math.gcd(candidate, phi) == 1:
            e = candidate
            break
    
    if e is None:
        e = random.randint(2, phi - 1)
        while math.gcd(e, phi) != 1:
            e = random.randint(2, phi - 1)
    
    d = mod_inverse(e, phi)
    
    return {
        'p': p,
        'q': q,
        'n': n,
        'phi': phi,
        'public': (e, n),
        'private': (d, n)
    }

def generate_multiple_key_pairs(p, q, count=3):
    key_pairs = []
    for i in range(count):
        print(f"\nГенерация пары ключей #{i+1}...")
        try:
            key_pair = generate_key_pair(p, q)
            key_pairs.append(key_pair)
            print(f"Пара #{i+1}: e = {key_pair['public'][0]}, d = {key_pair['private'][0]}")
        except Exception as e:
            print(f"Ошибка при генерации пары #{i+1}: {e}")
    
    return key_pairs

def print_menu():
    print("\n" + "="*50)
    print("ЛАБОРАТОРНАЯ РАБОТА №4: RSA")
    print("="*50)
    print("1. Генерация нескольких пар ключей")
    print("2. Шифрование текста (с выбором ключа)")
    print("3. Расшифрование текста (с выбором ключа)")
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
    current_p = None
    current_q = None
    
    while True:
        print_menu()
        choice = input("Выберите действие (1-5): ").strip()
        
        if choice == '1':
            try:
                p = int(input("Введите p (простое число): "))
                q = int(input("Введите q (простое число): "))
                
                if p == q:
                    print("Ошибка: p и q должны быть разными!")
                    continue
                
                current_p = p
                current_q = q
                
                count = int(input("Сколько пар ключей сгенерировать? (минимум 3): "))
                if count < 3:
                    count = 3
                    print(f"Будет сгенерировано минимум 3 пары ключей")
                
                print(f"\n[Генерация {count} пар ключей для p={p}, q={q}]")
                print(f"n = {p*q}")
                print(f"φ(n) = {(p-1)*(q-1)}")
                
                new_key_pairs = generate_multiple_key_pairs(p, q, count)
                all_key_pairs.extend(new_key_pairs)
                
                print(f"\n✓ Успешно сгенерировано {len(new_key_pairs)} пар ключей")
                print(f"Всего пар ключей в системе: {len(all_key_pairs)}")
                
            except ValueError as e:
                print(f"Ошибка: {e}")
            except Exception as e:
                print(f"Ошибка при генерации ключей: {e}")
        
        elif choice == '2':
            if not all_key_pairs:
                print("Ошибка: сначала сгенерируйте ключи!")
                continue
            
            print("\n[Выбор ключа для шифрования]")
            for i, kp in enumerate(all_key_pairs):
                e, n = kp['public']
                print(f"{i+1}. Открытый ключ: e={e}, n={n} (p={kp['p']}, q={kp['q']})")
            
            try:
                key_idx = int(input(f"Выберите ключ (1-{len(all_key_pairs)}): ")) - 1
                if key_idx < 0 or key_idx >= len(all_key_pairs):
                    print("Неверный номер ключа!")
                    continue
                
                key_pair = all_key_pairs[key_idx]
                e, n = key_pair['public']
                
                text = input("Введите текст для шифрования: ").strip()
                if not text:
                    print("Ошибка: текст не может быть пустым!")
                    continue
                
                nums = text_to_numbers(text)
                if not nums:
                    print("Ошибка: текст не содержит русских букв!")
                    continue
                
                print(f"\nЧисловое представление: {nums}")
                
                blocks = split_into_blocks(nums, n)
                print(f"Блоки для шифрования: {blocks}")
                
                encrypted_blocks = [bin_pow(block, e, n) for block in blocks]
                
                print(f"\n[Результат шифрования с ключом #{key_idx+1}]")
                print(f"Использован ключ: e={e}, n={n}")
                print(f"Зашифрованные блоки: {encrypted_blocks}")
                print(f"Строка для передачи: {', '.join(map(str, encrypted_blocks))}")
                
                global last_encrypted_data
                last_encrypted_data = {
                    'blocks': encrypted_blocks,
                    'key_idx': key_idx
                }
                print("\n(Зашифрованные данные сохранены для последующего расшифрования)")
                
            except ValueError:
                print("Ошибка: введите номер ключа!")
            except Exception as e:
                print(f"Ошибка при шифровании: {e}")
        
        elif choice == '3':
            if not all_key_pairs:
                print("Ошибка: сначала сгенерируйте ключи!")
                continue
            
            print("\n[Выбор ключа для расшифрования]")
            for i, kp in enumerate(all_key_pairs):
                d, n = kp['private']
                print(f"{i+1}. Закрытый ключ: d={d}, n={n} (p={kp['p']}, q={kp['q']})")
            
            try:
                key_idx = int(input(f"Выберите ключ (1-{len(all_key_pairs)}): ")) - 1
                if key_idx < 0 or key_idx >= len(all_key_pairs):
                    print("Неверный номер ключа!")
                    continue
                
                key_pair = all_key_pairs[key_idx]
                d, n = key_pair['private']
                
                if 'last_encrypted_data' in globals() and last_encrypted_data['key_idx'] == key_idx:
                    use_saved = input("Использовать последние зашифрованные данные? (y/n): ").lower()
                    if use_saved == 'y':
                        encrypted_blocks = last_encrypted_data['blocks']
                        print(f"Используются сохраненные блоки: {encrypted_blocks}")
                    else:
                        input_str = input("Введите блоки для расшифрования (через запятую): ").strip()
                        encrypted_blocks = list(map(int, input_str.split(',')))
                else:
                    input_str = input("Введите блоки для расшифрования (через запятую): ").strip()
                    encrypted_blocks = list(map(int, input_str.split(',')))
                
                decrypted_blocks = [bin_pow(block, d, n) for block in encrypted_blocks]
                print(f"\nРасшифрованные блоки: {decrypted_blocks}")
                
                nums = blocks_to_numbers(decrypted_blocks)
                print(f"Числовая последовательность: {nums}")
                
                text = numbers_to_text(nums)
                print(f"\n[Результат расшифрования с ключом #{key_idx+1}]")
                print(f"Использован ключ: d={d}, n={n}")
                print(f"Текст: {text}")
                
            except ValueError:
                print("Ошибка: неверный формат ввода!")
            except Exception as e:
                print(f"Ошибка при расшифровании: {e}")
        
        elif choice == '4':
            if not all_key_pairs:
                print("Нет сгенерированных ключей!")
                continue
            
            print(f"\n[Всего сгенерировано пар ключей: {len(all_key_pairs)}]")
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
            print("Неверный выбор! Попробуйте снова.")

if __name__ == "__main__":
    main()