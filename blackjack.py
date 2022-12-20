import abc
from enum import Enum
from typing import List, Tuple
import pandas as pd
import jinja2

from cards import Shoe, Hand, Card


class Action(Enum):
    STAND = 0
    HIT = 1
    DOUBLE = 2
    SPLIT = 3


class PlayableHand:
    def __init__(self, shoe: Shoe, bet: int, upcard=None, hand: Hand = None,
            hand_over: bool = False):
        self.shoe = shoe
        self.hand: Hand = hand or self.shoe.deal_hand()
        self.upcard = upcard or self.shoe.deal()
        self.bet = bet
        self.hand_over = hand_over or False

    def is_pair(self):
        return len(self.hand) == 2 and self.hand[0].value == self.hand[1].value

    def get_all_actions(self) -> List[Action]:
        actions = [Action.STAND, Action.HIT]
        if self.is_pair():
            actions.append(Action.SPLIT)
        if len(self.hand) == 2:
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
            print(f"Hand is bust with {self.hand} and upcard {self.upcard}") if verbose else None

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

        if dealer_hand.is_bust():
            print(f"Dealer busts with {dealer_hand}") if verbose else None
            return self.bet

        if self.hand.get_value()[0] > dealer_hand.get_value()[0]:
            if verbose: print(f"Player wins with {self.hand} vs {dealer_hand}")
            return self.bet
        elif self.hand.get_value()[0] == dealer_hand.get_value()[0]:
            if verbose: print(f"Push with {self.hand} vs {dealer_hand}")
            return 0
        else:
            if verbose: print(f"Dealer wins with {dealer_hand} vs {self.hand}")
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
            return PlayableHand(self.shoe, self.bet, self.upcard, new_hand, False)
        elif action == Action.DOUBLE:
            new_hand = Hand(self.hand.cards)
            new_hand.add_card(self.shoe.deal())
            return PlayableHand(self.shoe, self.bet * 2, self.upcard, new_hand, True)
        elif action == Action.SPLIT:
            new_hand = Hand([self.hand.cards[0]])
            new_hand.add_card(self.shoe.deal())
            if self.hand.cards[0].get_value() == 1:
                return PlayableHand(self.shoe, self.bet * 2, self.upcard, new_hand, True)
            return PlayableHand(self.shoe, self.bet * 2, self.upcard, new_hand, False)
        else:
            raise ValueError(f"Unknown action {action}")

    def get_value(self) -> Tuple[int, bool]:
        return self.hand.get_value()


class BlackjackStrategy(abc.ABC):

    @abc.abstractmethod
    def select_action(self, playable_hand: PlayableHand, shoe: Shoe) -> Action:
        pass

    @abc.abstractmethod
    def select_bet_size(self, shoe: Shoe) -> int:
        pass

    def color_background(self, action: Action):
        color = 'none'
        if action == "Stand":
            color = 'red'
        elif action == "Split":
            color = "blue"
        elif action == "Double":
            color = "green"
        return f"background-color: {color}"

    def print_strategy(self):
        action_to_words = {Action.SPLIT: "Split", Action.STAND: "Stand", Action.HIT: "Hit",
                           Action.DOUBLE: "Double"}
        strategy = {}
        hard_total_dict = {8: [3, 5], 9: [4, 5], 10: [4, 6], 11: [5, 6], 12: [5, 7], 13: [6, 7],
                           14: [6, 8], 15: [7, 8], 16: [7, 9], 17: [8, 9], 18: [8, 10], 19: [9, 10],
                           20: [10, 11], 21: [5, 6, 10]}
        for upcard in list(range(2, 11)) + [1]:
            res = []
            for hard_total in range(8, 21):
                fake_hand = Hand()
                for card in hard_total_dict[hard_total]:
                    fake_hand.add_card(Card(card))
                playable = PlayableHand(Shoe(), 1, Card(upcard), fake_hand)
                res.append(action_to_words[self.select_action(playable, Shoe())])
            for soft_card in range(2, 10):
                fake_hand = Hand([Card(1), Card(soft_card)])
                playable = PlayableHand(Shoe(), 1, Card(upcard), fake_hand)
                res.append(action_to_words[self.select_action(playable, Shoe())])
            for pair in range(1, 11):
                fake_hand = Hand([Card(pair), Card(pair)])
                playable = PlayableHand(Shoe(), 1, Card(upcard), fake_hand)
                res.append(action_to_words[self.select_action(playable, Shoe())])
            if upcard == 1:
                strategy["A"] = res
            else:
                strategy[f"{upcard}"] = res

        df = pd.DataFrame(strategy)
        df.index = [f"{i}" for i in range(8, 21)] + [f"A,{i}" for i in range(2, 10)] + ["A,A"] + [
            f"{i},{i}" for i in range(2, 11)]
        with open("strategy.html", "w") as f:
            f.write(f"""
            <html>
                <head><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css"></head>
            <body>{df.style.applymap(self.color_background).to_html()}</body>
            </html>""")


class BlackjackGame:
    def __init__(self, strategy: BlackjackStrategy, num_decks: int = 2, verbose=False):
        self.strategy = strategy
        self.shoe = Shoe(num_decks)
        self.verbose = verbose

    def play(self, num_hands: int = 100, initial_bankroll=1000):
        bankroll = initial_bankroll
        total_amount_bet = 0
        for i in range(num_hands):
            if self.verbose:
                print(f"-------------------")
                print(f"Hand #{i + 1}")
            bet = self.strategy.select_bet_size(self.shoe)
            if self.verbose:
                print(f"Bet: {bet}")
            # are we playing the same shoe over and over again here? I'm confused how this works
            playable_hand = PlayableHand(self.shoe, bet)
            while not playable_hand.is_terminal():
                action = self.strategy.select_action(playable_hand, self.shoe)
                if self.verbose:
                    print(
                        f"Hand: {playable_hand.hand} Value: {playable_hand.get_value()} Action: {action}")
                playable_hand = playable_hand.process_action(action)
            winnings = playable_hand.get_hand_value(self.verbose)
            bankroll += winnings
            if self.verbose:
                print(f"Bankroll: {bankroll}")
                print(f"-------------------\n")
            total_amount_bet += playable_hand.bet
        return bankroll, total_amount_bet
