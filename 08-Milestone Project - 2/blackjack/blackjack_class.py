from blackjack.base_classes import Deck, Dealer, Player, PlayerHand
from blackjack.helpers import input_choice, input_integer
from blackjack.constants import Winner, DEALER_SUM_BORDER, BLACKJACK


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
                start_new_round = self.start_new_round()
                if not start_new_round:
                    break

            self.rounds += 1

            # placing initial bets
            for player in self.all_players:
                print(f'{player.name} amount of chips: {player.chips}')
                self.place_bet(player)

            # initial dealing
            self.initial_dealing()

            # splitting
            self.splitting_phase()

            # check players for blackjack
            all_blackjack = self.check_players_for_blackjack()
            if all_blackjack:
                continue

            # players turn
            all_players_bust = self.players_turn()
            if all_players_bust:
                continue

            # dealer's turn
            round_finished = self.dealer_turn()
            if round_finished:
                continue

            # compare results
            self.compare_results()

        print('Thanks for playing')

    def start_new_round(self) -> bool:
        self.remove_players_without_chips()
        if not self.all_players:
            print('No more players. Game over.')
            return False

        self.poll_players_for_another_round()
        if not self.all_players:
            print('No more players. Game over.')
            return False

        self.prepare_next_round()
        return True

    def remove_players_without_chips(self):
        players_to_remove = []
        for i, player in enumerate(self.all_players):
            # remove players with no chips
            if player.out_of_chips():
                print(f'{player.name} is out of chips.')
                print(f'{player.name} is removed from game.\n')
                players_to_remove.append(i)
                continue

        self.remove_players(players_to_remove)

    def poll_players_for_another_round(self):
        players_to_remove = []
        for i, player in enumerate(self.all_players):
            # ask each player for another round
            another_round = input_choice(
                f'{player.name} play another round? (y/n)\n')

            if not another_round:
                players_to_remove.append(i)

        self.remove_players(players_to_remove)

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

    def initial_dealing(self):
        print('\nInitial dealing:')
        for _ in range(2):
            self.dealer.add_card(self.deck.deal_one())
            for player in self.all_players:
                print(f'{player.name}')
                player.first_hand().add_card(self.deck.deal_one())

    def splitting_phase(self):
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

    def check_players_for_blackjack(self) -> bool:
        for player in self.all_players:
            for hand in player.hands:
                if hand.sum_cards() == BLACKJACK:
                    print(f'*{player.name} {hand.name} got BLACKJACK!*')
                    player.process_round_winner(hand, Winner.PLAYER)

        if not self.current_players():
            print('No more players in this round.\n')
            return True

        return False

    def players_turn(self) -> bool:
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
                        f'*{player.name} {hand.name} BUSTS with {hand.sum_cards()}.*\n')
                    player.process_round_winner(hand, Winner.DEALER)

        if not self.current_players():
            print('No more players in this round.\n')
            return True

        return False

    def dealer_turn(self):
        self.dealer.show_hidden()
        if self.dealer.hand.sum_cards() == BLACKJACK:
            self.print_status()
            print(f'*Dealer got BLACKJACK!*')
            for player in self.current_players():
                for hand in player.get_hands():
                    player.process_round_winner(hand, Winner.DEALER)
            return True

        while self.dealer.hand.sum_cards() < DEALER_SUM_BORDER:
            print('Dealer hits.')
            self.dealer.add_card(self.deck.deal_one())
            print(f'Dealer: {self.dealer.hand.sum_cards()}')

        if self.dealer.hand.sum_cards() > BLACKJACK:
            self.print_status()
            print(f'*Dealer BUSTS with {self.dealer.hand.sum_cards()}.*\n')
            for player in self.current_players():
                while player.get_hands():
                    hand = player.first_hand()
                    player.process_round_winner(hand, Winner.PLAYER)
            return True

        print('Dealer stands.')
        return False

    def compare_results(self):
        self.print_status()

        for player in self.current_players():
            while player.get_hands():
                hand = player.first_hand()
                if self.dealer.hand.sum_cards() > hand.sum_cards():
                    print(f'{player.name} {hand.name} loses.')
                    player.process_round_winner(hand, Winner.DEALER)
                elif self.dealer.hand.sum_cards() == hand.sum_cards():
                    print(f'{player.name} {hand.name} and Dealer are draw.')
                    player.process_round_winner(hand, Winner.DRAW)
                else:
                    print(f'{player.name} {hand.name} wins!')
                    player.process_round_winner(hand, Winner.PLAYER)

    def print_status(self, player: Player = None):
        dealer_text = f'Dealer: {self.dealer.hand.sum_cards()}'
        if player:
            hand_text = ' '.join(
                [f' {hand.name} - {hand.sum_cards()};' for hand in player.get_hands()])
            print(f'{dealer_text} / {player.name}:{hand_text}')
            return

        print('\n'+'#'*15)
        print(dealer_text)
        for player in self.current_players():
            hand_text = ' '.join(
                [f' {hand.name} - {hand.sum_cards()};' for hand in player.get_hands()])
            print(f'{player.name}:{hand_text}')
        print('#'*15 + '\n')
