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
