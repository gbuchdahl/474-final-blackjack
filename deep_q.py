import random
from collections import deque

import keras.models
import numpy as np
from keras import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

from blackjack import BlackjackStrategy, PlayableHand, Action
from cards import Shoe


def hand_to_input_vector(hand: PlayableHand):
    hand_value, soft = hand.hand.get_value()
    hand_value = min(22, hand_value)
    hand_vector = np.zeros(22)
    hand_vector[hand_value - 1] = 1
    upcard_vector = np.zeros(10)
    upcard_vector[hand.upcard.get_value() - 1] = 1
    is_soft = [1] if soft else [0]
    return np.concatenate((hand_vector, upcard_vector, is_soft))


def step(hand: PlayableHand, action: Action):
    next_hand = hand.process_action(action)
    if next_hand.is_terminal():
        reward = next_hand.get_hand_value()
    else:
        reward = 0
    return next_hand, hand_to_input_vector(next_hand), reward, next_hand.is_terminal()


class DeepQBlackjack(BlackjackStrategy):

    def __init__(self):
        self.memory = deque(maxlen=2000)
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.1
        self.epsilon_max = 1.0
        self.epsilon_interval = (
                self.epsilon_max - self.epsilon_min
        )
        self.epsilon_decay = 0.995
        self.batch_size = 32
        self.max_steps_per_episode = 10000
        self.learning_rate = 0.001
        self.state_size = 33
        self.action_size = 2
        self.tau = .125
        self.model = self._build_model()
        self.target_model = self._build_model()

    def _build_model(self):
        model = Sequential()
        model.add(Dense(66, activation="relu", input_dim=self.state_size))
        model.add(Dense(self.action_size, activation="softmax"))
        model.compile(loss="mse", optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, is_terminal):
        self.memory.append((state, action, reward, next_state, is_terminal))

    def train(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, is_terminal in minibatch:
            target = reward  # if done
            if not is_terminal:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i] * self.tau + target_weights[i] * (1 - self.tau)
        self.target_model.set_weights(target_weights)

    def save_model(self, fn):
        self.model.save(fn)

    def load_model(self, fn):
        self.model = keras.models.load_model(fn)

    def run_dqn(self, n_episodes=10000, num_decks=8):
        shoe = Shoe(num_decks)
        for e in range(n_episodes):
            hand = shoe.deal_hand()
            upcard = shoe.deal()
            playable_hand = PlayableHand(shoe=shoe, bet=10, hand=hand, upcard=upcard)
            state = hand_to_input_vector(playable_hand)
            state = np.reshape(state, [1, self.state_size])
            for time in range(self.max_steps_per_episode):
                if self.epsilon > np.random.rand():
                    action = random.randrange(self.action_size)
                else:
                    action = np.argmax(self.model.predict(state)[0])

                next_hand, next_state, reward, is_terminal = step(playable_hand, Action(action))
                next_state = np.reshape(next_state, [1, self.state_size])
                self.remember(state, action, reward, next_state, is_terminal)
                playable_hand = next_hand
                if is_terminal:
                    print("episode: {}/{}, score: {}, e: {:.2}"
                          .format(e, n_episodes, time, self.epsilon))
                    break
            if len(self.memory) > self.batch_size:
                self.train(self.batch_size)
            if e % 10 == 0:
                self.target_train()
        self.save_model("dqn.h5")

    def select_action(self, playable_hand: PlayableHand, shoe: Shoe) -> Action:
        state = hand_to_input_vector(playable_hand)
        state = np.reshape(state, [1, self.state_size])
        action = np.argmax(self.model.predict(state)[0])
        return Action(action)

    def select_bet_size(self, shoe: Shoe) -> int:
        return 10


if __name__ == "__main__":
    dqn = DeepQBlackjack()
    dqn.run_dqn()
    dqn.save_model("dqn.h5")
    dqn.print_strategy()
