def nearest_min_left(a):
    n = len(a)
    ans = [-1] * n
    stack = []

    for i in range(n):
        while stack and a[stack[-1]] >= a[i]:
            stack.pop()

        if stack:
            ans[i] = stack[-1]
        
        stack.append(i)

    return ans


def main():
    a = [14, 3, 21, 23, 5, 87, 9, 61, 3, 45, 10, 1]
    n = len(a)

    print("Исходный массив:")
    print(f"  индекс: {list(range(n))}")
    print(f"  a     : {a}")
    print()

    ans = nearest_min_left(a)

    print(f"{'i':>4} | {'a[i]':>6} | {'индекс':>8} | {'значение':>10}")
    print("-" * 36)
    for i in range(n):
        if ans[i] == -1:
            print(f"{i:>4} | {a[i]:>6} | {'—':>8} | {'нет':>10}")
        else:
            print(f"{i:>4} | {a[i]:>6} | {ans[i]:>8} | {a[ans[i]]:>10}")

if __name__ == "__main__":
    main()
