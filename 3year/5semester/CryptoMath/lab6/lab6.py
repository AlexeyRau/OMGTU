import math

def integer_sqrt(m):
    """Алгоритм вычисления целочисленного квадратного корня"""
    if m <= 0:
        return 0
    x = m
    while True:
        y = (x + m // x) // 2
        if y >= x:
            return x
        x = y

def is_perfect_square(n):
    """Проверка, является ли число полным квадратом"""
    if n < 0:
        return False
    root = integer_sqrt(n)
    return root * root == n

def sieve_quadratic_residues(modulus):
    """Строит квадратичное решето для заданного модуля"""
    sieve = [False] * modulus
    for x in range(modulus):
        residue = (x * x) % modulus
        sieve[residue] = True
    return sieve

def quadratic_sieve(m, a, b, c):
    """Метод квадратичного решета для факторизации числа m"""
    print(f"\n[Квадратичное решето для m = {m}]")
    print(f"Модули решет: a={a}, b={b}, c={c}")
    
    sieve_a = sieve_quadratic_residues(a)
    sieve_b = sieve_quadratic_residues(b)
    sieve_c = sieve_quadratic_residues(c)
    
    print(f"\nКвадратичные вычеты по модулю {a}: {[i for i, val in enumerate(sieve_a) if val]}")
    print(f"Квадратичные вычеты по модулю {b}: {[i for i, val in enumerate(sieve_b) if val]}")
    print(f"Квадратичные вычеты по модулю {c}: {[i for i, val in enumerate(sieve_c) if val]}")
    
    start_x = math.isqrt(m) + 1
    end_x = (m + 1) // 2
    print(f"\nИнтервал поиска x: от {start_x} до {end_x}")
    
    start_a = start_x % a
    start_b = start_x % b
    start_c = start_x % c
    
    print(f"Начальные позиции в решетах: S_{a}({start_a}), S_{b}({start_b}), S_{c}({start_c})")
    
    for x in range(start_x, min(start_x + 100, end_x + 1)):
        z_mod_a = (x * x - m) % a
        z_mod_b = (x * x - m) % b
        z_mod_c = (x * x - m) % c
        
        if not sieve_a[z_mod_a] or not sieve_b[z_mod_b] or not sieve_c[z_mod_c]:
            continue
        
        Z = x * x - m
        if Z <= 0:
            continue
        
        if is_perfect_square(Z):
            y = integer_sqrt(Z)
            print(f"\nНайдено подходящее x = {x}")
            print(f"  Z = x² - m = {x}² - {m} = {Z}")
            print(f"  y = √{Z} = {y}")
            
            p = x + y
            q = x - y
            
            if p * q == m:
                return p, q, x, y
            else:
                print(f"  Проверка не пройдена: {p} * {q} = {p*q} != {m}")
    
    return None, None, None, None

def rho_method(m, x0=2):
    """ρ-метод факторизации (Полларда)"""
    print(f"\n[ρ-метод для m = {m}]")
    print(f"Начальное значение x0 = {x0}")
    print(f"Циклическая функция: f(x) = (x² + 1) mod m")
    
    def f(x):
        return (x * x + 1) % m
    
    x1 = x0
    x2 = x0
    step = 0
    
    print("\nШаг | x₁       | x₂       | a = |x₁ - x₂| | НОД(a, m)")
    print("-" * 55)
    
    while True:
        step += 1
        
        x1 = f(x1)
        x2 = f(f(x2))
        
        a = abs(x1 - x2)
        d = math.gcd(a, m)
        
        print(f"{step:4d} | {x1:8d} | {x2:8d} | {a:11d} | {d:8d}")
        
        if 1 < d < m:
            p = d
            q = m // d
            return p, q, step
        
        if step > 10000:
            print("Превышено максимальное количество шагов (10000)")
            return None, None, step


def main():
    print("="*60)
    print("ЛАБОРАТОРНАЯ РАБОТА №6: МЕТОДЫ ФАКТОРИЗАЦИИ ЧИСЛА")
    print("="*60)
    
    try:
        m = int(input("Введите число m для факторизации: "))
        if m <= 1:
            print("Ошибка: m должно быть больше 1.")
            return
    except ValueError:
        print("Ошибка: введите целое число.")
        return
    
    print(f"\nЧисло для факторизации: m = {m}")
    
    while True:
        print("\n" + "="*60)
        print("ВЫБЕРИТЕ МЕТОД ФАКТОРИЗАЦИИ:")
        print("1. Метод квадратичного решета")
        print("2. ρ-метод (Полларда)")
        print("3. Выход")
        print("="*60)
        
        choice = input("Ваш выбор (1-3): ").strip()
        
        if choice == '1':
            print("\n[МЕТОД КВАДРАТИЧНОГО РЕШЕТА]")
            print("Введите три модуля для решет (обычно небольшие простые числа)")
            
            try:
                a = int(input("Модуль a: "))
                b = int(input("Модуль b: "))
                c = int(input("Модуль c: "))
                
                if a <= 0 or b <= 0 or c <= 0:
                    print("Ошибка: модули должны быть положительными.")
                    continue
                
                p, q, x, y = quadratic_sieve(m, a, b, c)
                
                if p and q:
                    print(f"\n[РЕЗУЛЬТАТ]")
                    print(f"Найденные делители:")
                    print(f"  p = x + y = {x} + {y} = {p}")
                    print(f"  q = x - y = {x} - {y} = {q}")
                    print(f"Проверка: {p} × {q} = {p * q}")
                    print(f"Исходное число: {m}")
                    
                    if p * q == m:
                        print("✓ Факторизация выполнена успешно!")
                    else:
                        print("✗ Ошибка в вычислениях!")
                else:
                    print("Не удалось найти делители методом квадратичного решета.")
                    print("Попробуйте другие модули или увеличьте диапазон поиска.")
                    
            except ValueError:
                print("Ошибка: введите целые числа.")
                
        elif choice == '2':
            print("\n[ρ-МЕТОД (ПОЛЛАРДА)]")
            
            try:
                x0_input = input("Введите начальное значение x0 (по умолчанию 2): ").strip()
                x0 = int(x0_input) if x0_input else 2
                
                p, q, steps = rho_method(m, x0)
                
                if p and q:
                    print(f"\n[РЕЗУЛЬТАТ]")
                    print(f"Делитель найден на шаге {steps}:")
                    print(f"  p = {p}")
                    print(f"  q = m / p = {m} / {p} = {q}")
                    print(f"Проверка: {p} × {q} = {p * q}")
                    print(f"Исходное число: {m}")
                    
                    if p * q == m:
                        print("✓ Факторизация выполнена успешно!")
                    else:
                        print("✗ Ошибка в вычислениях!")
                else:
                    print("Не удалось найти делитель ρ-методом.")
                    print("Попробуйте другое начальное значение.")
                    
            except ValueError:
                print("Ошибка: введите целое число.")
                
        elif choice == '3':
            print("Выход из программы.")
            break
            
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()