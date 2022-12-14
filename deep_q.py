import random
from collections import deque

import keras.models
import numpy as np
import scipy
from keras import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

from blackjack import BlackjackStrategy, PlayableHand, Action, BlackjackGame
from cards import Shoe

NUM_HAND_VALUES = 22
NUM_UPCARDS = 10
NUM_PAIRS = 10
EXTRA_INPUTS = 1
STATE_SIZE = NUM_HAND_VALUES + NUM_UPCARDS + NUM_PAIRS + EXTRA_INPUTS


def hand_to_input_vector(hand: PlayableHand):
    """
    Our model processes hands as a couple concatenated one-hot vectors
    :param hand: the hand to process
    :return: a vector of length STATE_SIZE
    """
    hand_value, soft = hand.hand.get_value()
    hand_value = min(22, hand_value)
    hand_vector = np.zeros(NUM_HAND_VALUES)
    hand_vector[hand_value - 1] = 1
    upcard_vector = np.zeros(NUM_UPCARDS)
    upcard_vector[hand.upcard.get_value() - 1] = 1
    is_soft = [1] if soft else [0]
    pairs = np.zeros(NUM_PAIRS)
    if hand.hand[0] == hand.hand[1]:
        pairs[hand.hand[0].get_value() - 1] = 1
    return np.concatenate((hand_vector, upcard_vector, is_soft, pairs))


def step(hand: PlayableHand, action: Action):
    """
    Helper function to process an action and return state to be fed to the model
    :param hand: hand to apply action to
    :param action: action to apply
    :return: next hand, next state, reward, is_terminal
    """
    next_hand = hand.process_action(action)
    if next_hand.is_terminal():
        reward = next_hand.get_hand_reward()
    else:
        reward = 0
    return next_hand, hand_to_input_vector(next_hand), reward, next_hand.is_terminal()


class DeepQBlackjack(BlackjackStrategy):
    """
    Code inspired by this tutorial for a different DeepQ learning application:
    https://towardsdatascience.com/reinforcement-learning-w-keras-openai-dqns-1eed3a5338c
    """

    def __init__(self):
        self.memory = deque(maxlen=2000)
        self.gamma = 0.9999  # doesn't really need to be discounted
        self.alpha = 0.001
        self.tau = .250

        # Need exploratation to find splits/doubles
        self.epsilon = 0.25
        self.epsilon_min = 0.1
        self.epsilon_interval = (
                self.epsilon - self.epsilon_min
        )
        self.epsilon_decay = 0.995

        self.batch_size = 128
        self.state_size = STATE_SIZE
        self.action_size = len(Action)

        # Using Open-AI trick to copy weights from model to target model
        self.model = self._build_model()
        self.target_model = self._build_model()

        # Store the trained model's moves, so we don't have to look them up each time
        self.cache = {}

    def _build_model(self):
        model = Sequential()
        model.add(Dense(STATE_SIZE * 2, activation="relu", input_dim=self.state_size))
        model.add(Dense(STATE_SIZE, activation="relu"))
        model.add(Dense(self.action_size, activation="linear"))
        model.compile(loss="mse", optimizer=Adam(lr=self.alpha))
        return model

    def remember(self, state, action, reward, next_state, is_terminal):
        self.memory.append((state, action, reward, next_state, is_terminal))

    def train(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        inputs = np.array([m[0][0] for m in minibatch])

        # Do as many predictions as possible in one batch (faster)
        predictions = self.model.predict(inputs, batch_size=batch_size)

        for i, (state, action, reward, next_state, is_terminal) in enumerate(minibatch):
            target = reward
            if not is_terminal:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state, verbose=0)[
                                                            0]))
            target_f = np.array([predictions[i]])
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def target_train(self):
        """
        Copy weights from model to target model
        """
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i] * self.tau + target_weights[i] * (1 - self.tau)
        self.target_model.set_weights(target_weights)

    def save_model(self, fn):
        self.model.save(fn)

    def load_model(self, fn):
        self.model = keras.models.load_model(fn)

    def run_dqn(self, n_episodes=50_000, num_decks=2, stacked=False):
        """
        Trains the model using Deep Q Learning.
        """
        shoe = Shoe(num_decks=num_decks, is_stacked=stacked)
        for e in range(n_episodes):
            hand = shoe.deal_hand()
            upcard = shoe.deal()
            playable_hand = PlayableHand(shoe=shoe, bet=10, hand=hand, upcard=upcard)
            state = hand_to_input_vector(playable_hand)
            state = np.reshape(state, [1, self.state_size])
            while True:
                possible_actions = playable_hand.get_all_actions()
                if self.epsilon > np.random.rand():
                    action = random.choice(possible_actions)
                    action = action.value
                else:
                    action_values = self.model.predict(state, verbose=0)[0]
                    action_indices = [a.value for a in possible_actions]
                    for i in range(4):
                        if i not in action_indices:
                            action_values[i] = -np.inf
                    action = np.argmax(action_values)

                next_hand, next_state, reward, is_terminal = step(playable_hand, Action(action))
                next_state = np.reshape(next_state, [1, self.state_size])
                self.remember(state, action, reward, next_state, is_terminal)
                playable_hand = next_hand
                if is_terminal:
                    print(f"Episode {e}/{n_episodes}, hand: {str(playable_hand)}, score: {reward}")
                    break
            if len(self.memory) > self.batch_size and e % 100 == 0:
                self.train(self.batch_size)
            if e % 1000 == 0:
                self.target_train()
        self.save_model("dqn.h5")

    def select_action(self, playable_hand: PlayableHand, shoe: Shoe) -> Action:
        """
        Called after the model has been trained. Selects the action for given hand and shoe.
        """
        state = hand_to_input_vector(playable_hand)
        state = np.reshape(state, [1, self.state_size])
        if str(state) in self.cache.keys():
            return self.cache[str(state)]
        else:
            possible_actions = playable_hand.get_all_actions()
            action_values = self.model.predict(state, verbose=0)[0]
            action_indices = [a.value for a in possible_actions]
            for i in range(4):
                if i not in action_indices:
                    action_values[i] = -np.inf
            action = np.argmax(action_values)
            self.cache[str(state)] = Action(action)
            return Action(action)

    def select_bet_size(self, shoe: Shoe) -> int:
        return 10


if __name__ == "__main__":
    dqn = DeepQBlackjack()
    # dqn.run_dqn()
    # dqn.save_model("dqn-hidden-layers.h5")
    results = []
    dqn.load_model("trained-dqn-model.h5")
    dqn.print_strategy()

    game = BlackjackGame(dqn, num_decks=2, verbose=False)
    initial_bankroll = 1_000_000
    for _ in range(10):
        res = game.play(num_hands=50_000, initial_bankroll=initial_bankroll)
        results.append((res[0] - initial_bankroll) / res[1])
        print("Result: ", (res[0] - initial_bankroll) / res[1])

    print(scipy.stats.describe(results))
