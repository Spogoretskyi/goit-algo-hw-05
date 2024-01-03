def binary_search(arr, target):
    iterations = 0
    low, high = 0, len(arr) - 1
    upper_bound = None

    while low <= high:
        mid = (low + high) // 2
        mid_value = arr[mid]
        iterations += 1

        if mid_value < target:
            low = mid + 1
        elif mid_value > target:
            upper_bound = mid_value
            high = mid - 1
        else:
            upper_bound = mid_value
            break

    return iterations, upper_bound

sorted_array = [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.12, 11.11, 12.02, 13.1, 14.9, 15.15, 16.16, 17.17, 18.18, 19.19, 20.2]
target_value = 19.11

iterations, upper_bound = binary_search(sorted_array, target_value)

if upper_bound is not None:
    print(f"Елемент {target_value} знайдено за {iterations} ітерацій. Верхня межа: {upper_bound}")
else:
    print(f"Елемент {target_value} не знайдено у масиві.")