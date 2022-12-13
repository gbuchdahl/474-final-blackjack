from abc import ABC
from enum import Enum
from typing import List, Tuple

from cards import Shoe, Hand


class Action(Enum):
    STAND = 0
    HIT = 1
    DOUBLE = 2
    SPLIT = 3


class PlayableHand:
    def __init__(self, shoe: Shoe, bet: int, upcard=None, hand: Hand = None, hand_over:
    bool =
    False):
        self.shoe = shoe
        self.hand: Hand = hand or self.shoe.deal_hand()
        self.upcard = upcard or self.shoe.deal()
        self.bet = bet
        self.hand_over = hand_over or False

    def get_all_actions(self) -> List[Action]:
        actions = [Action.STAND, Action.HIT]
        if len(self.hand) == 2 and self.hand[0].value == self.hand[1].value:
            # actions.append(Action.SPLIT)
            # TODO: Splitting is not implemented yet
            pass
        if len(self.hand) == 2 and self.hand.get_value()[0] <= 11:
            actions.append(Action.DOUBLE)
        return actions

    def is_terminal(self) -> bool:
        return self.hand_over or self.hand.is_bust()

    def get_hand_value(self, verbose=False) -> int:
        """
        :return:  the value of a terminal hand after dealer play
        """
        if not self.is_terminal():
            raise ValueError("Hand is not terminal")
        if self.hand.is_bust():
            return -self.bet

        dealer_hand = Hand([self.upcard, self.shoe.deal()])
        if verbose:
            print(f"Dealer hand: {dealer_hand}")
        while dealer_hand.get_value()[0] < 17:
            dealer_hand.add_card(self.shoe.deal())
            if verbose:
                print(f"Dealer hand: {dealer_hand}")

        if self.hand.is_blackjack() and not dealer_hand.is_blackjack():
            return int(self.bet * 1.5)

        if self.hand.get_value()[0] > dealer_hand.get_value()[0]:
            return self.bet
        elif self.hand.get_value()[0] == dealer_hand.get_value()[0]:
            return 0
        else:
            return -self.bet

    def process_action(self, action: Action):
        """
        :param action: Action to process
        :return: a new instance of playable hand
        """
        if action == Action.STAND:
            return PlayableHand(self.shoe, self.bet, self.upcard, self.hand, True)
        elif action == Action.HIT:
            new_hand = Hand(self.hand.cards)
            new_hand.add_card(self.shoe.deal())
            return PlayableHand(self.shoe, self.bet, self.upcard, new_hand, self.hand_over)
        elif action == Action.DOUBLE:
            new_hand = Hand(self.hand.cards)
            new_hand.add_card(self.shoe.deal())
            return PlayableHand(self.shoe, self.bet * 2, self.upcard, new_hand, True)
        elif action == Action.SPLIT:
            raise NotImplementedError
        else:
            raise ValueError(f"Unknown action {action}")

    def get_value(self) -> Tuple[int, bool]:
        return self.hand.get_value()


class BlackjackStrategy(ABC):
    def get_action(self, playable_hand: PlayableHand, shoe: Shoe) -> Action:
        raise NotImplementedError

    def select_bet_size(self, shoe: Shoe) -> int:
        raise NotImplementedError


class BlackjackGame:
    def __init__(self, strategy: BlackjackStrategy, num_decks: int = 2, verbose=False,
            hands_to_play: int = 100, initial_bankroll=1000):
        self.strategy = strategy
        self.shoe = Shoe(num_decks)
        self.verbose = verbose
        self.hands_to_play = hands_to_play
        self.initial_bankroll = initial_bankroll

    def play(self):
        bankroll = self.initial_bankroll
        for _ in range(self.hands_to_play):
            bet = self.strategy.select_bet_size(self.shoe)
            if self.verbose:
                print(f"Bet: {bet}")
            playable_hand = PlayableHand(self.shoe, bet)
            while not playable_hand.is_terminal():
                action = self.strategy.get_action(playable_hand, self.shoe)
                playable_hand = playable_hand.process_action(action)
                if self.verbose:
                    print(
                        f"Hand: {playable_hand.hand} Value: {playable_hand.get_value()} Action: {action}")
            bankroll += playable_hand.get_hand_value(self.verbose)
            if self.verbose:
                print(f"Hand: {playable_hand.hand}")
                print(f"Bankroll: {bankroll}")
        return bankroll
