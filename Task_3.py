import timeit
from typing import Callable


def read_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def measure_time(algorithm: Callable, text: str, pattern: str):
    setup = f"from __main__ import {algorithm}, read_file; text = read_file('{text}'); pattern = '{pattern}'"
    stmt = f"{algorithm}(text, pattern)"

    time_taken = timeit.timeit(stmt, setup, number=1000)
    return time_taken


# Knuth Morris Pratt search
def lps_search(text, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1


def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


# Boyer Moore search
def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table


def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0

    while i <= len(text) - len(pattern):
        j = len(pattern) - 1

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:
            return i

        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    return -1


# Rabin Karp search
def polynomial_hash(s, base=256, modulus=101):
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value


def rabin_karp_search(text, pattern):
    substring_length = len(substring)
    main_string_length = len(main_string)

    base = 256
    modulus = 101

    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)

    h_multiplier = pow(base, substring_length - 1) % modulus

    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i : i + substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (
                current_slice_hash - ord(main_string[i]) * h_multiplier
            ) % modulus
            current_slice_hash = (
                current_slice_hash * base + ord(main_string[i + substring_length])
            ) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1


# Зазначте файли та підрядки для пошуку
text_file1 = "article1.txt"
text_file2 = "article2.txt"
real_pattern = "your_real_substring_here"
fake_pattern = "your_fake_substring_here"

# Вимір часу для реального підрядка в обох текстових файлах
time_brute_force1 = measure_time("brute_force_search", text_file1, real_pattern)
time_kmp1 = measure_time("knuth_morris_pratt_search", text_file1, real_pattern)
time_boyer_moore1 = measure_time("boyer_moore_search", text_file1, real_pattern)
time_rabin_karp1 = measure_time("rabin_karp_search", text_file1, real_pattern)

time_brute_force2 = measure_time("brute_force_search", text_file2, real_pattern)
time_kmp2 = measure_time("knuth_morris_pratt_search", text_file2, real_pattern)
time_boyer_moore2 = measure_time("boyer_moore_search", text_file2, real_pattern)
time_rabin_karp2 = measure_time("rabin_karp_search", text_file2, real_pattern)

# Вимір часу для вигаданого підрядка в обох текстових файлах
time_fake_brute_force1 = measure_time("brute_force_search", text_file1, fake_pattern)
time_fake_kmp1 = measure_time("knuth_morris_pratt_search", text_file1, fake_pattern)
time_fake_boyer_moore1 = measure_time("boyer_moore_search", text_file1, fake_pattern)
time_fake_rabin_karp1 = measure_time("rabin_karp_search", text_file1, fake_pattern)

time_fake_brute_force2 = measure_time("brute_force_search", text_file2, fake_pattern)
time_fake_kmp2 = measure_time("knuth_morris_pratt_search", text_file2, fake_pattern)
time_fake_boyer_moore2 = measure_time("boyer_moore_search", text_file2, fake_pattern)
time_fake_rabin_karp2 = measure_time("rabin_karp_search", text_file2, fake_pattern)

# Виведення результатів
print("Час для реального підрядка в article1.txt:")
print("Brute Force:", time_brute_force1)
print("KMP:", time_kmp1)
print("Boyer-Moore:", time_boyer_moore1)
print("Rabin-Karp:", time_rabin_karp1)

# Визначення найшвидшого алгоритму
fastest_algorithm1 = min(
    time_brute_force1, time_kmp1, time_boyer_moore1, time_rabin_karp1
)
fastest_algorithm2 = min(
    time_brute_force2, time_kmp2, time_boyer_moore2, time_rabin_karp2
)

print("\nНайшвидший алгоритм для article1.txt:", fastest_algorithm1)
print("Найшвидший алгоритм для article2.txt:", fastest_algorithm2)
