def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)

array = [7, 86, 1, 15, 65, 2, 21, 30, 1]
sorted_arr = quick_sort(array)
print("Arreglo ordenado:", sorted_arr)