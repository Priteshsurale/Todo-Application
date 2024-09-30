import random

def radixsort(arr):
    RADIX = 10
    placement = 1
 
    max_digit = max(arr)
 
    while placement < max_digit:
        buckets = [list() for _ in range(RADIX)]
        for i in arr:
            tmp = int((i / placement) % RADIX)
            buckets[tmp].append(i)
        a = 0
        for b in range(RADIX):
            buck = buckets[b]
            for i in buck:
                arr[a] = i
                a += 1
        placement *= RADIX
    return arr

# Testing the function
arr = [170, 45, 75, 90, 802, 24, 2, 66]
print("Unsorted array is:", end=' ')
print(arr)
arr=radixsort(arr)
print("\nSorted array is:", end=' ')
print(arr)
