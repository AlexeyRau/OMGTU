def push(stack, value):
    cur_min = min(value, stack[-1][1]) if stack else value
    stack.append((value, cur_min))

def transfer(tail, head):
    while tail:
        push(head, tail.pop()[0])

def sliding_window_minimum(A, K):
    n = len(A)
    tail, head = [], []
    result = []

    for i in range(K):
        push(tail, A[i])
    result.append(tail[-1][1])

    for i in range(K, n):
        push(tail, A[i])

        if not head:
            transfer(tail, head)

        head.pop()

        min_head = head[-1][1] if head else float('inf')
        min_tail = tail[-1][1] if tail else float('inf')
        result.append(min(min_head, min_tail))

    return result


A = [11, 18, 14, 3, 5, 17, 4, 15, 6, 17, 25, 3, 14, 1, 5, 47, 6, 13, 20, 23, 6, 13]
K = 7

ans = sliding_window_minimum(A, K)

print(f"A = {A}")
print(f"K = {K}\n")
print(f"Ответ: {ans}")