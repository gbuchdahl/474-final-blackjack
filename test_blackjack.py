import scipy

from blackjack import BlackjackStrategy, Action, PlayableHand, BlackjackGame
from cards import Shoe, Card
from q_learning import QStrategyStdBet


class TestStrategy(BlackjackStrategy):
    def select_action(self, hand: PlayableHand, shoe: Shoe) -> Action:
        if hand.get_value()[0] == 11:
            return Action.DOUBLE
        elif hand.get_value()[0] == 10 and hand.upcard.get_value() != 10 and hand.upcard.get_value() != 1:
            return Action.DOUBLE
        elif hand.get_value()[0] <= 16 and (hand.upcard.get_value() >= 7 or hand.upcard.get_value() == 1):
            return Action.HIT
        elif hand.get_value()[0] >= 12 and hand.upcard.get_value() >= 2 and hand.upcard.get_value() <= 6:
            return Action.STAND
        elif hand.get_value()[0] <= 11:
            return Action.HIT
        else:
            return Action.STAND

    def select_bet_size(self, shoe: Shoe) -> int:
        return 10



# strategy = QStrategyStdBet()
# Q_dict = strategy.q_learn()
# strategy.print_strategy()

strategy = TestStrategy()
strategy.print_strategy()

results = []
for _ in range(10):
    game = BlackjackGame(strategy, num_decks=2, verbose=False)
    initial_bankroll = 1_000_000
    res = game.play(num_hands=500_000, initial_bankroll=initial_bankroll)
    results.append((res[0] - initial_bankroll)/ res[1])
    print("Result: ", (res[0] - initial_bankroll)/ res[1])

print(scipy.stats.describe(results))
