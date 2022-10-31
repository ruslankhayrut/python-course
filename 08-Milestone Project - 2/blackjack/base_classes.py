import random
from blackjack.constants import *


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
        return self.cards[0].rank == self.cards[1].rank and self.to_split


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
