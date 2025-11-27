def heap_insert(heap: list, value):
    heap.append(value)
    index = len(heap) - 1

    while index > 0 and heap[(index - 1) // 2][0] > heap[index][0]:
        heap[(index - 1) // 2], heap[index] = heap[index], heap[(index - 1) // 2]
        index = (index - 1) // 2


def heapify(heap: list, i: int = 0):
    while i < len(heap):
        left = i * 2 + 1
        right = i * 2 + 2
        smallest = i

        if left < len(heap) and heap[left][0] < heap[smallest][0]:
            smallest = left
        if right < len(heap) and heap[right][0] < heap[smallest][0]:
            smallest = right

        if smallest == i:
            break
        heap[i], heap[smallest] = heap[smallest], heap[i]
        i = smallest


def heap_delete_min(heap: list):
    if not heap:
        return None
    size = len(heap)
    last = heap[size - 1]
    heap[0] = last

    heapify(heap, 0)

    heap.pop()


def heap_top(heap: list):
    if heap:
        return heap[0]
    return None
