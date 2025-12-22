import math

# ====================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ======================

def integer_sqrt(n):
    """Алгоритм вычисления целочисленного квадратного корня"""
    if n <= 0:
        return 0
    x = n
    while True:
        y = (x + n // x) // 2
        if y >= x:
            return x
        x = y

def bin_pow(a, k, n):
    """Бинарное возведение в степень по модулю"""
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

def baby_step_giant_step(a, b, p):
    """
    Алгоритм "шаг младенца - шаг великана" для решения a^x ≡ b (mod p)
    """
    print(f"\n[Решение уравнения: {a}^x ≡ {b} (mod {p})]")
    
    # 1. Вычисляем k
    k = integer_sqrt(p) + 1
    print(f"1. Вычисляем k = ⌊√{p}⌋ + 1 = {k}")
    
    # 2. Строим последовательности
    print(f"\n2. Строим последовательности длиной k = {k}:")
    print(f"   y_n = {a}^(n*{k}) mod {p}")
    print(f"   z_n = {b} * {a}^n mod {p}")
    
    # Вычисляем a^k mod p
    a_pow_k = bin_pow(a, k, p)
    
    # Последовательности
    y_sequence = []
    z_sequence = []
    
    # Словарь для быстрого поиска z_n
    z_dict = {}
    
    current_y = 1
    current_z = b % p
    
    for n in range(1, k + 1):
        # Вычисляем y_n
        current_y = (current_y * a_pow_k) % p
        y_sequence.append(current_y)
        
        # Вычисляем z_n
        if n == 1:
            current_z = (b * a) % p
        else:
            current_z = (current_z * a) % p
        z_sequence.append(current_z)
        
        # Сохраняем в словарь
        z_dict[current_z] = n
    
    # 3. Ищем совпадение
    print(f"\n3. Ищем совпадение y_i = z_j:")
    
    for i in range(k):
        y_value = y_sequence[i]
        if y_value in z_dict:
            j = z_dict[y_value]
            print(f"   Найдено: y_{i+1} = z_{j} = {y_value}")
            
            # 4. Вычисляем x
            x = (i + 1) * k - j
            print(f"\n4. Вычисляем x = i*k - j = {i+1}*{k} - {j} = {x}")
            
            # Проверка
            check = bin_pow(a, x, p)
            print(f"\n5. Проверка: {a}^{x} mod {p} = {check}")
            
            if check == b % p:
                print(f"   {check} = {b} mod {p} ✓")
                return x
            else:
                print(f"   Ошибка: {check} ≠ {b}")
                return None
    
    print("   Совпадений не найдено")
    return None

# ====================== ОСНОВНАЯ ПРОГРАММА ======================

def main():
    print("="*50)
    print("Лабораторная работа №7")
    print("ВЫЧИСЛЕНИЕ ДИСКРЕТНОГО ЛОГАРИФМА")
    print("Метод 'шаг младенца - шаг великана'")
    print("="*50)
    
    # Ввод параметров
    print("\nВведите параметры уравнения a^x ≡ b (mod p):")
    
    try:
        a = int(input("a = "))
        b = int(input("b = "))
        p = int(input("p = "))
        
        if p <= 1:
            print("Ошибка: p должно быть > 1")
            return
        
        # Решение уравнения
        print("\n" + "="*50)
        x = baby_step_giant_step(a, b, p)
        
        if x is not None:
            print("\n" + "="*50)
            print(f"Результат: x = {x}")
            print(f"Проверка: {a}^{x} ≡ {b} (mod {p})")
        else:
            print("\nРешение не найдено")
            
    except ValueError:
        print("Ошибка: введите целые числа")

if __name__ == "__main__":
    main()