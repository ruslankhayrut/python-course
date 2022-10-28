import random
from enum import Enum


SUITS = ("Hearts", "Diamonds", "Spades", "Clubs")
RANKS = ("Two", "Three", "Four", "Five", "Six", "Seven",
         "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace")

VALUES = {
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
    "Six": 6,
    "Seven": 7,
    "Eight": 8,
    "Nine": 9,
    "Ten": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10,
    "Ace": 1,
}

BLACKJACK = 21
DEALER_SUM_BORDER = 17


class Winner(Enum):
    PLAYER = 1
    DRAW = 0
    DEALER = -1


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = VALUES[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self, num_of_decks: int = 1):
        self.all_cards = []
        for _ in range(num_of_decks):
            for suit in SUITS:
                for rank in RANKS:
                    self.all_cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()

    def add_cards(self, cards: list[Card]):
        self.all_cards.extend(cards)
        self.shuffle()


class Hand():
    def __init__(self) -> None:
        self.cards: list[Card] = []
        self.has_ace = False

    def sum_cards(self) -> int:
        summed = sum([card.value for card in self.cards])
        if self.has_ace and summed < 12:
            summed += 10

        return summed

    def add_card(self, card: Card):
        self.cards.append(card)
        self.has_ace = card.rank == "Ace" or self.has_ace
        print(f'    {card}')

    def prepare_for_next_round(self) -> list[Card]:
        self.has_ace = False
        cards = self.cards
        self.cards = []

        return cards


class PlayerHand(Hand):
    def __init__(self, index: int = 1) -> None:
        self.name = f'Hand {index}'
        self.current_bet: int = 0
        self.to_split = True
        self.round_over = False
        super().__init__()

    def view_cards(self):
        cards = ', '.join([str(card) for card in self.cards])
        print(f'{self.name}: {cards}')

    def add_card(self, card: Card):
        print(f'{self.name} gets:')
        super().add_card(card)

    def process_round_winner(self, winner: Winner) -> int:
        self.round_over = True
        return self.current_bet * winner.value

    def can_be_split(self) -> bool:
        can_be_split = True if self.cards[0].rank == self.cards[1].rank else False
        return can_be_split and self.to_split


class Player():
    def __init__(self, name: str, chips: int) -> None:
        self.name = name
        self.chips = chips
        self.finished_round = False
        self.hands: list[PlayerHand] = [PlayerHand()]

    def get_hands(self):
        return [hand for hand in self.hands if not hand.round_over]

    def first_hand(self) -> PlayerHand:
        return self.get_hands()[0]

    def place_bet(self, hand: PlayerHand, bet: int) -> bool:
        if bet <= self.chips:
            hand.current_bet = bet
            return True

        print("Make smaller bet, not enough chips, try again.")
        return False

    def out_of_chips(self) -> bool:
        return self.chips == 0

    def process_round_winner(self, hand: PlayerHand, winner: Winner):
        self.chips += hand.process_round_winner(winner)

        if not self.get_hands():
            self.finished_round = True

    def prepare_for_next_round(self) -> list[Card]:
        self.finished_round = False
        cards = []
        for hand in self.hands:
            cards.extend(hand.prepare_for_next_round())

        self.hands = [PlayerHand()]
        return cards

    def has_splittable(self) -> bool:
        for hand in self.hands:
            if hand.can_be_split():
                return True
        return False

    def split(self, hand: PlayerHand) -> PlayerHand:
        new_hand = PlayerHand(len(self.hands) + 1)
        print('New (split) hand gets:')
        new_hand.add_card(hand.cards.pop())
        self.hands.append(new_hand)
        return new_hand


class Dealer():
    def __init__(self) -> None:
        self.name = 'Dealer'
        self.hidden_card: Card = None
        self.hand: Hand = Hand()

    def add_card(self, card: Card):
        if len(self.hand.cards) != 1 or self.hidden_card:
            print('Dealer got a:')
            self.hand.add_card(card)
            return

        print("Dealer got a hidden card")
        self.hidden_card = card

    def show_hidden(self):
        print(f"Dealer reveals hidden card:")
        self.hand.add_card(self.hidden_card)
        self.hidden_card = None
        print(f"Dealer's points after revealing: {self.hand.sum_cards()}")

    def prepare_for_next_round(self) -> list[Card]:
        self.hidden_card = None
        return self.hand.prepare_for_next_round()


class Blackjack:
    def __init__(self, deck: Deck, dealer: Dealer, players: list[Player]):
        self.all_players: list[Player] = players
        self.dealer: Dealer = dealer
        self.deck: Deck = deck
        deck.shuffle()
        self.rounds: int = 0

    def current_players(self):
        return [player for player in self.all_players if not player.finished_round]

    def play(self):
        print('\nWelcome to blackjack game!\n')

        # start round
        while True:
            if self.rounds > 0:
                players_to_remove = []
                for i, player in enumerate(self.all_players):
                    # remove players with no chips
                    if player.out_of_chips():
                        print(f'{player.name} is out of chips.')
                        print(f'{player.name} is removed from game.\n')
                        players_to_remove.append(i)
                        continue

                    # ask each player for another round
                    another_round = input_choice(
                        f'{player.name} play another round? (y/n)\n')

                    if not another_round:
                        players_to_remove.append(i)

                self.remove_players(players_to_remove)
                if not self.all_players:
                    print('No more players. Game over.')
                    break

                self.prepare_next_round()

            self.rounds += 1

            # placing initial bets
            for player in self.all_players:
                print(f'{player.name} amount of chips: {player.chips}')
                self.place_bet(player)

            print('\nInitial dealing:')
            # initial dealing
            for _ in range(2):
                self.dealer.add_card(self.deck.deal_one())
                for player in self.all_players:
                    print(f'{player.name}')
                    player.first_hand().add_card(self.deck.deal_one())

            # splitting
            for player in self.all_players:
                while player.has_splittable():
                    hand = player.first_hand()
                    if hand.can_be_split():
                        print(f'\n{player.name} can split:')
                        hand.view_cards()

                        split = input_choice(f'Want to split? (y/n)\n')
                        if not split:
                            hand.to_split = False
                            continue

                        new_hand = player.split(hand)
                        self.place_bet(player, new_hand)

                        hand.add_card(self.deck.deal_one())
                        new_hand.add_card(self.deck.deal_one())

            # check players for blackjack
            self.print_status()
            for player in self.all_players:
                for hand in player.hands:
                    if hand.sum_cards() == BLACKJACK:
                        print(f'{player.name} {hand.name} got Blackjack!')
                        player.process_round_winner(hand, Winner.PLAYER)

            if not self.current_players():
                print('All players got blackjack.')
                continue

            # players turn
            for player in self.current_players():
                for hand in player.get_hands():
                    hand.view_cards()
                    while hand.sum_cards() < BLACKJACK:
                        self.print_status(player)
                        hit = input_choice(
                            f'{player.name} take more cards for {hand.name}? (y/n)\n')

                        if not hit:
                            break

                        hand.add_card(self.deck.deal_one())

                    if hand.sum_cards() > BLACKJACK:
                        print(
                            f'{player.name} {hand.name} busts with {hand.sum_cards()}.\n')
                        player.process_round_winner(hand, Winner.DEALER)

            if not self.current_players():
                print('All players bust.\n')
                continue

            # dealer's turn
            self.dealer.show_hidden()
            if self.dealer.hand.sum_cards() == BLACKJACK:
                self.print_status()
                print(f'Dealer got Blackjack!')
                for player in self.current_players():
                    for hand in player.get_hands():
                        player.process_round_winner(hand, Winner.DEALER)
                continue

            while self.dealer.hand.sum_cards() < DEALER_SUM_BORDER:
                print('Dealer hits.')
                self.dealer.add_card(self.deck.deal_one())
                print(f'Dealer: {self.dealer.hand.sum_cards()}')

            if self.dealer.hand.sum_cards() > BLACKJACK:
                self.print_status()
                print(f'Dealer busts with {self.dealer.hand.sum_cards()}.\n')
                for player in self.current_players():
                    while player.get_hands():
                        hand = player.first_hand()
                        player.process_round_winner(hand, Winner.PLAYER)
                continue

            print('Dealer stands.')
            self.print_status()

            for player in self.current_players():
                while player.get_hands():
                    hand = player.first_hand()
                    if self.dealer.hand.sum_cards() > hand.sum_cards():
                        print(f'{player.name} {hand.name} loses.')
                        player.process_round_winner(hand, Winner.DEALER)
                    elif self.dealer.hand.sum_cards() == hand.sum_cards():
                        print(f'{player.name} {hand.name} and dealer are draw.')
                        player.process_round_winner(hand, Winner.DRAW)
                    else:
                        print(f'{player.name} {hand.name} wins!')
                        player.process_round_winner(hand, Winner.PLAYER)

        print('Thanks for playing')

    def prepare_next_round(self):
        cards = []
        for player in self.all_players:
            cards.extend(player.prepare_for_next_round())
        cards.extend(self.dealer.prepare_for_next_round())
        self.deck.add_cards(cards)

    def place_bet(self, player: Player, hand: PlayerHand = None):
        hand = hand if hand else player.first_hand()
        placed = False
        while not placed:
            bet = input_integer(
                f'{player.name} enter a bet value for {hand.name}: ')
            placed = player.place_bet(hand, bet)

    def remove_players(self, player_indexes: list[int]):
        for i in player_indexes[::-1]:
            self.all_players.pop(i)

    def print_status(self, player: Player = None):
        if player:
            hand_text = ' '.join(
                [f' {hand.name} - {hand.sum_cards()};' for hand in player.hands])
            print(
                f'Dealer: {self.dealer.hand.sum_cards()} / {player.name}:{hand_text}')
            return

        print('\n'+'#'*15)
        print(f'Dealer: {self.dealer.hand.sum_cards()}')
        for player in self.current_players():
            hand_text = ' '.join(
                [f' {hand.name} - {hand.sum_cards()};' for hand in player.hands])
            print(f'{player.name}:{hand_text}')
        print('#'*15 + '\n')


def input_integer(question: str = 'Enter an integer: ', min: int = 1, max: int = None) -> int:
    while True:
        value = input(question)

        if not value.isdigit():
            print('Not a number! Try again.')
            continue

        value = int(value)

        if value < min:
            print('Must be above zero! Try again.')
            continue

        if max and value > max:
            print(f'Maximum value is {max}! Try again')
            continue

        return value


def input_choice(question: str, choices: dict = {'y': True, 'n': False}) -> bool:
    while True:
        choice = input(question)

        if choice in choices.keys():
            return choices[choice]

        print('Choice not valid! Try again.')


def define_players() -> list[Player]:
    num_of_players = input_integer('How many players? (max 7) ', max=7)
    players = []
    for i in range(num_of_players):
        name = input(f'Player number {i+1} name: ')
        chips = input_integer(f'Player number {i+1} value in chips: ')
        players.append(Player(name, chips))

    return players


players = define_players()
dealer = Dealer()
num_of_decks = input_integer('How many decks? (max 7) ', max=7)
deck = Deck(num_of_decks)

game = Blackjack(deck, dealer, players)
game.play()
