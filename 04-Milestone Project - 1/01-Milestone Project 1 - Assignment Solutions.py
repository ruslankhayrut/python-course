# def print_board(board):
#     print('*************************')
#     i = 1
#     for field in board:
#         print(field)

#         if i % 3 == 0:
#             print('*************************')

#         i += 1


# def user_input(picks, player):
#     position = 'wrong'
#     not_in_range = True

#     while position.isdigit() == False or not_in_range:
#         print()
#         print(f'Player {player} turn')
#         position = input('Choose a position: (1-9)\n')
#         print()

#         if position.isdigit() == False:
#             print('Not a digit, try again')
#             continue

#         if int(position) in picks:
#             print('Position is occupied')
#             continue

#         if int(position) not in range(1, 10):
#             print('Not in range, try again')
#             continue

#         return int(position)


# def update_board(board, input, x_turn):
#     x_fields = ['* *', ' * ', '* *']
#     o_fields = [' * ', '* *', ' * ']

#     x = 0 if input < 4 else 6 if input > 6 else 3
#     y = 3 if input in [1, 4, 7] else 19 if input in [3, 6, 9] else 11

#     for i, j in enumerate(range(x, x+3)):
#         fields = x_fields[i] if x_turn else o_fields[i]
#         board[j] = board[j][:y] + fields + board[j][y + 3:]

#     return board


# def update_wins(wins, input, x_turn):
#     char = 'X' if x_turn else 'O'
#     new_wins = []
#     for win in wins:
#         new_wins.append(win.replace(str(input), char))

#     return new_wins


# def check_win(wins):
#     winner = False
#     for win in wins:
#         if len(set(win)) == 1:
#             winner = list(set(win))[0]

#     return winner


# def game():
#     winner = False
#     game_over = False
#     x_turn = True
#     picks = []
#     wins = ['123', '456', '789', '147', '258', '369', '159', '357']

#     board = ['*       *       *       *' for i in range(9)]
#     print('Your starting board:')
#     print_board(board)

#     while not game_over:
#         picks.append(user_input(picks, ('X' if x_turn else 'O')))
#         board = update_board(board, picks[-1], x_turn)
#         wins = update_wins(wins, picks[-1], x_turn)

#         print_board(board)

#         if len(picks) > 4:
#             winner = check_win(wins)
#             game_over = bool(winner)

#         if len(picks) == 9:
#             break

#         x_turn = not x_turn

#     if bool(winner):
#         print(f'The winner is {winner} player! Game over, thanks for playing.')
#     else:
#         print('Game over! No more playing fields! Try again.')


# game()


###############################


def print_board(board):
    printable = ''
    for i in range(1, 10):
        printable += board[i]+' '
        if i % 3 == 0:
            printable += '\n'

    print(printable)


def update_board(board, position, symbol):
    board[position] = symbol
    return board


def user_input(board, player):
    position = 'wrong'
    not_in_range = True

    while position.isdigit() == False or not_in_range:
        print()
        print(f'Player {player} turn')
        position = input('Choose a position: (1-9)\n')
        print()

        if position.isdigit() == False:
            print('Not a digit, try again')
            continue

        if int(position) not in range(1, 10):
            print('Not in range, try again')
            continue

        if board[int(position)] != '-':
            print('Position is occupied')
            continue

        return int(position)


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

    while not game_over:
        position = user_input(board, ('X' if x_turn else 'O'))

        board = update_board(board, position, ('X' if x_turn else 'O'))

        print_board(board)

        if len(board) > 5:
            winner = check_win(board)
            game_over = bool(winner)

        if counter == 9:
            break

        x_turn = not x_turn
        counter += 1

    if bool(winner):
        print(f'The winner is {winner} player! Game over, thanks for playing.')
    else:
        print('Game over! No more playing fields! Try again.')


game()
