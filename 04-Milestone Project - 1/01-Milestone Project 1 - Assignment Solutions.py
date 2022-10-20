from typing import Union


def print_board():
    print(f'{BOARD[1]} {BOARD[2]} {BOARD[3]}')
    print(f'{BOARD[4]} {BOARD[5]} {BOARD[6]}')
    print(f'{BOARD[7]} {BOARD[8]} {BOARD[9]}')


def user_input(player: str) -> int:
    position = 'wrong'

    print(f'\nPlayer {player} turn')

    while position.isdigit() == False:

        value = input('Choose a position: (1-9)\n')
        print()

        if value.isdigit() == False:
            print('Not a digit, try again.')
            continue

        if int(value) not in range(1, 10):
            print('Not in range, try again.')
            continue

        if BOARD[int(value)] != '-':
            print('Position is occupied, try again.')
            continue

        position = value

        return int(position)


def set_has_win(the_set: set) -> bool:
    return len(the_set) == 1 and the_set != set('-')


def check_win() -> Union[bool, str]:
    winner = False
    # horizontal check
    for i in range(1, 8, 3):
        if set_has_win(set((BOARD[i], BOARD[i+1], BOARD[i+2]))):
            return BOARD[i]

    # vertical check
    for i in range(1, 4):
        if set_has_win(set((BOARD[i], BOARD[i+3], BOARD[i+6]))):
            return BOARD[i]

    # diagonal check
    if set_has_win(set((BOARD[1], BOARD[5], BOARD[9]))):
        return BOARD[1]

    if set_has_win(set((BOARD[3], BOARD[5], BOARD[7]))):
        return BOARD[3]

    return winner


def game():
    winner = False
    current_turn = 'X'
    counter = 0

    print('Starting board:')
    print_board()

    while not winner and counter != 9:
        position = user_input(current_turn)

        BOARD[position] = current_turn

        print_board()

        if counter > 3:
            winner = check_win()

        current_turn = 'X' if current_turn == 'O' else 'O'
        counter += 1

    if winner:
        print(f'The winner is {winner} player! Game over, thanks for playing.')
    else:
        print('Game over! No more playing fields!')


BOARD = ['placeholder'] + ['-' for _ in range(9)]
game()
