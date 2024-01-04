import os
import timeit
from typing import Callable


def read_file(filename):
    project_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(project_dir, filename)
    with open(full_path, "r", encoding="utf-8", errors="ignore") as file:
        return file.read()


def measure_time(algorithm: Callable, text: str, pattern: str):
    setup = f"from __main__ import {algorithm}, read_file; text = read_file('{text}'); pattern = '{pattern}'"
    stmt = f"{algorithm}(text, pattern)"

    time_taken = timeit.timeit(stmt, setup, number=1)
    return time_taken


# Knuth-Morris-Pratt search
def knuth_morris_pratt_search(main_string, pattern):
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


# Boyer-Moore search
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


# Rabin-Karp search
def polynomial_hash(s, base=256, modulus=101):
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value


def rabin_karp_search(main_string, substring):
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


text_file_1 = "article_1.txt"
text_file_2 = "article_2.txt"
real_pattern_1 = "Жадібний алгоритм у цьому випадку полягає в тому, щоб на кожному кроці побудови рішення використовувати монети максимального номіналу,"
real_pattern_2 = "ті блоки, де шуканий елемент належить до інтервалу, утвореного найменшим та найбільшим елементами блоку."
fake_pattern = "Dura lex sed lex"

time_kmp_1 = measure_time("knuth_morris_pratt_search", text_file_1, real_pattern_1)
time_boyer_moore_1 = measure_time("boyer_moore_search", text_file_1, real_pattern_1)
time_rabin_karp_1 = measure_time("rabin_karp_search", text_file_1, real_pattern_1)

dict_real_1 = {
    time_kmp_1: "Knuth-Morris-Pratt",
    time_boyer_moore_1: "Boyer-Moore",
    time_rabin_karp_1: "Rabin-Karp",
}

print()
print(f"Час виконання алгоритмів для існуючого підрядка в {text_file_1}:")
for key, value in dict_real_1.items():
    print(f"{value}: {key}")

time_fake_kmp_1 = measure_time("knuth_morris_pratt_search", text_file_1, fake_pattern)
time_fake_boyer_moore_1 = measure_time("boyer_moore_search", text_file_1, fake_pattern)
time_fake_rabin_karp_1 = measure_time("rabin_karp_search", text_file_1, fake_pattern)

dict_fake_1 = {
    time_fake_kmp_1: "Knuth-Morris-Pratt",
    time_fake_boyer_moore_1: "Boyer-Moore",
    time_fake_rabin_karp_1: "Rabin-Karp",
}

print()
print(f"Час виконання алгоритмів для вигаданого підрядка в {text_file_1}:")
for key, value in dict_fake_1.items():
    print(f"{value}: {key}")

fastest_algorithm_real_1 = min(time_kmp_1, time_boyer_moore_1, time_rabin_karp_1)
fastest_algorithm_fake_1 = min(
    time_fake_kmp_1, time_fake_boyer_moore_1, time_fake_rabin_karp_1
)

dict_best_time = {
    fastest_algorithm_real_1: dict_real_1[fastest_algorithm_real_1]
    + f" (real, {text_file_1})",
    fastest_algorithm_fake_1: dict_fake_1[fastest_algorithm_fake_1]
    + f" (fake, {text_file_1})",
}

print()
print(
    f"Найшвидший алгоритм для існуючого підрядка в {text_file_1}: {dict_real_1[fastest_algorithm_real_1]}: {fastest_algorithm_real_1}"
)
print(
    f"Найшвидший алгоритм для для вигаданого підрядка в {text_file_1}: {dict_fake_1[fastest_algorithm_fake_1]}: {fastest_algorithm_fake_1}"
)

time_kmp_2 = measure_time("knuth_morris_pratt_search", text_file_2, real_pattern_2)
time_boyer_moore_2 = measure_time("boyer_moore_search", text_file_2, real_pattern_2)
time_rabin_karp_2 = measure_time("rabin_karp_search", text_file_2, real_pattern_2)

dict_real_2 = {
    time_kmp_2: "Knuth-Morris-Pratt",
    time_boyer_moore_2: "Boyer-Moore",
    time_rabin_karp_2: "Rabin-Karp",
}

print()
print(f"Час виконання алгоритмів для існуючого підрядка в {text_file_2}:")
for key, value in dict_real_2.items():
    print(f"{value}: {key}")

time_fake_kmp_2 = measure_time("knuth_morris_pratt_search", text_file_2, fake_pattern)
time_fake_boyer_moore_2 = measure_time("boyer_moore_search", text_file_2, fake_pattern)
time_fake_rabin_karp_2 = measure_time("rabin_karp_search", text_file_2, fake_pattern)

dict_fake_2 = {
    time_fake_kmp_2: "Knuth-Morris-Pratt",
    time_fake_boyer_moore_2: "Boyer-Moore",
    time_fake_rabin_karp_2: "Rabin-Karp",
}

print()
print(f"Час виконання алгоритмів для вигаданого підрядка в {text_file_2}:")
for key, value in dict_fake_2.items():
    print(f"{value}: {key}")

fastest_algorithm_real_2 = min(time_kmp_2, time_boyer_moore_2, time_rabin_karp_2)
fastest_algorithm_fake_2 = min(
    time_fake_kmp_2, time_fake_boyer_moore_2, time_fake_rabin_karp_2
)

dict_best_time[fastest_algorithm_real_2] = (
    dict_real_2[fastest_algorithm_real_2] + f" (real, {text_file_2})"
)
dict_best_time[fastest_algorithm_fake_2] = (
    dict_fake_2[fastest_algorithm_fake_2] + f" (fake, {text_file_2})"
)

print()
print(
    f"Найшвидший алгоритм для існуючого підрядка в {text_file_2}: {dict_real_2[fastest_algorithm_real_2]}: {fastest_algorithm_real_2}"
)
print(
    f"Найшвидший алгоритм для для вигаданого підрядка в {text_file_2}: {dict_fake_2[fastest_algorithm_fake_2]}: {fastest_algorithm_fake_2}"
)

min_value_key = min(dict_best_time, key=lambda k: dict_best_time[k])
min_value = dict_best_time[min_value_key]

print()
print(
    f"Найшвидший алгоритм серед усіх замірів виявився алгоритм {min_value}: {min_value_key}"
)
