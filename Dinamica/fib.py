import time
from memory_profiler import memory_usage
# import sys

# sys.setrecursionlimit(100000)


def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


if __name__ == "__main__":
    nondp = []
    for exp in range(5):
        for k in range(1, 10):
            n = int(k * 10 ** exp)
            if n > 40:
                break
            start = time.perf_counter()
            mem = memory_usage((fib, (n,)))
            end = time.perf_counter()
            duration = end - start
            print(n, mem[-1], duration)
            nondp.append((n, mem[-1], duration))
    print(nondp)

