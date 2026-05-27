from heapq import heappop, heappush


def huffman_codes(frequencies):
    heap = []

    for symbol, freq in frequencies.items():
        heappush(heap, (freq, symbol, symbol))

    if len(heap) == 1:
        symbol = heap[0][1]
        return {symbol: '0'}

    steps = []

    while len(heap) > 1:
        freq1, name1, tree1 = heappop(heap)
        freq2, name2, tree2 = heappop(heap)

        new_freq = freq1 + freq2
        new_name = name1 + name2
        new_tree = (tree1, tree2)

        steps.append((name1, freq1, name2, freq2, new_name, new_freq))
        heappush(heap, (new_freq, new_name, new_tree))

    codes = {}

    def bypass(node, code):
        if isinstance(node, str):
            codes[node] = code
            return

        left, right = node
        bypass(left, code + '0')
        bypass(right, code + '1')

    bypass(heap[0][2], '')
    return codes, steps

frequencies = {
    'a': 5,
    'b': 9,
    'c': 12,
    'd': 13,
    'e': 16,
    'f': 45,
}

print('Символы и частоты:')
for symbol, freq in frequencies.items():
    print(symbol, '-', freq)