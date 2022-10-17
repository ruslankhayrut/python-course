import random

number = random.randint(1, 100)
guesses = [0]

print('This is a number guessing game!')

while guesses[-1] != number:
    guesses.append(input('Choose a number between 1 and 100.'))

    if guesses[-1].isnumeric():
        guesses[-1] = int(guesses[-1])
    else:
        print(f'{guesses[-1]} is not a number!')
        guesses.pop(-1)
        continue

    if 1 > guesses[-1] or guesses[-1] > 100:
        print('OUT OF BOUNDS')
        guesses.pop(-1)
        continue

    if guesses[-1] == number:
        break

    if len(guesses) < 3:
        if abs(number - guesses[-1]) > 10:
            print('COLD!')
        else:
            print('WARM!')
    else:
        if abs(number - guesses[-2]) > abs(number - guesses[-1]):
            print('WARMER!')
        else:
            print('COLDER!')

print(f'Success after {len(guesses) - 1} guesses')
