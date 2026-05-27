def hindenburg(n):
    result = []

    def generate(sum_left, parts_left, min_value, current):
        if parts_left == 0:
            if sum_left == 0:
                partition = [x for x in current if x != 0]
                result.append(partition)
            return

        for value in range(min_value, sum_left + 1):
            if sum_left - value < value * (parts_left - 1):
                break

            generate(sum_left - value, parts_left - 1, value, current + [value])

    generate(n, n, 0, [])
    return result


n = 10
partitions = hindenburg(n)

print(f'Число: {n}')
print(f'Количество разбиений: {len(partitions)}')

for i, partition in enumerate(partitions, start=1):
    text = ' + '.join(map(str, partition))
    print(f'{i}) {text}')