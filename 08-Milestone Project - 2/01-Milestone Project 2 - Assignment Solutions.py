import random
from abc import ABC
from typing import List

"""
No need to write error message in __init__ actually. 
You can do

class NoMoreChips(Exception):
    pass

And then

raise NoMoreChips("Error msg")

Which is more flexible
"""


class NoMoreChips(Exception):
    def __init__(self):
        super().__init__("You don't have any more chips for playing.")


class Card:
    suits = ("Hearts", "Diamonds", "Spades", "Clubs")
    ranks = (
        "Two",
        "Three",
        "Four",
        "Five",
        "Six",
        "Seven",
        "Eight",
        "Nine",
        "Ten",
        "Jack",
        "Queen",
        "King",
        "Ace",
    )

    values = {
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

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = Card.values[rank]

    def __str__(self):
        # always try to use fstrings, since they are more readable and faster
        return self.rank + " of " + self.suit


class Deck:
    def __init__(self, num_of_decks: int = 1):
        self.all_cards = []
        for _ in range(num_of_decks):
            for suit in Card.suits:
                for rank in Card.ranks:
                    self.all_cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()

    def add_cards(self, cards: List[Card]):
        self.all_cards.extend(cards)
        self.shuffle()


class Playable(ABC):
    """
    Name should be declared in __init__, as I assume it's an instance property, not a class one
    Because in general we can have several players with different names
    In practice, class properties are not used very often

    The way you implemented it in Card class is reasonable,
    but suits, ranks and values could also be implemented as constants

    For this base class you can do

        ...
        self.name = "Unnamed"

    then in Player class
    def __init__(self, name, chips):
        super().__init__()
        self.name = name
        ...

    and in Dealer class

        ...
        self.name = "Dealer"
    """

    name = "Dealer"

    def __init__(self) -> None:
        self.cards: List[Card] = []
        self.has_ace = False

    def get_cards(self) -> List[Card]:
        return self.cards

    def sum_cards(self) -> int:
        summed = sum([card.value for card in self.cards])
        if self.has_ace and summed < 12:
            summed += 10

        return summed

    def add_card(self, card: Card):
        self.cards.append(card)

        """
        this can be substituted with a one-liner
        self.has_ace = card.rank == "Ace"
        """

        if card.rank == "Ace":
            self.has_ace = True
        print(f"{self.name} got a {card}")

    def prepare_for_next_round(self) -> List[Card]:
        self.has_ace = False
        cards = self.cards
        self.cards = []

        return cards


class Player(Playable):
    def __init__(self, name: str, chips: int) -> None:
        super().__init__()
        self.name = name
        self.chips = chips
        self.current_bet = 0

    def place_bet(self, bet: int) -> bool:
        if not self.chips:
            raise NoMoreChips()

        if bet <= self.chips:
            self.current_bet = bet
            return True

        print("Make smaller bet, not enough chips, try again.")
        return False

    def has_won(self, win: bool = None):
        """
        This can be simplified
        self.chips += self.current_bet if win else -self.current_bet

        I see that you have 3 states here
        win = True, False or None

        I'd handle this like that:

        if win:
            do stuff
        elif win is None:
            pass
        else:
            do another stuff

        self.current_bet = 0

        But actually this ternary condition is not supposed to be handled with booleans, since they are binary.
        I'd introduce something like `coefficients`, -1, 0, 1

        Going further, these 3 win states could be introduced as simple enum like
        WinnerEnum:
            PLAYER = 1
            DRAW = 0
            DEALER = -1

        Then the method could be renamed to `process_round_winner`
        I.e.
            self.process_round_winner(winner: int):
                self.chips += self.current_bet * winner
                self.current_bet = 0
        """
        if win:
            self.chips += self.current_bet
        elif win == False:
            self.chips -= self.current_bet

        self.current_bet = 0


class Dealer(Playable):
    def __init__(self) -> None:
        super().__init__()
        self.hidden_card: Card = None

    def add_card(self, card: Card):
        """
        Use guard clauses https://medium.com/lemon-code/guard-clauses-3bc0cd96a2d3
        E.g.

        if len(self.cards) != 1 or self.hidden_card:
            super().add_card(card)
            return

        print('Dealer got a hidden card')
        self.hidden_card = card
        """
        if len(self.cards) == 1 and not self.hidden_card:
            print("Dealer got a hidden card")
            self.hidden_card = card
        else:
            super().add_card(card)

    def show_hidden(self):
        print(f"Dealer reveals hidden card: {self.hidden_card}")

        # same as per user
        if self.hidden_card.rank == "Ace":
            self.has_ace = True

        self.cards.append(self.hidden_card)
        self.hidden_card = None
        print(f"Dealer's points after revealing: {self.sum_cards()}")

    def prepare_for_next_round(self) -> List[Card]:
        self.hidden_card = None
        return super().prepare_for_next_round()


# this is not needed I think
class Interface:
    pass


def print_status():
    print(f"\nDealer:{dealer.sum_cards()}/{player.name}:{player.sum_cards()}\n")


"""
Can you implement Blackjack as a class, 
containing all Dealer, Player, Deck in it?
And run game like this

game = Blackjack(Dealer, Player)
game.run()
"""


def blackjack():
    rounds = 0

    while True:
        if rounds > 0:
            # play another game
            if input("Play another round? y/n\n") != "y":
                break

            deck.add_cards(player.prepare_for_next_round())
            deck.add_cards(dealer.prepare_for_next_round())

        rounds += 1
        # place bet
        print(f"You have {player.chips} in value of chips")

        try:
            while True:
                bet = input("Enter a bet value: ")

                if not bet.isdigit():
                    print("You didn't enter a number. Try again")
                    continue

                bet = int(bet)

                placed = player.place_bet(bet)

                if placed:
                    break
        except NoMoreChips as e:
            print(str(e))
            break

        print()

        # deal initial cards
        for _ in range(2):
            player.add_card(deck.deal_one())
            dealer.add_card(deck.deal_one())

        # check player for blackjack

        """
        Why 21? 
        Avoid using `magic numbers` https://stackoverflow.com/questions/47882/what-is-a-magic-number-and-why-is-it-bad
        
        The example is for Java, but I think the idea is clear
        """
        if player.sum_cards() == 21:
            print_status()
            print(f"You got Blackjack! You win!")
            player.has_won(True)
            continue

        # player turn
        while player.sum_cards() < 21:
            print_status()
            # hit (y), stand (n)
            if input("Do you want to take more cards? (y/n)\n") != "y":
                break

            player.add_card(deck.deal_one())

        if player.sum_cards() > 21:
            print_status()
            print(f"{player.name} busts.")
            player.has_won(False)
            continue

        # dealer turn
        dealer.show_hidden()
        if dealer.sum_cards() == 21:
            print_status()
            print(f"Dealer got Blackjack! You lose!")
            player.has_won(False)
            continue

        while dealer.sum_cards() < 17:
            print_status()
            print("Dealer hits.")
            dealer.add_card(deck.deal_one())

        if dealer.sum_cards() > 21:
            print_status()
            print(f"Dealer busts. You win!")
            player.has_won(True)
            continue

        print("Dealer stands.")

        # compare final results
        print_status()
        if dealer.sum_cards() > player.sum_cards():
            print(f"Dealer wins. You lose!")
            player.has_won(False)
        elif dealer.sum_cards() == player.sum_cards():
            print(f"Draw! No one wins.")
            player.has_won(None)
        else:
            print(f"You win!")
            player.has_won(True)

    print("Thanks for playing")


print("\nWelcome to blackjack game!\n")
name = input("What's your name? ")

while True:
    chips = input("How much chips will you start the game with? ")
    if not chips.isdigit():
        print("You didn't enter a number. Try again")
        continue

    chips = int(chips)

    if chips <= 0:
        print("Must enter game with more than 0 chips")
        continue

    break

player = Player(name, chips)
dealer = Dealer()
deck = Deck()
deck.shuffle()

blackjack()
