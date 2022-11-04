"""
Count Vowels
Enter a string and the program counts the number of vowels in the text. 
For added complexity have it report a sum of each vowel found.
"""


def count_vowels(sentence: str):
    filtered = str([c for c in sentence if c in 'aeiou'])
    return {v: filtered.count(v) for v in 'aeiou'}


print(count_vowels('disdia'))
