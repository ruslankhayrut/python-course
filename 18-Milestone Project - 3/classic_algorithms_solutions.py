"""
Collatz Conjecture
Start with a number n > 1. 
Find the number of steps it takes to reach one using the following process: 
If n is even, divide it by 2. 
If n is odd, multiply it by 3 and add 1.
"""


def collatz(n: int) -> int:
    steps = 0
    while n != 1:
        steps += 1
        n = n / 2 if not n % 2 else n * 3 + 1

    return steps


print(collatz(221))
