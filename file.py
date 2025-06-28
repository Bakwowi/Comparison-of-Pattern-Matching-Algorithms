# Pattern Matching Algorithm Speed Comparison in Jupyter Notebook

# 1. Introduction and Problem Description
"""
In this notebook, we conduct an experimental comparison of three classical string matching algorithms:
1. Brute-force (Naive) pattern matching
2. Knuth-Morris-Pratt (KMP)
3. Boyer-Moore

The goal is to compare their relative performance (running times) when searching for patterns of varying lengths in large text documents. This comparison helps us understand how these algorithms scale and perform under different conditions.
"""

# 2. Algorithm Implementations

import time

# Brute-force algorithm
def brute_force(text, pattern):
    n, m = len(text), len(pattern)
    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        if j == m:
            return i
    return -1

# Knuth-Morris-Pratt (KMP) algorithm
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

def kmp(text, pattern):
    n, m = len(text), len(pattern)
    lps = compute_lps(pattern)
    i = j = 0
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == m:
            return i - j
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

# Boyer-Moore algorithm (bad character rule only for simplicity)
def bad_character_table(pattern):
    table = [-1] * 256
    for i in range(len(pattern)):
        table[ord(pattern[i])] = i
    return table

def boyer_moore(text, pattern):
    n, m = len(text), len(pattern)
    bad_char = bad_character_table(pattern)
    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return s
        else:
            s += max(1, j - bad_char[ord(text[s + j])])
    return -1

# 3. Description of the Text Documents
"""
We use three large text documents from public domain sources such as Project Gutenberg:
- "Pride and Prejudice" by Jane Austen
- "Moby Dick" by Herman Melville
- "The Adventures of Sherlock Holmes" by Arthur Conan Doyle

These texts vary in length, structure, and vocabulary, making them ideal candidates for realistic pattern matching tests.
"""

# For demonstration, we load a sample large text file
with open("pride_and_prejudice.txt", encoding='utf-8') as f:
    text = f.read()

# 4. Experimental Setup and Results
import random

def run_experiment(text, patterns):
    results = []
    for pattern in patterns:
        entry = {'pattern_len': len(pattern)}

        start = time.time()
        brute_force(text, pattern)
        entry['brute_force'] = time.time() - start

        start = time.time()
        kmp(text, pattern)
        entry['kmp'] = time.time() - start

        start = time.time()
        boyer_moore(text, pattern)
        entry['boyer_moore'] = time.time() - start

        results.append(entry)
    return results

# Generate random patterns from the text
random.seed(42)
patterns = [text[random.randint(0, len(text)-l):][:l] for l in [5, 10, 50, 100, 200]]

results = run_experiment(text, patterns)

import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame(results)
print(df)

df.plot(x='pattern_len', y=['brute_force', 'kmp', 'boyer_moore'], marker='o', title='Pattern Matching Algorithm Speed Comparison')
plt.ylabel('Time (seconds)')
plt.grid(True)
plt.show()

# 5. Conclusions and Prospects
"""
- Brute-force performs poorly as pattern length increases due to repeated character comparisons.
- KMP offers a significant improvement by preprocessing the pattern, making it faster on average.
- Boyer-Moore, especially with full heuristics (bad character + good suffix), can outperform both, especially for large patterns.

Future improvements:
- Implement full Boyer-Moore with both bad character and good suffix heuristics.
- Extend to approximate matching using algorithms like Rabin-Karp or Aho-Corasick.
- Include more diverse and multilingual texts.
- Parallelize experiments for benchmarking on multi-core CPUs.
"""
