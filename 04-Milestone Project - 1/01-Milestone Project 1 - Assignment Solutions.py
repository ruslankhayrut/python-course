board = ['-' for _ in range(9)]
winner = False
current_player = 'X'


def print_board():
    for i in range(0, 9, 3):
        print(' '.join(board[i:i+3]))


def user_input() -> int:
    print(f'\nPlayer {current_player} turn')

    while True:
        value = input('Choose a position: (1-9)\n')
        print()

        if not value.isdigit():
            print('Not a digit, try again.')
            continue

        position = int(value) - 1

        if position not in range(0, 9):
            print('Not in range, try again.')
            continue

        print(board[position])
        if board[position] != '-':
            print('Position is occupied, try again.')
            continue

        return position


def set_has_win(the_set: set) -> bool:
    return len(the_set) == 1 and the_set != set('-')


def check_win():
    global winner
    # horizontal check
    for i in range(0, 7, 3):
        if set_has_win({board[i], board[i+1], board[i+2]}):
            winner = board[i]

    # vertical check
    for i in range(0, 3):
        if set_has_win({board[i], board[i+3], board[i+6]}):
            winner = board[i]

    # diagonal check
    if set_has_win({board[0], board[4], board[8]}):
        winner = board[0]

    if set_has_win({board[2], board[4], board[6]}):
        winner = board[2]


def game():
    global winner, current_player
    counter = 0

    print('Starting board:')
    print_board()

    while not winner and counter != 9:
        position = user_input()
        board[position] = current_player

        print_board()

        if counter > 3:
            check_win()

        current_player = 'X' if current_player == 'O' else 'O'
        counter += 1

    if winner:
        print(f'\nThe winner is {winner} player! Thanks for playing.')
    else:
        print('\nGame over! No more playing fields!')


game()
