def print_board(board):
    print('*************************')
    i = 1
    for field in board:
        print(field)

        if i % 3 == 0:
            print('*************************')

        i += 1


def user_input(board, player):
    position = 'wrong'

    while position.isdigit() == False:
        print()
        print(f'Player {player} turn')
        position = input('Choose a position: (1-9)\n')
        print()

        if position.isdigit() == False:
            print('Not a digit, try again')
            continue

        if int(position) in board:
            print('Position is occupied')
            continue

        if int(position) not in range(1, 10):
            print('Not in range, try again')
            continue

        return int(position)


def update_board_looks(board, position, x_turn):
    x_fields = ['* *', ' * ', '* *']
    o_fields = [' * ', '* *', ' * ']

    x = 0 if position < 4 else 6 if position > 6 else 3
    y = 3 if position in [1, 4, 7] else 19 if position in [3, 6, 9] else 11

    for i, j in enumerate(range(x, x+3)):
        fields = x_fields[i] if x_turn else o_fields[i]
        board[j] = board[j][:y] + fields + board[j][y + 3:]

    return board


def update_board(board, position, symbol):
    board[position] = symbol
    return board


def set_has_win(the_set):
    return len(the_set) == 1 and the_set != set('-')


def check_win(board):
    winner = False
    # horizontal check
    for i in range(1, 8, 3):
        if set_has_win(set((board[i], board[i+1], board[i+2]))):
            return board[i]

    # vertical check
    for i in range(1, 4):
        if set_has_win(set((board[i], board[i+3], board[i+6]))):
            return board[i]

    # diagonal check
    if set_has_win(set((board[1], board[5], board[9]))):
        return board[1]

    if set_has_win(set((board[3], board[5], board[7]))):
        return board[3]

    return winner


def game():
    board = ['placeholder'] + ['-' for i in range(9)]
    game_over = False
    x_turn = True
    counter = 1

    board_looks = ['*       *       *       *' for i in range(9)]
    print('Your starting board:')
    print_board(board_looks)

    while not game_over:
        position = user_input(board, ('X' if x_turn else 'O'))

        board = update_board(board, position, ('X' if x_turn else 'O'))
        board_looks = update_board_looks(board_looks, position, x_turn)

        print_board(board_looks)

        if counter > 5:
            winner = check_win(board)
            game_over = bool(winner)

        if counter == 9:
            break

        counter += 1
        x_turn = not x_turn

    print()
    if bool(winner):
        print(f'The winner is {winner} player! Game over, thanks for playing.')
    else:
        print('Game over! No more playing fields! Try again.')


game()
