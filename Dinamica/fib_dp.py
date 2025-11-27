import time
from memory_profiler import memory_usage
import sys

sys.setrecursionlimit(10000000)
# sys.set_int_max_str_digits(1000000)


def fib_dp_util(n, memo):
    if n <= 1:
        return n
    if memo[n] != -1:
        return memo[n]

    memo[n] = fib_dp_util(n - 1, memo) + fib_dp_util(n - 2, memo)
    return memo[n]


def fib_dp(n):
    memo = [-1] * (n + 1)
    return fib_dp_util(n, memo)


if __name__ == "__main__":
    dp = []
    for exp in range(5):
        for k in range(1, 10):
            n = int(k * 10 ** exp)
            start = time.perf_counter()
            mem = memory_usage((fib_dp, (n,)))
            end = time.perf_counter()
            duration = end - start
            print(n, mem[-1], duration)
            dp.append((n, mem[-1], duration))
    print(dp)
