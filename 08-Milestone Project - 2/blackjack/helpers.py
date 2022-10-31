from blackjack.base_classes import Player


def input_integer(question: str = 'Enter an integer: ', min_int: int = 1, max_int: int = None) -> int:
    while True:
        value = input(question)

        if not value.isdigit():
            print('Not a number! Try again.')
            continue

        value = int(value)

        if value < min_int:
            print(f'Must be above {min_int}! Try again.')
            continue

        if max_int and value > max_int:
            print(f'Maximum value is {max_int}! Try again')
            continue

        return value


def input_choice(question: str, choices: dict = None) -> bool:
    choices = choices if choices else {'y': True, 'n': False}
    while True:
        choice = input(question)

        if choice in choices.keys():
            return choices[choice]

        print('Choice not valid! Try again.')


def define_players() -> list[Player]:
    num_of_players = input_integer('How many players? (max 7) ', max_int=7)
    players = []
    for i in range(num_of_players):
        name = input(f'Player number {i+1} name: ')
        chips = input_integer(f'Player number {i+1} value in chips: ')
        players.append(Player(name, chips))

    return players
