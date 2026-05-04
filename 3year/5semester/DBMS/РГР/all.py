import re
from pathlib import Path

def natural_sort_key(filename):
    """
    Разбивает полное имя файла на части для сортировки.
    Числа (31.1, 32) сравниваются как числа, остальное как текст.
    """
    parts = re.split(r'(\d+\.\d+|\d+)', filename)
    key = []
    for p in parts:
        if not p:
            continue
        # Если часть похожа на число (целое или с одной точкой)
        if re.match(r'^\d+(\.\d+)?$', p):
            key.append((0, float(p)))
        else:
            key.append((1, p.lower()))
    return key

def merge_files():
    output_name = "0. Все запросы"
    current_dir = Path('.')
    
    # Собираем файлы, игнорируя результат и сам скрипт
    # Используем f.name, так как расширений нет
    files = [
        f for f in current_dir.iterdir() 
        if f.is_file() and f.name not in [output_name, "all.py", "merge.py"]
    ]

    # Сортируем по полному имени файла
    files.sort(key=lambda x: natural_sort_key(x.name))

    all_blocks = []

    for file_path in files:
        try:
            content = file_path.read_text(encoding='utf-8').strip()
            
            if content:
                # ВАЖНО: берем name целиком, так как точек в названии много, а расширения нет
                header = file_path.name 
                
                # Формируем блок: Имя файла + 2 переноса + Контент
                block = f"{header}\n\n{content}"
                all_blocks.append(block)
                print(f"Добавлен: {header}")
        except Exception as e:
            print(f"Ошибка в файле {file_path.name}: {e}")

    # Записываем всё в итоговый файл
    with open(output_name, 'w', encoding='utf-8') as out_f:
        out_f.write("\n\n".join(all_blocks))

    print(f"\nУспех! Проверь файл: {output_name}")

if __name__ == "__main__":
    merge_files()