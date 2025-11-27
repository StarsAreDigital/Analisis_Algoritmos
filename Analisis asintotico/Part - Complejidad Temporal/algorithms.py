import numpy


def generate(list_size: int):
    arr = numpy.random.randint(1, list_size + 1, list_size)
    return arr


def return_sorted(arr):
    return numpy.sort(arr)


def linear_search(target: int, arr):
    for i, num in enumerate(arr):
        if num == target:
            return i
    return -1


def binary_search(target: int, arr):
    L = 0
    R = arr.size - 1
    while L <= R:
        m = L + (R - L) // 2
        if arr[m] < target:
            L = m + 1
        elif arr[m] > target:
            R = m - 1
        else:
            return m
    return -1
