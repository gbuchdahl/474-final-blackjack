from blackjack import BlackjackStrategy, Action, PlayableHand, BlackjackGame
from cards import Shoe, Card
import time
import random
import numpy as np


class QStrategyStdBet(BlackjackStrategy):
    def __init__(self) -> None:
        self.Q_dict = {}

    def q_learn(self, num_decks=8):
        epsilon = .25
        alpha = .1
        gamma = .99

        start = time.time()
        shoe = Shoe(num_decks)
        while time.time() - start < 600:
            hand = shoe.deal_hand()
            upcard = shoe.deal()
            playable_hand = PlayableHand(shoe, 10, upcard, hand)
            key = (min(22, hand.get_value()[0]), hand.get_value()[1], upcard.get_value())
            if key not in self.Q_dict.keys():
                self.Q_dict[key] = [0, 0, 0, 0]
            while not playable_hand.is_terminal():
                key = (
                    min(22, playable_hand.hand.get_value()[0]), playable_hand.hand.get_value()[1],
                    upcard.get_value())
                if random.random() < epsilon:
                    action = random.choice(playable_hand.get_all_actions())
                else:
                    action = Action(np.argmax(self.Q_dict[key]))
                # remove later
                if action == Action.SPLIT:
                    action = random.choice(playable_hand.get_all_actions())
                next_step = playable_hand.process_action(action)
                reward = 0
                if next_step.is_terminal():
                    reward = next_step.get_hand_value()
                next_key = (min(22, next_step.hand.get_value()[0]), next_step.hand.get_value()[1],
                            next_step.upcard.get_value())
                if next_key not in self.Q_dict.keys():
                    self.Q_dict[next_key] = [0, 0, 0, 0]
                self.Q_dict[key][Action([action])] += alpha * (
                        reward + gamma * self.Q_dict[next_key][Action(action)] -
                        self.Q_dict[key][Action(action)])
                playable_hand = next_step

    def select_action(self, hand: PlayableHand, shoe: Shoe) -> Action:
        key = (min(22, hand.hand.get_value()[0]), hand.hand.get_value()[1], hand.upcard.get_value())

        # remove this line once split implemented
        self.Q_dict[key][3] = -100000000000

        return Action(np.argmax(self.Q_dict[key]))

    def select_bet_size(self, shoe: Shoe) -> int:
        return 10
