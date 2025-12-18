import math

def extended_gcd(a, b):
    """Расширенный алгоритм Евклида."""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(e, phi):
    """Нахождение обратного элемента d: (e * d) mod phi = 1."""
    gcd, x, y = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("Обратный элемент не существует")
    return x % phi

def factorize_n(n):
    """Факторизация n методом пробного деления."""
    if n < 2:
        return None, None
    
    # Проверяем делимость на 2
    if n % 2 == 0:
        return 2, n // 2
    
    # Перебираем нечетные числа от 3 до √n
    limit = int(math.isqrt(n)) + 1
    for p in range(3, limit, 2):
        if n % p == 0:
            q = n // p
            return p, q
    
    return None, None  # n простое или не факторизуется

def decrypt_rsa(C, d, n):
    """Расшифрование сообщения RSA."""
    return pow(C, d, n)

def main():
    print("="*60)
    print("ЛАБОРАТОРНАЯ РАБОТА №5: КРИПТОАНАЛИЗ ШИФРА RSA")
    print("="*60)
    
    while True:
        try:
            print("\n" + "="*40)
            print("ВВЕДИТЕ ПАРАМЕТРЫ RSA:")
            print("="*40)
            
            e = int(input("Введите открытую экспоненту e: "))
            n = int(input("Введите модуль n: "))
            C = int(input("Введите зашифрованное число C: "))
            
            print("\n[1] ФАКТОРИЗАЦИЯ МОДУЛЯ n...")
            p, q = factorize_n(n)
            
            if p is None or q is None:
                print(f"Не удалось факторизовать n = {n} методом пробного деления")
                print("Возможно, n слишком большое или простое")
                continue
            
            print(f"Найдены множители:")
            print(f"  p = {p}")
            print(f"  q = {q}")
            print(f"  Проверка: p * q = {p} * {q} = {p*q} {'=' if p*q == n else '≠'} {n}")
            
            print("\n[2] ВЫЧИСЛЕНИЕ ЗАКРЫТОГО КЛЮЧА...")
            phi = (p - 1) * (q - 1)
            print(f"  φ(n) = (p-1)*(q-1) = ({p}-1)*({q}-1) = {phi}")
            
            d = mod_inverse(e, phi)
            print(f"  Находим d = e⁻¹ mod φ(n)")
            print(f"  d = {e}⁻¹ mod {phi} = {d}")
            print(f"  Проверка: e * d mod φ(n) = {e} * {d} mod {phi} = {(e * d) % phi}")
            
            print("\n[3] РАСШИФРОВАНИЕ СООБЩЕНИЯ...")
            print(f"  Исходное зашифрованное число: C = {C}")
            
            M = decrypt_rsa(C, d, n)
            print(f"  Расшифрованное число: M = C^d mod n")
            print(f"  M = {C}^{d} mod {n} = {M}")
            
            print("\n" + "="*60)
            print("РЕЗУЛЬТАТЫ:")
            print("="*60)
            print(f"Открытый ключ: (e, n) = ({e}, {n})")
            print(f"Закрытый ключ: (d, n) = ({d}, {n})")
            print(f"Множители: p = {p}, q = {q}")
            print(f"Функция Эйлера: φ(n) = {phi}")
            print(f"Зашифрованное сообщение: C = {C}")
            print(f"Расшифрованное сообщение: M = {M}")
            print("="*60)
            
            # Дополнительно: если M может быть текстом
            try:
                # Попытка интерпретировать M как ASCII
                if 32 <= M <= 126:
                    print(f"ASCII символ: '{chr(M)}'")
                
                # Попытка разбить на двузначные числа для русского текста (как в ЛР4)
                temp = M
                blocks = []
                while temp > 0:
                    blocks.append(temp % 100)
                    temp //= 100
                blocks.reverse()
                
                if len(blocks) > 0 and all(10 <= b <= 41 or b == 99 for b in blocks):
                    print(f"Возможные числовые блоки (для русского текста): {blocks}")
                    
            except:
                pass
            
        except ValueError as ve:
            print(f"Ошибка: {ve}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        
        print("\n" + "="*40)
        choice = input("Продолжить работу? (y/n): ").strip().lower()
        if choice != 'y':
            print("Программа завершена.")
            break

if __name__ == "__main__":
    main()