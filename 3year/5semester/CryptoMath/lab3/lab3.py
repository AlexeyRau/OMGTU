import tkinter as tk
from tkinter import filedialog
import math
import matplotlib.pyplot as plt

def get_text_input():
    print("\n" + "=" * 50)
    print("Выберите способ ввода текста:")
    print("1. Ввод с консоли")
    print("2. Чтение из файла")
    
    choice = input("\nВаш выбор (1-2): ").strip()
    
    if choice == '1':
        print("\n" + "=" * 50)
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

def clean_text(text):
    russian_letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    cleaned = []
    for ch in text.lower():
        if ch in russian_letters:
            cleaned.append(ch)
    return ''.join(cleaned)

def get_kgrams(text, k):
    kgrams = {}
    total = 0
    for i in range(len(text) - k + 1):
        kgram = text[i:i+k]
        kgrams[kgram] = kgrams.get(kgram, 0) + 1
        total += 1
    for key in kgrams:
        kgrams[key] = kgrams[key] / total
    return kgrams

def calculate_entropy(kgrams):
    entropy = 0.0
    for freq in kgrams.values():
        if freq > 0:
            entropy -= freq * math.log2(freq)
    return entropy

def analyze_text(text):
    cleaned = clean_text(text)
    if len(cleaned) < 5:
        print("Текст слишком короткий после очистки!")
        return None
    
    print(f"Текст после очистки: {len(cleaned)} символов")
    if len(cleaned) < 100:
        print(f"Первые 100 символов: {cleaned[:100]}...")
    
    results = []
    for k in range(1, 6):
        kgrams = get_kgrams(cleaned, k)
        Hk = calculate_entropy(kgrams)
        Hk_per_k = Hk / k
        results.append({
            'k': k,
            'Hk': Hk,
            'Hk_per_k': Hk_per_k,
            'unique_kgrams': len(kgrams)
        })
        print(f"k={k}: Hk = {Hk:.4f}, Hk/k = {Hk_per_k:.4f}, уникальных k-грамм: {len(kgrams)}")
    
    return results, cleaned

def plot_results(results):
    k_values = [r['k'] for r in results]
    Hk_per_k_values = [r['Hk_per_k'] for r in results]
    
    plt.figure(figsize=(8, 5))
    plt.plot(k_values, Hk_per_k_values, 'bo-', linewidth=2, markersize=8)
    plt.xlabel('k (длина k-граммы)', fontsize=12)
    plt.ylabel('Hk(T) / k', fontsize=12)
    plt.title('Зависимость Hk(T)/k от k', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.xticks(k_values)
    plt.tight_layout()
    
    print("\nГрафик будет отображен в отдельном окне.")
    print("Закройте окно с графиком, чтобы продолжить работу программы.")
    plt.show()

def print_results(results, cleaned_text):
    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТЫ АНАЛИЗА")
    print("=" * 60)
    print(f"Длина очищенного текста: {len(cleaned_text)} символов")
    print("\nТаблица результатов:")
    print("-" * 60)
    print("k\tHk(T)\t\tHk(T)/k\t\tУникальных k-грамм")
    print("-" * 60)
    
    for r in results:
        print(f"{r['k']}\t{r['Hk']:.4f}\t\t{r['Hk_per_k']:.4f}\t\t{r['unique_kgrams']}")

def main():
    print("=" * 60)
    print("ЛАБОРАТОРНАЯ РАБОТА №3: МОДЕЛЬ ОТКРЫТОГО ТЕКСТА")
    print("=" * 60)
    
    while True:
        text = get_text_input()
        
        if text is None:
            print("Текст не получен. Попробуйте еще раз.")
            continue
        
        if len(text.strip()) == 0:
            print("Текст пустой. Попробуйте еще раз.")
            continue
        
        analysis_result = analyze_text(text)
        if analysis_result is None:
            continue
        
        results, cleaned_text = analysis_result
        
        print_results(results, cleaned_text)
        
        try:
            plot_results(results)
        except Exception as e:
            print(f"Ошибка при построении графика: {e}")
        
        print("\n" + "=" * 60)
        choice = input("Хотите проанализировать другой текст? (y/n): ").strip().lower()
        if choice not in 'y':
            break
    
    print("\nПрограмма завершена.")

if __name__ == "__main__":
    main()