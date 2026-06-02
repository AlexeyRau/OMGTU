import heapq
import time
from collections import Counter

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def count_frequencies(text: str) -> dict:
    return dict(Counter(text))

def build_huffman_tree(freq: dict) -> Node:
    heap = [Node(char, f) for char, f in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        parent = Node(None, left.freq + right.freq)
        parent.left = left
        parent.right = right 

        heapq.heappush(heap, parent)

    return heap[0]

def build_codes(node: Node, prefix: str = "", codes: dict = None) -> dict:
    if codes is None:
        codes = {}

    if node is None:
        return codes

    if node.char is not None:
        codes[node.char] = prefix if prefix else "0"
        return codes

    build_codes(node.left,  prefix + "0", codes)
    build_codes(node.right, prefix + "1", codes)
    return codes

def encode(text: str, codes: dict) -> str:
    return "".join(codes[ch] for ch in text)

def decode(encoded: str, root: Node) -> str:
    result = []
    current = root
    for bit in encoded:
        current = current.left if bit == "0" else current.right
        if current.char is not None:
            result.append(current.char)
            current = root
    return "".join(result)

def check_prefix_property(codes: dict) -> bool:
    code_list = sorted(codes.values())
    for i in range(len(code_list) - 1):
        if code_list[i + 1].startswith(code_list[i]):
            return False
    return True

def print_complexity():
    print("\n=== Оценка сложности алгоритма ===")
    print("  n — количество различных символов в тексте")
    print("  Подсчёт частот:          O(N), где N — длина текста")
    print("  Построение дерева:       O(n log n)  — n-1 операций над кучей")
    print("  Построение таблицы:      O(n)")
    print("  Кодирование текста:      O(N * L), L — средняя длина кода ≈ log n")
    print("  Декодирование текста:    O(M), M — длина закодированной строки")
    print("  Итого (доминирует):      O(N log n)")

def main():
    text = input("Введите текст для кодирования: ")
    if not text:
        text = "hello"

    print(f"\nИсходный текст: «{text}»")
    print(f"Длина текста: {len(text)} символов")

    start = time.perf_counter()

    freq = count_frequencies(text)
    print("\nЧастоты символов")
    for ch, f in sorted(freq.items(), key=lambda x: -x[1]):
        label = repr(ch)
        print(f"  {label:6s}: {f}")

    root = build_huffman_tree(freq)

    codes = build_codes(root)
    print("\nСловарь Хаффмана (условие Фано выполнено)")
    for ch, code in sorted(codes.items(), key=lambda x: len(x[1])):
        label = repr(ch)
        print(f"  {label:6s}: {code}")

    ok = check_prefix_property(codes)
    print(f"\nПрефиксное свойство (условие Фано): {'✓ выполнено' if ok else '✗ нарушено'}")

    encoded = encode(text, codes)
    print(f"\nКодирование")
    print(f"Закодированная строка ({len(encoded)} бит):")
    print(f"  {encoded}")

    decoded = decode(encoded, root)
    print(f"\nДекодирование")
    print(f"Восстановленный текст: «{decoded}»")
    print(f"Декодирование корректно: {'✓' if decoded == text else '✗'}")

    end = time.perf_counter()

    original_bits = len(text) * 8
    huffman_bits  = len(encoded)
    savings = (1 - huffman_bits / original_bits) * 100

    print(f"\n-Сравнение размеров")
    print(f"  Без сжатия (8 бит/символ): {original_bits} бит")
    print(f"  Код Хаффмана:              {huffman_bits} бит")
    print(f"  Экономия:                  {savings:.1f}%")

    print(f"\nВремя выполнения: {(end - start) * 1000:.4f} мс")

    print_complexity()


if __name__ == "__main__":
    main()