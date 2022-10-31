from blackjack.base_classes import Dealer, Deck
from blackjack.blackjack_class import Blackjack
from blackjack.helpers import define_players, input_integer


players = define_players()
dealer = Dealer()
num_of_decks = input_integer('How many decks? (max 7) ', max_int=7)
deck = Deck(num_of_decks)

game = Blackjack(deck, dealer, players)
game.play()
