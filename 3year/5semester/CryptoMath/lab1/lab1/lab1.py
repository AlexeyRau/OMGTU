alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
m = len(alphabet)

def prepare_text(text):
    result = []
    for b_i in text.lower():
        if b_i in alphabet:
            result.append(b_i)
    return ''.join(result)

def symbol_to_num(symbol):
    """Преобразование символа в код (0-31)"""
    return alphabet.index(symbol)

def num_to_symbol(num):
    """Преобразование кода (0-31) в символ"""
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
    """Сохранение данных в файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(data)

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
            text = input("Введите текст для шифрования: ")
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
            
            print("\nРезультат:")
            print(result)
            
            save_to_file('encryption_result.txt', result)
            print("Результат сохранен в файл 'encryption_result.txt'")
            
        elif choice == '2':
            # Расшифрование
            text = input("Введите текст для расшифрования: ")
            try:
                key = int(input("Введите ключ (1-31): "))
                if not 1 <= key <= 31:
                    print("Ключ должен быть в диапазоне 1-31!")
                    continue
            except ValueError:
                print("Ключ должен быть числом!")
                continue
            
            decrypted_text = decrypt(text, key)
            
            result = f"Зашифрованный текст: {text}\n"
            result += f"Ключ: {key}\n"
            result += f"Расшифрованный текст: {decrypted_text}\n"
            
            print("\nРезультат:")
            print(result)
            
            save_to_file('decryption_result.txt', result)
            print("Результат сохранен в файл 'decryption_result.txt'")
            
        elif choice == '3':
            ciphertext_variant_14 = "чпмечпыхкоэвкщшзькщшсшъкцпхшбчеяшлтомшыыькхшчщъшьтмцчпчтуымпькшотчфкфщъпроптэлть"
            
            results = brute_force(ciphertext_variant_14)
            
            with open('brute_force_results.txt', 'w', encoding='utf-8') as f:
                for key, decrypted in results:
                    f.write(f"Ключ {key}: {decrypted}\n")
            
            print("Все варианты расшифровки сохранены в файл 'brute_force_results.txt'")

            key, text = results[9]
            author_work = "лермонтовсмертьпоэта"
            encrypted_author_work = encrypt(author_work, 10)

            print("Ответ на задание 3, вариант 14:")
            print(f"ШИФР-ТЕКСТ: {ciphertext_variant_14}")
            print(f"РАСШИФРОВАННЫЙ ТЕКСТ: {text}")
            print(f"КЛЮЧ: {key}")
            print(f"АВТОР И ПРОИЗВЕДЕНИЕ: {author_work}")
            print(f"ЗАШИФРОВАННЫЕ ФАМИЛИЯ И НАЗВАНИЕ: {encrypted_author_work}")

        elif choice == '4':
            print("Выход из программы.")
            break
            
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()