import random

number = random.randint(1, 100)
new_user_number = 0
old_user_number = None
guesses = 0

while new_user_number != number:
    new_user_number = input('Choose a number between 0 and 100.\n')

    # Check is it a number
    if new_user_number.isdecimal():
        new_user_number = int(new_user_number)
    else:
        print(f'{new_user_number} is not a number!')
        continue

    # Check is it a right guess
    if new_user_number == number:
        break

    # Check is it out of bounds
    if 1 > new_user_number or new_user_number > 100:
        print('OUT OF BOUNDS!')
        continue

    guesses += 1

    if old_user_number is None:
        if abs(number - new_user_number) > 10:
            print('COLD!')
        else:
            print('WARM!')
    else:
        if abs(number - old_user_number) > abs(number - new_user_number):
            print('WARMER!')
        else:
            print('COLDER!')

    old_user_number = new_user_number

print(f'Success after {guesses} guesses')
